use pyo3::prelude::*;
use rfd::FileDialog;

#[pyfunction]
pub fn file_picker_blocking() -> PyResult<Option<String>> {
        let file = FileDialog::new()
            .pick_file();

        let file = match file {
            Some(file) => Some(file.to_str().unwrap().to_string()),
            None => None,
        };
        Ok(file)
}
/// A Python module implemented in Rust.
#[pymodule]
fn file_picker_py(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(file_picker_blocking, m)?)?;
    Ok(())
}
