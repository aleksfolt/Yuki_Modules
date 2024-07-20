from pyrogram import Client, filters
import json
import os
from PIL import Image
import requests

SAVE_DIR = "saved_accounts"
AVATAR_DIR = "avatars"
os.makedirs(SAVE_DIR, exist_ok=True)
os.makedirs(AVATAR_DIR, exist_ok=True)

with open("Yuki.bot", "r") as file:
    data = {}
    for line in file:
        key, value = line.strip().split('=')
        data[key] = value
    prefix_userbot = data['prefix']
    OWNER_ID = int(data['user_id'])

cinfo = f"☀{prefix_userbot}saveacc"
ccomand = " Напишите -saveacc help для получения подробной информации."


async def save_avatar(app, photo_file_id, avatar_path):
    photo_file = await app.download_media(photo_file_id)
    image = Image.open(photo_file)
    image.save(avatar_path)
    os.remove(photo_file)


def register_module(app: Client):
    @app.on_message(filters.me & filters.command("saveacc help", prefixes=prefix_userbot))
    async def saveacc_help(_, message):
        help_text = (f"**ℹ️ Помощь по модулю сохранения аккаунтов:**\n\n"
                     f"**{prefix_userbot}saveacc <name>** - Сохранить текущее состояние аккаунта с именем <name>.\n"
                     f"**{prefix_userbot}setacc <name>** - Установить состояние аккаунта с именем <name>.\n"
                     f"**{prefix_userbot}saveacc help** - Показать эту помощь.\n\n"
                     f"**Пример использования:**\n"
                     f"Сохранение аккаунта: `{prefix_userbot}saveacc mybackup`\n"
                     f"Установка аккаунта: `{prefix_userbot}setacc mybackup`\n\n"
                     f"Модуль сделан чтобы поставить другую аватарку, никнейм по желанию и сохранить аккаунт, а потом поставить другую аватарку, никнейм и быстро переключаться между этими аккаунтами. Создавать можно неограниченное количество копий.")
        await message.reply_text(help_text)
        
    @app.on_message(filters.me & filters.command("saveacc", prefixes=prefix_userbot))
    async def saveacc(_, message):
        try:
            acc_name = message.text.split(" ", maxsplit=1)[1]
            user = await app.get_users(OWNER_ID)

            account_data = {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "username": user.username,
                "bio": (await app.get_chat(OWNER_ID)).bio
            }

            profile_photos = app.get_chat_photos(OWNER_ID)
            async for photo in profile_photos:
                avatar_path = os.path.join(AVATAR_DIR, f"{acc_name}.jpg")
                await save_avatar(app, photo.file_id, avatar_path)
                account_data["avatar"] = avatar_path
                break 

            with open(os.path.join(SAVE_DIR, f"{acc_name}.json"), "w") as f:
                json.dump(account_data, f, ensure_ascii=False, indent=4)

            await message.reply_text(f"**✅Аккаунт сохранен под именем {acc_name}.**")

        except IndexError:
            await message.reply_text("**❌Пожалуйста, укажите имя для сохранения аккаунта. Пример: `.saveacc <name>`**")
        except Exception as e:
            await message.reply_text(f"**❌Произошла ошибка: {e}**")

    @app.on_message(filters.me & filters.command("setacc", prefixes=prefix_userbot))
    async def setacc(_, message):
        try:
            acc_name = message.text.split(" ", maxsplit=1)[1]
            with open(os.path.join(SAVE_DIR, f"{acc_name}.json"), "r") as f:
                account_data = json.load(f)

            await app.update_profile(
                first_name=account_data.get("first_name"),
                last_name=account_data.get("last_name"),
                bio=account_data.get("bio")
            )

            avatar_path = account_data.get("avatar")
            if avatar_path and os.path.exists(avatar_path):
                await app.set_profile_photo(photo=avatar_path)

            await message.reply_text(f"**✅Аккаунт установлен как {acc_name}.**")

        except IndexError:
            await message.reply_text("**❌Пожалуйста, укажите имя для установки аккаунта. Пример: `.setacc <name>`**")
        except FileNotFoundError:
            await message.reply_text("**❌Сохраненный аккаунт не найден. Убедитесь, что имя указано правильно.**")
        except Exception as e:
            await message.reply_text(f"**❌Произошла ошибка: {e}**")
