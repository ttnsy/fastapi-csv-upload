import json
import logging
from datetime import datetime


class JsonFormatter(logging.Formatter):
    def format(self, record):
        log_record = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "module": record.module,
            "line": record.lineno,
            "message": record.getMessage(),
        }
        whitelist = ["method", "path", "status_code", "duration_ms", "user"]
        for key in whitelist:
            if hasattr(record, key):
                log_record[key] = getattr(record, key)
        return json.dumps(log_record)


LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {"format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s"},
        "json": {"()": JsonFormatter},
        "telemetry": {"format": "[%(method)s] %(path)s took %(duration_ms)s ms"},
    },
    "handlers": {
        "stream": {
            "class": "logging.StreamHandler",
            "level": "INFO",
            "formatter": "default",
        },
        "stream_telemetry": {
            "class": "logging.StreamHandler",
            "formatter": "telemetry",
            "level": "INFO",
        },
        "file": {
            "class": "logging.handlers.TimedRotatingFileHandler",
            "filename": "logs/app.jsonl",
            "when": "midnight",
            "interval": 1,
            "backupCount": 7,
            "level": "DEBUG",
            "formatter": "json",
            "encoding": "utf-8",
        },
    },
    "loggers": {
        "app": {"level": "DEBUG", "handlers": ["stream", "file"], "propagate": False},
        "telemetry": {
            "handlers": ["stream_telemetry", "file"],
            "level": "INFO",
            "propagate": False,
        },
        "uvicorn.error": {"level": "INFO"},
        "uvicorn.access": {"level": "INFO", "handlers": ["stream", "file"]},
    },
    "root": {"level": "DEBUG", "handlers": ["stream", "file"]},
}

logging.config.dictConfig(LOG_CONFIG)

logger = logging.getLogger("app")
logger_telemetry = logging.getLogger("telemetry")
