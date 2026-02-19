import os
import json
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    filters,
    ContextTypes,
)

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    level=logging.INFO,
)
log = logging.getLogger("fileid-bot")

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

CACHE_PATH = "file_ids.json"

def load_cache():
    if os.path.exists(CACHE_PATH):
        with open(CACHE_PATH, "r") as f:
            return json.load(f)
    return {"videos": []}

def save_cache(data):
    with open(CACHE_PATH, "w") as f:
        json.dump(data, f, indent=2)

FILE_IDS = load_cache()

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg:
        return

    file_id = None

    if msg.video:
        file_id = msg.video.file_id
        tipo = "VIDEO"
    elif msg.video_note:
        file_id = msg.video_note.file_id
        tipo = "VIDEO_NOTE"
    else:
        return

    log.info(f"{tipo} capturado: {file_id}")

    if file_id not in FILE_IDS["videos"]:
        FILE_IDS["videos"].append(file_id)
        save_cache(FILE_IDS)

    await msg.reply_text(f"{tipo} FILE_ID:\n{file_id}")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.VIDEO | filters.VIDEO_NOTE, handle))
    log.info("Bot rodando...")
    app.run_polling()

if __name__ == "__main__":
    main()
