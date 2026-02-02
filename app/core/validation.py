import streamlit as st

def validate_uploaded_files(files, max_size_mb: int):
    """Validate uploaded file(s) size."""
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
