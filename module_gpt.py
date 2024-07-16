from pyrogram import Client, filters
import g4f

g4f.debug.logging = False
g4f.check_version = False

with open("Yuki.bot", "r") as file:
    lines = file.readlines()
    prefix_userbot = lines[2].strip().split('=')[1]
    OWNER_ID = int(lines[1].strip().split('=')[1])

cinfo = f"🧠`{prefix_userbot}gpt`"
ccomand = " ChatGPT"

def is_owner(_, __, message):
    return message.from_user.id == OWNER_ID

def register_module(app: Client):
    @app.on_message(filters.create(is_owner) & filters.command("gpt", prefixes=prefix_userbot))
    async def gpt_command(_, message):
        user_input = message.text.split(f"{prefix_userbot}gpt ", maxsplit=1)[1]
        response = g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}],
        )
        response_text = response["choices"][0]["message"]["content"]
        reply_text = f"**👨Ваш запрос: {user_input}**\n🧠Ответ от ChatGPT: `{response_text}`"
        await message.reply_text(reply_text)
