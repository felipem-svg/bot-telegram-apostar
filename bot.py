import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8542251478:AAEzP4IiTjKlB6jsCsPfdjVzGtjL_T0dm7E"

# Seu FILE_ID do vídeo circular
VIDEO_FILE_ID = "BAACAgEAAxkBAAIBeWmXXriakXooBPdl0AbvdJ2hq7cFAAKjBwACmMXBRJG4SSjXj3FQOgQ"

LINK_COMUNIDADE = "https://t.me/+byKlrMy8nys1ZmFh"

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id

    # Envia o vídeo circular
    await context.bot.send_video_note(
        chat_id=chat_id,
        video_note=VIDEO_FILE_ID
    )

    # Envia a mensagem com link
    await context.bot.send_message(
        chat_id=chat_id,
        text=f"🎁 **Entre na nossa comunidade com vários prêmios e promoções exclusivas!**\n\n👉 {LINK_COMUNIDADE}",
        parse_mode="Markdown",
        disable_web_page_preview=True
    )


def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("Bot rodando...")
    app.run_polling()


if __name__ == "__main__":
    main()
