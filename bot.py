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
log = logging.getLogger("video-welcome-bot")

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
CACHE_PATH = "file_ids.json"

if not TOKEN:
    log.error("TELEGRAM_TOKEN não encontrada!")

def load_cache() -> dict:
    try:
        if os.path.exists(CACHE_PATH):
            with open(CACHE_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
    except Exception as e:
        log.warning(f"Erro ao carregar cache: {e}")
    return {"videos": []}

def save_cache(data: dict):
    try:
        with open(CACHE_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        log.warning(f"Erro ao salvar cache: {e}")

FILE_IDS = load_cache()

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    message = update.message

    video_file_id = None
    is_note = False

    if message.video:
        video_file_id = message.video.file_id
    elif message.video_note:
        video_file_id = message.video_note.file_id
        is_note = True

    if video_file_id:
        log.info(f"Vídeo absorvido do utilizador {chat_id}")

        if video_file_id not in FILE_IDS["videos"]:
            FILE_IDS["videos"].append(video_file_id)
            save_cache(FILE_IDS)

        if not is_note:
            await message.reply_video(video=video_file_id)
        else:
            await message.reply_video_note(video_note=video_file_id)

        id_msg = f"🆔 FILE_ID:\n`{video_file_id}`"
        await message.reply_text(id_msg, parse_mode="Markdown")

        welcome_text = "Seja bem-vindo à nossa comunidade! 🌟"
        await message.reply_text(welcome_text)

    else:
        log.warning("Recebido algo que não é um vídeo.")

def main():
    if not TOKEN:
        return

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.VIDEO | filters.VIDEO_NOTE, handle_video))

    log.info("🤖 Bot em execução...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
