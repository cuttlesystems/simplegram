
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
    def __init__(self, bot_id, messages, variants, start_message_id):
        self.bot_id = bot_id
        self.messages = messages
        self.variants = variants
        self.start_message_id = start_message_id
        self.states = []
    def create_bot(self):
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
        

    def create_keyboard_array(self, message_id: int, variants: typing.List[dict]):
        return create_keyboard_array(message_id, variants)
    
    def create_reply_keyboard(self, message_id: int, buttons: typing.List[dict]):
        return create_reply_keyboard(message_id, buttons)
    

    def find_previous_messages(self, message_id: int, variants: typing.List[dict]):
        return find_previous_messages(message_id, variants)

    def create_file_keyboard(self, bot_name: str, keyboard_name: str, keyboard_code: str):
        create_file_keyboard(bot_name, keyboard_name, keyboard_code)
    
    def create_state_handler(self, imports: str, curr_state: str, curr_state_text: str, next_state: str, send_method: str, text: str, kb: str):
        return create_state_handler(imports, curr_state, curr_state_text, next_state, send_method, text, kb = '')
    
    def create_file_handler(self, bot_name: str, message_id: str, code: str):
        create_file_handler(bot_name, message_id, code)
    
    def create_file_state(self, bot_name: str, states: str):
        create_file_state(bot_name, self.state_generator(states))

    def state_generator(self, states: list):
        return state_generator(states)
    
    def get_dir_name(self, bot_id):
        return '../bot_{0}'.format(bot_id)
    
    def delete_dir(self, dir_name):
        try:
            shutil.rmtree(dir_name)
        except FileNotFoundError:
            pass
        except Exception as e:
            print(e)
    
    def get_template(self, bot_id):
        dir_name = self.get_dir_name(bot_id)
        self.delete_dir(dir_name)
        copy_tree('bot', dir_name)
        return dir_name

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


def create_bot(bot_id, messages, variants, start_message_id):
    bot_name = get_template(bot_id)
    
    states = []
    # create_state_handler take 1 more positional argument send_method, it needs to generate method to send message
    for message in messages:
        message_id = message['id']
        states.append(message_id)
        buttons = create_keyboard_array(message_id, variants)
        keyboard_code = create_reply_keyboard(message_id, buttons) if buttons else ''
        keyboard_name = message_id + '_kb' if keyboard_code else ''
        imp = 'from keyboards import {0}'.format(keyboard_name) if keyboard_name else ''
        if message['id'] == start_message_id:
            # create start message
            continue

        previouses = find_previous_messages(message_id, variants)

        for previous in previouses:
            if keyboard_name:
                create_file_keyboard(bot_name, keyboard_name, keyboard_code)
            code = create_state_handler(imp, previous['current_id'], previous['text'], message_id, 'photo', message['text'], keyboard_name)
            create_file_handler(bot_name, message_id, code)

        if not previouses:
            if keyboard_name:
                create_file_keyboard(bot_name, keyboard_name, keyboard_code)
            code = create_state_handler(imp, '', '', message_id, 'photo', message['text'], keyboard_name)
            create_file_handler(bot_name, message_id, code)
    
    create_file_state(bot_name, state_generator(states))

start_message_id = 'asdf345'
botGenerator = BotGenerator('1235', messages, variants, start_message_id)
botGenerator.create_bot()