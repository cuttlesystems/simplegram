import typing
import io
import os

from b_logic.data_objects import BotMessage, BotVariant, ButtonTypes, HandlerInit
from cuttle_builder.bot_gen_exceptions import BotGeneratorException
from cuttle_builder.bot_generator_params import CUTTLE_BUILDER_PATH
from cuttle_builder.builder.keyboard_generator.create_keyboard import create_reply_keyboard, create_inline_keyboard
from cuttle_builder.builder.handler_generator.create_state_handler import (create_state_message_handler,
                                                                           create_state_callback_handler)
from cuttle_builder.builder.config_generator.create_config import create_config
from cuttle_builder.builder.state_generator.create_state import create_state
from cuttle_builder.APIFileCreator import APIFileCreator
from typing import List, Optional
from PIL import Image

from cuttle_builder.builder.state_generator.to_state import get_state_name_by_mes_id

START_COMANDS = [
    'start',
    'restart'
]


class BotGenerator:

    def __init__(
            self,
            messages: List[BotMessage],
            variants: List[BotVariant],
            start_message_id: int,
            token: str,
            bot_path: str,
            error_message_id: int = None
    ):
        """
        Класс для создания исходного кода ТГ бота по входному набору сообщений и вариантов
        Args:
            messages: список сообщений
            variants: список вариантов
            start_message_id: идентификатор начального сообщения, с которого начинается бот
            token: токен телеграм бота
            bot_path: путь куда будут помещены исходники бота
        """
        assert all(isinstance(bot_mes, BotMessage) for bot_mes in messages)
        assert all(isinstance(variant, BotVariant) for variant in variants)
        assert isinstance(start_message_id, int)
        assert isinstance(token, str)
        assert isinstance(bot_path, str)

        self._handler_inits: List[HandlerInit] = []
        self._variants: List[BotVariant] = variants
        self._start_message_id = start_message_id
        self._states: List[int] = []
        self._file_manager = APIFileCreator()
        self._token = token
        self._bot_directory = bot_path
        self._media_directory = bot_path + '/media'
        self._error_message_id = error_message_id
        for message in messages:
            self._states.append(message.id)
        self._messages: List[BotMessage] = messages

    def _check_token(self):
        left, sep, right = self._token.partition(':')
        if (not sep) or (not left.isdigit()) or (not right):
            raise Exception('Token is invalid!')

        return True

    def _create_generated_bot_directory(self) -> None:
        print(self._bot_directory)
        self._file_manager.create_bot_directory(self._bot_directory)

    def _is_valid_data(self) -> bool:
        if not self._messages:
            raise BotGeneratorException('No messages in database')
        self._check_token()
        return True

    def _get_variants_of_message(self, message_id: int) -> typing.List[BotVariant]:
        """generate list of variants, names of buttons in keyboard

        Args:
            message_id (int): id of message

        Returns:
            typing.List[MessageVariant]: list of variants (keyboard buttons) related to concrete message
        """
        return [item for item in self._variants if item.current_message_id == message_id]

    def _get_keyboard_name_for_message(self, message_id: int) -> str:
        assert isinstance(message_id, int)
        return f'keyboard_for_message_id_{message_id}'

    def _get_handler_name_for_message(self, message_id: int) -> str:
        assert isinstance(message_id, int)
        return get_state_name_by_mes_id(message_id)

    def _get_imports_sample(self, imports_file_name) -> str:
        imports = str(
            CUTTLE_BUILDER_PATH / 'builder' / 'additional' / 'samples' / 'imports' / f'{imports_file_name}.txt')
        extended_imports = self._file_manager.read_file(imports)
        return extended_imports

    def _get_message_object_by_id(self, message_id: int) -> Optional[BotMessage]:
        """Ищет и возвращает объект сообщения с нужным ид

        Args:
            message_id (int): Ид сообщения

        Returns:
            Optional[BotMessage]: Объект сообщения или None
        """
        for message in self._messages:
            if message.id == message_id:
                return message
        return None

    def create_image_file_from_bytes(self, file: bytes, path_to_save: str, filename: str, format: str) -> str:
        full_path = path_to_save + '/' + filename + '.' + format
        Image.open(io.BytesIO(file)).save(full_path)
        assert os.path.exists(full_path)
        # print(f'Image {filename} created')
        return full_path

    def create_keyboard(self, message_id: int, keyboard_type: ButtonTypes) -> typing.Optional[str]:
        assert isinstance(keyboard_type, ButtonTypes)
        # variants
        variants = self._get_variants_of_message(message_id)
        if len(variants) == 0:
            return None
        keyboard_name = self._get_keyboard_name_for_message(message_id)

        # imports and keyboard
        if keyboard_type == ButtonTypes.REPLY:
            imports_for_keyboard = self._get_imports_sample('reply_keyboard_import')
            keyboard_source_code = create_reply_keyboard(
                keyboard_variable_name_without_suffix=keyboard_name,
                buttons=variants,
                extended_imports=imports_for_keyboard
            )
        elif keyboard_type == ButtonTypes.INLINE:
            imports_for_keyboard = self._get_imports_sample('inline_keyboard_import')
            keyboard_source_code = create_inline_keyboard(
                keyboard_variable_name_without_suffix=keyboard_name,
                buttons=variants,
                extended_imports=imports_for_keyboard
            )

        self._file_manager.create_file_keyboard(self._bot_directory, keyboard_name, keyboard_source_code)
        self._file_manager.create_keyboard_file_init(self._bot_directory, keyboard_name)
        return keyboard_name

    def _create_state_handler(self, command: str, prev_state: Optional[str], text_to_handle: Optional[str],
                              state_to_set_name: Optional[str], text_of_answer: str, image_answer: Optional[str],
                              kb: str, handler_type: ButtonTypes, extended_imports: str = '') -> str:
        """Подготовка данных и выбор генерируемого хэндлера в зависимости от типа клавиатуры

        Args:
            keyboard_name: keyboard name if it is need
            command (str): type of message, command, content-type or null, if method give prev state
            prev_state (str): id of previous state
            text_to_handle (str): text of previous state that connect to current state
            state_to_set_name (str): id of current state
            text_of_answer (str): text of answer
            image_answer (Optional[str]): path to image file in bot directory
            kb (str): keyboard of answer
            handler_type (ButtonTypes): type of handler (inline or reply)
            extended_imports: __

        Returns:
            str: generated code for handler with state and handled text
        """
        assert isinstance(handler_type, ButtonTypes)

        import_keyboard = 'from keyboards import {0}'.format(kb) if kb else ''
        extended_imports += '\n' + import_keyboard
        full_command = f'Command(\'{command}\')' if command != '' else command
        if handler_type == ButtonTypes.REPLY:
            return create_state_message_handler(extended_imports, full_command, prev_state, text_to_handle,
                                                state_to_set_name, text_of_answer, image_answer, kb)
        elif handler_type == ButtonTypes.INLINE:
            return create_state_callback_handler(extended_imports, full_command, prev_state, text_to_handle,
                                                 state_to_set_name, text_of_answer, image_answer, kb)

    def _find_previous_variants(self, message_id: int) -> typing.List[BotVariant]:
        """Получает список вариантов у которых next_message == message.id (принемаемый
        на вход функцией)

        Args:
            message_id (int): id of current message

        Returns:
            typing.List[dict]: list of all previous variants for concrete message
        """
        return [item for item in self._variants if item.next_message_id == message_id]

    def _create_init_handler_files(self):
        for handler_init in self._handler_inits:
            if handler_init.is_error_message:
                self._file_manager.create_handler_file_init(self._bot_directory, handler_init.handler_name)
        for handler_init in self._handler_inits:
            if not handler_init.is_error_message:
                self._file_manager.create_handler_file_init(self._bot_directory, handler_init.handler_name)

    def create_file_handlers(self, message: BotMessage) -> None:
        keyboard_generation_counter = 0
        imports_generation_counter = 0
        imports_for_handler = self._get_imports_sample('handler_import')
        keyboard_type = message.keyboard_type
        is_init_created = False
        # создать файл с изображение в директории бота и вернуть адрес
        if message.photo:
            image = self.create_image_file_from_bytes(
                file=message.photo,
                path_to_save=self._media_directory,
                filename='message' + str(message.id),
                format='png'
            )
        else:
            image = message.photo

        if message.id == self._start_message_id:

            # Создание клавиатуры для сообщения.
            keyboard_name = self.create_keyboard(message.id, keyboard_type)
            keyboard_generation_counter += 1

            # Создание стартовых хэндлеров.
            imports_for_start_handler = imports_for_handler + '\n' + 'from aiogram.dispatcher.filters import ' \
                                                                     'Command'
            start_handler_code = self._create_state_handler(
                command='start',
                prev_state=None,
                text_to_handle='',
                state_to_set_name=self._get_handler_name_for_message(message.id),
                text_of_answer=message.text,
                image_answer=image,
                kb=keyboard_name,
                handler_type=ButtonTypes.REPLY,
                extended_imports=imports_for_start_handler
            )
            self._file_manager.create_file_handler(self._bot_directory, message.id, start_handler_code)
            if not is_init_created:
                self._handler_inits.append(
                    HandlerInit(handler_name=message.id, is_error_message=False)
                )
                is_init_created = True

            imports_generation_counter += 1
            restart_handler_code = self._create_state_handler(
                command='restart',
                prev_state='*',
                text_to_handle='',
                state_to_set_name=self._get_handler_name_for_message(message.id),
                text_of_answer=message.text,
                image_answer=image,
                kb=keyboard_name,
                handler_type=ButtonTypes.REPLY,
                extended_imports=''
            )
            self._file_manager.create_file_handler(self._bot_directory, message.id, restart_handler_code)

        if message.id == self._error_message_id:
            # Создание клавиатуры для сообщения.
            keyboard_name = self.create_keyboard(message.id, keyboard_type)
            keyboard_generation_counter += 1

            # Создание стартовых хэндлеров.
            error_handler_code = self._create_state_handler(
                command='',
                prev_state='*',
                text_to_handle='',
                state_to_set_name=self._get_handler_name_for_message(message.id),
                text_of_answer=message.text,
                image_answer=image,
                kb=keyboard_name,
                handler_type=ButtonTypes.REPLY,
                extended_imports=imports_for_handler
            )
            self._file_manager.create_file_handler(self._bot_directory, message.id, error_handler_code)
            if not is_init_created:
                self._handler_inits.append(
                    HandlerInit(handler_name=message.id, is_error_message=True)
                )
                is_init_created = True

        # Получение списка вариантов у которых next_message == message.id (принемаемый на вход функцией).
        previous_variants: typing.List[BotVariant] = self._find_previous_variants(message.id)
        for prev_variant in previous_variants:
            if keyboard_generation_counter == 0:
                keyboard_name = self.create_keyboard(message.id, keyboard_type)
            else:
                keyboard_name = self._get_keyboard_name_for_message(message.id)

            # Создание хэндлера для команды /prev_variant.text
            # нужно получить prev_variant.current_message.keyboard_type
            # prev_variant.current_message_id
            current_message_of_variant = self._get_message_object_by_id(prev_variant.current_message_id)

            handler_code = self._create_state_handler(
                command='',
                prev_state=self._get_handler_name_for_message(prev_variant.current_message_id),
                text_to_handle=prev_variant.text,
                state_to_set_name=self._get_handler_name_for_message(message.id),
                text_of_answer=message.text,
                image_answer=image,
                kb=keyboard_name,
                handler_type=current_message_of_variant.keyboard_type,
                extended_imports=imports_for_handler if imports_generation_counter == 0 else ''
            )
            self._file_manager.create_file_handler(self._bot_directory, message.id, handler_code)
            if not is_init_created:
                self._handler_inits.append(
                    HandlerInit(handler_name=message.id, is_error_message=False)
                )
                is_init_created = True

            keyboard_generation_counter += 1
            imports_generation_counter += 1

    def create_bot(self) -> None:
        self._file_manager.delete_dir(self._bot_directory)
        self._is_valid_data()
        self._create_generated_bot_directory()
        self._create_config_file()
        for message in self._messages:
            self.create_file_handlers(message)
        self._create_init_handler_files()
        self._file_manager.create_state_file(self._bot_directory, self._create_state())
        self._file_manager.create_state_file_init(self._bot_directory)

    def _create_state(self) -> str:
        """generate code of state class

        Returns:
            str: generated class for states
        """
        extended_imports = self._get_imports_sample('state_import')
        return create_state(extended_imports, self._states)

    def _create_config_file(self):
        extend_imports = self._get_imports_sample('config_import')
        config_code = create_config(extend_imports, {'TOKEN': self._token})
        self._file_manager.create_config_file(self._bot_directory, config_code)
