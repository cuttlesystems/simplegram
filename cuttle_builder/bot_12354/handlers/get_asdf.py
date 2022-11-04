from aiogram import types
from aiogram.dispatcher.filters import Command
from loader import dp
from state import States


@dp.message_handler()
async def get_asdf(message: types.Message):
    await States.asdf.set() # add commands 
    photo # send message