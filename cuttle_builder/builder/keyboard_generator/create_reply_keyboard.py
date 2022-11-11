from b_logic.data_objects import MessageVariant
from cuttle_builder.bot_generator_params import CUTTLE_BUILDER_PATH
from cuttle_builder.builder.additional.file_read_write.read_file import read_file
import typing
from pathlib import Path


def create_reply_keyboard(kb_name: str, buttons: typing.List[MessageVariant]) -> str:
    reply_keyboard_sample = (
            CUTTLE_BUILDER_PATH / 'builder' / 'additional' /
            'samples' / 'reply_keyboard_sample.txt')
    code = read_file(reply_keyboard_sample)
    code = code.format(
            kb_name,
            ','.join([
                f'KeyboardButton(text="{button.text}")\n'
                for button in buttons
            ])
    )
    return code
