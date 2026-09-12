import json
import logging as std_logging
from typing import Any


class JsonFormatter(std_logging.Formatter):
    def format(self, record: std_logging.LogRecord) -> str:
        payload = {"level": record.levelname, "logger": record.name, "message": record.getMessage()}
        if hasattr(record, "event"):
            payload["event"] = getattr(record, "event")
        return json.dumps(payload, default=str)


def get_logger(name: str = "enterprise_data_platform", level: int = std_logging.INFO) -> std_logging.Logger:
    logger = std_logging.getLogger(name)
    logger.setLevel(level)
    if not logger.handlers:
        handler = std_logging.StreamHandler()
        handler.setFormatter(JsonFormatter())
        logger.addHandler(handler)
        logger.propagate = False
    return logger


def log_event(logger: std_logging.Logger, event: str, **fields: Any) -> None:
    logger.info(event, extra={"event": {"name": event, **fields}})
