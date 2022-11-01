import rest_framework.request
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets

from .serializers import User, BotSerializer, \
    MessageSerializer, VariantSerializer
from bots.models import Bot, Message, Variant


# class UserViewSet(viewsets.ModelViewSet):
#     # queryset = User.objects.all()
#     serializer_class = UserSerializer


class BotViewSet(viewsets.ModelViewSet):
    # queryset = Bot.objects.all()
    serializer_class = BotSerializer

    def get_queryset(self): 
        return Bot.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        author = self.request.user
        serializer.save(owner=author)


class MessageViewSet(viewsets.ModelViewSet):
    # queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def get_queryset(self):
        return Message.objects.filter(
            bot__owner=self.request.user,
            bot__id=self.kwargs.get('bot_id')
        )


class VariantViewSet(viewsets.ModelViewSet):
    # queryset = Variant.objects.all()
    serializer_class = VariantSerializer

    def get_queryset(self):
        return Variant.objects.filter(
            current_message__bot__owner=self.request.user,
            current_message__id=self.kwargs.get('message_id')
        )


@api_view(['GET'])
def get_message(request: rest_framework.request.Request, value: str):
    assert isinstance(request, rest_framework.request.Request)
    return Response(
        {
            'message_id': value
        }
    )
