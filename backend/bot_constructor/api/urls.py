from django.urls import include, path
from rest_framework import routers

from .views import UserViewSet, BotViewSet, MessageViewSet, VariantViewSet


router = routers.DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'bots', BotViewSet, basename='bots')
router.register(r'messages', MessageViewSet, basename='messages')
router.register(r'variants', VariantViewSet, basename='variants')


urlpatterns = [
    path('', include(router.urls))
]
