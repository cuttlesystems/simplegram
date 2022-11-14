from aiogram import types, Dispatcher


async def set_default_commands(dp: Dispatcher):
    await dp.bot.set_my_commands([
        types.BotCommand('start', 'Start bot'),
        types.BotCommand('update', 'Update profile'),
        types.BotCommand('choose', 'Find pair')
        # types.BotCommand('menu', 'Переход в главное меню'),
        # types.BotCommand('registration', 'Начать регистрацию'),
        # types.BotCommand('update', 'Обновить профиль'),
        # types.BotCommand('match', 'Найти человека'),
        # types.BotCommand('profile', 'Показать мой профиль')
    ])