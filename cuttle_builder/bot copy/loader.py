from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# from utils.dp_api import DataBase
from data import config

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)

storage = MemoryStorage()

# db = DataBase()
dp = Dispatcher(bot=bot, storage=storage)


__all__ = ['dp', 'db', 'bot', 'storage']