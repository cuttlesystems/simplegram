from aiogram.types import InlineKeyboardButton

def generate_keyboard(statuses):
    return [[InlineKeyboardButton(text=status, callback_data=status)] for status in statuses]