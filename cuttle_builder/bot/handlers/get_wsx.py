from aiogram import types
from aiogram.dispatcher.filters import Command
from loader import dp
from state import States


@dp.message_handler(lambda message: message.text == 'zxcv_wsx', state=States.zxcv)
async def get_wsx(message: types.Message):
    await States.wsx.set() # add commands 
    await message.answer(text='wsxtext', ) # send messagefrom aiogram import types
from aiogram.dispatcher.filters import Command
from loader import dp
from state import States


@dp.message_handler(lambda message: message.text == 'qwer_to_wsx', state=States.qwer)
async def get_wsx(message: types.Message):
    await States.wsx.set() # add commands 
    await message.answer(text='wsxtext', ) # send message