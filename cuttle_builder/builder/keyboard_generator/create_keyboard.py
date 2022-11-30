from b_logic.data_objects import BotVariant
from cuttle_builder.bot_generator_params import CUTTLE_BUILDER_PATH
from cuttle_builder.builder.additional.file_read_write.read_file import read_file
import typing


def create_reply_keyboard(keyboard_variable_name_without_suffix: str, buttons: typing.List[BotVariant], extended_imports: str) -> str:
    reply_keyboard_sample = (
        CUTTLE_BUILDER_PATH / 'builder' / 'additional' / 'samples' / 'reply_keyboard_sample.txt')
    code = read_file(reply_keyboard_sample)
    code = code.format(
        imports=extended_imports,
        keyboard_name=keyboard_variable_name_without_suffix,
        all_buttons=',\n\t\t'.join([
            f'KeyboardButton(text="{button.text}")'
            for button in buttons
        ])
    )
    return code


def create_inline_keyboard(keyboard_variable_name_without_suffix: str, buttons: typing.List[BotVariant], extended_imports: str) -> str:
    reply_keyboard_sample = (
        CUTTLE_BUILDER_PATH / 'builder' / 'additional' / 'samples' / 'inline_keyboard_sample.txt')
    code = read_file(reply_keyboard_sample)
    code = code.format(
        imports=extended_imports,
        keyboard_name=keyboard_variable_name_without_suffix,
        all_buttons=',\n\t'.join([
            f'InlineKeyboardButton(text="{button.text}", callback_data="{button.text}")'
            for button in buttons
        ])
    )
    return code
