import pymongo
from pyrogram import Client, filters
from datetime import datetime
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
import time
import requests
from pyrogram.errors import PeerIdInvalid
import concurrent.futures
from datetime import datetime
import  json
import asyncio
import os


api_id = 26441690
api_hash = "dd761c6930a7812fb6b5dcd562255018"
ss = "BACXLmMAlmW0HUIyTVVCkXY7o_-ShfBpPw12aldoicXIZVodJaVPhOIT4O_cqYLZUMReypQtwY9Q2uAqhPxmq6nbUvTNrDO8asa32y1TuP-14bxrsOl3yQAEOBgnfQcG6aa60cp3sefC-vyrgcwuaDwuOJPvBcEgC27iyRQoJ2yzG-PzLByg5u30I4oxU0zE9jpZwemNr17og_IOTt3k2yWrX6SnSFgCIRKe8gfEuE4x9cfoXAgd7QyU4BQuVivY0MaLM9rYyzW8gId7ElhYQvW-1DnMtD8IS6hqYLkF52L8HUcdBq5ZKnBD_myxIak6_gy-yBaENK48x5PYaBxCH_Fykh9G5AAAAAGENGYMAA"

app = Client('SangMata Userbot', api_id=api_id, api_hash=api_hash, session_string=ss)

client = pymongo.MongoClient("mongodb+srv://martimalexanderfr:BSR9TiPoV1nbCub3@sangbio.cdls30r.mongodb.net/?retryWrites=true&w=majority")  # Replace with your MongoDB connection URL
db = client["SangMata"] 
users_collection = db["users"]
db2 = client["bio_sang"]
col = db2["data"]
botusers_col = db2["botusers"]



#notification
def send_notification_to_chat(chat_id, message):
    try:
        # Send a notification message to the chat
        app.send_message(-1001819457213, message)
    except Exception as e:
        print(f"Error sending notification to chat {chat_id}: {str(e)}")
    
def save_bio(id,bio):
    try:
        user = col.find_one({"id": id})
        if user:
            if len(user["bio"]) > 0:
                last_bio = user["bio"][-1]
                if bio != last_bio:
                    col.update_one({"_id": user["_id"]}, {"$push": {"bio": bio}})
                    send_notification_to_chat(13414225, f"**🔍 User {id} changed bio from {last_bio} to {bio}**")
            elif len(user["bio"]) == 0:
                col.update_one({"_id": user["_id"]}, {"$push": {"bio": bio}})
        else:
            new_user = {"id": id, "bio": [bio]}
            col.insert_one(new_user)
    except pymongo.errors.PyMongoError as e:
        print(f"Error while saving bio for user {id}: {e}")

#update
def update_user_data(user_id, username, full_name, chatid):
    user_data = {
        "_id": user_id,
    }

    # Check if user exists in the database
    existing_user = users_collection.find_one({"_id": user_id})

    if existing_user:
        # Check if the username has changed and not already in history
        if username and username != existing_user.get("username"):
            last_username = existing_user.get("usernames", [])[-1] if existing_user.get("usernames") else None
            if username != last_username:
                users_collection.update_one({"_id": user_id}, {"$push": {"usernames": username}})
                send_notification_to_chat(chatid, f"**🔍 User {user_id} changed username from {last_username} to @{username}**")
        
        # Check if the full_name has changed and not already in history
        if full_name:
            last_full_name = existing_user.get("names", [])[-1] if existing_user.get("names") else None
            if full_name != last_full_name:
                users_collection.update_one({"_id": user_id}, {"$push": {"names": full_name}})
                send_notification_to_chat(chatid, f"**🔍 User {user_id} changed name from {last_full_name} to {full_name}**")
    else:
        # If the user doesn't exist, add them to the database with initial values as arrays
        user_data["usernames"] = [username] if username else []
        user_data["names"] = [full_name] if full_name else []

        users_collection.insert_one(user_data)


    
@app.on_message(filters.text)
def handle_messages(_, message):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    full_name = f"{first_name} {last_name}" if first_name and last_name else first_name or last_name
    chatid = message.chat.id
    user_bio = app.get_chat(message.from_user.id)
    save_bio(user_bio.id, user_bio.bio)
    update_user_data(user_id, username, full_name, chatid)


@app.on_message(filters.command("spy"))
def spy(_,message):
    app.send_message("Spy Bot up","me")


app.run()
