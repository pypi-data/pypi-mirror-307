use pyo3::prelude::*;

#[pyclass]
struct HelloWorld {}

#[pymethods]
impl HelloWorld {
    #[new]
    fn new() -> Self {
        HelloWorld {}
    }

    #[staticmethod]
    fn greet() -> PyResult<String> {
        Ok("Hello from Rust!".to_string())
    }
}

#[pymodule]
fn hello_world_rs(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_class::<HelloWorld>()?;
    Ok(())
}