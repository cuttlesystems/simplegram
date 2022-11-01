from aiogram import types
from aiogram.dispatcher.filters import Command
from loader import dp
from state import States

@dp.message_handler(Command('start'))
async def command_start(message: types.Message):
    await message.answer('Hi it is my bot' , reply_markup='')
    await States.asdf.set()