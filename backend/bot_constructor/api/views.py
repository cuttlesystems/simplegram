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
