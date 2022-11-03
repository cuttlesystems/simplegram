import rest_framework.request
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from django.shortcuts import get_object_or_404

from .serializers import User, BotSerializer, \
    MessageSerializer, VariantSerializer
from bots.models import Bot, Message, Variant
from .mixins import RetrieveUpdateDestroyViewSet


class BotViewSet(viewsets.ModelViewSet):
    serializer_class = BotSerializer

    def get_queryset(self): 
        return Bot.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(owner=author)

# Вот эта функция, точнее класс, но в данный момент это не сильно важно))
# Тут в 14 строке ссылка на BotSerializer, он импортирован из serializers.py, идем туда.
# 
# Вью функция(вью класс) инициализирует сериализатор.
# А данные для сериализатора она возьмет из коллекции Queryset.
# Queryset определяется в методе get_queryset, которая возвращает множество
# объектов Bot в которых Bot.owner равен пользователю, который делает запрос.
# В итоге BotViewSet вернет данные из Queryset, прошедшие через сереализатор,
# то есть только с теми полями, которые мы выбрали в сериализаторе и в формате JSON.
#
# P.S. В функции perform_create задается значение для поля Bot.owner, функция актуальна для POST запросов.
# POST запрос создает новую запись в таблице Bot.
# В теле POST запроса мы не будем указывать значение для поля owner явно, за нас это сделает метод perform_create.

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer

    def get_queryset(self):
        return Message.objects.filter(
            bot__owner=self.request.user,
            bot__id=self.kwargs.get('bot_id')
        )
    
    def perform_create(self, serializer):
        bot_id = self.kwargs.get('bot_id')
        bot = get_object_or_404(Bot, id=bot_id)
        serializer.save(bot=bot)


class OneMessageViewSet(RetrieveUpdateDestroyViewSet):
    serializer_class = MessageSerializer

    def get_queryset(self):
        return Message.objects.filter(bot__owner=self.request.user)


class VariantViewSet(viewsets.ModelViewSet):
    serializer_class = VariantSerializer

    def get_queryset(self):
        return Variant.objects.filter(
            current_message__bot__owner=self.request.user,
            current_message__id=self.kwargs.get('message_id')
        )
    
    def perform_create(self, serializer):
        message_id = self.kwargs.get('message_id')
        message = get_object_or_404(Message, id=message_id)
        serializer.save(current_message=message)


class OneVariantViewSet(RetrieveUpdateDestroyViewSet):
    serializer_class = VariantSerializer

    def get_queryset(self):
        return Variant.objects.filter(current_message__bot__owner=self.request.user)


@api_view(['GET'])
def get_message(request: rest_framework.request.Request, value: str):
    assert isinstance(request, rest_framework.request.Request)
    return Response(
        {
            'message_id': value
        }
    )


@api_view(['GET'])
def generate_bot(request: rest_framework.request.Request, bot_id: str):
    return Response(
        {
            'message': 'generate bot',
            'bot_id': bot_id,
            'data': request.data
        }
    )
