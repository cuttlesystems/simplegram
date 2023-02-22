import os
import sys

from django.apps import AppConfig

from api.check_guinicorn import is_run_with_gunicorn


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self) -> None:
        from bot_constructor.log_configs import logger_django
        logger_django.info_logging('Method "ready" is activated')
        execute_code = False
        if is_run_with_gunicorn():
            execute_code = True
        else:
            if os.environ.get('RUN_MAIN'):
                execute_code = True
        if execute_code:
            from bots.started_bots_managing.restart_bots_manage import start_all_launched_bots
            logger_django.info_logging('Django is started. Call autorun bots')
            start_all_launched_bots()
