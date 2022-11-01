from aiogram import types
from aiogram.dispatcher.filters import Command
from loader import dp
from state import States
from keyboards import asdf_kb

@dp.message_handler()
async def get_asdf(message: types.Message):
    await States.asdf.set() # add commands 
    await message.answer(text='asdftext', reply_markup=asdf_kb) # send message