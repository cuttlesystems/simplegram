

def send_method(type_, text, kb):
    if type_ == 'text':
        return f'await message.answer(text=\'{text}\', {"reply_markup="+kb if kb else ""})'
    if type_ == 'photo':
        return 'await bot.send_photo(message.from_user.id, photo)'
    if type_ == 'video':
        return 'await bot.send_video(message.from_user.id, photo)'