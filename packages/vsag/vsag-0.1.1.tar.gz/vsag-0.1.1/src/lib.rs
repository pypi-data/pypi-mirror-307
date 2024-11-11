//! Python binding for VSAG, a vector indexing library used for similarity search.
//! https://github.com/alipay/vsag

use pyo3::exceptions::PyValueError;
use pyo3::prelude::*;
use vsag_sys as sys;

#[pyclass]
struct Index {
    core: sys::VsagIndex,
}

#[pymethods]
impl Index {
    #[new]
    fn try_new(index_type: &str, params: &str) -> PyResult<Self> {
        sys::VsagIndex::new(index_type, params)
            .map_err(|e| PyValueError::new_err(e.message))
            .map(|core| Self { core })
    }

    /// Add vectors to index.
    fn add_vectors(
        &self,
        vectors: Vec<f32>,
        ids: Vec<i64>,
        num_elements: usize,
        dim: usize,
    ) -> PyResult<()> {
        let _ = self
            .core
            .build(num_elements, dim, &ids, &vectors)
            .map_err(|e| PyValueError::new_err(e.message))?;

        Ok(())
    }

    /// Searches for the `k` nearest neighbors of the `query_vector`.
    fn knn_search(
        &self,
        query: Vec<f32>,
        k: usize,
        params: &str,
    ) -> PyResult<(Vec<i64>, Vec<f32>)> {
        self.core
            .knn_search(&query, k, params)
            .map_err(|e| PyValueError::new_err(e.message))
            .map(|res| (res.ids, res.distances))
    }
}

/// Formats the sum of two numbers as string.
#[pyfunction]
fn sum_as_string(a: usize, b: usize) -> PyResult<String> {
    Ok((a * b).to_string())
}

/// A Python module implemented in Rust.
#[pymodule]
fn vsag(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(sum_as_string, m)?)?;
    m.add_class::<Index>()?;
    Ok(())
}
