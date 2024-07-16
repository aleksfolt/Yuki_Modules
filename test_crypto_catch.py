from pyrogram import Client, filters
import re

with open("Yuki.bot", "r") as file:
    data = {}
    for line in file:
        key, value = line.strip().split('=')
        data[key] = value
    prefix_userbot = data['prefix']
    OWNER_ID = int(data['user_id'])
    print(OWNER_ID)

cinfo = f"🔗`{prefix_userbot}check_buttons`"
ccomand = " проверяет кнопки в сообщениях и отправляет команду /start соответствующему боту с параметром из ссылки. Пример: `check_buttons`"

def is_owner(_, __, message):
    return message.from_user.id == OWNER_ID

def register_module(app: Client):
    @app.on_message(filters.create(is_owner) & filters.command("check_buttons", prefixes=prefix_userbot))
    async def check_buttons(_, message):
        if message.reply_markup:
            for row in message.reply_markup.inline_keyboard:
                for button in row:
                    if button.url:
                        match = re.match(r"http://t.me/(send|cryptobot|cryptotestnetbot)\?start=(.+)", button.url)
                        if match:
                            bot_name, start_param = match.groups()
                            await message.reply(f"Отправка команды /start {start_param} боту @{bot_name}")
                            await app.send_message(f"@{bot_name}", f"/start {start_param}")
