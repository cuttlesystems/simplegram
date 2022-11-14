from aiogram import types, Dispatcher
from create_bot import bot
from aiogram.types import ReplyKeyboardRemove

from keyboards.client_kb import (kb_client_model, kb_client_color,
                                 kb_client_memory)


# @dp.message_handler(commands=['start', 'help'])
async def chose_model(message: types.Message):
    """Отлавливает сообщения start и help"""
    try:
        await bot.send_message(
            chat_id=message.from_user.id,
            text='Пакупай айфон, какой нада?',
            reply_markup=kb_client_model  # добавляет клаву
        )
    except Exception:
        await message.reply('Bot cant write first. Sand smth to him.')


async def chose_color(message: types.Message):
    await bot.send_message(
        chat_id=message.from_user.id,
        text='Супер! Выбирай цвет',
        reply_markup=kb_client_color
    )


async def chose_memory(message: types.Message):
    await bot.send_message(
        chat_id=message.from_user.id,
        text='Супер! Выбирай объем памяти',
        reply_markup=kb_client_memory
    )


async def what_i_sent(message: types.Message):
    await bot.send_message(
        chat_id=message.from_user.id,
        text=(f'You sent: {message.text}, but nothing happened.\n'
              'Try a different command.')
    )


def register_handlers_client(dp: Dispatcher):
    """Функция для регистрации хендлеров"""
    dp.register_message_handler(chose_model, commands=['start'])
    dp.register_message_handler(
        chose_color,
        commands=['11-ый', '12-ый', '13-ый', '228-ой']
    )
    dp.register_message_handler(
        chose_memory,
        commands=['красный', 'белый', 'черный', 'зеленый']
    )
    dp.register_message_handler(what_i_sent)
