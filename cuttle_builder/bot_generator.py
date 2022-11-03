from builder import state_generator, create_reply_keyboard, create_state_handler, create_keyboard_array, find_previous_messages, create_file, FileManager
from distutils.dir_util import copy_tree
import shutil
import typing

messages = [
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

variants = [
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

class BotGenerator():
    def __init__(self, bot_id: int, messages: typing.List[str], variants: typing.List[str], start_message_id: int):
        self.bot_id = bot_id
        self.messages = messages
        self.variants = variants
        self.start_message_id = start_message_id
        self.states = []
        self.fileManager = FileManager()

    def create_bot(self) -> None:
        bot_name = self.fileManager.get_template(self.bot_id)
        print(bot_name)

        for message in self.messages:
            message_id = message['id']
            self.states.append(message_id)
            buttons = self.create_keyboard_array(message_id, variants)
            keyboard_code = self.create_reply_keyboard(message_id, buttons) if buttons else ''
            keyboard_name = f'{message_id}_kb' if keyboard_code else ''
            imp = 'from keyboards import {0}'.format(keyboard_name) if keyboard_name else ''

            if message_id == start_message_id:
                if keyboard_name:
                    self.create_file_keyboard(bot_name, keyboard_name, keyboard_code)
                code = self.create_state_handler(imp, previous['current_id'], previous['text'], message_id, 'photo', message['text'], keyboard_name)

            previouses = self.find_previous_messages(message_id, variants)            
            for previous in previouses:
                if keyboard_name:
                    self.create_file_keyboard(bot_name, keyboard_name, keyboard_code)
                code = self.create_state_handler(imp, previous['current_id'], previous['text'], message_id, 'photo', message['text'], keyboard_name)
                self.create_file_handler(bot_name, message_id, code)

            if not previouses:
                if keyboard_name:
                    self.create_file_keyboard(bot_name, keyboard_name, keyboard_code)
                code = self.create_state_handler(imp, '','', message_id, 'photo', message['text'], keyboard_name)
                self.create_file_handler(bot_name, message_id, code)
        
        self.create_file_state(bot_name, self.states)
        
    
    def create_keyboard_array(self, message_id: int, variants: typing.List[dict]) -> typing.List[str]:
        '''
        get keyboard buttons related to concrete message from list of all keyboard buttons
        :param message_id - id of message
        :param variants - list of all varinats (contain text of button, previous and current states)
        :return list of keyboard buttons related to concrete message
        '''
        return create_keyboard_array(message_id, variants)
    
    # generate code of reply keyboard, take text from file and add keyboard with keyboard name
    def create_reply_keyboard(self, kb_name: str, buttons: typing.List[str]) -> str:
        '''
        generate code of reply keyboard
        :param kb_name - name of keyboard
        :param buttons - buttons, related to this keyboard
        :return generated code for concrete keyboard
        '''
        return create_reply_keyboard(kb_name, buttons)
    
    # find previous message id's from variants list
    def find_previous_messages(self, message_id: int, variants: typing.List[dict]) -> typing.List[dict]:
        '''
        get previous message id's related to concrete message from list of all variants
        :param message_id - id of current message
        :param variants - list of all variants
        :return list of all previous message id's for concrete message
        '''
        return find_previous_messages(message_id, variants)

    # generate code of state handler, get imports (keyboard if in use), states (previous and next), text with keyboard and send method (send file, photo, video, text or group message)
    def create_state_handler(self, imports: str, prev_state: str, prev_state_text: str, curr_state: str, send_method: str, text: str, kb: str) -> str:
        '''
        generate code of state handler
        :param imports - imports used in this handler (keyboard and etc.)
        :param prev_state - id of previous state
        :param prev_state_text - text of previous state that connect to current state
        :param curr_state - id of current state
        :param send_method - type of sending method (text, photo, video, file, group)
        :param text - text of answer
        :param kb - keyboard of answer
        :return(void) generated code for handler with state and handled text
        '''
        return create_state_handler(imports, prev_state, prev_state_text, curr_state, send_method, text, kb = '')

    # create keyboard file in directory
    def create_file_keyboard(self, bot_name: str, keyboard_name: str, keyboard_code: str):
        '''
        create file of keyboard in specific file
        :param bot_name - name of bot
        :param keyboard_name - name of keyboard (message_id + _kb)
        :param keyboard_code - generated code of keyboard
        :return(void) create file in specific directory, contains keyboard and register this keyboard in the package 
        '''
        create_file(f'{bot_name}/keyboards/{keyboard_name}.py', keyboard_code, f'{bot_name}/keyboards/__init__.py', f'\nfrom .{keyboard_name} import {keyboard_name}')
    
    # create handler file in directory
    def create_file_handler(self, bot_name: str, name: str, code: str):
        '''
        create file of handler in specific file
        :param bot_name - name of bot
        :param name - name of handler (message_id)
        :param code - generated code of handler
        :return(void) create file in specific directory, contains handler and register this handler in the package 
        '''
        create_file(f'{bot_name}/handlers/get_{name}.py', code, f'{bot_name}/handlers/__init__.py', f'from .get_{name} import dp\n')
    
    # create state file in directory
    def create_file_state(self, bot_name: str, states: str) -> None:
        '''
        create file of states in specific file
        :param bot_name - name of bot
        :param states - generated code of states
        :return(void) create file in specific directory, contains states class and register this class in the package 
        '''
        create_file(f'{bot_name}/state/states.py', self.state_generator(states), f'{bot_name}/state/__init__.py', 'from .states import States')

    # generate code of state, based on states, that given from bot (id's of each message given as state)
    def state_generator(self, states: list) -> str:
        '''
        generate code of state class
        :param states - list of states (str)
        :return(void) generated class for states
        '''
        return state_generator(states)


start_message_id = 'asdf345'
botGenerator = BotGenerator('12354', messages, variants, start_message_id)
botGenerator.create_bot()