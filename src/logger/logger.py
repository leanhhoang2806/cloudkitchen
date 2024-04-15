import logging


def initialize_logger():
    logging.basicConfig(level=logging.INFO)
    return logging.getLogger(__name__)
