import requests
from pyrogram import Client, filters
from pyrogram.errors import PeerIdInvalid
from pyrogram.types import Message
from io import BytesIO

with open("Yuki.bot", "r") as file:
    data = {}
    for line in file:
        key, value = line.strip().split('=')
        data[key] = value
    prefix_userbot = data['prefix']
    OWNER_ID = int(data['user_id'])
    print(OWNER_ID)

cinfo = f"📝`{prefix_userbot}userinfo`"
ccomand = " получает информацию о пользователе, на сообщение которого ответили, или о себе, если команды используется без ответа."

def is_owner(_, __, message):
    return message.from_user.id == OWNER_ID

def download_profile_photo(client, user_id):
    profile_photos = client.get_chat_photos(user_id)
    if profile_photos:
        file_id = profile_photos[0].file_id
        file_path = client.download_media(file_id)
        with open(file_path, "rb") as file:
            return BytesIO(file.read())
    return None

def fetch_user_info(client, message, target_user):
    try:
        user = client.get_users(target_user.id)
        shared_chats_count = len(client.get_common_chats(user.id))

        bio = user.bio if user.bio else "🚫"
        last_name = user.last_name if user.last_name else "🚫"
        username = f"@{user.username}" if user.username else "🚫"
        shared_chats_text = f"Shared Chats: {shared_chats_count}"
        
        info_text = (
            f"👤 User:\n\n"
            f"First name: {user.first_name}\n"
            f"Last name: {last_name}\n"
            f"Username: {username}\n"
            f"About: {bio}\n\n"
            f"{shared_chats_text}\n\n"
            f"ID: {user.id}"
        )

        photo = download_profile_photo(client, user.id)
        if photo:
            message.reply_photo(photo, caption=info_text)
        else:
            message.reply_text(info_text)

    except PeerIdInvalid:
        message.reply_text("**❌ Не удалось получить информацию о пользователе.**")

def register_module(app: Client):
    @app.on_message(filters.create(is_owner) & filters.command("userinfo", prefixes=prefix_userbot))
    def userinfo_handler(client: Client, message: Message):
        target_user = message.reply_to_message.from_user if message.reply_to_message else message.from_user
        fetch_user_info(client, message, target_user)
