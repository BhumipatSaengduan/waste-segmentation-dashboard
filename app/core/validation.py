import streamlit as st

def validate_uploaded_files(files, max_size_mb: int):
    """
    Check uploaded file(s) do not exceed the maximum size.

    Args:
        files: Single file or list of uploaded files.
        max_size_mb (int): Maximum allowed file size in megabytes.

    Raises:
        Stops Streamlit execution and shows error if a file exceeds the limit.
    """
    if not files:
        return

    # Normalize to list
    if not isinstance(files, list):
        files = [files]

    for file in files:
        file_size_mb = file.size / (1024 * 1024)
        if file_size_mb > max_size_mb:
            st.error(
                f"❌ File '{file.name}' exceeds {max_size_mb} MB limit "
                f"({file_size_mb:.1f} MB)"
            )
            st.stop()
