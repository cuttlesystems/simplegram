from django.shortcuts import render


def index(request):
    template = 'index.html/'
    download_app_link = "#"
    context = {
        'download_app_link': download_app_link,
    }
    return render(request, template, context)
