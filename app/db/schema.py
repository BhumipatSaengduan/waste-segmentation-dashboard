import sqlite3

from ..core.config import DB_PATH, IMAGE_SOURCE, MODEL_VERSION

def create_tables():
    """Initialize SQLite database and create the analysis_history table if missing."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analysis_history (
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

def migrate_db():
    """Add missing columns (source, model_version, image_hash) to the database if they do not exist."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    existing_cols = [
        row[1]
        for row in cursor.execute("PRAGMA table_info(analysis_history)")
    ]

    if "model_version" not in existing_cols:
        cursor.execute("ALTER TABLE analysis_history ADD COLUMN model_version TEXT")

    if "source" not in existing_cols:
        cursor.execute("ALTER TABLE analysis_history ADD COLUMN source TEXT")

    if "image_hash" not in existing_cols:
        cursor.execute("ALTER TABLE analysis_history ADD COLUMN image_hash TEXT")

    conn.commit()
    conn.close()

def backfill_metadata():
    """Fill missing source and model_version fields for existing records in the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        UPDATE analysis_history
        SET source = ?, model_version = ?
        WHERE source IS NULL OR model_version IS NULL
    """, (IMAGE_SOURCE, MODEL_VERSION))

    conn.commit()
    conn.close()
