from pyrogram import Client, filters

with open("Yuki.bot", "r") as file:
    data = {}
    for line in file:
        key, value = line.strip().split('=')
        data[key] = value
    prefix_userbot = data['prefix']
    OWNER_ID = int(data['user_id'])
    print(OWNER_ID)

cinfo = f"☀{prefix_userbot}userinfo"
ccomand = " показывает информацию о пользователе"

def is_owner(_, __, message):
    return message.from_user.id == OWNER_ID

def register_module(app: Client):
    @app.on_message(filters.create(is_owner) & filters.command("userinfo", prefixes=prefix_userbot))
    async def userinfo(_, message):
        if not message.reply_to_message:
            await message.reply_text("**❌Пожалуйста, ответьте на сообщение пользователя командой `.userinfo`**")
            return
        
        user = message.reply_to_message.from_user
        first_name = user.first_name if user.first_name else "Не указано"
        last_name = user.last_name if user.last_name else "Не указано"
        username = f"@{user.username}" if user.username else "Не указано"
        user_id = user.id

        reply_text = (f"**👤Информация о пользователе:**\n"
                      f"**Имя:** {first_name}\n"
                      f"**Фамилия:** {last_name}\n"
                      f"**Юзернейм:** {username}\n"
                      f"**ID:** {user_id}")
        
        await message.delete()
        await message.reply_text(reply_text)
