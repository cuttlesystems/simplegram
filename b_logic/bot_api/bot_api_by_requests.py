import json
import typing
from typing import List, Optional
from urllib.error import HTTPError

import requests
import urllib.request

from b_logic.bot_api.i_bot_api import IBotApi, BotApiException, SignUpException, CreatingBotException, \
    GetBotListException, UserAuthenticationException, ChangingBotException, DeletingBotException, \
    SettingBotStartMessageException, SettingBotErrorMessageException, GettingBotMessagesException, \
    CreatingMessageException, GettingMessageInformationException, EditingMessageException, DeletingMessageException, \
    DeletingImageException, GettingMessagesVariantsListException, CreatingVariantException, EditingVariantException, \
    LinkingVariantWithNextMessageException, DeletingVariantException, GettingBotCommandsException, \
    CreatingCommandException, BotGenerationException, BotStopException, BotStartupException, \
    GettingRunningBotsInfoException, ReceivingBotLogsException, ConnectionException
from b_logic.data_objects import BotCommand, BotDescription, BotMessage, BotVariant, ButtonTypesEnum, BotLogs, \
    MessageTypeEnum


def convert_image_from_api_response_to_bytes(url: Optional[str]) -> Optional[bytes]:
    """
    Конвертирует изображение по его url в байт код

    Args:
        url (Optional[str]): Url изображения

    Returns:
        Optional[bytes]: Байт код изображения
    """
    result = None
    if url is not None:
        with urllib.request.urlopen(url) as file:
            result = file.read()
    return result


class BotApiByRequests(IBotApi):
    def __init__(self, suite_url: typing.Optional[str] = None):
        """
        Создать объект для работы с данными ботов через rest_api
        Args:
            suite_url: адрес сайта, откуда вызываем методы API
        """
        self._suite_url: str = suite_url
        self._auth_token: Optional[str] = None

    def set_suite(self, suite_url: str):
        """Устанавливает suite_url: корневой URL для API запросов"""
        assert isinstance(suite_url, str)
        self._suite_url = suite_url

    def sign_up(self, username: str, email: str, password: str) -> None:
        """
        Регистрация нового пользователя.

        Args:
            username: Имя
            email: Электронная почта
            password: Пароль
        """
        try:
            response = requests.post(
                url=self._suite_url + 'api/users/',
                data={
                    'username': username,
                    'email': email,
                    'password': password
                }
            )
            if response.status_code != requests.status_codes.codes.created:
                raise SignUpException(response)
                # BotApiException(self._tr('Sign up error: {0}').format(response.text))
        except requests.exceptions.ConnectionError as connection_error:
            raise ConnectionException(str(connection_error))
            # raise BotApiException(self._tr('Connection error: {0}').format(connection_error))

    def authentication(self, username: str, password: str) -> None:
        """
        Провести аутентификацию пользователя и запомнить токен авторизации для
        дальнейшего вызова методов
        Args:
            username: имя пользователя
            password: пароль
        """
        try:
            response = requests.post(
                url=self._suite_url + 'api/auth/token/login/',
                data={
                    'username': username,
                    'password': password
                }
            )
            if response.status_code != requests.status_codes.codes.ok:
                raise UserAuthenticationException(response)
                # raise BotApiException(self._tr('User authentication error: {0}').format(response.text))
            self._auth_token = json.loads(response.text)['auth_token']
        except requests.exceptions.ConnectionError as connection_error:
            raise ConnectionException(str(connection_error))
            # raise BotApiException(self._tr('Connection error: {0}').format(connection_error))

    def auth_by_token(self, token: str) -> None:
        """
        Авторизация пользователя по токену
        Args:
            token: токен авторизации
        """
        assert isinstance(token, str)
        self._auth_token = token

    def get_bots(self) -> List[BotDescription]:
        """
        Получить список ботов пользователя
        Returns:
            список ботов
        """
        response = requests.get(
            url=self._suite_url + 'api/bots/',
            headers=self._get_headers()
        )
        if response.status_code != requests.status_codes.codes.ok:
            raise GetBotListException(response)
            # raise BotApiException(self._tr('Getting bot list error: {0}').format(response.text))
        bots_dict_list: List[dict] = json.loads(response.text)
        bots_list: List[BotDescription] = []
        for bot_dict in bots_dict_list:
            bots_list.append(self._create_bot_obj_from_data(bot_dict))
        return bots_list

    def create_bot(self, bot_name: str, bot_token: str, bot_description: str) -> BotDescription:
        """
        Создать бота
        Args:
            bot_name: название бота
            bot_token: токен бота
            bot_description: описание бота

        Returns:
            объект созданного бота
        """
        bot = BotDescription(
            bot_name=bot_name,
            bot_token=bot_token,
            bot_description=bot_description
        )
        response = requests.post(
            url=self._suite_url + 'api/bots/',
            data=self._create_bot_dict_from_obj(bot),
            headers=self._get_headers()
        )
        if response.status_code != requests.status_codes.codes.created:
            raise CreatingBotException(response)
            # raise BotApiException(self._tr('Creating bot error: {0}').format(response.text))
        return self._create_bot_obj_from_data(json.loads(response.text))
    # -------------------------------------
    def get_bot_by_id(self, bot_id: int, with_link: int = 0) -> BotDescription:
        """
        Получить объект бота с заданным идентификатором
        Args:
            bot_id: идентификатор бота
            with_link: при значении 1 выведет доп поле bot_link

        Returns:
            объект бота
        """
        params = {
            'with_link': with_link,
        }
        response = requests.get(
            url=self._suite_url + f'api/bots/{bot_id}/',
            headers=self._get_headers(),
            params=params
        )
        if response.status_code != requests.status_codes.codes.ok:
            raise GetBotListException(response)
            # raise BotApiException(self._tr('Getting bot list error: {0}').format(response.text))

        return self._create_bot_obj_from_data(json.loads(response.text))

    def change_bot(self, bot: BotDescription) -> None:
        assert isinstance(bot.id, int)
        bot_dict = self._create_bot_dict_from_obj(bot)
        response = requests.patch(
            url=self._suite_url + f'api/bots/{bot.id}/',
            json=bot_dict,
            headers=self._get_headers()
        )
        if response.status_code != requests.status_codes.codes.ok:
            raise ChangingBotException(response)
            # raise BotApiException(self._tr('Changing bot error: {0}').format(response.text))

    def delete_bot(self, bot_id: int) -> None:
        """
        Удалить бота
        Args:
            bot_id: идентификатор бота
        """
        response = requests.delete(
            url=self._suite_url + f'api/bots/{bot_id}/',
            headers=self._get_headers()
        )
        if response.status_code != requests.status_codes.codes.no_content:
            raise DeletingBotException(response)
            # raise BotApiException(self._tr('Deleting bot error: {0}'))

    def set_bot_start_message(self, bot: BotDescription, start_message: BotMessage) -> None:
        """
        Установить сообщение с которого начнется работа с ботом
        Args:
            bot: объект бота
            start_message: объект сообщения, которое будет установлено в качестве стартового
        в качестве стартового
        """
        assert isinstance(bot, BotDescription)
        assert isinstance(start_message, BotMessage)
        response = requests.patch(
            url=self._suite_url + f'api/bots/{bot.id}/',
            json={
                'start_message': start_message.id
            },
            headers=self._get_headers()
        )
        if response.status_code != requests.status_codes.codes.ok:
            raise SettingBotStartMessageException(response)
            # raise BotApiException(self._tr('Settings bot start message error: {0}').format(
            #     response.text))

    def set_bot_error_message(self, bot: BotDescription, error_message: BotMessage) -> None:
        """
        Установить ошибочное сообщение для бота.

        Args:
            bot: объект бота
            error_message: объект сообщения, которое будет установлено в
            качестве ошибочного
        """
        assert isinstance(bot, BotDescription)
        assert isinstance(error_message, BotMessage)
        response = requests.patch(
            url=self._suite_url + f'api/bots/{bot.id}/',
            json={
                'error_message': error_message.id
            },
            headers=self._get_headers()
        )
        if response.status_code != requests.status_codes.codes.ok:
            raise SettingBotErrorMessageException(response)
            # raise BotApiException(self._tr('Settings bot error message error: {0}').format(
            #     response.text))

    def get_messages(self, bot: BotDescription) -> List[BotMessage]:
        """
        Получить все сообщения заданного бота

        Args:
            bot: бот, у которого нужно получить сообщения

        Returns:
            список сообщений бота
        """
        assert isinstance(bot, BotDescription)
        response = requests.get(
            url=self._suite_url + f'api/bots/{bot.id}/messages/',
            headers=self._get_headers()
        )
        if response.status_code != requests.status_codes.codes.ok:
            raise GettingBotMessagesException(response)
            # raise BotApiException(self._tr('Getting bot messages error: {0}').format(response.text))
        messages_list: List[BotMessage] = []
        for message_dict in json.loads(response.text):
            messages_list.append(self._create_bot_message_from_data(message_dict))
        return messages_list

    def create_message(self, bot: BotDescription, text: str,
                       keyboard_type: ButtonTypesEnum, x: int, y: int,
                       photo: Optional[str] = None,
                       photo_filename: Optional[str] = None) -> BotMessage:
        """
        Создать сообщение
        Args:
            bot: объект бота, для которого создается сообщение
            text: тест сообщения
            keyboard_type: тип клавиатуры для сообщения
            x: координата по x
            y: координата по y
            photo: полный путь к файлу с изображением включая имя файла и расширение
            photo_filename: имя файла с расширением

        Returns:
            объект созданного сообщения
        """
        assert isinstance(bot, BotDescription)
        message = BotMessage(
            text=text,
            keyboard_type=keyboard_type,
            photo=photo,
            photo_filename=photo_filename,
            x=x,
            y=y
        )
        response = requests.post(
            url=self._suite_url + f'api/bots/{bot.id}/messages/',
            data=self._create_message_dict_from_message_obj(message),
            headers=self._get_headers(),
            files=self._create_upload_files_message_dict_from_message_obj(message)
        )
        if response.status_code != requests.status_codes.codes.created:
            raise CreatingMessageException(response)
            # raise BotApiException(self._tr('Creating message error: {0}').format(response.text))
        return self._create_bot_message_from_data(json.loads(response.text))

    def get_message_image_by_url(self, message: BotMessage) -> Optional[bytes]:
        assert isinstance(message, BotMessage)
        try:
            url = message.photo
            image_data = urllib.request.urlopen(url).read()
        except HTTPError as image_not_found_error:
            print(f'----------->Image not found: {image_not_found_error}')
            image_data = None
        return image_data

    def get_one_message(self, message_id: int) -> BotMessage:
        assert isinstance(message_id, int)
        response = requests.get(
            url=self._suite_url + f'api/message/{message_id}/',
            headers=self._get_headers()
        )
        if response.status_code != requests.status_codes.codes.ok:
            raise GettingMessageInformationException(response)
            # raise BotApiException(
            #     'Getting message information error: {0}'.format(response.text))
        return self._create_bot_message_from_data(json.loads(response.text))

    def change_message(self, message: BotMessage) -> None:
        assert isinstance(message, BotMessage)
        response = requests.patch(
            url=self._suite_url + f'api/message/{message.id}/',
            json=self._create_message_dict_from_message_obj(message),
            headers=self._get_headers(),
            files=self._create_upload_files_message_dict_from_message_obj(message)
        )
        if response.status_code != requests.status_codes.codes.ok:
            raise EditingMessageException(response)
            # raise BotApiException(
            #     self._tr('Editing message error: {0}').format(response.text))

    def remove_message_image(self, message: BotMessage) -> None:
        assert isinstance(message, BotMessage)
        response = requests.patch(
            url=self._suite_url + f'api/message/{message.id}/',
            json={'photo': None},
            headers=self._get_headers()
        )
        if response.status_code != requests.status_codes.codes.ok:
            raise DeletingImageException(response)
            # raise BotApiException(
            #     self._tr('Deleting image error: {0}').format(response.text))

    def delete_message(self, message: BotMessage):
        assert isinstance(message, BotMessage)
        print(f'delete message id {message.id}')
        response = requests.delete(
            url=self._suite_url + f'api/message/{message.id}/',
            headers=self._get_headers()
        )
        print(f'delete response {response.status_code}')
        if response.status_code != requests.status_codes.codes.no_content:
            raise DeletingMessageException(response)
            # raise BotApiException(self._tr('Deleting message error: {0}').format(response.text))

    def get_variants(self, message: BotMessage) -> List[BotVariant]:
        """
        Получить варианты для заданного сообщения
        Args:
            message: сообщение для которого получаем варианты

        Returns:
            список вариантов
        """
        assert isinstance(message, BotMessage)
        response = requests.get(
            url=self._suite_url + f'api/messages/{message.id}/variants/',
            headers=self._get_headers()
        )
        if response.status_code != requests.status_codes.codes.ok:
            raise GettingMessagesVariantsListException(response)
            # raise BotApiException(
            #     self._tr('Getting variants list for message error: {0}').format(response.text))
        variants: List[BotVariant] = []
        variants_dict_list: List[dict] = json.loads(response.text)
        for variant_dict in variants_dict_list:
            variants.append(self._create_variant_from_data(variant_dict))
        return variants

    def create_variant(self, message: BotMessage, text: str) -> BotVariant:
        """
        Создание варианта
        Args:
            message: объект сообщения для которого создается вариант
            text: текст создаваемого варианта

        Returns:
            объект созданного варианта
        """
        assert isinstance(message, BotMessage)
        variant_obj = BotVariant(
            text=text
        )
        response = requests.post(
            url=self._suite_url + f'api/messages/{message.id}/variants/',
            data=self._create_variant_dict_from_variant_obj(variant_obj),
            headers=self._get_headers()
        )
        if response.status_code != requests.status_codes.codes.created:
            raise CreatingVariantException(response)
            # raise BotApiException(self._tr('Creating variant error: {0}').format(response.text))
        return self._create_variant_from_data(json.loads(response.text))

    def change_variant(self, variant: BotVariant) -> None:
        """
        Изменение варианта.

        Args:
            variant (BotVariant): Вариант который необходимо изменить.
        """
        assert isinstance(variant, BotVariant)
        response = requests.patch(
            url=self._suite_url + f'api/variant/{variant.id}/',
            json=self._create_variant_dict_from_variant_obj(variant),
            headers=self._get_headers()
        )
        if response.status_code != requests.status_codes.codes.ok:
            raise EditingVariantException(response)
            # raise BotApiException(self._tr('Editing variant error: {0}').format(response.text))

    def connect_variant(self, variant: BotVariant, message: BotMessage) -> None:
        """
        Связать вариант и сообщение, к которому перейдем при выборе этого варианта
        Args:
            variant: связываемый вариант
            message: сообщение к которому перейдем
        """
        assert isinstance(variant, BotVariant)
        assert isinstance(message, BotMessage)
        response = requests.patch(
            url=self._suite_url + f'api/variant/{variant.id}/',
            json={
                'next_message': message.id
            },
            headers=self._get_headers()
        )
        if response.status_code != requests.status_codes.codes.ok:
            raise LinkingVariantWithNextMessageException(response)
            # raise BotApiException(
            #     self._tr('Linking variant with next message error: {0}').format(response.text))

    def delete_variant(self, variant: BotVariant) -> None:
        """
        Удаление варианта

        Args:
            variant: вариант который необходимо удалить
        """
        assert isinstance(variant, BotVariant)
        print(f'delete variant id {variant.id}')
        response = requests.delete(
            url=self._suite_url + f'api/variant/{variant.id}/',
            headers=self._get_headers()
        )
        print(f'delete response {response.status_code}')
        if response.status_code != requests.status_codes.codes.no_content:
            raise DeletingVariantException(response)
            # raise BotApiException(self._tr('Deleting variant error: {0}').format(response.text))

    def get_commands(self, bot: BotDescription) -> List[BotCommand]:
        """
        Получить все команды заданного бота

        Args:
            bot: бот, у которого нужно получить команды

        Returns:
            список команд бота
        """
        assert isinstance(bot, BotDescription)
        response = requests.get(
            url=self._suite_url + f'api/bots/{bot.id}/commands/',
            headers=self._get_headers()
        )
        if response.status_code != requests.status_codes.codes.ok:
            raise GettingBotCommandsException(response)
            # raise BotApiException(self._tr('Getting bot commands error: {0}').format(response.text))
        commands_list: List[BotCommand] = []
        for command_dict in json.loads(response.text):
            commands_list.append(self._create_command_from_data(command_dict))
        return commands_list

    def create_command(self, bot: BotDescription, command: str,
                       description: str) -> BotCommand:
        """
        Создать команду

        Args:
            bot: объект бота, для которого создается сообщение
            command: тест сообщения
            description: краткое описание команды

        Returns:
            Объект созданной команды
        """
        assert isinstance(bot, BotDescription)
        command_obj = BotCommand(
            command=command,
            description=description
        )
        response = requests.post(
            url=self._suite_url + f'api/bots/{bot.id}/commands/',
            data=self._create_command_dict_from_command_obj(command_obj),
            headers=self._get_headers()
        )
        if response.status_code != requests.status_codes.codes.created:
            raise CreatingCommandException(response)
            # raise BotApiException(self._tr('Creating command error: {0}').format(response.text))
        return self._create_command_from_data(json.loads(response.text))

    def generate_bot(self, bot: BotDescription) -> None:
        assert isinstance(bot, BotDescription)
        response = requests.post(
            url=self._suite_url + f'api/bots/{bot.id}/generate/',
            headers=self._get_headers()
        )
        if response.status_code != requests.status_codes.codes.ok:
            raise BotGenerationException(response)
            # raise BotApiException(
            #     self._tr('Bot generation error: {0}').format(response.text))

    def start_bot(self, bot: BotDescription) -> None:
        assert isinstance(bot, BotDescription)
        response = requests.post(
            url=self._suite_url + f'api/bots/{bot.id}/start/',
            headers=self._get_headers()
        )
        if response.status_code != requests.status_codes.codes.ok:
            raise BotStartupException(response)
            # raise BotApiException(
            #     self._tr('Bot startup error: {0}').format(response.text))

    def stop_bot(self, bot: BotDescription) -> None:
        assert isinstance(bot, BotDescription)
        response = requests.post(
            url=self._suite_url + f'api/bots/{bot.id}/stop/',
            headers=self._get_headers()
        )
        if response.status_code != requests.status_codes.codes.ok:
            raise BotStopException(response)
            # raise BotApiException(
            #     self._tr('Bot stop error: {0}').format(response.text))

    def get_running_bots_info(self) -> List[int]:
        response = requests.get(
            url=self._suite_url + f'api/bots/get_all_starting_bots/',
            headers=self._get_headers()
        )
        if response.status_code != requests.status_codes.codes.ok:
            raise GettingRunningBotsInfoException(response)
            # raise BotApiException(
            #     self._tr('Getting running bots info error: {0}').format(response.text))
        return json.loads(response.text)

    def get_bot_logs(self, bot: BotDescription) -> BotLogs:
        assert isinstance(bot, BotDescription)
        response = requests.get(
            url=self._suite_url + f'api/bots/{bot.id}/logs/',
            headers=self._get_headers()
        )
        if response.status_code != requests.status_codes.codes.ok:
            raise ReceivingBotLogsException(response)
            # raise BotApiException(self._tr('Receiving bot logs error: {0}').format(response.text))
        response_dict = json.loads(response.text)
        logs = BotLogs()
        logs.stderr_lines = response_dict['stderr']
        logs.stdout_lines = response_dict['stdout']
        return logs

    def _get_headers(self) -> typing.Dict[str, str]:
        """
        Получить словарь заголовков, которые добавляются к запросам.
        Содержит информацию об авторизации.
        Returns:
            словарь с заголовками для запроса
        """
        assert self._auth_token is not None
        return {
            'Authorization': 'Token ' + self._auth_token
        }

    def _create_bot_dict_from_obj(self, bot_obj: BotDescription) -> typing.Dict[str, typing.Any]:
        assert isinstance(bot_obj, BotDescription)
        return {
            'id': bot_obj.id,
            'name': bot_obj.bot_name,
            'token': bot_obj.bot_token,
            'description': bot_obj.bot_description,
            'start_message': bot_obj.start_message_id,
            'error_message': bot_obj.error_message_id
        }

    def _create_bot_obj_from_data(self, bot_dict: dict) -> BotDescription:
        """Создает объект класса BotDescription из входящих данных"""
        bot_description = BotDescription()
        bot_description.id = bot_dict['id']
        bot_description.bot_name = bot_dict['name']
        bot_description.bot_token = bot_dict['token']
        bot_description.bot_description = bot_dict['description']
        bot_description.start_message_id = bot_dict['start_message']
        bot_description.error_message_id = bot_dict['error_message']
        bot_description.bot_link = bot_dict.get('bot_link')
        return bot_description

    def _create_bot_message_from_data(self, message_dict: dict) -> BotMessage:
        """Создает объект класса BotMessage из входящих данных"""
        bot_message = BotMessage()
        bot_message.id = message_dict['id']
        bot_message.text = message_dict['text']
        bot_message.keyboard_type = ButtonTypesEnum(message_dict['keyboard_type'])

        # todo: с этими полями надо разобраться, похоже,
        #  там передается url путь, который надо сначала получить
        bot_message.photo = message_dict['photo']
        bot_message.video = message_dict['video']
        bot_message.file = message_dict['file']

        bot_message.x = message_dict['coordinate_x']
        bot_message.y = message_dict['coordinate_y']

        bot_message.message_type = MessageTypeEnum(message_dict['message_type'])
        bot_message.next_message_id = message_dict['next_message']
        bot_message.variable = message_dict['variable']
        return bot_message

    def _create_message_dict_from_message_obj(self, message: BotMessage) -> dict:
        assert isinstance(message, BotMessage)
        message_dict = {
            'id': message.id,
            'text': message.text,
            'keyboard_type': message.keyboard_type.value,
            'coordinate_x': message.x,
            'coordinate_y': message.y,
            'message_type': message.message_type.value,
            'next_message': message.next_message_id,
            'variable': message.variable
        }
        return message_dict

    def _create_upload_files_message_dict_from_message_obj(self, message: BotMessage) -> dict:
        assert isinstance(message, BotMessage)
        upload_files_message_dict = dict()
        if message.photo and message.photo_filename:
            file_data = get_binary_data_from_image_file(message.photo)
            upload_files_message_dict['photo'] = (message.photo_filename, file_data)
        return upload_files_message_dict

    def _create_variant_from_data(self, variant_dict: dict) -> BotVariant:
        """Создает объект класса MessageVariant из входящих данных"""
        variant = BotVariant()
        variant.id = variant_dict['id']
        variant.text = variant_dict['text']
        variant.current_message_id = variant_dict['current_message']
        variant.next_message_id = variant_dict['next_message']
        return variant

    def _create_variant_dict_from_variant_obj(self, variant_obj: BotVariant) -> dict:
        """Создание payload(body) для api запроса"""
        variant_dict = {
            'id': variant_obj.id,
            'text': variant_obj.text,
            'current_message': variant_obj.current_message_id,
            'next_message': variant_obj.next_message_id
        }
        return variant_dict

    def _create_command_from_data(self, command_dict: dict) -> BotCommand:
        """Создает объект класса BotCommand из входящих данных"""
        command = BotCommand()
        command.id = command_dict['id']
        command.bot_id = command_dict['bot']
        command.command = command_dict['command']
        command.description = command_dict['description']
        return command

    def _create_command_dict_from_command_obj(self, command_obj: BotCommand) -> dict:
        """Создание payload(body) для api запроса"""
        command_dict = {
            'id': command_obj.id,
            'bot': command_obj.bot_id,
            'command': command_obj.command,
            'description': command_obj.description
        }
        return command_dict

    def _tr(self, mes: str) -> str:
        return tran('BotApiByRequests.manual', mes)
