import rest_framework.request
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets

from .serializers import User, UserSerializer, BotSerializer, \
    MessageSerializer, VariantSerializer
from bots.models import Bot, Message, Variant


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class BotViewSet(viewsets.ModelViewSet):
    queryset = Bot.objects.all()
    serializer_class = BotSerializer


class MessageViewSet(viewsets.ModelViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer


class VariantViewSet(viewsets.ModelViewSet):
    queryset = Variant.objects.all()
    serializer_class = VariantSerializer


@api_view(['GET'])
def get_message(request: rest_framework.request.Request, value: str):
    assert isinstance(request, rest_framework.request.Request)
    return Response(
        {
            'message_id': value
        }
    )
