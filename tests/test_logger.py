import pytest
import sys
sys.path.insert(0, '..')
from core.logger import Logger

def test_logger_info():
    logger = Logger()
    logger.info("Test info message")
    assert len(logger.get_logs()) > 0

def test_logger_error():
    logger = Logger()
    logger.error("Test error message")
    logs = logger.get_logs()
    assert any("ERROR" in log for log in logs)

def test_logger_clear():
    logger = Logger()
    logger.info("Test")
    logger.clear()
    assert len(logger.get_logs()) == 0