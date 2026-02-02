import logging
import os

# =========================
# LOG DIRECTORY
# =========================
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LOG_DIR = os.path.join(BASE_DIR, "logs")
os.makedirs(LOG_DIR, exist_ok=True)

# =========================
# LOGGER FACTORY
# =========================
def get_logger(name: str) -> logging.Logger:
    """
    Create or retrieve a logger with file and console handlers.

    The log file is selected based on the logger name prefix:
      - "ui" -> ui.log
      - "batch" -> batch.log
      - "db" -> database.log
      - others -> app.log

    Args:
        name (str): Name of the logger.

    Returns:
        logging.Logger: Configured logger instance.
    """
    if name.startswith("ui"):
        filename = "ui.log"
    elif name.startswith("batch"):
        filename = "batch.log"
    elif name.startswith("db"):
        filename = "database.log"
    else:
        filename = "app.log"

    log_path = os.path.join(LOG_DIR, filename)

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)

    return logger
