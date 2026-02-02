import pytest
import streamlit as st

from app.core.validation import validate_uploaded_files

# pytest tests/core/test_validation.py -v 

class DummyFile:
    """Dummy file object mimicking Streamlit UploadedFile behavior."""

    def __init__(self, name: str, size_mb: int):
        self.name = name
        # Streamlit uses bytes for file.size
        self.size = size_mb * 1024 * 1024

# =========================
# Single file cases
# =========================

def test_single_file_within_size_limit():
    """A single file under the size limit should pass validation."""
    file = DummyFile("test.jpg", size_mb=5)

    # Should not raise any exception
    validate_uploaded_files(file, 20)


def test_single_file_exceeds_size_limit(monkeypatch):
    """A single file exceeding the size limit should raise an error."""
    file = DummyFile("large.jpg", size_mb=50)

    # Force st.stop to raise SystemExit
    monkeypatch.setattr(st, "stop", lambda: (_ for _ in ()).throw(SystemExit))

    with pytest.raises(SystemExit):
        validate_uploaded_files(file, 20)

# =========================
# Batch file cases
# =========================

def test_multiple_files_all_within_size_limit():
    """Multiple files under the size limit should pass validation."""
    files = [
        DummyFile("a.jpg", size_mb=3),
        DummyFile("b.jpg", size_mb=15),
        DummyFile("c.jpg", size_mb=12),
    ]

    validate_uploaded_files(files, 20)


def test_multiple_files_one_exceeds_size_limit(monkeypatch):
    """Validation should fail if any file exceeds the size limit."""
    files = [
        DummyFile("a.jpg", size_mb=3),
        DummyFile("b.jpg", size_mb=30),
        DummyFile("c.jpg", size_mb=2),
    ]

    monkeypatch.setattr(st, "stop", lambda: (_ for _ in ()).throw(SystemExit))

    with pytest.raises(SystemExit):
        validate_uploaded_files(files, 20)

# =========================
# Edge cases
# =========================

def test_no_file_uploaded():
    """Passing None should be treated as no upload and pass silently."""
    validate_uploaded_files(None, 20)
