
from builder import state_generator, create_reply_keyboard, create_state_handler, create_keyboard_array, find_previous_messages, create_file_handler, create_file_keyboard, create_file_state
from distutils.dir_util import copy_tree
import shutil
import typing


def get_dir_name(bot_id):
    return '../bot_{0}'.format(bot_id)

def delete_dir(dir_name):
    try:
        shutil.rmtree(dir_name)
    except FileNotFoundError as e:
        pass 
    except Exception as e:
        print(e)
    
def get_template(bot_id):
    dir_name = get_dir_name(bot_id)
    delete_dir(dir_name)
    copy_tree('bot', dir_name)
    return dir_name

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

    def create_bot(self) -> None:
        bot_name = self.get_template(self.bot_id)

        for message in self.messages:
            message_id = message['id']
            self.states.append(message_id)
            buttons = self.create_keyboard_array(message_id, variants)
            keyboard_code = self.create_reply_keyboard(message_id, buttons) if buttons else ''
            keyboard_name = f'{message_id}_kb' if keyboard_code else ''
            imp = 'from keyboards import {0}'.format(keyboard_name) if keyboard_name else ''

            if message_id == start_message_id:
                continue

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
        
    # create a list of strings, that contains names of buttons
    def create_keyboard_array(self, message_id: int, variants: typing.List[dict]) -> typing.List[str]:
        return create_keyboard_array(message_id, variants)
    
    # generate code of reply keyboard, take text from file and add keyboard with keyboard name
    def create_reply_keyboard(self, kb_name: str, buttons: typing.List[str]) -> str:
        return create_reply_keyboard(kb_name, buttons)
    
    # find previous message id's from variants list
    def find_previous_messages(self, message_id: int, variants: typing.List[dict]) -> typing.List[dict]:
        return find_previous_messages(message_id, variants)

    # create keyboard file in directory
    def create_file_keyboard(self, bot_name: str, keyboard_name: str, keyboard_code: str):
        create_file_keyboard(bot_name, keyboard_name, keyboard_code)
    
    # generate code of state handler, get imports (keyboard if in use), states (previous and next), text with keyboard and send method (send file, photo, video, text or group message)
    def create_state_handler(self, imports: str, curr_state: str, curr_state_text: str, next_state: str, send_method: str, text: str, kb: str) -> str:
        return create_state_handler(imports, curr_state, curr_state_text, next_state, send_method, text, kb = '')

    # create handler file in directory
    def create_file_handler(self, bot_name: str, message_id: str, code: str) -> None:
        create_file_handler(bot_name, message_id, code)
    
    # create state file in directory
    def create_file_state(self, bot_name: str, states: str) -> None:
        create_file_state(bot_name, self.state_generator(states))

    # generate code of state, based on states, that given from bot (id's of each message given as state)
    def state_generator(self, states: list) -> str:
        return state_generator(states)
    
    # place, where we store the bot (doesn't work if call outside of this file)
    def get_dir_name(self, bot_id: int) -> str:
        return '../bot_{0}'.format(bot_id)
    
    # delete directory, to prevent writing file over exist file
    def delete_dir(self, dir_name: str) -> None:
        try:
            shutil.rmtree(dir_name)
        except FileNotFoundError:
            pass 
        except Exception as e:
            print(e)
    
    # get template of bot and copy in upper directory with id of bot
    def get_template(self, bot_id: int) -> str:
        dir_name = self.get_dir_name(bot_id)
        self.delete_dir(dir_name)
        copy_tree('bot', dir_name)
        return dir_name


start_message_id = 'asdf345'
botGenerator = BotGenerator('12359', messages, variants, start_message_id)
botGenerator.create_bot()