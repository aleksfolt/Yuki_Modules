from pyrogram import Client, filters
import requests
import json

CONFIG_FILE = "config.json"

with open(CONFIG_FILE, "r") as file:
    config_data = json.load(file)
    prefix_userbot = config_data['prefix']
    OWNER_ID = int(config_data['user_id'])

cinfo = f"💱`{prefix_userbot}exchange_rate`"
ccomand = f" показывает курс обмена валют. Пример: `{prefix_userbot}exchange_rate USD RUB`"

def register_module(app: Client):
    @app.on_message(filters.me & filters.command("exchange_rate", prefixes=prefix_userbot))
    async def exchange_rate(_, message):
        try:
            base, target = message.text.split(" ")[1:3]
            response = requests.get(f"https://api.exchangerate-api.com/v4/latest/{base.upper()}")
            data = response.json()
            rate = data["rates"].get(target.upper())
            if rate:
                reply_text = f"**Курс {base.upper()} к {target.upper()}:** {rate}"
            else:
                reply_text = "**❌Неверная валюта.**"
        except Exception as e:
            reply_text = f"**❌Произошла ошибка: {e}**"
        await message.delete()
        await message.reply_text(reply_text)
