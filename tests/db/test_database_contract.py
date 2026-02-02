import sqlite3
import tempfile
import os
import pytest

from app.db.database import save_to_db

# pytest tests/db/test_database_contract.py -v 

@pytest.fixture
def temp_db(monkeypatch):
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)

    # patch DB_PATH
    monkeypatch.setattr("app.db.database.DB_PATH", path)

    # create schema
    conn = sqlite3.connect(path)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE analysis_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            datetime TEXT,
            image TEXT,
            image_hash TEXT,
            source TEXT,
            model_version TEXT,
            confidence REAL,
            metal_percent REAL,
            mixed_waste_percent REAL,
            paper_cardboard_percent REAL,
            plastic_percent REAL,
            wood_percent REAL
        )
    """)

    conn.commit()
    conn.close()

    yield path
    os.remove(path)

def test_save_to_db_accepts_valid_input(temp_db):
    percentages = {
        "Metal": 10.0,
        "Mixed waste": 20.0,
        "Paper&Cardboard": 30.0,
        "Plastic": 25.0,
        "Wood": 15.0,
    }

    save_to_db(
        image="test.jpg",
        image_hash="hash123",
        conf=0.5,
        percentages=percentages,
    )

def test_save_to_db_persists_correctly(temp_db):
    percentages = {
        "Metal": 1.0,
        "Mixed waste": 2.0,
        "Paper&Cardboard": 3.0,
        "Plastic": 4.0,
        "Wood": 5.0,
    }

    save_to_db(
        image="img.png",
        image_hash="abc",
        conf=0.9,
        percentages=percentages,
    )

    conn = sqlite3.connect(temp_db)
    cur = conn.cursor()

    cur.execute("""
        SELECT image, image_hash, confidence,
               metal_percent, mixed_waste_percent,
               paper_cardboard_percent, plastic_percent, wood_percent
        FROM analysis_history
    """)

    row = cur.fetchone()
    conn.close()

    assert row == (
        "img.png",
        "abc",
        0.9,
        1.0,
        2.0,
        3.0,
        4.0,
        5.0,
    )

def test_save_to_db_does_not_mutate_percentages(temp_db):
    percentages = {
        "Metal": 10.0,
        "Mixed waste": 20.0,
        "Paper&Cardboard": 30.0,
        "Plastic": 40.0,
        "Wood": 0.0,
    }

    original = percentages.copy()

    save_to_db(
        image="a.jpg",
        image_hash="x",
        conf=0.3,
        percentages=percentages,
    )

    assert percentages == original
