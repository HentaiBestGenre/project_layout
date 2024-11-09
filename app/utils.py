import logging
import logging.config

import sys


logging_config = {
    "version": 1,
    'filters': {
        'correlation_id': {
            '()': 'asgi_correlation_id.CorrelationIdFilter',
            'uuid_length': 32,
            'default_value': '-',
        },
    },
    "formatters": {
        "json": {
            "class": "pythonjsonlogger.jsonlogger.JsonFormatter",
            'format': '%(levelname)s ... %(datetime)% [%(correlation_id)s] %(name)s %(message)s %(funcName)s %(lineno)s',
        }
    },
    "handlers": {
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "formatter": "json",
            'filters': ['correlation_id'],
            "stream": sys.stderr,
        },
        "file": {
            "level": "DEBUG",
            "class": "logging.FileHandler",
            "formatter": "json",
            'filters': ['correlation_id'],
            "filename": "app.log",
            "mode": "a",
        }
    },
    "root": {
        "level": "DEBUG",
        "handlers": [
            "console",
            "file"
        ],
        "propagate": True
    }
}

logging.config.dictConfig(logging_config)


class AsyncIteratorWrapper:
    def __init__(self, obj):
        self._it = iter(obj)

    def __aiter__(self):
        return self

    async def __anext__(self):
        try:
            value = next(self._it)
        except StopIteration:
            raise StopAsyncIteration
        return value
