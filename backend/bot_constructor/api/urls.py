from django.urls import include, path

from .views import first_endpoint, get_message

urlpatterns = [
    path('first_endpoint/', first_endpoint, name='first_endpoint'),
    path('message/id/<str:value>/', get_message, name='get_message')
]