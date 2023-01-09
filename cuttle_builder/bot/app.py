from loader import dp
from aiogram import executor
from handlers import dp
from on_startup_commands import set_default_commands

if __name__ == '__main__':
    print('Bot started')
    print('Bot process messages')
    executor.start_polling(dp,
                           skip_updates=True,
                           on_startup=set_default_commands)
