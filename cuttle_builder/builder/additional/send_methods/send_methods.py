from aiogram import types, filters
import asyncio

def send_method(type_, text, kb):
    if type_ == 'text':
        return f'await message.answer(text=\'{text}\', {"reply_markup="+kb if kb else ""})'
    if type_ == 'photo':
        return 'await bot.send_photo(message.from_user.id, photo)'
    if type_ == 'video':
        return 'await bot.send_video(message.chat.id, video = video)'
    
def additional_functions(type_, addinional_function, id):
    if type_ == 'photo':
        return 'photo = '

def body_method(type_, body, data):
    if type_ == 'photo':
        body += 'photo = {0}'.format(data['file_id'])
    if type_ == 'video':
        body += 'video = open(\'{0}\', \'rb\')'.format(data['file_id'])
    if type_ == 'group':
        body += \
'''
    media = types.MediaGroup()
    media.attach_photo(types.InputFile({}))
'''

@dp.message_handler(commands = ["video"])
async def send_video(message: types.Message):
    video = open("name", "rb")
    await bot.send_video(message.chat.id, video = video)


@dp.message_handler(filters.CommandStart())
async def send_welcome(message: types.Message):
    # So... At first I want to send something like this:
    await message.reply("Do you want to see many pussies? Are you ready?")

    # And wait few seconds...
    await asyncio.sleep(1)

    # Good bots should send chat actions. Or not.
    await types.ChatActions.upload_photo()

    # Create media group
    media = types.MediaGroup()

    # Attach local file
    media.attach_photo(types.InputFile('data/cat.jpg'), 'Cat!')
    # More local files and more cats!
    media.attach_photo(types.InputFile('data/cats.jpg'), 'More cats!')

    # You can also use URL's
    # For example: get random puss:
    media.attach_photo('http://lorempixel.com/400/200/cats/', 'Random cat.')

    # And you can also use file ID:
    # media.attach_photo('<file_id>', 'cat-cat-cat.')

    # Done! Send media group
    await message.reply_media_group(media=media)