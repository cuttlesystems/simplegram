# ----------------------------
from pymongo import MongoClient
from datetime import datetime
import certifi
from data.config import MONGO_CONNECTION_KEY

class DataBase():
    def __init__(self):
        print('conncetion to mongo')
        ca = certifi.where()
        self.client = MongoClient(MONGO_CONNECTION_KEY, tlsCAFile=ca)
        self.db = self.client.get_database('hitba')
    
    async def create_user(self, user):
        collection = self.db.get_collection('users')
        response = collection.insert_one(user)
        return response
    

    # async def update_user(self, user):
    #     collection = self.db.get_collection('users')
    #     response = collection.update_one({
    #         '_id': user['_id']
    #     },{
    #         '$set': {
    #             'name': user['name'],
    #             'age': user['age'],
    #             'status': 'active',
    #             'photo_id': user['photo_id']
    #     }})
    #     return response

    async def select_user(self, id):
        collection = self.db.get_collection('users')
        response = collection.find_one({"_id":id})
        return response
    
    async def select_all_users(self):
        collection = self.db.get_collection('users')
        cursor = collection.find({})
        return list(cursor)
    
    async def create_application(self, user, table):
        collection = self.db.get_collection(table)
        response = collection.insert_one(user)
        return response

    async def create_match(self, match):
        collection = self.db.get_collection('matches')
        response = collection.insert_one(match)
        return response
    
    async def select_match(self, chat_id):
        collection = self.db.get_collection('matches')
        response = collection.find_one({"$or":[ {"user1":chat_id}, {"user2":chat_id}]})
        if response['user1'] == chat_id:
            return response['user2']
        return response['user1']
    
    async def insert_message(self, message, receiver):
        file_path = await self.msg.getPhotoPath(message)
        collection = self.db.get_collection('chats')
        response = collection.insert_one({
            'sender': message.chat.id,
            'receiver': receiver,
            'image_path': file_path,
            'send_date': datetime.now()
        })

    async def create_application(self, user, table):
        collection = self.db.get_collection(table)
        response = collection.insert_one(user)
        return response

    async def select_all_male_applications(self):
        collection = self.db.get_collection('males_applicaitons')
        cursor = collection.find({})
        return list(cursor)
    
    async def select_all_female_applications(self):
        collection = self.db.get_collection('females_applicaitons')
        cursor = collection.find({})
        return list(cursor)

    async def delete_application(self, id, table):
        collection = self.db.get_collection(table)
        response = collection.delete_one({'_id': id})
        
# -----------------------------------------------------
# from typing import Collection
# from aiogram import Bot, Dispatcher, executor, types
# import motor.motor_asyncio
# from pymongo import MongoClient
# from data.config import BOT_TOKEN, MONGO_CONNECTION_KEY
# from datetime import datetime

# bot = Bot(token=BOT_TOKEN)
# dp = Dispatcher(bot=bot)
# cluster = motor.motor_asyncio.AsyncIOMotorClient(MONGO_CONNECTION_KEY)
# collection = cluster.hitba.users

# executor.start_polling()


# class DataBase():
#     def __init__(self):
#         CONNECTION_STRING = "mongodb+srv://admin:TwRMdudJTmoHNnfK@cluster0.0swwclu.mongodb.net/?retryWrites=true&w=majority"
#         self.client = MongoClient(CONNECTION_STRING)
#         self.db = self.client.get_database('hitba')
    
#     async def create_user(self, user):
#         collection = self.db.get_collection('users')
#         response = collection.insert_one(user)
#         return response
    
#     async def select_all_users(self):
#         collection = self.db.get_collection('users')
#         cursor = collection.find({})
#         return list(cursor)

#     async def create_match(self, match):
#         collection = self.db.get_collection('matches')
#         response = collection.insert_one(match)
#         return response
    
#     async def select_match(self, chat_id):
#         collection = self.db.get_collection('matches')
#         response = collection.find_one({"$or":[ {"user1":chat_id}, {"user2":chat_id}]})
#         if response['user1'] == chat_id:
#             return response['user2']
#         return response['user1']
    
#     async def insert_message(self, message, receiver):
#         file_path = await self.msg.getPhotoPath(message)
#         collection = self.db.get_collection('chats')
#         response = collection.insert_one({
#             'sender': message.chat.id,
#             'receiver': receiver,
#             'image_path': file_path,
#             'send_date': datetime.now()
#         })
