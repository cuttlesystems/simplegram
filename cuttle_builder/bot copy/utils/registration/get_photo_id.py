from aiogram.types import Message

def get_photo_id(message: Message):
    try:
        photo = message.photo[-1].file_id
        return photo
    except Exception as e:
        print(e)
        return ''