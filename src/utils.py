import logging

def setup_logger(name: str):
    logger = logging.getLogger(name)
    logging.basicConfig(level=logging.INFO)
    return logger
