import logging
import acoustid
import config
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text="This Bot is for recognizing music. So you can just send hime a voice message "
                                        "and he'll respond with the song title.")


async def voice(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Received voice message")
    voice_msg = update.message.voice
    file = await context.bot.get_file(voice_msg.file_id)

    filename = "song.mp3"
    generate_finger_print()

    await file.download_to_drive(filename)
    (duration, fingerprint) = acoustid.fingerprint_file('song.mp3')
    await update.message.reply_text(acoustid.lookup(fingerprint=fingerprint, apikey=config.api_key, duration=duration))


def generate_finger_print():
    (duration, fingerprint) = acoustid.fingerprint_file('song.ogg')
    print(acoustid.lookup(fingerprint=fingerprint, apikey=config.api_key, duration=duration))
    print(fingerprint)
    print("WiP")


if __name__ == '__main__':
    application = ApplicationBuilder().token(config.bot_token).build()

    start_handler = CommandHandler('start', start)
    voice_handler = MessageHandler(filters.ATTACHMENT, voice)

    application.add_handler(start_handler)
    application.add_handler(voice_handler)

    application.run_polling()
