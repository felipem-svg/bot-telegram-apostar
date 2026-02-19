import os
import json
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# ===== LOG =====
logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    level=logging.INFO,
)
log = logging.getLogger("fileid-bot")

# ===== ENV =====
load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")

CACHE_PATH = "file_ids.json"

# ===== CACHE =====
def load_cache():
    if os.path.exists(CACHE_PATH):
        with open(CACHE_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"videos": []}

def save_cache(data):
    with open(CACHE_PATH, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)

FILE_IDS = load_cache()

# ===== HANDLER =====
async def handle_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = update.message
    if not msg:
        return

    file_id = None
    tipo = None

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

    # SEM Markdown, SEM parse_mode → impossível dar erro
    texto = tipo + " FILE_ID:\n" + file_id
    await msg.reply_text(texto)

# ===== MAIN =====
def main():
    if not TOKEN:
        log.error("TELEGRAM_TOKEN não encontrada!")
        return

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.VIDEO | filters.VIDEO_NOTE, handle_video))

    log.info("🤖 Bot rodando...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
