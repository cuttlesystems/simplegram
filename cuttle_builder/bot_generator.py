import re
import shutil
import typing
import os
from pathlib import Path

from b_logic.data_objects import BotDescription, BotMessage, BotVariant, ButtonTypesEnum, HandlerInit, BotCommand
from cuttle_builder.builder.additional.helpers.user_message_validator import UserMessageValidator
from cuttle_builder.create_dir_if_doesnt_exist import create_dir_if_it_doesnt_exist
from cuttle_builder.exceptions.bot_gen_exceptions import NoOneMessageException, TokenException, NoStartMessageException
from cuttle_builder.bot_generator_params import CUTTLE_BUILDER_PATH
from cuttle_builder.builder.keyboard_generator.create_keyboard import create_reply_keyboard, create_inline_keyboard
from cuttle_builder.builder.handler_generator.create_state_handler import (create_state_message_handler,
                                                                           create_state_callback_handler)
from cuttle_builder.builder.config_generator.create_config import create_config
from cuttle_builder.builder.state_generator.create_state import create_state
from cuttle_builder.builder.commands_generator.generate_commands import generate_commands_code
from cuttle_builder.builder.app_file_generator.generate_app_file import generate_app_file_code
from cuttle_builder.APIFileCreator import APIFileCreator
from typing import List, Optional

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
            commands: List[BotCommand],
            bot: BotDescription,
            bot_path: str,
    ):
        """
        Класс для создания исходного кода ТГ бота по входному набору сообщений и вариантов
        Args:
            messages: список сообщений
            variants: список вариантов
            bot: экземпляр BotDescription
            bot_path: путь куда будут помещены исходники бота
        """
        assert all(isinstance(bot_mes, BotMessage) for bot_mes in messages)
        assert all(isinstance(variant, BotVariant) for variant in variants)
        assert all(isinstance(command, BotCommand) for command in commands)
        assert isinstance(bot, BotDescription)
        assert isinstance(bot_path, str)

        self._handler_inits: List[HandlerInit] = []
        self._messages: List[BotMessage] = messages
        self._variants: List[BotVariant] = variants
        self._commands: List[BotCommand] = commands
        self._start_message_id = bot.start_message_id
        self._states: List[int] = []
        self._file_manager = APIFileCreator(bot_path)
        self._token = bot.bot_token
        self._bot_directory = bot_path
        self._logs_file_path = self._get_bot_logs_file_path(bot, bot_path)
        self._media_directory = bot_path + '/media'
        self._user_message_validator = UserMessageValidator(messages)

        self._error_message_id = bot.error_message_id
        for message in messages:
            self._states.append(message.id)

    def create_bot(self) -> None:
        self._file_manager.delete_dir(self._bot_directory)
        self._check_valid_data()
        self._create_generated_bot_directory()
        self._create_config_file()
        self._create_app_file()
        self._create_on_startup_commands_file()
        self._create_log_dir_if_it_doesnt_exist()
        for message in self._messages:
            self.create_file_handlers(message)
        self._create_init_handler_files()
        self._file_manager.create_state_file(self._create_state())
        self._file_manager.create_state_file_init()

    def create_file_handlers(self, message: BotMessage) -> None:
        assert isinstance(message, BotMessage)
        # вернет переменные, которые найдены в message.text и присутствуют среди всех объявленных переменных
        variables = self._user_message_validator.get_variables_from_text_exist_in_user_variables(message.text)
        # если переменная из текста сообщения не найдена среди всех заявленных переменных
        # то добавить к ней фигурные скобки
        text = self._user_message_validator.get_validated_message_text(message.text)
        # Fill in additional functions, if variables are exist, get variables, that use in text
        additional_functions = ''
        if len(variables) != 0:
            variable_string_sequence = ", ".join(variables)
            variable_value_string_sequence = ', '.join([f"variables.get('{variable}', '')" for variable in variables])
            additional_functions += self._tab_from_new_line('variables = await state.get_data()')
            additional_functions += \
                self._tab_from_new_line(f'{variable_string_sequence} = {variable_value_string_sequence}')

        keyboard_generation_counter = 0
        imports_generation_counter = 0
        imports_for_handler = self._get_imports_sample('handler_import')
        keyboard_type = message.keyboard_type
        is_init_created = False
        # создать файл с изображением в директории бота и вернуть адрес
        if message.photo is not None:
            image = self.create_image_file_in_bot_directory(
                full_path_to_source_file=message.photo,
                path_to_bot_media_dir=self._media_directory,
                filename='message' + str(message.id),
                file_format=message.photo_file_format
            )
        else:
            image = None

        if message.id == self._start_message_id:
            # Создание клавиатуры для сообщения.
            keyboard_name = self.create_keyboard(message.id, keyboard_type)
            keyboard_generation_counter += 1

            # Создание стартовых хэндлеров.
            imports_for_start_handler = imports_for_handler + '\n' + 'from aiogram.dispatcher.filters import ' \
                                                                     'Command'
            start_handler_code = self._create_state_handler(
                command='start',
                prev_state='*',
                text_to_handle='',
                state_to_set_name=self._get_handler_name_for_message(message.id),
                text_of_answer=text,
                image_answer=image,
                kb=keyboard_name,
                handler_type=ButtonTypesEnum.REPLY,
                extended_imports=imports_for_start_handler,
                additional_functions=additional_functions
            )
            self._file_manager.create_file_handler(str(message.id), start_handler_code)
            is_init_created = self._add_handler_init_by_condition(is_init_created, message.id)

            imports_generation_counter += 1

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
                text_of_answer=text,
                image_answer=image,
                kb=keyboard_name,
                handler_type=ButtonTypesEnum.REPLY,
                extended_imports=imports_for_handler,
                additional_functions=additional_functions
            )
            self._file_manager.create_file_handler(str(message.id), error_handler_code)
            is_init_created = self._add_handler_init_by_condition(is_init_created, message.id)

        # Получение списка вариантов у которых next_message == message.id (принемаемый на вход функцией).
        previous_variants: typing.List[BotVariant] = self._find_previous_variants(message.id)
        for prev_variant in previous_variants:
            if keyboard_generation_counter == 0:
                keyboard_name = self.create_keyboard(message.id, keyboard_type)
            else:
                keyboard_name = self._get_keyboard_name_for_message(message.id)

            # Создание хэндлера для команды /prev_variant.text
            current_message_of_variant = self._get_message_object_by_id(prev_variant.current_message_id)

            handler_code = self._create_state_handler(
                command='',
                prev_state=self._get_handler_name_for_message(prev_variant.current_message_id),
                text_to_handle=prev_variant.text,
                state_to_set_name=self._get_handler_name_for_message(message.id),
                text_of_answer=text,
                image_answer=image,
                kb=keyboard_name,
                handler_type=current_message_of_variant.keyboard_type,
                extended_imports=imports_for_handler if imports_generation_counter == 0 else '',
                additional_functions=additional_functions
            )
            self._file_manager.create_file_handler(str(message.id), handler_code)
            is_init_created = self._add_handler_init_by_condition(is_init_created, message.id)

            keyboard_generation_counter += 1
            imports_generation_counter += 1
        # Получение списка сообщений у которых next_message == message.id (принемаемый на вход функцией).
        previous_messages = self._find_previous_messages(message.id)
        previous_message = previous_messages[0] if previous_messages else None

        # it is ANY_INPUT
        if previous_message is not None:
            if keyboard_generation_counter == 0:
                keyboard_name = self.create_keyboard(message.id, keyboard_type)
            else:
                keyboard_name = self._get_keyboard_name_for_message(message.id)

            # Создание хэндлера для команды /previous_message.variable
            update_state_data = f'await state.update_data({previous_message.variable}=message.text)' \
                if previous_message.variable else ''
            additional_functions = self._tab_from_new_line(update_state_data) + additional_functions
            handler_code = self._create_state_handler(
                command='',
                prev_state=self._get_handler_name_for_message(previous_message.id),
                text_to_handle=None,
                state_to_set_name=self._get_handler_name_for_message(message.id),
                text_of_answer=text,
                image_answer=image,
                kb=keyboard_name,
                handler_type=ButtonTypesEnum.REPLY,
                extended_imports=imports_for_handler if imports_generation_counter == 0 else '',
                additional_functions=additional_functions
            )
            self._file_manager.create_file_handler(str(message.id), handler_code)
            is_init_created = self._add_handler_init_by_condition(is_init_created, message.id)
            keyboard_generation_counter += 1
            imports_generation_counter += 1

    def create_image_file_in_bot_directory(self, full_path_to_source_file: str, path_to_bot_media_dir: str,
                                           filename: str, file_format: str) -> str:
        assert isinstance(full_path_to_source_file, str)
        assert isinstance(path_to_bot_media_dir, str)
        assert isinstance(filename, str)
        assert isinstance(file_format, str)
        Path(path_to_bot_media_dir).mkdir(exist_ok=True)
        full_path_to_file_in_bot_dir = path_to_bot_media_dir + '/' + filename + '.' + file_format
        try:
            shutil.copyfile(full_path_to_source_file, full_path_to_file_in_bot_dir)
            assert os.path.exists(full_path_to_file_in_bot_dir)
            result = full_path_to_file_in_bot_dir
        except FileNotFoundError as error:
            print(f'----------->>>Logging error: {error}')
            result = None
        return result

    def create_keyboard(self, message_id: int, keyboard_type: ButtonTypesEnum) -> typing.Optional[str]:
        assert isinstance(keyboard_type, ButtonTypesEnum)
        variants = self._get_variants_of_message(message_id)
        if len(variants) == 0:
            return None
        keyboard_name = self._get_keyboard_name_for_message(message_id)

        # imports and keyboard
        if keyboard_type == ButtonTypesEnum.REPLY:
            imports_for_keyboard = self._get_imports_sample('reply_keyboard_import')
            keyboard_source_code = create_reply_keyboard(
                keyboard_variable_name_without_suffix=keyboard_name,
                buttons=variants,
                extended_imports=imports_for_keyboard
            )
        elif keyboard_type == ButtonTypesEnum.INLINE:
            imports_for_keyboard = self._get_imports_sample('inline_keyboard_import')
            keyboard_source_code = create_inline_keyboard(
                keyboard_variable_name_without_suffix=keyboard_name,
                buttons=variants,
                extended_imports=imports_for_keyboard
            )

        self._file_manager.create_file_keyboard(keyboard_name, keyboard_source_code)
        self._file_manager.create_keyboard_file_init(keyboard_name)
        return keyboard_name

    def _add_handler_init_by_condition(self, is_init_created: bool, message_id: int) -> bool:
        assert isinstance(is_init_created, bool)
        assert isinstance(message_id, int)
        if not is_init_created:
            is_error_message = message_id == self._error_message_id
            self._handler_inits.append(
                HandlerInit(handler_name=str(message_id), is_error_message=is_error_message)
            )
            is_init_created = True
        return is_init_created

    def _get_bot_logs_dir(self, bot: BotDescription, bot_dir: str) -> str:
        """
        Получает полный путь к файлу для хранения логов бота.

        Args:
            bot (BotDescription): экземпляр BotDescription

        Returns (str): Полный путь к файлу логов бота.

        """
        assert isinstance(bot, BotDescription)
        bot_log_path = Path(bot_dir).parent / 'bot_logs'
        return str(bot_log_path)

    def _get_bot_logs_file_path(self, bot: BotDescription, bot_dir: str) -> str:
        """
        Получает полный путь к файлу для хранения логов бота.

        Args:
            bot (BotDescription): экземпляр BotDescription

        Returns (str): Полный путь к файлу логов бота.

        """
        assert isinstance(bot, BotDescription)

        directory = Path(self._get_bot_logs_dir(bot, bot_dir))
        return str(directory / f'bot_{bot.id}.log')

    def _check_token(self) -> bool:
        left, sep, right = self._token.partition(':')
        if (not sep) or (not left.isdigit()) or (not right):
            raise TokenException('Token is invalid!')
        return True

    def _check_valid_data(self) -> None:
        if not self._messages:
            raise NoOneMessageException(
                'Can\'t generate bot without messages. '
                'At least one message is required.')
        if self._start_message_id is None:
            raise NoStartMessageException(
                'Can\'t generate bot without start message. '
                'Set start message is required.'
            )

    def _create_app_file(self) -> None:
        """Генерирует код app файла (исполняемый файл бота)."""
        extend_imports = self._get_imports_sample('app_file_import')

        app_file_code = generate_app_file_code(extend_imports, self._logs_file_path)
        self._file_manager.create_app_file(app_file_code)

    def _create_config_file(self) -> None:
        extend_imports = self._get_imports_sample('config_import')
        config_code = create_config(extend_imports, {'TOKEN': self._token})
        self._file_manager.create_config_file(config_code)

    def _create_generated_bot_directory(self) -> None:
        self._file_manager.create_bot_directory(self._bot_directory)

    def _create_init_handler_files(self) -> None:
        prepared_handler_inits = self._prepare_init_handlers()
        for handler_init in prepared_handler_inits:
            self._file_manager.create_handler_file_init(handler_init.handler_name)

    def _create_log_dir_if_it_doesnt_exist(self) -> None:
        create_dir_if_it_doesnt_exist(Path(self._logs_file_path).parent)

    def _create_on_startup_commands_file(self) -> None:
        """
        Создает файл с функцией для отображения команд бота.
        """
        commands_code = generate_commands_code(self._commands)
        self._file_manager.create_commands_file(commands_code)

    def _create_state(self) -> str:
        """generate code of state class

        Returns:
            str: generated class for states
        """
        extended_imports = self._get_imports_sample('state_import')
        return create_state(extended_imports, self._states)

    def _create_state_handler(self, command: str, prev_state: Optional[str], text_to_handle: Optional[str],
                              state_to_set_name: Optional[str], text_of_answer: str, image_answer: Optional[str],
                              kb: str, handler_type: ButtonTypesEnum, extended_imports: str = '',
                              additional_functions: str = '') -> str:
        """Подготовка данных и выбор генерируемого хэндлера в зависимости от типа клавиатуры

        Args:
            command (str): type of message, command, content-type or null, if method give prev state
            prev_state (str): id of previous state
            text_to_handle (str): text of previous state that connect to current state
            state_to_set_name (str): id of current state
            text_of_answer (str): text of answer
            image_answer (Optional[str]): path to image file in bot directory
            kb (str): keyboard of answer
            handler_type (ButtonTypesEnum): type of handler (inline or reply)
            extended_imports: __

        Returns:
            str: generated code for handler with state and handled text
        """
        assert isinstance(handler_type, ButtonTypesEnum)
        assert isinstance(additional_functions, str)

        import_keyboard = 'from keyboards import {0}'.format(kb) if kb else ''
        extended_imports += '\n' + import_keyboard
        full_command = f'Command(\'{command}\')' if command != '' else command

        if handler_type == ButtonTypesEnum.REPLY:
            message_handler = create_state_message_handler(extended_imports, full_command, prev_state, text_to_handle,
                                                state_to_set_name, text_of_answer, image_answer, kb,
                                                additional_functions)
        elif handler_type == ButtonTypesEnum.INLINE:
            message_handler = create_state_callback_handler(extended_imports, full_command, prev_state, text_to_handle,
                                                 state_to_set_name, text_of_answer, image_answer, kb,
                                                 additional_functions)
        return message_handler

    def _find_previous_messages(self, message_id: int) -> typing.List[BotMessage]:
        """Получает список собщении у которых next_message == message.id (принемаемый
        на вход функцией)

        Args:
            message_id (int): id of current message

        Returns:
            typing.List[dict]: list of all previous messages for concrete message
        """
        return [item for item in self._messages if item.next_message_id == message_id]

    def _find_previous_variants(self, message_id: int) -> typing.List[BotVariant]:
        """Получает список вариантов у которых next_message == message.id (принемаемый
        на вход функцией)

        Args:
            message_id (int): id of current message

        Returns:
            typing.List[dict]: list of all previous variants for concrete message
        """
        return [item for item in self._variants if item.next_message_id == message_id]

    def _get_handler_name_for_message(self, message_id: int) -> str:
        assert isinstance(message_id, int)
        return get_state_name_by_mes_id(message_id)

    def _get_imports_sample(self, imports_file_name: str) -> str:
        assert isinstance(imports_file_name, str)
        imports = str(
            CUTTLE_BUILDER_PATH / 'builder' / 'additional' / 'samples' / 'imports' / f'{imports_file_name}.txt')
        extended_imports = self._file_manager.read_file(imports)
        return extended_imports

    def _get_keyboard_name_for_message(self, message_id: int) -> Optional[str]:
        assert isinstance(message_id, int)
        keyboard_name = f'keyboard_for_message_id_{message_id}'
        variants = self._get_variants_of_message(message_id)
        if len(variants) == 0:
            keyboard_name = None
        return keyboard_name

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

    def _get_variants_of_message(self, message_id: int) -> typing.List[BotVariant]:
        """generate list of variants, names of buttons in keyboard

        Args:
            message_id (int): id of message

        Returns:
            typing.List[MessageVariant]: list of variants (keyboard buttons) related to concrete message
        """
        return [item for item in self._variants if item.current_message_id == message_id]

    def _prepare_init_handlers(self) -> List[HandlerInit]:
        prepared_handler_inits = []
        for handler_init in self._handler_inits:
            if handler_init.is_error_message:
                prepared_handler_inits.append(handler_init)

        for handler_init in self._handler_inits:
            if not handler_init.is_error_message:
                prepared_handler_inits.append(handler_init)
        return prepared_handler_inits

    def _tab_from_new_line(self, code: str) -> str:
        """
        Prepare generate code: replace next string to new line and add tabulation
        Args:
            code (str): code, that will writen in file
        Returns:
            prepared string, that move next string to new line and add tabulation
        """
        assert isinstance(code, str)
        return f'{code}\n\t'
