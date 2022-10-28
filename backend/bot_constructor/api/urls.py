from django.urls import include, path
from rest_framework import routers

from .views import first_endpoint, get_message, UserViewSet


router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')


urlpatterns = [
    path('', include(router.urls)),
    path('first_endpoint/', first_endpoint, name='first_endpoint'),
    path('message/id/<str:value>/', get_message, name='get_message')
]
