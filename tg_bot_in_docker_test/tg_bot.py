from aiogram.utils import executor
from create_bot import dp

from handlers import admin, client


async def on_startup(__):  # Функция при старте бота
    print('Bot is online')


async def on_shutdown(__):  # Функция при завершение бота
    print('Bot is offline')


client.register_handlers_client(dp)  # Активация зарегистрированных хэндлеров


if __name__ == '__main__':  # Запуск бота тут
    executor.start_polling(
        dp,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown
    )
