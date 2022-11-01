from aiogram import types
from aiogram.dispatcher.filters import Command
from loader import dp
from state import States
from keyboards import zxcv_kb

@dp.message_handler(lambda message: message.text == 'asdf_to_zxcv', state=States.asdf)
async def get_zxcv(message: types.Message):
    await States.zxcv.set() # add commands 
    await message.answer(text='zxcvtext', reply_markup=zxcv_kb) # send message