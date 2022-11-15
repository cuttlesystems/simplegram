import shutil
import uuid
from pathlib import Path
import rest_framework.request
from django.http import HttpResponse, FileResponse, HttpResponseBase
from rest_framework.response import Response
from rest_framework import viewsets, status
from django.shortcuts import get_object_or_404
from b_logic.bot_api import BotApi
from b_logic.bot_processes_manager import BotProcessesManager
from b_logic.bot_runner import BotRunner
from bot_constructor.settings import BASE_DIR, MEDIA_ROOT, DATA_FILES_ROOT, BOTS_DIR
from rest_framework.request import Request
from rest_framework.decorators import action

from .serializers import BotSerializer, MessageSerializer, VariantSerializer
from bots.models import Bot, Message, Variant
from .mixins import RetrieveUpdateDestroyViewSet
from .permissions import IsMessageOwnerOrForbidden, IsVariantOwnerOrForbidden, IsBotOwnerOrForbidden


class BotViewSet(viewsets.ModelViewSet):
    """
    Отображение всех ботов пользователя и 
    CRUD-функционал для экземпляра бота
    """
    serializer_class = BotSerializer
    permission_classes = (IsBotOwnerOrForbidden,)

    # указываем имя параметра, в котором будет приходить номер бота, взятый из url (по умолчанию 'pk')
    lookup_url_kwarg = 'bot_id_str'

    def get_queryset(self):
        # todo: не указан возвращаемый тип
        return Bot.objects.filter(owner=self.request.user)

    def perform_create(self, serializer: BotSerializer):
        author = self.request.user
        serializer.save(owner=author)

    def _get_bot_dir(self, bot_id: int) -> Path:
        assert isinstance(bot_id, int)
        bot_dir = BOTS_DIR / f'bot_{bot_id}'
        return bot_dir

    @action(
        methods=['POST'],
        detail=True,
        url_path='start'
    )
    def start_bot(self, request: Request, bot_id_str: str) -> HttpResponse:
        """
        Запустить бота. Если бот уже был запущен, то он будет перезапущен
        Args:
            request: данные HTTP запроса
            bot_id_str: идентификатор бота, который хотим запустить

        Returns:
            результат запуска бота
        """
        bot_id = int(bot_id_str)
        bot = get_object_or_404(Bot, id=bot_id)
        self.check_object_permissions(request, bot)

        bot_dir = self._get_bot_dir(bot_id)
        runner = BotRunner(bot_dir)
        bot_process_manager = BotProcessesManager()

        # если оказалось, что этого бота уже запускали, то остановим его
        already_started_bot = bot_process_manager.get_process_info(bot_id)
        if already_started_bot is not None:
            runner.stop(already_started_bot.process_id)
            bot_process_manager.remove(bot_id)

        process_id = runner.start()
        if process_id is not None:
            bot_process_manager.register(bot_id, process_id)
            result = HttpResponse(f'Start bot (pid={process_id})', status=200)
        else:
            result = HttpResponse('Bot start error', status=404)

        return result

    @action(
        methods=['POST'],
        detail=True,
        url_path='stop'
    )
    def stop_bot(self, request: Request, bot_id_str: str) -> HttpResponse:
        """
        Остановить бота
        Args:
            request: данные HTTP запроса
            bot_id_str: идентификатор бота, которого хотим остановить

        Returns:
            http ответ результата запуска бота
        """
        runner = BotRunner(Path())
        bot_id_int = int(bot_id_str)
        bot = get_object_or_404(Bot, id=bot_id_int)
        self.check_object_permissions(request, bot)
        bot_processes_manager = BotProcessesManager()
        bot_process = bot_processes_manager.get_process_info(bot_id_int)
        if bot_process is not None:
            if runner.stop(bot_process.process_id):
                bot_processes_manager.remove(bot_id_int)
                result = HttpResponse('Bot stopped is ok', status=200)
            else:
                result = HttpResponse('Can not stop bot', status=500)
        else:
            result = HttpResponse('Can not stop bot because bot is not stared', status=404)
        return result

    @action(
        methods=['POST'],
        detail=True,
        url_path='generate'
    )
    def generate_bot(self, request: rest_framework.request.Request, bot_id_str: str) -> HttpResponseBase:
        """
        Сгенерировать исходный код бота
        Args:
            request: данные запроса
            bot_id_str: идентификатор бота, исходник которого надо сгенерировать

        Returns:
            http ответ - зип файл со сгенерированным ботом
        """
        bot_id = int(bot_id_str)
        bot = get_object_or_404(Bot, id=bot_id)

        # проверка прав, что пользователь может работать с данным ботом (владелец бота)
        self.check_object_permissions(request, bot)

        # todo: это заглушка, временный код (сюда состыкуем реальные данные)
        bot_api = BotApi('http://127.0.0.1:8000/')
        bot_api.auth_by_token(request.auth.key)
        bot = bot_api.get_bot_by_id(bot.id)
        bot_info_str = ''
        messages = bot_api.get_messages(bot)
        for message in messages:
            bot_info_str += f'    {message}\n'
            variants = bot_api.get_variants(message)
            for variant in variants:
                bot_info_str += f'        {variant}\n'
        bots_dir = BOTS_DIR
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
    """
    Отображение всех меседжей бота и 
    CRUD-функционал для экземпляра меседжа
    """
    serializer_class = MessageSerializer

    def get_queryset(self):
        return Message.objects.filter(
            bot__owner=self.request.user,
            bot__id=self.kwargs.get('bot_id')
        )
    
    def perform_create(self, serializer: MessageSerializer) -> None:
        bot_id = self.kwargs.get('bot_id')
        bot = get_object_or_404(Bot, id=bot_id)
        serializer.save(bot=bot)
    
    def create(self, request: Request, bot_id: int) -> Response:
        bot = get_object_or_404(Bot, id=bot_id)
        if bot.owner != request.user:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().create(request, bot_id)


class OneMessageViewSet(RetrieveUpdateDestroyViewSet):
    """Чтение, обновление и удаление для экземпляра сообщения"""
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = (IsMessageOwnerOrForbidden,)


class VariantViewSet(viewsets.ModelViewSet):
    """
    Отображение всех вариантов сообщения и 
    CRUD-функционал для экземпляра варианта
    """
    serializer_class = VariantSerializer

    def get_queryset(self):
        return Variant.objects.filter(
            current_message__bot__owner=self.request.user,
            current_message__id=self.kwargs.get('message_id')
        )
    
    def perform_create(self, serializer: VariantSerializer) -> None:
        message_id = self.kwargs.get('message_id')
        message = get_object_or_404(Message, id=message_id)
        serializer.save(current_message=message)
    
    def create(self, request: Request, message_id: int) -> Response:
        message = get_object_or_404(Message, id=message_id)
        if message.bot.owner != request.user:
            return Response(
                {"detail": "You do not have permission to perform this action."},
                status=status.HTTP_403_FORBIDDEN
            )
        return super().create(request, message_id)


class OneVariantViewSet(RetrieveUpdateDestroyViewSet):
    """Чтение, обновление и удаление для экземпляра варианта"""
    queryset = Variant.objects.all()
    serializer_class = VariantSerializer
    permission_classes = (IsVariantOwnerOrForbidden,)

