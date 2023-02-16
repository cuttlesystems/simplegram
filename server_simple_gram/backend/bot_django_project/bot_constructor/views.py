from django.shortcuts import render, redirect
from django.http import FileResponse

from bot_constructor.log_configs import logger_django
from bot_constructor.settings import DESKTOP_APPS_ROOT
from bots.models import User, Bot


DESKTOP_APPS_FILENAME = {
    'chamomile': 'simple_gram_chamomile_2023_02_15.zip',
    'shiboken': 'simple_gram_shiboken_2023_02_15.zip'
}


def index(request):
    template = 'index.html/'
    users_count = User.objects.all().count()
    bots_count = Bot.objects.all().count()
    context = {
        'users_count': users_count,
        'bots_count': bots_count,
    }
    return render(request, template, context)


def download_app(request, os_choice: str):
    desktop_filename = DESKTOP_APPS_FILENAME.get(os_choice, '')
    path_to_file = DESKTOP_APPS_ROOT / desktop_filename
    try:
        response = FileResponse(open(str(path_to_file), 'rb'), as_attachment=True)
        return response
    except FileNotFoundError as error:
        logger_django.error_logging(error)
        return redirect('index')
