import sqlite3
import pandas as pd
from datetime import datetime

from ..core.config import DB_PATH, IMAGE_SOURCE, MODEL_VERSION
from ..core.logger import get_logger

logger = get_logger("db.database")

def save_to_db(image, image_hash, conf, percentages):
    """
    Save a single analysis result to the database.

    Args:
        image (str): Image filename.
        image_hash (str): SHA256 hash of the image.
        conf (float): Model confidence score.
        percentages (dict): Class-wise percentage of detected pixels.
    """
    logger.info(f"Saving analysis result | image={image}")

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO analysis_history (
                datetime, image, image_hash, source, model_version, confidence,
                metal_percent, mixed_waste_percent,
                paper_cardboard_percent, plastic_percent, wood_percent
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            image,
            image_hash,
            IMAGE_SOURCE,
            MODEL_VERSION,
            conf,
            percentages["Metal"],
            percentages["Mixed waste"],
            percentages["Paper&Cardboard"],
            percentages["Plastic"],
            percentages["Wood"]
        ))

        conn.commit()
        conn.close()

        logger.info(f"Save success | image={image}")

    except Exception as e:
        logger.error(
            f"Save failed | image={image} | error={str(e)}",
            exc_info=True
        )
        raise

def load_history():
    """
    Load all historical analysis records from the database.

    Returns:
        pd.DataFrame: DataFrame containing all records, empty if load fails.
    """
    logger.info("Loading analysis history")

    try:
        conn = sqlite3.connect(DB_PATH)
        df = pd.read_sql_query(
            "SELECT * FROM analysis_history ORDER BY datetime ASC",
            conn
        )
        conn.close()

        logger.info(f"History loaded | records={len(df)}")
        return df

    except Exception as e:
        logger.error(
            f"Load history failed | error={str(e)}",
            exc_info=True
        )
        return pd.DataFrame()

def undo_last_save():
    """"Remove the most recent analysis record from the database."""
    logger.info("Undo last save")

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT MAX(id) FROM analysis_history")
        last_id = cursor.fetchone()[0]

        if last_id is None:
            logger.warning("Undo failed | no record found")
            return

        cursor.execute("""
            DELETE FROM analysis_history
            WHERE id = ?
        """, (last_id,))

        conn.commit()
        conn.close()

        logger.info(f"Undo success | deleted_id={last_id}")

    except Exception as e:
        logger.error(
            f"Undo failed | error={str(e)}",
            exc_info=True
        )

def clear_history():
    """Delete all analysis records from the database."""
    logger.info("Clearing analysis history")

    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute("SELECT COUNT(*) FROM analysis_history")
        count = cursor.fetchone()[0]

        cursor.execute("DELETE FROM analysis_history")
        conn.commit()
        conn.close()

        logger.info(f"Clear history success | deleted_records={count}")

    except Exception as e:
        logger.error(
            f"Clear history failed | error={str(e)}",
            exc_info=True
        )
