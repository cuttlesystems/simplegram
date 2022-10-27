from django.urls import include, path

from .views import first_endpoint


urlpatterns = [
    path('first_endpoint/', first_endpoint, name='first_endpoint'),
]