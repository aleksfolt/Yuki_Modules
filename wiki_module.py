from pyrogram import Client, filters
from pyrogram.types import Message
import wikipediaapi
import json

CONFIG_FILE = "config.json"

with open(CONFIG_FILE, "r") as file:
    config_data = json.load(file)
    prefix_userbot = config_data['prefix']

cinfo = f"🔍{prefix_userbot}wiki"
ccomand = f" ищет информацию по Википедии.\nПример: {prefix_userbot}wiki <запрос>"

wiki_wiki = wikipediaapi.Wikipedia(
    language='en',
    extract_format=wikipediaapi.ExtractFormat.WIKI,
    user_agent='Yuki/1.0'
)

def register_module(app: Client):
    @app.on_message(filters.me & filters.command("wiki", prefixes=prefix_userbot))
    async def wiki_search(client: Client, message: Message):
        try:
            query = " ".join(message.command[1:])
            if not query:
                await message.reply_text("❌ Пожалуйста, укажите запрос для поиска. Пример: `.wiki Python`")
                return

            page = wiki_wiki.page(query)

            if page.exists():
                title = page.title
                summary = page.summary[:500]
                page_url = page.fullurl

                reply_text = f"**📚 {title}**\n\n{summary}\n\n🔗 [Читать далее]({page_url})"
            else:
                reply_text = "❌ Не удалось найти информацию по вашему запросу."

            await message.reply_text(reply_text, disable_web_page_preview=True)

        except Exception as e:
            await message.reply_text(f"❌ Произошла ошибка: {e}")

    @app.on_message(filters.me & filters.command("wiki help", prefixes=prefix_userbot))
    async def wiki_help(client: Client, message: Message):
        help_text = (f"**ℹ️ Помощь по модулю поиска по Википедии:**\n\n"
                     f"**{prefix_userbot}wiki <запрос>** - Ищет информацию по указанному запросу на Википедии.\n"
                     f"**{prefix_userbot}wiki help** - Показать эту помощь.\n\n"
                     f"**Пример использования:**\n"
                     f"Поиск информации: `{prefix_userbot}wiki Python`")
        await message.reply_text(help_text)

