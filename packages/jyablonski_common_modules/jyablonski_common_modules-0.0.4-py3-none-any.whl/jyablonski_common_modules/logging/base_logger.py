import logging


def create_logger(log_file: str, date_format: str = "%Y-%m-%d %I:%M:%S %p"):
    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s] %(asctime)s %(message)s",
        datefmt=date_format,
        handlers=[logging.FileHandler(log_file), logging.StreamHandler()],
    )
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    return logger
