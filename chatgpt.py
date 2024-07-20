from pyrogram import Client, filters
import g4f

g4f.debug.logging = False
g4f.check_version = False

with open("Yuki.bot", "r") as file:
    data = {}
    for line in file:
        key, value = line.strip().split('=')
        data[key] = value
    prefix_userbot = data['prefix']
    OWNER_ID = int(data['user_id'])

cinfo = f"🤖`{prefix_userbot}gpt`"
ccomand = " ChatGPT"


def register_module(app: Client):
    @app.on_message(filters.me & filters.command("gpt", prefixes=prefix_userbot))
    async def gpt_command(_, message):
        user_input = message.text.split(f"{prefix_userbot}gpt ", maxsplit=1)[1]
        response = g4f.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": user_input}],
        )
        reply_text = (
            f"**🔍 Запрос:** `{user_input}`\n"
            f"**🧠 Ответ:** `{response}`"
        )
        await message.reply_text(reply_text)
