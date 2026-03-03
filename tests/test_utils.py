import logging
from src.utils import setup_logger

def test_setup_logger():
    logger_name = "test_logger"
    logger = setup_logger(logger_name)
    
    assert logger is not None
    assert isinstance(logger, logging.Logger)
    assert logger.name == logger_name
