from django.urls import include, path
from rest_framework import routers

from .views import (BotViewSet, MessageViewSet, OneMessageViewSet,
                    VariantViewSet, OneVariantViewSet, generate_bot)


router = routers.DefaultRouter()
router.register(r'bots', BotViewSet, basename='bots')
router.register(r'bots/(?P<bot_id>\d+)/messages', MessageViewSet, basename='messages')
router.register(r'message', OneMessageViewSet, basename='one_message')
router.register(r'messages/(?P<message_id>\d+)/variants', VariantViewSet, basename='variants')
router.register(r'variant', OneVariantViewSet, basename='one_variant')


urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),

    path(r'generate_bot/<bot_id>/', generate_bot),
]

# Как тут всё работает:
#
# Допустим, что мы отправляем такой GET запрос:
# http://127.0.0.1:8000/api/bots/
# Джанга берет то, что прописано в запросе после http://127.0.0.1:8000/api/
# Это будет - bots/
# И ищет совпадения среди зарегистрированных эндпоинтов(с 9 по 13 строку)
# Находит совпадение в 9-ой строке
# В которой, вторым аргументом указано, какая функция будет выполнена
# Это функция BotViewSet, она импортирована из views.py
# Идём смотреть эту функцию
