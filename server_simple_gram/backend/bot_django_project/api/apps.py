from django.apps import AppConfig

from bot_constructor.log_configs import logger_django
# from bots.started_bots_managing.restart_bots_manage import start_all_launched_bots


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'

    def ready(self):
        logger_django.info_logging('Django is started. Call autorun bots')
