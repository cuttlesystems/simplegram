import shutil
from pathlib import Path
import os

import requests
import rest_framework.request
from django.db.models import QuerySet
from django.http import HttpResponse, FileResponse, HttpResponseBase, JsonResponse
from rest_framework.response import Response
from rest_framework import viewsets, status
from django.shortcuts import get_object_or_404
from b_logic.bot_api.bot_api_django_orm import BotApiByDjangoORM
from b_logic.bot_processes_manager import BotProcessesManagerSingle
from b_logic.bot_runner import BotRunner
from bot_constructor.log_configs import logger_django
from bot_constructor.settings import BOTS_DIR
from rest_framework.request import Request
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError

from process_manager_utils.notification_sender import NotificationSender
from process_manager_utils.notification_sender_to_bot_manager import NotificationSenderToBotManager
from .utils import check_bot_token_when_generate_bot
from cuttle_builder.bot_generator_db import BotGeneratorDb
from cuttle_builder.exceptions.bot_gen_exceptions import BotGeneratorException
from .serializers import (BotSerializer, BotSerializerWithBotLink, MessageSerializer, MessageSerializerWithVariants,
                          VariantSerializer, CommandSerializer)
from bots.models import Bot, Message, Variant, Command
from .mixins import RetrieveUpdateDestroyViewSet, ListPostViewSet
from .permissions import (IsMessageOwnerOrForbidden, IsVariantOwnerOrForbidden, IsBotOwnerOrForbidden,
                          IsCommandOwnerOrForbidden, check_is_bot_owner_or_permission_denied)
from .exceptions import ErrorsFromBotGenerator

MESSAGE_WITH_VARIANTS = 'with_variants'
BOT_WITH_LINK = 'with_link'


def set_bot_must_be_generated_value(bot: Bot, must_be_generated: bool) -> None:
    """
    Устанавливает значение в поле бота must_be_generated.
    Args:
        bot: Экземпляр бота из БД.
        must_be_generated: True или False.
    """
    assert isinstance(bot, Bot)
    assert isinstance(must_be_generated, bool)
    if bot.must_be_generated != must_be_generated:
        bot.must_be_generated = must_be_generated
        bot.save()
        logger_django.info_logging(f'Bot_id_{bot.id} must_be_generated value set to: {must_be_generated}.')


class BotViewSet(viewsets.ModelViewSet):
    """
    Отображение всех ботов пользователя и
    CRUD-функционал для экземпляра бота

    Есть такое описание:
    Вот эта функция, точнее класс, но в данный момент это не сильно важно))
    Тут в 14 строке ссылка на BotSerializer, он импортирован из serializers.py, идем туда.

    Вью функция(вью класс) инициализирует сериализатор.
    А данные для сериализатора она возьмет из коллекции Queryset.
    Queryset определяется в методе get_queryset, которая возвращает множество
    объектов Bot в которых Bot.owner равен пользователю, который делает запрос.
    В итоге BotViewSet вернет данные из Queryset, прошедшие через сереализатор,
    то есть только с теми полями, которые мы выбрали в сериализаторе и в формате JSON.

    P.S. В функции perform_create задается значение для поля Bot.owner, функция актуальна для POST запросов.
    POST запрос создает новую запись в таблице Bot.
    В теле POST запроса мы не будем указывать значение для поля owner явно, за нас это сделает метод perform_create.
    """
    permission_classes = (IsBotOwnerOrForbidden,)
    lookup_url_kwarg = 'bot_id_str'
    # указываем имя параметра, в котором будет приходить номер бота, взятый из url (по умолчанию 'pk')

    def get_serializer_class(self):
        if self.request.query_params.get(BOT_WITH_LINK) == '1':
            return BotSerializerWithBotLink
        return BotSerializer

    def get_queryset(self) -> QuerySet:
        return Bot.objects.filter(owner=self.request.user)

    def perform_create(self, serializer: BotSerializer):
        author = self.request.user
        serializer.save(owner=author)

    def perform_update(self, serializer: BotSerializer):
        bot_id = self.kwargs['bot_id_str']
        bot = get_object_or_404(Bot, id=bot_id)
        serializer.save()
        set_bot_must_be_generated_value(bot, True)

    def perform_destroy(self, instance: Bot):
        self._stop_bot_if_it_run(instance.id)
        bot_dir = self._get_bot_dir(instance.id)
        if bot_dir.exists():
            shutil.rmtree(path=bot_dir)
        instance.delete()

    def _get_bot_dir(self, bot_id: int) -> Path:
        assert isinstance(bot_id, int)
        bot_dir = BOTS_DIR / f'bot_{bot_id}'
        return bot_dir

    def _stop_bot_if_it_run(self, bot_id: int):
        assert isinstance(bot_id, int)
        bot_process_manager = BotProcessesManagerSingle()
        # если оказалось, что этого бота уже запускали, то остановим его
        already_started_bot = bot_process_manager.get_process_info(bot_id)
        if already_started_bot is not None:
            already_started_bot.bot_runner.stop()
            bot_process_manager.remove(bot_id)

    def _set_bot_must_be_started_value(self, bot: Bot, must_be_started: bool) -> None:
        """
        Устанавливает значение в поле бота must_be_started.
        Args:
            bot: Экземпляр бота из БД.
            must_be_started: True или False.
        """
        assert isinstance(bot, Bot)
        assert isinstance(must_be_started, bool)
        bot.must_be_started = must_be_started
        bot.save()

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

        self._stop_bot_if_it_run(bot_id)

        if bot.must_be_generated:
            self.generate_bot(request, bot_id_str)

        notification_sender_to_manager = NotificationSenderToBotManager()
        runner = BotRunner(bot_dir, notification_sender_to_manager)
        process_id = runner.start()
        if process_id is not None:
            bot_process_manager = BotProcessesManagerSingle()
            bot_process_manager.register(bot_id, runner)
            notification_sender_to_manager.set_process_manager(bot_process_manager)
            result = JsonResponse(
                {
                    'is_started': True,
                    'result': {
                        'message': 'Start bot ok',
                        'bot_id': bot_id,
                        'process_id': process_id
                    },
                },
                status=requests.codes.ok
            )
            logger_django.info_logging(f'Bot {bot_id} started. Process id: {process_id}')

            self._set_bot_must_be_started_value(bot=bot, must_be_started=True)
            # После выполнения метода generate_bot, в поле бота must_be_generated установиться False.
            # Но, метод _set_bot_must_be_started_value переведёт его обратно в True.
            # Поэтому устанавливаем False для must_be_generated повторно))
            set_bot_must_be_generated_value(bot, False)
        else:
            result = JsonResponse(
                {
                    'is_started': False,
                    'result': 'Bot start error'
                },
                status=requests.codes.method_not_allowed
            )
            logger_django.error_logging('Bot start error')
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
        bot_id_int = int(bot_id_str)
        bot = get_object_or_404(Bot, id=bot_id_int)
        self.check_object_permissions(request, bot)
        if bot.must_be_started:
            self._set_bot_must_be_started_value(bot=bot, must_be_started=False)
        bot_processes_manager = BotProcessesManagerSingle()
        bot_process = bot_processes_manager.get_process_info(bot_id_int)
        if bot_process is not None:
            is_error = bot_process.is_terminated
            if is_error:
                bot_processes_manager.remove(bot_id_int)
                result = JsonResponse(
                    {
                        'is_started': False,
                        'result': {
                            'message': 'There are errors when bot is running, next time fix error before start',
                            'bot_id': bot_id_int
                        }
                    },
                    status=requests.codes.conflict
                )
            elif bot_process.bot_runner.stop():
                bot_processes_manager.remove(bot_id_int)
                result = JsonResponse(
                    {
                        'is_started': False,
                        'result': {
                            'message': 'Bot stopped is ok',
                            'bot_id': bot_id_int,
                            'process_id': bot_process.bot_runner.process_id
                        }
                    },
                    status=requests.codes.ok
                )
            else:
                result = JsonResponse(
                    {
                        'is_started': False,
                        'result': {
                            'message': 'Bot stop error',
                            'bot_id': bot_id_int
                        }
                    },
                    status=requests.codes.internal_server_error
                )
        else:
            result = JsonResponse(
                {
                    'is_started': False,
                    'result': {
                        'message': 'Bot stopped is ok',
                        'bot_id': bot_id_int
                    }
                },
                status=requests.codes.ok
            )
        return result

    @action(
        methods=['POST'],
        detail=True,
        url_path='generate'
    )
    def generate_bot(self, request: rest_framework.request.Request, bot_id_str: str) -> Response:
        """
        Сгенерировать исходный код бота
        Args:
            request: данные запроса
            bot_id_str: идентификатор бота, исходник которого надо сгенерировать
        """
        bot_id = int(bot_id_str)
        bot_django = get_object_or_404(Bot, id=bot_id)
        check_bot_token_when_generate_bot(bot_django)
        # проверка прав, что пользователь может работать с данным ботом (владелец бота)
        self.check_object_permissions(request, bot_django)
        self._stop_bot_if_it_run(bot_id)
        bot_api = BotApiByDjangoORM()
        bot_obj = bot_api.get_bot_by_id(bot_django.id)
        bot_dir = self._get_bot_dir(bot_django.id)
        try:
            generator = BotGeneratorDb(bot_api, bot_obj, str(bot_dir))
            generator.create_bot()
            set_bot_must_be_generated_value(bot_django, False)
            logger_django.info_logging(f'Bot_{bot_id} was generated.')
        except BotGeneratorException as exception:
            # set_bot_must_be_generated_value(bot_django, True)
            raise ErrorsFromBotGenerator(detail=exception)

        return Response({"generate_status": f"Бот № {bot_id} - успешно сгенерирован"},
                        status=status.HTTP_200_OK)

    @action(
        methods=['GET'],
        detail=True,
        url_path='get_bot_zip'
    )
    def get_bot_zip(self, request: rest_framework.request.Request, bot_id_str: str) -> HttpResponseBase:
        """
        Получить zip архив с исходным кодом бота
        Args:
            request: данные запроса
            bot_id_str: идентификатор бота, исходник которого надо получить

        Returns:
            http ответ - зип файл со сгенерированным ботом
        """
        bot_id = int(bot_id_str)
        bot_django = get_object_or_404(Bot, id=bot_id)
        # проверка прав, что пользователь может работать с данным ботом (владелец бота)
        self.check_object_permissions(request, bot_django)
        bot_dir = self._get_bot_dir(bot_django.id)

        if not os.path.exists(bot_dir):
            return Response(
                {'error': f'Код для бота № {bot_id} ещё не сгенерирован'},
                status=status.HTTP_204_NO_CONTENT)

        bot_zip_file_name = str(bot_dir) + '.zip'
        shutil.make_archive(str(bot_dir), 'zip', bot_dir)
        return FileResponse(open(bot_zip_file_name, 'rb'))

    @action(
        methods=['GET'],
        detail=True,
        url_path='state'
    )
    def bot_state(self, request: rest_framework.request.Request, bot_id_str: str) -> JsonResponse:
        bot_id = int(bot_id_str)
        bot_django = get_object_or_404(Bot, id=bot_id)

        # проверка прав, что пользователь может работать с данным ботом (владелец бота)
        self.check_object_permissions(request, bot_django)

        result_dict = {
            'is_started': False,
            'process_id': None,
            'is_generated': self._get_bot_dir(bot_id).exists(),
            'bot_id': bot_id
        }
        bot_processes_manager = BotProcessesManagerSingle()
        bot_info = bot_processes_manager.get_process_info(bot_id)
        if bot_info is not None:
            is_error = bot_info.is_terminated
            result_dict['is_started'] = True
            result_dict['process_id'] = bot_info.bot_runner.process_id
            result_dict['bot_id'] = bot_info.bot_id
            result_dict['is_terminated'] = is_error
        return JsonResponse(result_dict, status=requests.codes.ok)

    @action(
        methods=['GET'],
        detail=True,
        url_path='logs'
    )
    def logs(self, request: rest_framework.request.Request, bot_id_str: str) -> JsonResponse:
        bot_id = int(bot_id_str)
        bot_django = get_object_or_404(Bot, id=bot_id)

        # проверка прав, что пользователь может работать с данным ботом (владелец бота)
        self.check_object_permissions(request, bot_django)

        stdout_log = []
        stderr_log = []
        bot_processes_manager = BotProcessesManagerSingle()
        bot_info = bot_processes_manager.get_process_info(bot_id)
        if bot_info is not None:
            stderr_log = bot_info.bot_runner.get_bot_stderr()
            stdout_log = bot_info.bot_runner.get_bot_stdout()

        result_dict = {
            'bot_id': bot_id,
            'stderr': stderr_log,
            'stdout': stdout_log
        }
        return JsonResponse(result_dict, status=requests.codes.ok)

    @action(
        methods=['GET'],
        detail=False,
        url_path='get_all_starting_bots'
    )
    def get_all_starting_bots(self, request: rest_framework.request.Request) -> Response:
        """
        Получает данные о запущенных ботах пользователя, который делает запрос.
        запрос: {your server address}/api/bots/get_all_starting_bots/

        Args:
            request: объект запроса.

        Returns:
            Апи ответ содержащий список id, запущенных ботов.
        """
        user_bots_from_db = Bot.objects.filter(owner=request.user)
        user_bots_id_list = [bot.id for bot in user_bots_from_db]

        bot_processes_manager = BotProcessesManagerSingle()
        all_running_bots_id_list = bot_processes_manager.get_all_running_bots_id_list()

        all_running_user_bots = set(user_bots_id_list).intersection(set(all_running_bots_id_list))
        return Response(
            data=list(all_running_user_bots),
            status=requests.codes.ok
        )


class MessageViewSet(ListPostViewSet):
    """
    Отображение всех меседжей бота и добавление нового меседжа.
    """

    def get_queryset(self):
        return Message.objects.filter(
            bot__owner=self.request.user,
            bot__id=self.kwargs.get('bot_id')
        )

    def get_serializer_class(self):
        if self.request.query_params.get(MESSAGE_WITH_VARIANTS) == '1':
            return MessageSerializerWithVariants
        return MessageSerializer

    def perform_create(self, serializer: MessageSerializer) -> None:
        bot_id = self.kwargs['bot_id']
        bot = get_object_or_404(Bot, id=bot_id)
        serializer.save(bot=bot)
        set_bot_must_be_generated_value(bot, True)

    def create(self, request: Request, bot_id: int) -> Response:
        bot = get_object_or_404(Bot, id=bot_id)
        check_is_bot_owner_or_permission_denied(request, bot)
        return super().create(request, bot_id)


class OneMessageViewSet(RetrieveUpdateDestroyViewSet):
    """Чтение, обновление и удаление для экземпляра сообщения"""
    queryset = Message.objects.all()
    permission_classes = (IsMessageOwnerOrForbidden,)
    lookup_url_kwarg = 'message_id'

    def get_serializer_class(self):
        if self.request.query_params.get(MESSAGE_WITH_VARIANTS) == '1':
            return MessageSerializerWithVariants
        return MessageSerializer

    def perform_update(self, serializer: MessageSerializer):
        message_id = self.kwargs['message_id']
        message = get_object_or_404(Message, id=message_id)
        serializer.save()
        set_bot_must_be_generated_value(message.bot, True)

    def perform_destroy(self, instance: Message):
        set_bot_must_be_generated_value(instance.bot, True)
        instance.delete()


class VariantViewSet(ListPostViewSet):
    """
    Отображение всех вариантов сообщения и создание нового варианта
    """
    serializer_class = VariantSerializer

    def get_queryset(self):
        return Variant.objects.filter(
            current_message__bot__owner=self.request.user,
            current_message__id=self.kwargs['message_id']
        )

    def perform_create(self, serializer: VariantSerializer) -> None:
        message_id = self.kwargs['message_id']
        message = get_object_or_404(Message, id=message_id)
        serializer.save(current_message=message)
        set_bot_must_be_generated_value(message.bot, True)

    def create(self, request: Request, message_id: int) -> Response:
        message = get_object_or_404(Message, id=message_id)
        if Variant.objects.filter(text=request.data['text'],
                                  current_message=message).exists():
            raise ValidationError(detail={"non_field_errors": "This variant is alredy exists."}, code=400)
        check_is_bot_owner_or_permission_denied(request, message.bot)
        return super().create(request, message_id)


class OneVariantViewSet(RetrieveUpdateDestroyViewSet):
    """Чтение, обновление и удаление для экземпляра варианта"""
    queryset = Variant.objects.all()
    serializer_class = VariantSerializer
    permission_classes = (IsVariantOwnerOrForbidden,)
    lookup_url_kwarg = 'variant_id'

    def perform_update(self, serializer: VariantSerializer):
        variant_id = self.kwargs['variant_id']
        variant: Variant = get_object_or_404(Variant, id=variant_id)
        message: Message = variant.current_message
        serializer.save()
        set_bot_must_be_generated_value(message.bot, True)

    def perform_destroy(self, instance: Variant):
        message: Message = instance.current_message
        set_bot_must_be_generated_value(message.bot, True)
        instance.delete()


class CommandViewSet(ListPostViewSet):
    """
    Отображение всех команд бота и со
    CRUD-функционал для экземпляра команды
    """
    serializer_class = CommandSerializer

    def get_queryset(self):
        return Command.objects.filter(
            bot__owner=self.request.user,
            bot__id=self.kwargs['bot_id'])

    def perform_create(self, serializer: CommandSerializer) -> None:
        bot_id = self.kwargs['bot_id']
        bot = get_object_or_404(Bot, id=bot_id)
        serializer.save(bot=bot)
        set_bot_must_be_generated_value(bot, True)

    def create(self, request: Request, bot_id: int) -> Response:
        bot = get_object_or_404(Bot, id=bot_id)
        check_is_bot_owner_or_permission_denied(request, bot)
        return super().create(request, bot_id)


class OneCommandViewSet(RetrieveUpdateDestroyViewSet):
    """Чтение, обновление и удаление для экземпляра команды"""
    queryset = Command.objects.all()
    serializer_class = CommandSerializer
    permission_classes = (IsCommandOwnerOrForbidden,)
    lookup_url_kwarg = 'command_id'

    def perform_update(self, serializer: CommandSerializer):
        command_id = self.kwargs['command_id']
        command = get_object_or_404(Message, id=command_id)
        serializer.save()
        set_bot_must_be_generated_value(command.bot, True)

    def perform_destroy(self, instance: Command):
        set_bot_must_be_generated_value(instance.bot, True)
        instance.delete()
