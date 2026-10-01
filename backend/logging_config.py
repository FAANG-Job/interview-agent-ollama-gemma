# logging_config.py
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
APP_LOGGER = "local_llm"

def configure_logging() -> None:
    logger = logging.getLogger(APP_LOGGER)
    logger.setLevel(logging.INFO)
    logger.propagate = False

    if logger.handlers:
        return

    log_dir = Path(__file__).resolve().parent / "logs"
    log_dir.mkdir(exist_ok=True)

    handler = RotatingFileHandler(
        log_dir / "app.log",
        maxBytes=5_000_000,
        backupCount=3,
        encoding="utf-8",
    )
    handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
    )
    logger.addHandler(handler)


def get_logger(module_name: str) -> logging.Logger:
    return logging.getLogger(f"{APP_LOGGER}.{module_name}")

