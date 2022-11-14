from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage  # Хранилеще данных в оперативке

TG_TOKEN = '5498777595:AAEC146VKvAVgfE69mqsrnc3zdMkJIzOaAw'  # Найти бота в телеге: @Shamil256Bot

storage = MemoryStorage()

bot = Bot(token=TG_TOKEN)
dp = Dispatcher(bot, storage=storage)
