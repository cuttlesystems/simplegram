from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

start = KeyboardButton('/start')  # Кнопка просто отправляет сообщение start
model11 = KeyboardButton('/11-ый')
model12 = KeyboardButton('/12-ый')
model13 = KeyboardButton('/13-ый')
model228 = KeyboardButton('/228-ой')

kb_client_model = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client_model.add(start).row(model11, model12).row(model13, model228)

red = KeyboardButton('/красный')
white = KeyboardButton('/белый')
black = KeyboardButton('/черный')
green = KeyboardButton('/зеленый')

kb_client_color = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client_color.add(start).row(red, white).row(black, green)

gb32 = KeyboardButton('/32')
gb64 = KeyboardButton('/64')
gb128 = KeyboardButton('/128')
gb256 = KeyboardButton('/256')

kb_client_memory = ReplyKeyboardMarkup(resize_keyboard=True)
kb_client_memory.add(start).row(gb32, gb64).row(gb128, gb256)
