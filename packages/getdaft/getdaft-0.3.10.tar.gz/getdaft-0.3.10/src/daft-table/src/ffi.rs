use common_error::DaftResult;
use daft_core::{
    prelude::SchemaRef,
    series::Series,
    utils::arrow::{cast_array_for_daft_if_needed, cast_array_from_daft_if_needed},
};
use pyo3::{exceptions::PyValueError, prelude::*, types::PyList};

use crate::Table;

pub fn record_batches_to_table(
    py: Python,
    batches: &[Bound<PyAny>],
    schema: SchemaRef,
) -> PyResult<Table> {
    if batches.is_empty() {
        return Ok(Table::empty(Some(schema))?);
    }

    let names = schema.names();
    let num_batches = batches.len();
    // First extract all the arrays at once while holding the GIL
    let mut extracted_arrow_arrays: Vec<(Vec<Box<dyn arrow2::array::Array>>, usize)> =
        Vec::with_capacity(num_batches);

    for rb in batches {
        let pycolumns = rb.getattr(pyo3::intern!(py, "columns"))?;
        let columns = pycolumns
            .downcast::<PyList>()?
            .into_iter()
            .map(|col| common_arrow_ffi::array_to_rust(py, col))
            .collect::<PyResult<Vec<_>>>()?;
        if names.len() != columns.len() {
            return Err(PyValueError::new_err(format!("Error when converting Arrow Record Batches to Daft Table. Expected: {} columns, got: {}", names.len(), columns.len())));
        }
        extracted_arrow_arrays.push((columns, rb.len()?));
    }
    // Now do the heavy lifting (casting and concats) without the GIL.
    py.allow_threads(|| {
        let mut tables: Vec<Table> = Vec::with_capacity(num_batches);
        for (cols, num_rows) in extracted_arrow_arrays {
            let columns = cols
                .into_iter()
                .enumerate()
                .map(|(i, array)| {
                    let cast_array = cast_array_for_daft_if_needed(array);
                    Series::try_from((names.get(i).unwrap().as_str(), cast_array))
                })
                .collect::<DaftResult<Vec<_>>>()?;
            tables.push(Table::new_with_size(schema.clone(), columns, num_rows)?);
        }
        Ok(Table::concat(tables.as_slice())?)
    })
}

pub fn table_to_record_batch(
    py: Python,
    table: &Table,
    pyarrow: Bound<PyModule>,
) -> PyResult<PyObject> {
    let mut arrays = Vec::with_capacity(table.num_columns());
    let mut names: Vec<String> = Vec::with_capacity(table.num_columns());

    for i in 0..table.num_columns() {
        let s = table.get_column_by_index(i)?;
        let arrow_array = s.to_arrow();
        let arrow_array = cast_array_from_daft_if_needed(arrow_array.to_boxed());
        let py_array = common_arrow_ffi::to_py_array(py, arrow_array, &pyarrow)?;
        arrays.push(py_array);
        names.push(s.name().to_string());
    }

    let record = pyarrow
        .getattr(pyo3::intern!(py, "RecordBatch"))?
        .call_method1(pyo3::intern!(py, "from_arrays"), (arrays, names.clone()))?;

    Ok(record.into())
}
