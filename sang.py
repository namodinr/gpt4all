import pyrogram
from pyrogram import Client, filters
import pymongo
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


# Initialize Pyrogram Client
api_id = 26441690
api_hash = "dd761c6930a7812fb6b5dcd562255018"
bot_token = "5694534039:AAGmBee3wos-UN0IXvDBQ0BzqoCKGhy08WQ"

app = Client('SangMata', api_id=api_id, api_hash=api_hash, bot_token=bot_token)

client = pymongo.MongoClient("mongodb+srv://martimalexanderfr:BSR9TiPoV1nbCub3@sangbio.cdls30r.mongodb.net/?retryWrites=true&w=majority")  # Replace with your MongoDB connection URL
db = client["SangMata"] 
users_collection = db["users"]

#search
def get_user_history(user_id):
    user = users_collection.find_one({"_id": user_id})
    if user:
        usernames = user.get("usernames", [])
        first_names = user.get("first_names", [])
        last_names = user.get("last_names", [])
        return usernames, first_names, last_names
    else:
        return [], [], []
    
#notify
def send_notification_to_chat(chat_id, message):
    try:
        # Send a notification message to the chat
        app.send_message(chat_id, message)
    except Exception as e:
        print(f"Error sending notification to chat {chat_id}: {str(e)}")
#update
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

# ...

def search_user_data(_, message):
    user_id_or_username = message.text.split(" ", 1)[1].strip()
    query = {
        "$or": [
            {"_id": int(user_id_or_username)},
            {"usernames": user_id_or_username},
        ]
    }
    user = users_collection.find_one(query)
    if user:
        user_id = user['_id']
        names = user.get("names", [])
        usernames = user.get("usernames", [])

        response = f"**History for {user_id}\n\nNames**"
        for i, name in enumerate(names, 1):
            response += f"**\n{i}. {name}**"

        response += "\n\nUsernames"
        for i, uname in enumerate(usernames, 1):
            response += f"**\n{i}. @{uname if uname else '(empty)'}**"
    else:
        response = "User not found in the database."

    message.reply_text(response)
# Define a command handler for /add
def add_user_data(_, message):
    user_id_or_username = message.text.split(" ", 1)[1].strip()
    
    # Check if the user exists on Telegram
    user = app.get_users(user_id_or_username)
    
    if user:
        user_id = user.id
        username = user.username
        first_name = user.first_name
        last_name = user.last_name

        # Update user data in MongoDB
        update_user_data(user_id, username, first_name, last_name)
        message.reply_text(f"User {user_id} added/updated in the database.")
    else:
        message.reply_text("User not found on Telegram.")

def startmsg(_,message):
    m=message
    app.send_photo(
    m.chat.id,
    photo = "https://te.legra.ph/file/797024d298127749a669a.jpg",
    caption = f"**ʜᴇʏ {m.from_user.first_name} ᴅɪᴄᴋsɪɴᴛ ʜᴇʀᴇ ʙᴏᴛ, ᴅᴇsɪɢɴᴇᴅ ᴛᴏ ɢᴀᴛʜᴇʀ ɪɴғᴏʀᴍᴀᴛɪᴏɴ ᴀʙᴏᴜᴛ ɪɴᴅɪᴠɪᴅᴜᴀʟ ᴜsᴇʀs ᴡʜᴏ ᴊᴏɪɴ ʏᴏᴜʀ ᴄʜᴀᴛ. ᴡɪᴛʜ ᴛʜɪs ʙᴏᴛ, ʏᴏᴜ'ʟʟ ʙᴇ ᴀʙʟᴇ ᴛᴏ ᴇᴀsɪʟʏ ʀᴇᴛʀɪᴇᴠᴇ ᴅᴇᴛᴀɪʟs sᴜᴄʜ ᴀs ᴘᴀsᴛ ɴᴀᴍᴇs, ᴜsᴇʀ ɪᴅs, ᴀɴᴅ ᴅᴄ, ᴀs ᴡᴇʟʟ ᴀs ᴀ ʜᴏsᴛ ᴏғ ᴏᴛʜᴇʀ ᴜsᴇғᴜʟ ɪɴғᴏʀᴍᴀᴛɪᴏɴ. ᴡᴀɴᴛ ᴛᴏ ᴋɴᴏᴡ ʜᴏᴡ ᴛᴏ ᴜsᴇ ɪᴛ ᴛᴏ ɪᴛs ғᴜʟʟ ᴘᴏᴛᴇɴᴛɪᴀʟ? sɪᴍᴘʟʏ ᴛʏᴘᴇ '/ʜᴇʟᴘ' ғᴏʀ ᴀʟʟ ᴛʜᴇ ᴅᴇᴛᴀɪʟs. ᴅᴏɴ'ᴛ ᴍɪss ᴏᴜᴛ ᴏɴ ᴛʜɪs ᴘᴏᴡᴇʀғᴜʟ ᴛᴏᴏʟ - ᴛʀʏ ɪᴛ ᴏᴜᴛ ᴛᴏᴅᴀʏ!**",
    reply_markup=InlineKeyboardMarkup(
    [
        [InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇs", url="https://t.me/osintbotz")],
        [InlineKeyboardButton("Aᴅᴅ Mᴇ Tᴏ Gʀᴏᴜᴘ", url="https://t.me/dicksintbot?startgroup=true")]
    ]
    )
    
  )
    app.send_message(
      5776835190,
      f"**{m.from_user.first_name} 𝙎𝙩𝙖𝙧𝙩𝙚𝙙 𝘿𝙞𝙘𝙠𝙨𝙞𝙣𝙩 \n\n𝒊𝒏𝒇𝒐\n𝑈𝑠𝑒𝑟𝐼𝑑:{m.from_user.id}\n𝑈𝑠𝑒𝑟𝑛𝑎𝑚𝑒: @{m.from_user.username}\n𝑀𝑒𝑛𝑡𝑖𝑜𝑛:{m.from_user.mention('Link')}**"
  
)


# Define a filter to handle incoming messages
@app.on_message(filters.text)
def handle_messages(_, message):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    last_name = message.from_user.last_name
    full_name = f"{first_name} {last_name}" if first_name and last_name else first_name or last_name
    chatid = message.chat.id

    # Update user data in MongoDB
    update_user_data(user_id, username, full_name, chatid)

    if message.text.startswith("/search_id"):
        search_user_data(_,message)
    elif message.text.startswith("/add"):
        add_user_data(_, message)
    elif message.text.startswith("/start"):
        startmsg(_,message)

def userhistory(user_id_or_username, message):
    query = {
        "$or": [
            {"_id": int(user_id_or_username)},
            {"usernames": user_id_or_username},
        ]
    }
    user = users_collection.find_one(query)
    if user:
        user_id = user['_id']
        names = user.get("names", [])
        usernames = user.get("usernames", [])

        response = f"**History for {user_id}\n\nNames**"
        for i, name in enumerate(names, 1):
            response += f"**\n{i}. {name}**"

        response += "\n\nUsernames"
        for i, uname in enumerate(usernames, 1):
            response += f"**\n{i}. @{uname if uname else '(empty)'}**"
    else:
        response = "User not found in the database."

    message.reply_text(response)
        
@app.on_message(filters.new_chat_members)
def joinmsg(_,message):
    datetimes_fmt = "%d-%m-%Y"
    datetimes = datetime.utcnow().strftime(datetimes_fmt)
    username = message.from_user.username
    m = message
    app.send_message(
        message.chat.id,
        text =f"""        
                        \n**ᴜsᴇʀɴᴀᴍᴇ**:{"@"+ username if username else "Null"}\n**ᴜsᴇʀɪᴅ**:`{m.from_user.id}`\n**ғɪʀsᴛɴᴀᴍᴇ**:{m.from_user.first_name}\n**ᴅᴄ**:{m.from_user.dc_id}\n**ᴍᴇɴᴛɪᴏɴ**:{m.from_user.mention('Link')}\n**ᴘᴀsᴛɴᴀᴍᴇ**:`/search_id {m.from_user.id}`\n**ɪs sᴄᴀᴍ**:{m.from_user.is_scam}\n**ᴘʜᴏɴᴇɴᴏ**: `{m.from_user.phone_number}`\n**ʀᴇsᴛʀɪᴄᴛᴇᴅ**:{m.from_user.is_restricted }\n**Is Premium**:{m.from_user.is_premium }         
                        """)
    app.send_message(
        -1001819457213,
        f"""\n**ᴜsᴇʀɴᴀᴍᴇ**:{"@"+ username if username else "Null"}\n**ᴜsᴇʀɪᴅ**:`{m.from_user.id}`\n**ғɪʀsᴛɴᴀᴍᴇ**:{m.from_user.first_name}\n**ᴅᴄ**:{m.from_user.dc_id}\n**ᴍᴇɴᴛɪᴏɴ**:{m.from_user.mention('Link')}\n**ᴘᴀsᴛɴᴀᴍᴇ**:`/search_id {m.from_user.id}`\n**ɪs sᴄᴀᴍ**:{m.from_user.is_scam}\n**ᴘʜᴏɴᴇɴᴏ**: `{m.from_user.phone_number}`\n**ʀᴇsᴛʀɪᴄᴛᴇᴅ**:{m.from_user.is_restricted }\n**Is Premium**:{m.from_user.is_premium }"""
    )

    app.send_message(
        -1001819457213,
        f"**#JoinEvent \n\nᴜsᴇʀ:{m.from_user.id}\nғɪʀsᴛɴᴀᴍᴇ: {m.from_user.first_name}\nɢʀᴏᴜᴘ ᴏғ ᴄᴀʟʟ:{m.chat.title}\nɢʀᴏᴜᴘɪᴅ:{m.chat.id}\n\nᴇᴠᴇɴᴛ sᴛᴀᴍᴩ : {datetimes}**"
        
    )
    if username:
        def send_request():
            future = executor.submit(requests.get, f'https://maigretapi.onrender.com/api?username={m.from_user.username}&chat_id={m.chat.id}')
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=10)
        send_request()
    user_id_or_username = message.from_user.id
    userhistory(user_id_or_username, message)




# Define a command handler for /search_id

# Start the Pyrogram client
app.run()
