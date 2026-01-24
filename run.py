import logging

from src import start_clock
from src.conf import setup_logging

setup_logging()

log = logging.getLogger(__name__)

if __name__ == "__main__":
    try:
        log.info("Starting...")
        start_clock()
    except KeyboardInterrupt:
        log.info("Done.")
    except Exception:
        log.exception("Error.")
