from aiogram import types
from aiogram.dispatcher.filters import Command
from loader import dp
from state import States


@dp.message_handler(lambda message: message.text == 'asdf_to_qaz', state=States.asdf)
async def get_qaz(message: types.Message):
    await States.qaz.set() # add commands 
    await message.answer(text='qaztext', ) # send message