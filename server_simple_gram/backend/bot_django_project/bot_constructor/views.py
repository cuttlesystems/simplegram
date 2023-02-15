from django.shortcuts import render, redirect
from django.http import FileResponse

from bot_constructor.log_configs import logger_django
from bot_constructor.settings import BASE_DIR
from bots.models import User, Bot


def index(request):
    template = 'index.html/'
    users_count = User.objects.all().count()
    bots_count = Bot.objects.all().count()
    context = {
        'users_count': users_count,
        'bots_count': bots_count,
    }
    return render(request, template, context)


def download_app(request):
    path_to_file = BASE_DIR / 'test.txt'
    try:
        response = FileResponse(open(str(path_to_file), 'rb'), as_attachment=True)
        return response
    except FileNotFoundError as error:
        logger_django.error_logging(error)
        return redirect('index')
