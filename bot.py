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
log = logging.getLogger("video-fileid-bot")

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")
CACHE_PATH = "file_ids.json"

if not TOKEN:
    log.error("TELEGRAM_TOKEN não encontrada!")

# ========= CACHE =========

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

# =========================

async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = update.message

    video_file_id = None

    if message.video:
        video_file_id = message.video.file_id
    elif message.video_note:
        video_file_id = message.video_note.file_id

    if not video_file_id:
        return

    log.info(f"FILE_ID capturado: {video_file_id}")

    # Salvar no cache
    if video_file_id not in FILE_IDS["videos"]:
        FILE_IDS["videos"].append(video_file_id)
        save_cache(FILE_IDS)

    # Apenas mostrar FILE_ID (SEM reenviar vídeo)
    await message.reply_text(
        f"🆔 FILE_ID do vídeo:\n`{video_file_id}`",
        parse_mode="Markdown"
    )


def main():
    if not TOKEN:
        return

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.VIDEO | filters.VIDEO_NOTE, handle_video))

    log.info("🤖 Bot capturador de FILE_ID em execução...")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
