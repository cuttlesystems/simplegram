from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status


@api_view(['GET', 'POST'])
def first_endpoint(request):
    if request.method == 'GET':
        return Response({'message': 'Get запрос', 'data': request.data}, status=status.HTTP_200_OK)
    if request.method == 'POST':
        return Response({'message': 'Post запрос', 'data': request.data}, status=status.HTTP_200_OK)
