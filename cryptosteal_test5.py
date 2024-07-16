from pyrogram import Client, filters
import re
import asyncio

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

class CryptoSteal:
    def __init__(self, app):
        self.app = app
        self.acquired = []
        self.regex = None
        self.id_regex = None
        self.username_id_map = {}
        self.regex_ready = asyncio.Event()
        self.config = {
            "delay": 100,
            "bots": ["send", "cryptobot", "cryptotestnetbot"],
            "only_inline": False,
            "token_length_limit": 32
        }

    async def start(self):
        await self.process_config()

    async def process_config(self):
        self.regex_ready.clear()

        whitelist = []
        whitelist_ids = []
        for bot_name in self.config["bots"]:
            entity = await self.app.get_users(bot_name)
            whitelist.append(re.escape(entity.username.lower()))
            self.username_id_map[entity.username.lower()] = entity.id
            whitelist_ids.append(str(entity.id))

        self.regex = f"t\\.me\\/(?i:(?P<bot>{'|'.join(whitelist)}))\\?start=(?P<token>[a-zA-Z0-9+/_-]+)"
        self.id_regex = f"({'|'.join(whitelist_ids)})"
        self.regex_ready.set()

    async def acquire(self, bot, token):
        if token.lower() in self.acquired or len(token) > self.config["token_length_limit"]:
            return

        self.acquired.append(token.lower())

        await asyncio.sleep(self.config["delay"] / 1000)

        await self.app.send_message(bot, f"/start {token}")

    async def check_buttons(self, client, message):
        if message.reply_markup:
            for row in message.reply_markup.inline_keyboard:
                for button in row:
                    if button.url:
                        match = re.match(self.regex, button.url)
                        if match:
                            bot_name, start_param = match.groups()
                            await self.acquire(bot_name, start_param)

def register_module(app: Client):
    crypto_steal = CryptoSteal(app)
    
    @app.on_message(filters.create(is_owner) & filters.regex(r"^🦋 Чек на"))
    async def check_buttons_handler(client, message):
        await crypto_steal.check_buttons(client, message)

    app.add_handler(check_buttons_handler)
    app.add_handler(crypto_steal.start, group=0)
