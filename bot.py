import os
import asyncio
from aiohttp import web
from telebot.async_telebot import AsyncTeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
from sample_config import Config

bot = AsyncTeleBot(Config.TG_BOT_TOKEN)

if not os.path.isdir("DOWNLOADS"):
    os.makedirs("DOWNLOADS")

async def handle_ping(request):
    return web.Response(text="Hello, I am healthy!")

async def start_web_server():
    app = web.Application()
    app.router.add_get('/', handle_ping)
    app.router.add_get('/ping', handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.environ.get("PORT", 8080))
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()
    print(f"Web server started on port {port}")

@bot.message_handler(commands=['start'])
async def start_command(message):
    buttons = InlineKeyboardMarkup()
    buttons.add(
        InlineKeyboardButton('Help', callback_data='help'),
        InlineKeyboardButton('Close', callback_data='close')
    )
    text = (
        "<b>Hey there,</b>\n\n"
        "<b>I'm Image to graph.org Uploader.</b>\n\n"
        "<b>Simply send me a photo, video or gif to upload and get graph.org link.</b>"
    )
    await bot.reply_to(message, text, reply_markup=buttons, parse_mode='html')

@bot.message_handler(commands=['help'])
async def help_command(message):
    buttons = InlineKeyboardMarkup()
    buttons.add(
        InlineKeyboardButton('Home', callback_data='home'),
        InlineKeyboardButton('Close', callback_data='close')
    )
    text = (
        "Just Send Me A Video/gif/photo Upto 5mb.\n\n"
        "I'll upload and give you the direct links (graph.org, telegra.ph, tele.pe)."
    )
    await bot.reply_to(message, text, reply_markup=buttons, parse_mode='html')

@bot.callback_query_handler(func=lambda call: True)
async def callback_query(call):
    if call.data == "help":
        await bot.edit_message_text(
            "Just Send Me A Video/gif/photo Upto 5mb.\n\n"
            "I'll upload and give you the direct links (graph.org, telegra.ph, tele.pe).",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton('Home', callback_data='home'),
                InlineKeyboardButton('Close', callback_data='close')
            ),
            parse_mode='html'
        )
    elif call.data == "close":
        await bot.delete_message(call.message.chat.id, call.message.message_id)
    elif call.data == "home":
        await bot.edit_message_text(
            "<b>Hey there,</b>\n\n"
            "<b>I'm Image to graph.org Uploader.</b>\n\n"
            "<b>Simply send me a photo, video or gif to upload and get graph.org link.</b>",
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            reply_markup=InlineKeyboardMarkup().add(
                InlineKeyboardButton('Help', callback_data='help'),
                InlineKeyboardButton('Close', callback_data='close')
            ),
            parse_mode='html'
        )

def upload_to_imgbb(file_path):
    with open(file_path, 'rb') as f:
        resp = requests.post(
            "https://api.imgbb.com/1/upload",
            data={"key": Config.IMGBB_API_KEY},
            files={"image": f}
        ).json()
    if not resp.get("success"):
        raise Exception(resp.get("error", {}).get("message", "imgbb upload failed"))
    return resp["data"]["url"]

async def process_upload(message, file_id, extension, max_size=5242880):
    file_info = await bot.get_file(file_id)

    if file_info.file_size > max_size:
        await bot.reply_to(message, "Size Should Be Less Than 5 mb")
        return

    msg = await bot.reply_to(message, "<code>Downloading...</code>", parse_mode="html")
    userid = str(message.chat.id)
    file_path = f"./DOWNLOADS/{userid}_{file_id}.{extension}"

    downloaded_file = await bot.download_file(file_info.file_path)
    with open(file_path, 'wb') as new_file:
        new_file.write(downloaded_file)
        
    await bot.edit_message_text("<code>Uploading...</code>", chat_id=msg.chat.id, message_id=msg.message_id, parse_mode="html")

    try:
        url = await asyncio.to_thread(upload_to_imgbb, file_path)
        links = f"<b>imgbb:</b> {url}"
        await bot.edit_message_text(links, chat_id=msg.chat.id, message_id=msg.message_id, disable_web_page_preview=True, parse_mode="html")
    except Exception as e:
        await bot.edit_message_text(f"<code>Something went wrong: {e}</code>", chat_id=msg.chat.id, message_id=msg.message_id, parse_mode="html")
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)

@bot.message_handler(content_types=['photo'])
async def handle_photo(message):
    file_id = message.photo[-1].file_id
    await process_upload(message, file_id, "jpg")

@bot.message_handler(content_types=['animation'])
async def handle_animation(message):
    file_id = message.animation.file_id
    await process_upload(message, file_id, "mp4")

@bot.message_handler(content_types=['video'])
async def handle_video(message):
    file_id = message.video.file_id
    await process_upload(message, file_id, "mp4")

async def main():
    await start_web_server()
    await bot.polling(non_stop=True)

if __name__ == '__main__':
    asyncio.run(main())
