import os
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from nude import Nude

# Replace 'YOUR_BOT_TOKEN' with the actual token obtained from BotFather
TOKEN = '6844479075:AAH4QS78vCO8zLZ2ZXGpEOgC034Q-POmSSI'

def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! I am your Telegram Bot. Send me images, and I will check for nudity.')

def handle_images(update: Update, context: CallbackContext) -> None:
    message = update.message

    # Check if the message contains an image
    if message.photo:
        # Get the file ID of the largest photo in the message
        file_id = message.photo[-1].file_id

        # Download the image
        file_path = context.bot.get_file(file_id).download()

        # Check for nudity using the Nude class from nude.py
        n = Nude(file_path)
        n.parse()

        # If nudity is detected, delete the message
        if n.result:
            message.delete()
            update.message.reply_text('Nudity detected. Image deleted.')
        else:
            update.message.reply_text('No nudity detected. Image allowed.')
        
        # Remove the downloaded image file
        os.remove(file_path)
    else:
        update.message.reply_text('Please send me an image.')

def main() -> None:
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.photo, handle_images))

    updater.start_polling()

    # Run the bot until you send a signal to stop it
    updater.idle()

if __name__ == '__main__':
    main()
