"""
WSGI config for bot_constructor project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from bot_constructor.log_configs import logger_django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bot_constructor.settings')

from bots.started_bots_managing.restart_bots_manage import start_all_launched_bots

logger_django.info_logging('Django is started. Call autorun bots')
start_all_launched_bots()

application = get_wsgi_application()
