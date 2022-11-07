from cuttle_builder.builder.additional.file_read_write.read_file import read_file
import typing
from pathlib import Path

def create_reply_keyboard(kb_name: str, buttons: typing.List[str]) -> str:
    reply_keyboard_sample = Path(__file__).parent.parent / 'additional/samples/reply_keyboard_sample.txt'
    print(reply_keyboard_sample)
    code = read_file(reply_keyboard_sample)
    new_line = '\n'
    code = code.format(kb_name,','.join([
                f'KeyboardButton(text="{button}"){new_line}' 
                for button in buttons
            ]) )
    return code