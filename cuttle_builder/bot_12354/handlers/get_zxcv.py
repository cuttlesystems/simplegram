from aiogram import types
from aiogram.dispatcher.filters import Command
from loader import dp
from state import States


@dp.message_handler()
async def get_zxcv(message: types.Message):
    await States.zxcv.set() # add commands 
    photo # send message