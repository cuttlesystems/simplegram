import rest_framework.request
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets

from .serializers import UserSerializer, MessageSerializer, VariantSerializer
from bots.models import User, Message, Variant

@api_view(['GET', 'POST'])
def first_endpoint(request: rest_framework.request.Request):
    if request.method == 'GET':
        return Response({'message': 'Get запрос', 'data': request.data}, status=status.HTTP_200_OK)
    if request.method == 'POST':
        return Response({'message': 'Post запрос', 'data': request.data}, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


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
