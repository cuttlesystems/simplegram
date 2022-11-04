from builder import create_state, create_reply_keyboard, create_state_handler, create_keyboard_array, find_previous_messages, create_file, FileManager, BotDescription, BotMessage, MessageVariant
import typing

messages_json = [
        {
            'id': 'asdf',
            'text': 'asdftext',
            'photo': None,
            'video': None,
            'file': None
        },
        {
            'id': 'qwer',
            'text': 'qwertext',
            'photo': None,
            'video': None,
            'file': None
        },
        {
            'id': 'zxcv',
            'text': 'zxcvtext',
            'photo': None,
            'video': None,
            'file': None
        },
        {
            'id': 'qaz',
            'text': 'qaztext',
            'photo': None,
            'video': None,
            'file': None
        },
        {
            'id': 'wsx',
            'text': 'wsxtext',
            'photo': None,
            'video': None,
            'file': None
        },
    ]

variants_json = [
        {
            'text': 'asdf_to_zxcv',
            'current_id': 'asdf',
            'next_id': 'zxcv'
        },
        {
            'text': 'asdf_to_qwer',
            'current_id': 'asdf',
            'next_id': 'qwer'
        },
        {
            'text': 'asdf_to_qaz',
            'current_id': 'asdf',
            'next_id': 'qaz'
        },
        {
            'text': 'zxcv_wsx',
            'current_id': 'zxcv',
            'next_id': 'wsx'
        },
        {
            'text': 'qwer_to_wsx',
            'current_id': 'qwer',
            'next_id': 'wsx'
        }
    ]

messages = messages_json
variants = variants_json


class BotGenerator():
    def __init__(self, bot_id: int, messages: typing.List[str], variants: typing.List[str], start_message_id: int):
        self._bot_id = bot_id
        self._messages = messages
        self._variants = variants
        self._start_message_id = start_message_id
        self._states = []
        self._file_manager = FileManager()

    def create_bot(self) -> None:
        bot_directory = self._file_manager.create_bot_directory(self._bot_id)
        print(bot_directory)

        for message in self._messages:
            message_id = message['id']
            self._states.append(message_id)
            buttons = self.create_keyboard_array(message_id, variants)
            keyboard_code = self.create_reply_keyboard(message_id, buttons) if buttons else ''
            keyboard_name = f'{message_id}_kb' if keyboard_code else ''
            import_keyboard = 'from keyboards import {0}'.format(keyboard_name) if keyboard_name else ''

            if message_id == start_message_id:
                if keyboard_name:
                    self.create_file_keyboard(bot_directory, keyboard_name, keyboard_code)
                code = self.create_state_handler(import_keyboard, previous['current_id'], previous['text'], message_id, 'photo', message['text'], keyboard_name)

            previouses = self.find_previous_messages(message_id, variants)            
            for previous in previouses:
                if keyboard_name:
                    self.create_file_keyboard(bot_directory, keyboard_name, keyboard_code)
                code = self.create_state_handler(import_keyboard, previous['current_id'], previous['text'], message_id, 'photo', message['text'], keyboard_name)
                self.create_file_handler(bot_directory, message_id, code)

            if not previouses:
                if keyboard_name:
                    self.create_file_keyboard(bot_directory, keyboard_name, keyboard_code)
                code = self.create_state_handler(import_keyboard, '','', message_id, 'photo', message['text'], keyboard_name)
                self.create_file_handler(bot_directory, message_id, code)
        
        self.create_file_state(bot_directory,  self._states)
        
    
    def create_keyboard_array(self, message_id: int, variants: typing.List[dict]) -> typing.List[str]:
        """_summary_

        Args:
            message_id (int): id of message
            variants (typing.List[dict]): list of all varinats (contain text of button, previous and current states)

        Returns:
            typing.List[str]: list of keyboard buttons related to concrete message
        """
        return create_keyboard_array(message_id, variants)
    
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
    def find_previous_messages(self, message_id: int, variants: typing.List[dict]) -> typing.List[dict]:
        """get previous message id's related to concrete message from list of all variants

        Args:
            message_id (int): id of current message
            variants (typing.List[dict]): list of all variants

        Returns:
            typing.List[dict]: _descrilist of all previous message id's for concrete messageption_
        """
        return find_previous_messages(message_id, variants)

    # generate code of state handler, get imports (keyboard if in use), states (previous and next), text with keyboard and send method (send file, photo, video, text or group message)
    def create_state_handler(self, imports: str, prev_state: str, prev_state_text: str, curr_state: str, send_method: str, text: str, kb: str) -> str:
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
        return create_state_handler(imports, prev_state, prev_state_text, curr_state, send_method, text, kb)

    # create keyboard file in directory
    def create_file_keyboard(self, bot_name: str, keyboard_name: str, keyboard_code: str):
        """create file in specific directory, contains keyboard and register this keyboard in the package 

        Args:
            bot_name (str): name of bot
            keyboard_name (str): name of keyboard (message_id + _kb)
            keyboard_code (str): generated code of keyboard
        """
        create_file(f'{bot_name}/keyboards/{keyboard_name}.py', keyboard_code, f'{bot_name}/keyboards/__init__.py', f'\nfrom .{keyboard_name} import {keyboard_name}')
    
    # create handler file in directory
    def create_file_handler(self, bot_name: str, name: str, code: str):
        """create file in specific directory, contains handler and register this handler in the package 

        Args:
            bot_name (str): name of bot
            name (str): name of handler (message_id)
            code (str): generated code of handler
        """
        create_file(f'{bot_name}/handlers/get_{name}.py', code, f'{bot_name}/handlers/__init__.py', f'from .get_{name} import dp\n')
    
    # create state file in directory
    def create_file_state(self, bot_name: str, states: str) -> None:
        """create file in specific directory, contains states class and register this class in the package 

        Args:
            bot_name (str): name of bot
            states (str): generated code of states
        """
        create_file(f'{bot_name}/state/states.py', self.create_state(states), f'{bot_name}/state/__init__.py', 'from .states import States')

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