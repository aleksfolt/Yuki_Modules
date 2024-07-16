from pyrogram import Client, filters
import asyncio
import random

with open("Yuki.bot", "r") as file:
    data = {}
    for line in file:
        key, value = line.strip().split('=')
        data[key] = value
    prefix_userbot = data['prefix']
    OWNER_ID = int(data['user_id'])

cinfo = f"☀`{prefix_userbot}mq`"
ccommand = " запускает отправку случайных сообщений из списка с указанным таймингом. Пример: `mq 5` (интервал в секундах)"


def is_owner(_, __, message):
    return message.from_user.id == OWNER_ID


messages = [
    "Привет! Как дела?",
    "Сегодня отличный день!",
    "Не забудь улыбнуться!",
    "Ты сегодня выглядишь отлично!",
    "Время для нового достижения!"
]

sending_task = None


def register_module(app: Client):
    @app.on_message(filters.create(is_owner) & filters.command("mq", prefixes=prefix_userbot))
    async def message_queue(_, message):
        global sending_task

        if sending_task:
            sending_task.cancel()
            sending_task = None
            await message.reply_text("**я устал тебя унижать,петух!**")
            return

        try:
            timing = int(message.text.split(" ", maxsplit=1)[1])
        except (IndexError, ValueError):
            await message.reply_text(f"**❌ Еблан по примеру указывай (там секунды если что) Пример: `{prefix_userbot}mq 5`**")
            return

        async def send_messages():
            while True:
                msg = random.choice(messages)
                await message.reply_text(msg)
                await asyncio.sleep(timing)

        sending_task = asyncio.create_task(send_messages())
        await message.reply_text(f"**тебя сын шлюхи не падай духом**\n\n**але петух** `я тебя убью нахуй`")
