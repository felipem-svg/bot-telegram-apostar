import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = os.getenv("BOT_TOKEN")  # Use variável de ambiente

VIDEO_ID = "BAACAgEAAxkBAAIBeWmXXriakXooBPdl0AbvdJ2hq7cFAAKjBwACmMXBRJG4SSjXj3FQOgQ"
LINK_COMUNIDADE = "https://t.me/+byKlrMy8nys1ZmFh"

logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Botão
    keyboard = [
        [InlineKeyboardButton("🎁 Entrar na Comunidade", url=LINK_COMUNIDADE)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Envia vídeo
    await update.message.reply_video(
        video=VIDEO_ID,
        caption="🎉 Entre na nossa comunidade com vários prêmios e promoções exclusivas!",
        supports_streaming=True,
        reply_markup=reply_markup
    )

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    print("Bot rodando...")
    app.run_polling()

if __name__ == "__main__":
    main()
