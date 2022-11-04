import shutil
import uuid
from pathlib import Path
from zipfile import ZipFile

import rest_framework.request
from django.http import HttpResponse, FileResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets, status
from django.shortcuts import get_object_or_404
from b_logic.bot_api import BotApi
from bot_constructor.settings import BASE_DIR, MEDIA_ROOT, DATA_FILES_ROOT

from .serializers import BotSerializer, MessageSerializer, VariantSerializer
from bots.models import Bot, Message, Variant
from .mixins import RetrieveUpdateDestroyViewSet
from .permissions import IsBotOwnerOrForbidden


class BotViewSet(viewsets.ModelViewSet):
    serializer_class = BotSerializer

    def get_queryset(self): 
        return Bot.objects.filter(owner=self.request.user)

    def perform_create(self, serializer: BotSerializer):
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
    
    def perform_create(self, serializer: MessageSerializer):
        bot_id = self.kwargs.get('bot_id')
        bot = get_object_or_404(Bot, id=bot_id)
        serializer.save(bot=bot)
    
    def create(self, request, *args, **kwargs):
        bot_id = self.kwargs.get('bot_id')
        bot = get_object_or_404(Bot, id=bot_id)
        if bot.owner != request.user:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().create(request, *args, **kwargs)


class OneMessageViewSet(RetrieveUpdateDestroyViewSet):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (IsBotOwnerOrForbidden,)


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
    
    def create(self, request, *args, **kwargs):
        message_id = self.kwargs.get('message_id')
        message = get_object_or_404(Message, id=message_id)
        if message.bot.owner != request.user:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().create(request, *args, **kwargs)


class OneVariantViewSet(RetrieveUpdateDestroyViewSet):
    queryset = Variant.objects.all()
    serializer_class = VariantSerializer
    permission_classes = (IsBotOwnerOrForbidden,)


@api_view(['GET'])
def generate_bot(request: rest_framework.request.Request, bot_id: str):
    bot_api = BotApi('http://127.0.0.1:8000/')
    bot_api.auth_by_token(request.auth.key)
    bot = bot_api.get_bot_by_id(int(bot_id))
    bot_info_str = ''
    messages = bot_api.get_messages(bot)
    for message in messages:
        bot_info_str += f'    {message}\n'
        variants = bot_api.get_variants(message)
        for variant in variants:
            bot_info_str += f'        {variant}\n'
    bots_dir = Path(DATA_FILES_ROOT) / 'generated_bots'
    bots_dir.mkdir(parents=True, exist_ok=True)
    botname = str(uuid.uuid4())
    bot_dir = bots_dir / botname
    bot_dir.mkdir()
    bot_info_file = bot_dir / 'bot_information.txt'
    with open(bot_info_file, 'w') as bot_info_file:
        bot_info_file.write(bot_info_str)

    bot_zip_file_name = str(bot_dir) + '.zip'
    shutil.make_archive(str(bot_dir), 'zip', bot_dir)

    return FileResponse(open(bot_zip_file_name, 'rb'))
