from b_logic.data_objects import BotMessage, MessageVariant
from cuttle_builder.builder.additional.file_read_write.file_manager import FileManager
from cuttle_builder.builder.keyboard_generator.create_reply_keyboard import create_reply_keyboard
from cuttle_builder.builder.handler_generator.create_state_handler import create_state_handler
from cuttle_builder.builder.config_generator.create_config import create_config
from cuttle_builder.builder.state_generator.create_state import create_state
from typing import List
import typing


# underscore and types
class BotGenerator:

    def __init__(
            self,
            messages: List[BotMessage],
            variants: List[MessageVariant],
            start_message_id: int,
            bot_id: int,
            TOKEN: str
    ):

        # гарантии типов
        assert all(isinstance(bot_mes, BotMessage) for bot_mes in messages)
        assert all(isinstance(variant, MessageVariant) for variant in variants)
        assert isinstance(start_message_id, int)
        assert isinstance(bot_id, int)

        self._messages: List[BotMessage] = messages
        self._variants: List[MessageVariant] = variants
        self._start_message_id_str = f'a{start_message_id}'
        self._states: List[int] = []
        self._bot_id: int = bot_id
        self._file_manager = FileManager()
        self._TOKEN = TOKEN

        for message in self._messages:
            self._states.append(message.id)

    def _get_keyboard_name_for_message(self, message_id: int) -> str:
        assert isinstance(message_id, int)
        return f'keyboard_for_message_id_{message_id}'

    def _generate_keyboard(self, message_id: int, bot_directory: str) -> typing.Optional[str]:
        """create keyboard in directory and return name of this keyboard

        Args:
            message_id (int): id of message, that will used in name of keyboard
            bot_directory (str): directory, where keyboard will store

        Returns:
            str: name of generated keyboard or None
        """
        variants = self._get_variants_of_message(message_id)

        keyboard_name: typing.Optional[str] = None

        # если есть варианты, которые принадлежат текущему сообщению
        if len(variants) > 0:
            keyboard_name = self._get_keyboard_name_for_message(message_id)
            keyboard_source_code = self._create_reply_keyboard(keyboard_name, variants)
            self.create_file_keyboard(bot_directory, keyboard_name, keyboard_source_code)

        return keyboard_name

    def _validate(self) -> List[BotMessage]:
        return self._messages

    def check_token(self) -> bool:
        """
        Validate BOT token

        :param token:
        :return:
        """
        left, sep, right = self._TOKEN.partition(':')
        if (not sep) or (not left.isdigit()) or (not right):
            raise Exception('Token is invalid!')

        return True
    def create_bot(self) -> None:

        if not self._validate():
            print('U not create a messages')
            self._file_manager.delete_bot_by_id(self._bot_id)
            return
        bot_directory = self._file_manager.create_bot_directory(self._bot_id)
        if self.check_token():
            self._create_config_file(bot_directory)
        for message in self._messages:

            keyboard_generation_counter = 0  # count number of generation of keyboard
            message_id = f'a{message.id}'

            if message_id == self._start_message_id_str:
                keyboard_name = self._generate_keyboard(message.id, bot_directory)
                keyboard_generation_counter += 1
                start_handler_code = self._create_state_handler(
                    'Command(\'start\')',
                    None,
                    '',
                    f'a{message.id}',
                    'text',
                    message.text,
                    keyboard_name
                )
                self.create_file_handler(bot_directory, message_id, start_handler_code)

                restart_handler_code = self._create_state_handler(
                    'Command(\'restart\')',
                    '*',
                    '',
                    f'a{message.id}',
                    'text',
                    message.text,
                    keyboard_name
                )
                self.create_file_handler(bot_directory, message_id, restart_handler_code)
                # continue

            previous = self._find_previous_messages(message.id)
            for prev in previous:
                keyboard_name = ''
                if keyboard_generation_counter == 0:
                    keyboard_name = self._generate_keyboard(message.id, bot_directory)
                else:
                    keyboard_name = self._get_keyboard_name_for_message(message.id)
                handler_code = self._create_state_handler(
                    '',
                    f'a{prev.current_message_id}',
                    prev.text,
                    f'a{message.id}',
                    'text',
                    message.text,
                    keyboard_name
                )
                self.create_file_handler(bot_directory, message_id, handler_code)
                keyboard_generation_counter += 1

            if not previous:
                keyboard_name = self._generate_keyboard(message.id, bot_directory)

                handler_code = self._create_state_handler(
                    '',
                    None,
                    '',
                    message_id,
                    'photo',
                    message.text,
                    keyboard_name
                )
                self.create_file_handler(bot_directory, message_id, handler_code)
        self.create_file_state(bot_directory)

    def _get_variants_of_message(self, message_id: int) -> typing.List[MessageVariant]:
        """generate list of variants, names of buttons in keyboard

        Args:
            message_id (int): id of message

        Returns:
            typing.List[MessageVariant]: list of variants (keyboard buttons) related to concrete message
        """
        return [item for item in self._variants if item.current_message_id == message_id]

    # generate code of reply keyboard, take text from file and add keyboard with keyboard name
    def _create_reply_keyboard(self, keyboard_variable_name_without_suffix: str, buttons: typing.List[MessageVariant]) -> str:
        """generate code of reply keyboard

        Args:
            keyboard_variable_name_without_suffix (str): name of keyboard
            buttons (typing.List[MessageVariant]): buttons, related to this keyboard

        Returns:
            str: generated code for concrete keyboard
        """
        return create_reply_keyboard(keyboard_variable_name_without_suffix, buttons)

    # find previous message id's from variants list
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

    def _create_state_handler(self, type_, prev_state: str, prev_state_text: str, curr_state: str,
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

        all_imports = import_keyboard
        if extended_imports == '':
            all_imports += '\n' + extended_imports

        return create_state_handler(all_imports, type_, prev_state, prev_state_text, curr_state, send_method, text, kb)

    # create keyboard file in directory
    def create_file_keyboard(self, bot_name: str, keyboard_name: str, keyboard_code: str):
        """create file in specific directory, contains keyboard and register this keyboard in the package

        Args:
            bot_name (str): name of bot
            keyboard_name (str): name of keyboard (message_id + _kb)
            keyboard_code (str): generated code of keyboard
        """
        self._file_manager.create_file(f'{bot_name}/keyboards/{keyboard_name}.py', keyboard_code,
                                       f'{bot_name}/keyboards/__init__.py',
                                       f'\nfrom .{keyboard_name} import {keyboard_name}')

    # create handler file in directory
    def create_file_handler(self, bot_name: str, name: str, code: str):
        """create file in specific directory, contains handler and register this handler in the package

        Args:
            bot_name (str): name of bot
            name (str): name of handler (message_id)
            code (str): generated code of handler
        """
        self._file_manager.create_file(f'{bot_name}/handlers/get_{name}.py', code, f'{bot_name}/handlers/__init__.py',
                                       f'from .get_{name} import dp\n')

    # create state file in directory
    def create_file_state(self, bot_name: str) -> None:
        """create file in specific directory, contains states class and register this class in the package

        Args:
            bot_name (str): name of bot
        """
        self._file_manager.create_file(f'{bot_name}/state/states.py', self._create_state(),
                                       f'{bot_name}/state/__init__.py', 'from .states import States')
    def _create_config_file(self, bot_directory: str):
        config_code = create_config({'TOKEN': self._TOKEN})
        self._file_manager.create_file(f'{bot_directory}/data/config.py', config_code)

    # generate code of state, based on states, that given from bot (id's of each message given as state)
    def _create_state(self) -> str:
        """generate code of state class

        Returns:
            str: generated class for states
        """
        return create_state(self._states)
