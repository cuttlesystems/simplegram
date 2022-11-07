from loader import dp
from utils.notify_admins import on_startup_notify


async def on_startup(_unused_variable):
    await on_startup_notify(dp)

    print('Bot work')


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp
    
    executor.start_polling(dp, on_startup=on_startup)
