from .settings_base import *
from .settings_base import INSTALLED_APPS, os

INSTALLED_APPS = [*INSTALLED_APPS, "sslserver"]

ENV_LOG_LEVEL = os.getenv("DJANGO_LOG_LEVEL", "INFO")
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "human": {
            "format": "{asctime} {module} [{levelname}] {message}",
            "style": "{",
        },
    },
    "handlers": {"console": {"class": "logging.StreamHandler", "formatter": "human",},},
    "root": {"handlers": ["console"], "level": "INFO",},
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": ENV_LOG_LEVEL,
            "propagate": False,
        },
        "react": {"handlers": ["console"], "level": ENV_LOG_LEVEL, "propagate": False,},
    },
}
