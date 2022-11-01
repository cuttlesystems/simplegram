from aiogram import types
from aiogram.dispatcher.filters import Command
from loader import dp
from state import States
from keyboards import qwer_kb

@dp.message_handler(lambda message: message.text == 'asdf_to_qwer', state=States.asdf)
async def get_qwer(message: types.Message):
    await States.qwer.set() # add commands 
    await message.answer(text='qwertext', reply_markup=qwer_kb) # send message