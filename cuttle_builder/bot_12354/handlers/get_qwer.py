from aiogram import types
from aiogram.dispatcher.filters import Command
from loader import dp
from state import States


@dp.message_handler()
async def get_qwer(message: types.Message):
    await States.qwer.set() # add commands 
    photo # send message