import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = '5643702459:AAH8bWcmY9gTlM4nPXHMGMiax5RqvOdI08o'

admins = [
    332783067
]

USER = str(os.getenv('MONGO_USER'))
PASSWORD = str(os.getenv('MONGO_PASSWORD'))
IP = str(os.getenv('MONGO_IP'))

MONGO_CONNECTION_KEY = f'mongodb+srv://{USER}:{PASSWORD}@{IP}/?retryWrites=true&w=majority'