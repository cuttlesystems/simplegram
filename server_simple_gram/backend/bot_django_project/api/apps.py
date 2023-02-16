import os
import sys

from django.apps import AppConfig
from bot_constructor.log_configs import logger_django


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self) -> None:
        if os.environ.get('RUN_MAIN'):
            pass
