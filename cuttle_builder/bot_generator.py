from b_logic.bot_api import BotApi
from b_logic.data_objects import BotDescription, BotMessage, MessageVariant
from cuttle_builder.builder.additional.file_read_write.file_manager import FileManager
from cuttle_builder.builder.keyboard_generator.create_reply_keyboard import create_reply_keyboard
from cuttle_builder.builder.handler_generator.create_state_handler import create_state_handler
from cuttle_builder.builder.state_generator.create_state import create_state
import typing

messages_json = [
        {
            'id': 'message_10',
            'text': 'Message 10 text',
            'photo': None,
            'video': None,
            'file': None
        },
        {
            'id': 'message_20',
            'text': 'Message 20 text',
            'photo': None,
            'video': None,
            'file': None
        },
        {
            'id': 'message_30',
            'text': 'Message 30 text',
            'photo': None,
            'video': None,
            'file': None
        },
        {
            'id': 'message_40',
            'text': 'Message 40 text',
            'photo': None,
            'video': None,
            'file': None
        },
        {
            'id': 'message_50',
            'text': 'Message 50 text',
            'photo': None,
            'video': None,
            'file': None
        },
    ]

variants_json = [
        {
            'text': 'from 10 to 30',
            'current_id': 'message_10',
            'next_id': 'message_30'
        },
        {
            'text': 'From 10 to 20',
            'current_id': 'message_10',
            'next_id': 'message_20'
        },
        {
            'text': 'From 10 to 40',
            'current_id': 'message_10',
            'next_id': 'message_40'
        },
        {
            'text': 'From 30 to 50',
            'current_id': 'message_30',
            'next_id': 'message_50'
        },
        {
            'text': 'From 20 to 50',
            'current_id': 'message_20',
            'next_id': 'message_50'
        },
        # {
        #     'text': 'From 50 to 10',
        #     'current_id': 'message_50',
        #     'next_id': 'message_10'
        # }
    ]

messages = messages_json
variants = variants_json


class BotGenerator():
    def __init__(self, bot_api: BotApi, bot: BotDescription):
        messages = bot_api.get_messages(bot)
        all_vars = []
        for mes in messages:
            variants = bot_api.get_variants(mes)
            all_vars.extend(variants)

        self._bot_id = bot.id
        self._messages = messages
        self._variants = all_vars
        self._start_message_id = bot.start_message_id
        self._states = []
        self._file_manager = FileManager()

    def generate_keyboard(self, message_id: int, bot_directory: str) -> str:
        buttons = self.create_keyboard_array(message_id, self._variants)
        keyboard_code = self.create_reply_keyboard(f'a{message_id}', buttons) if buttons else ''
        keyboard_name = f'a{message_id}_kb' if keyboard_code else ''
        if keyboard_name:
            self.create_file_keyboard(bot_directory, keyboard_name, keyboard_code)
        return keyboard_name

    def create_bot(self) -> None:
        bot_directory = self._file_manager.create_bot_directory(self._bot_id)

        for message in self._messages:
            message_id = f'a{message.id}'

            if message_id == self._start_message_id:
                keyboard_name = self.generate_keyboard(message.id, bot_directory)
                import_keyboard = 'from keyboards import {0}'.format(keyboard_name) if keyboard_name else ''
                handler_code = self.create_state_handler(
                    import_keyboard,
                    'Command(\'start\')'
                    '',
                    '',
                    f'a{message.id}',
                    'text',
                    message.text,
                    keyboard_name
                )
            previous = self.find_previous_messages(message.id, self._variants)
            for prev in previous:
                keyboard_name = self.generate_keyboard(message.id, bot_directory)
                import_keyboard = 'from keyboards import {0}'.format(keyboard_name) if keyboard_name else ''
                handler_code = self.create_state_handler(
                    import_keyboard,
                    '',
                    f'a{prev.current_message_id}',
                    prev.text,
                    f'a{message.id}',
                    'text',
                    message.text,
                    keyboard_name
                )
                self.create_file_handler(bot_directory, message_id, handler_code)

            if not previous:
                keyboard_name = self.generate_keyboard(message.id, bot_directory)
                handler_code = self.create_state_handler(
                    import_keyboard,
                    '',
                    '',
                    message_id,
                    'photo',
                    message.text,
                    keyboard_name
                )
                self.create_file_handler(bot_directory, message_id, handler_code)
        self.generate_state(bot_directory)

    def generate_state(self, bot_directory):
        for message in self._messages:
            self._states.append(message.id)
        self.create_file_state(bot_directory, self._states)
    
    def create_keyboard_array(self, message_id: int, variants: typing.List[MessageVariant]) -> typing.List[MessageVariant]:
        """_summary_

        Args:
            message_id (int): id of message
            variants (typing.List[dict]): list of all varinats (contain text of button, previous and current states)

        Returns:
            typing.List[str]: list of keyboard buttons related to concrete message
        """
        return [item.text for item in variants if item.current_message_id==message_id]
    
    # generate code of reply keyboard, take text from file and add keyboard with keyboard name
    def create_reply_keyboard(self, kb_name: str, buttons: typing.List[str]) -> str:
        """generate code of reply keyboard

        Args:
            kb_name (str): name of keyboard
            buttons (typing.List[str]): buttons, related to this keyboard

        Returns:
            str: generated code for concrete keyboard
        """
        return create_reply_keyboard(kb_name, buttons)
    
    # find previous message id's from variants list
    def find_previous_messages(self,
                               message_id: int,
                               variants: typing.List[MessageVariant]
                               ) -> typing.List[MessageVariant]:
        """get previous message id's related to concrete message from list of all variants

        Args:
            message_id (int): id of current message
            variants (typing.List[dict]): list of all variants

        Returns:
            typing.List[dict]: _descrilist of all previous message id's for concrete messageption_
        """
        return [item for item in variants if item.next_message_id==message_id]

    # generate code of state handler, get imports (keyboard if in use), states (previous and next), text with keyboard and send method (send file, photo, video, text or group message)
    def create_state_handler(self, imports: str, type_, prev_state: str, prev_state_text: str, curr_state: str, send_method: str, text: str, kb: str) -> str:
        """generate code of state handler

        Args:
            imports (str): imports used in this handler (keyboard and etc.)
            prev_state (str): id of previous state
            prev_state_text (str): text of previous state that connect to current state
            curr_state (str): id of current state
            send_method (str): type of sending method (text, photo, video, file, group)
            text (str): text of answer
            kb (str): keyboard of answer

        Returns:
            str: generated code for handler with state and handled text
        """
        return create_state_handler(imports, type_, prev_state, prev_state_text, curr_state, send_method, text, kb)

    # create keyboard file in directory
    def create_file_keyboard(self, bot_name: str, keyboard_name: str, keyboard_code: str):
        """create file in specific directory, contains keyboard and register this keyboard in the package 

        Args:
            bot_name (str): name of bot
            keyboard_name (str): name of keyboard (message_id + _kb)
            keyboard_code (str): generated code of keyboard
        """
        self._file_manager.create_file(f'{bot_name}/keyboards/{keyboard_name}.py', keyboard_code, f'{bot_name}/keyboards/__init__.py', f'\nfrom .{keyboard_name} import {keyboard_name}')
    
    # create handler file in directory
    def create_file_handler(self, bot_name: str, name: str, code: str):
        """create file in specific directory, contains handler and register this handler in the package 

        Args:
            bot_name (str): name of bot
            name (str): name of handler (message_id)
            code (str): generated code of handler
        """
        self._file_manager.create_file(f'{bot_name}/handlers/get_{name}.py', code, f'{bot_name}/handlers/__init__.py', f'from .get_{name} import dp\n')
    
    # create state file in directory
    def create_file_state(self, bot_name: str, states: str) -> None:
        """create file in specific directory, contains states class and register this class in the package 

        Args:
            bot_name (str): name of bot
            states (str): generated code of states
        """
        self._file_manager.create_file(f'{bot_name}/state/states.py', self.create_state(states), f'{bot_name}/state/__init__.py', 'from .states import States')

    # generate code of state, based on states, that given from bot (id's of each message given as state)
    def create_state(self, states: list) -> str:
        """generate code of state class

        Args:
            states (list): list of states (str)

        Returns:
            str: generated class for states
        """
        return create_state(states)


if __name__ == '__main__':
    start_message_id = 'asdf345'
    botGenerator = BotGenerator('12354', messages, variants, start_message_id)
    botGenerator.create_bot()