
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.dispatcher import FSMContext

async def cancel_registration(state: FSMContext, message: Message):
    await state.finish()
    await message.answer('Вы прервали регистрацию', reply_markup=ReplyKeyboardRemove(selective=False))
    return