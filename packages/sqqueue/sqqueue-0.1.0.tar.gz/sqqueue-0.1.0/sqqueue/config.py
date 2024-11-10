# sqqueue/config.py

import json
import logging


class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "time": self.formatTime(record, self.datefmt),
            "level": record.levelname,
            "message": record.getMessage(),
            "function": record.funcName,
            "line": record.lineno,
        }
        return json.dumps(log_record)


def setup_logging() -> logging.Logger:
    """
    Sets up and returns a logger with JSON formatting.

    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger("sqqueue")
    logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())

    if not logger.handlers:
        logger.addHandler(handler)

    return logger
