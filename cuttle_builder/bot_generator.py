from b_logic.data_objects import BotMessage, MessageVariant
from cuttle_builder.bot_gen_exceptions import BotGeneratorException
from cuttle_builder.bot_generator_params import CUTTLE_BUILDER_PATH
from cuttle_builder.builder.additional.file_read_write.file_manager import FileManager
from cuttle_builder.builder.keyboard_generator.create_reply_keyboard import create_reply_keyboard
from cuttle_builder.builder.handler_generator.create_state_handler import create_state_handler
from cuttle_builder.builder.config_generator.create_config import create_config
from cuttle_builder.builder.state_generator.create_state import create_state
from cuttle_builder.APIFileCreator import APIFileCreator
from typing import List
import typing


class BotGenerator:

    def __init__(
            self,
            messages: List[BotMessage],
            variants: List[MessageVariant],
            start_message_id: int,
            bot_id: int,
            token: str,
            bot_path: str
    ):


        assert all(isinstance(bot_mes, BotMessage) for bot_mes in messages)
        assert all(isinstance(variant, MessageVariant) for variant in variants)
        assert isinstance(start_message_id, int)
        assert isinstance(bot_id, int)

        self._messages: List[BotMessage] = messages
        self._variants: List[MessageVariant] = variants
        self._start_message_id = start_message_id
        self._states: List[int] = []
        self._bot_id: int = bot_id
        self._file_manager = APIFileCreator()
        self._TOKEN = token
        self._bot_directory = bot_path
        self._bot_path = bot_path


        for message in self._messages:
            self._states.append(message.id)

    def _check_token(self):
        left, sep, right = self._TOKEN.partition(':')
        if (not sep) or (not left.isdigit()) or (not right):
            raise Exception('Token is invalid!')

        return True

    def _set_generated_bot_directory(self) -> None:
        print(self._bot_directory)
        self._file_manager.create_bot_directory(self._bot_directory)

    def _is_valid_data(self) -> bool:
        if not self._messages:
            self._file_manager.delete_dir(self._bot_directory)
            raise BotGeneratorException('No messages in database')
        self._check_token()
        return True

    def _get_variants_of_message(self, message_id: int) -> typing.List[MessageVariant]:
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
        return f'a{message_id}'
    def _get_imports_sample(self, imports_file_name):
        imports = str(
            CUTTLE_BUILDER_PATH / 'builder' / 'additional' / 'samples' / 'imports' / f'{imports_file_name}.txt')
        extended_imports = self._file_manager.read_file(imports)
        return extended_imports

    def create_reply_keyboard(self, message_id: int):
        keyboard_name: typing.Optional[str] = None
        # imports
        imports_for_keyboard = self._get_imports_sample('reply_keyboard_import')

        # variants
        variants = self._get_variants_of_message(message_id)

        if len(variants) > 0:
            keyboard_name = self._get_keyboard_name_for_message(message_id)
            keyboard_source_code = create_reply_keyboard(keyboard_name, variants, imports_for_keyboard)
            self._file_manager.create_file_keyboard(self._bot_directory, keyboard_name, keyboard_source_code)

        return keyboard_name

    def _create_state_handler(self, type_, prev_state: typing.Optional[str], prev_state_text: typing.Optional[str], curr_state: typing.Optional[str],
                              send_method: str, text: str, kb: str, extended_imports: str = '') -> str:
        """generate code of state handler

        Args:

            keyboard_name: keyboard name if it is need
            type_ (str): type of message, command, content-type or null, if method give prev state
            prev_state (str): id of previous state
            prev_state_text (str): text of previous state that connect to current state
            curr_state (str): id of current state
            send_method (str): type of sending method (text, photo, video, file, group)
            text (str): text of answer
            kb (str): keyboard of answer
            extended_imports: __

        Returns:
            str: generated code for handler with state and handled text
        """
        import_keyboard = 'from keyboards import {0}'.format(kb) if kb else ''

        extended_imports += '\n' + import_keyboard
        return create_state_handler(extended_imports, type_, prev_state, prev_state_text, curr_state, send_method, text,
                                    kb)

    def _find_previous_messages(self,
                                message_id: int
                                ) -> typing.List[MessageVariant]:
        """get previous message id's related to concrete message from list of all variants

        Args:
            message_id (int): id of current message
            variants (typing.List[dict]): list of all variants

        Returns:
            typing.List[dict]: list of all previous message id's for concrete message
        """
        return [item for item in self._variants if item.next_message_id == message_id]

    def create_file_handlers(self, message: BotMessage) -> None:
        keyboard_generation_counter = 0
        imports_generation_counter = 0
        imports_for_handler = self._get_imports_sample('handler_import')
        if message.id == self._start_message_id:
            keyboard_name = self.create_reply_keyboard(message.id)
            keyboard_generation_counter += 1
            imports_for_start_handler = imports_for_handler + '\n' + 'from aiogram.dispatcher.filters import ' \
                                                                     'Command'
            start_handler_code = self._create_state_handler(
                'Command(\'start\')',
                None,
                '',
                self._get_handler_name_for_message(message.id),
                'text',
                message.text,
                keyboard_name,
                imports_for_start_handler
            )

            self._file_manager.create_file_handler(self._bot_directory, message.id, start_handler_code)
            imports_generation_counter += 1
            restart_handler_code = self._create_state_handler(
                'Command(\'restart\')',
                '*',
                '',
                self._get_handler_name_for_message(message.id),
                'text',
                message.text,
                keyboard_name,
                ''
            )
            self._file_manager.create_file_handler(self._bot_directory, message.id, restart_handler_code)

        previous: typing.List[MessageVariant] = self._find_previous_messages(message.id)
        for prev in previous:
            if keyboard_generation_counter == 0:
                keyboard_name = self.create_reply_keyboard(message.id)
            else:
                keyboard_name = self._get_keyboard_name_for_message(message.id)
            handler_code = self._create_state_handler(
                '',
                f'a{prev.current_message_id}',
                prev.text,
                self._get_handler_name_for_message(message.id),
                'text',
                message.text,
                keyboard_name,
                imports_for_handler if imports_generation_counter == 0 else ''
            )
            self._file_manager.create_file_handler(self._bot_directory, message.id, handler_code)
            keyboard_generation_counter += 1
            imports_generation_counter += 1

        if not previous:
            if keyboard_generation_counter == 0:
                keyboard_name = self.create_reply_keyboard(message.id)
            else:
                keyboard_name = self._get_keyboard_name_for_message(message.id)

            handler_code = self._create_state_handler(
                '',
                None,
                '',
                self._get_handler_name_for_message(message.id),
                'text',
                message.text,
                keyboard_name
            )
            self._file_manager.create_file_handler(message.id, handler_code)


    def create_bot(self) -> None:
        # self._is_valid_data()
        self._set_generated_bot_directory()
        self._create_config_file()
        for message in self._messages:
            self.create_file_handlers(message)
        self._file_manager.create_file_state(self._bot_directory, self._create_state())

    def _create_state(self) -> str:
        """generate code of state class

        Returns:
            str: generated class for states
        """
        extended_imports = self._get_imports_sample('state_import')
        return create_state(extended_imports, self._states)

    def _create_config_file(self):
        extend_imports = self._get_imports_sample('config_import')
        config_code = create_config(extend_imports, {'TOKEN': self._TOKEN})
        self._file_manager.create_config_file(self._bot_directory, config_code)
