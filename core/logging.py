import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logging():
    log_dir = Path("core/logs")
    log_dir.mkdir(exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            RotatingFileHandler(
                log_dir / "booking_app.log",
                maxBytes=5 * 1024 * 1024,
                backupCount=3
            ),
            logging.StreamHandler()
        ]
    )


logger = logging.getLogger(__name__)
