from django.urls import include, path
from rest_framework import routers

from .views import BotViewSet, MessageViewSet, VariantViewSet


router = routers.DefaultRouter()
router.register(r'bots', BotViewSet, basename='bots')
router.register(r'bots/(?P<bot_id>\d+)/messages', MessageViewSet, basename='messages')
router.register(r'bots/(?P<bot_id>\d+)/messages/(?P<message_id>\d+)/variants', VariantViewSet, basename='variants')


urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
