import rest_framework.request
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets

from .serializers import User, UserSerializer

@api_view(['GET', 'POST'])
def first_endpoint(request: rest_framework.request.Request):
    if request.method == 'GET':
        return Response({'message': 'Get запрос', 'data': request.data}, status=status.HTTP_200_OK)
    if request.method == 'POST':
        return Response({'message': 'Post запрос', 'data': request.data}, status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

@api_view(['GET'])
def get_message(request: rest_framework.request.Request, value: str):
    assert isinstance(request, rest_framework.request.Request)
    return Response(
        {
            'message_id': value
        }
    )
