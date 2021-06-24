"""Core Domain for Mower App"""

import logging.config

LOGGING_CONFIG = {
  "version": 1,
  "disable_existing_loggers": True,
  "formatters": {
    "default": {
      "format": "%(asctime)s [%(levelname)s] ## %(message)s"
    }
  },
  "handlers": {
    "appStream": {
      "class": "logging.StreamHandler",
      "level": "INFO",
      "formatter": "default",
      "stream": "ext://sys.stdout"
    }
  },
  "loggers": {
    "appLogger": {
      "level": "INFO",
      "handlers": [
        "appStream"
      ],
      "propagate": False
    }
  }
}

logging.config.dictConfig(LOGGING_CONFIG)
