from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

asdf_kb = ReplyKeyboardMarkup(
    keyboard=[
        [
        KeyboardButton(text="asdf_to_zxcv")
,KeyboardButton(text="asdf_to_qwer")
,KeyboardButton(text="asdf_to_qaz")

        ]
    ], resize_keyboard=True, one_time_keyboard=True
)