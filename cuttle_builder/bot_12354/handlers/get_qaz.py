from aiogram import types
from aiogram.dispatcher.filters import Command
from loader import dp
from state import States


@dp.message_handler()
async def get_qaz(message: types.Message):
    await States.qaz.set() # add commands 
    photo # send message