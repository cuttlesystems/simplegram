from b_logic.data_objects import BotVariant
from cuttle_builder.bot_generator_params import CUTTLE_BUILDER_PATH
from cuttle_builder.builder.additional.file_read_write.read_file import read_file
import typing


def generate_reply_keyboard_code(buttons: typing.List[BotVariant], buttons_in_row: int) -> str:
    """
    Генерирует код для клавиатуры вида REPLY, с указание количества кнопок на один ряд.

    Args:
        buttons (typing.List[BotVariant]): Список кнопок (объектов BotVariant)
        buttons_in_row (int): Количесто кнопок на один ряд

    Returns:
        str: Сгенерированный код клавиатуры
    """
    assert all(isinstance(button, BotVariant) for button in buttons)
    assert isinstance(buttons_in_row, int)
    button_counter = 0
    all_buttons_content = ''
    row = []
    for button in buttons:
        if button_counter < buttons_in_row:
            row.append(f'KeyboardButton(text="{button.text}")')
            button_counter += 1
        else:
            all_buttons_content += ('.add(\n\t' + ', '.join(row) + '\n)')
            button_counter = 0
            row = []
            row.append(f'KeyboardButton(text="{button.text}")')
    all_buttons_content += ('.add(\n\t' + ', '.join(row) + '\n)')
    return all_buttons_content


def create_reply_keyboard(keyboard_variable_name_without_suffix: str, buttons: typing.List[BotVariant], extended_imports: str) -> str:
    reply_keyboard_sample = (
        CUTTLE_BUILDER_PATH / 'builder' / 'additional' / 'samples' / 'reply_keyboard_sample.txt')
    code = read_file(reply_keyboard_sample)
    code = code.format(
        imports=extended_imports,
        keyboard_name=keyboard_variable_name_without_suffix,
        # all_buttons=',\n\t\t'.join([f'KeyboardButton(text="{button.text}")'for button in buttons])
        all_buttons=generate_reply_keyboard_code(buttons=buttons, buttons_in_row=3)
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
