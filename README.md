# Image to graph.org Uploader Bot

A simple, asynchronous Telegram bot that uploads images, GIFs, and videos (under 5MB) to graph.org. It also outputs links for telegra.ph and tele.pe so you always have a working link in India.

The bot features a built-in `aiohttp` web server to pass Render.com health checks and stay awake!

## Features
- Uploads Photo, GIF, and Video up to 5MB.
- Asynchronous setup using `pyTelegramBotAPI` and `asyncio`.
- Output links for `graph.org`, `telegra.ph`, and `tele.pe`.
- A built-in web server listening on the `$PORT` environment variable for `Render` health checks.
- Clean and modern HTML parse mode formatting.

## Deployment on Render.com
1. Fork or download this repository.
2. Sign up on [Render.com](https://render.com) and create a new **Web Service**.
3. Connect your GitHub repository.
4. Set the runtime environment to **Docker**.
5. Render will automatically detect the `Dockerfile` and build it.
6. In the **Environment Variables** section, add your Bot Token:
   - Key: `TG_BOT_TOKEN`
   - Value: `your_bot_token_here` (get it from [@BotFather](https://t.me/botfather) on Telegram)
7. Click **Create Web Service**.
8. The bot will deploy, and the built-in web server will keep it healthy!

## Environment Variables
- `TG_BOT_TOKEN`: The API token from BotFather (Required).
- `PORT`: Automatically set by Render.com for the web server to bind to (Default is 8080).

## Local Testing
1. Clone the repository and `cd` into it.
2. Install dependencies: `pip install -r requirements.txt`
3. Export your bot token:
   ```bash
   export TG_BOT_TOKEN="your_bot_token_here"
   ```
4. Run the bot: `python3 bot.py`
