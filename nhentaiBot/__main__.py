import logging
from telegram.ext.dispatcher import run_async
from nhentaiBot import dp, updater
from telegram.ext import CommandHandler


def start(update, context):
    text = "`working`"
    try:
        context.bot.deleteMessage(
            chat_id=update.message.chat_id, message_id=update.message.message_id)
    except Exception as e:
        logging.error("no admin rights unable to delete message")
    context.bot.sendMessage(chat_id=update.message.chat_id,
                            text=text, parse_mode="Markdown")


def code(update, context):
    text = "feature code"
    try:
        context.bot.deleteMessage(
            chat_id=update.message.chat_id, message_id=update.message.message_id)
    except Exception as e:
        logging.error("no admin rights unable to delete message")
    context.bot.sendMessage(chat_id=update.message.chat_id,
                            text=text, parse_mode="Markdown")


def help(update, context):
    text = """\
`start` : `to start the bot`
`code`  : `download with code`
"""
    try:
        context.bot.deleteMessage(
            chat_id=update.message.chat_id, message_id=update.message.message_id)
    except Exception as e:
        logging.error("no admin rights unable to delete message")
    context.bot.sendMessage(chat_id=update.message.chat_id,
                            text=text, parse_mode="Markdown")


def main():
    dp.add_handler(CommandHandler("start", start, run_async=True))
    dp.add_handler(CommandHandler("code", code, run_async=True))
    dp.add_handler(CommandHandler("help", help, run_async=True))
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
