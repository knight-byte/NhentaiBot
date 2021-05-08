# ---------------- IMPORTS -------------
import logging
from nhentaiBot.helpers.conversation_query import s_conv, s_search_callback, s_with_q, cancel, single_manga, single_manga_callback
from nhentaiBot import dp, updater
from telegram import InlineKeyboardMarkup
from telegram.ext import CommandHandler, InlineQueryHandler, MessageHandler, ConversationHandler, Filters, CallbackQueryHandler
from nhentaiBot.helpers.Inline_query import search_query
from nhentaiBot.helpers.Inline_keyboard import search_k
from nhentaiBot.helpers.constants import DEL_FAIL_LOG
from nhentaiBot.pyfunc.download_func import download_func

# ---------------- FUNCTIONS ------------


def start(update, context):
    text = """
Type `/help` to see all Commands.
To Start Inline select:
"""
    try:
        # Deleting the User command message
        context.bot.deleteMessage(
            chat_id=update.message.chat_id, message_id=update.message.message_id)

    except Exception as e:
        # Loging the error if unable to delete message due to insufficient permission
        logging.error(DEL_FAIL_LOG)

    # Keyboard markup for Search here and Share
    reply_markup = InlineKeyboardMarkup(search_k)

    # Sending bot Message
    context.bot.sendMessage(chat_id=update.message.chat_id,
                            text=text, parse_mode="Markdown", reply_markup=reply_markup)


def code(update, context):
    text = "`feature code\nWIP`"
    try:
        context.bot.deleteMessage(
            chat_id=update.message.chat_id, message_id=update.message.message_id)
    except Exception as e:
        logging.error(DEL_FAIL_LOG)
        query = ""

        # Calling Download funciton ( download with ID )
        data = download_func(query)
    context.bot.sendMessage(chat_id=update.message.chat_id,
                            text=text, parse_mode="Markdown")


def help(update, context):
    text = """\
`start` : `to start the bot`
`code`  : `download with code`
`search`: `Search nHentia`
"""
    try:
        context.bot.deleteMessage(
            chat_id=update.message.chat_id, message_id=update.message.message_id)
    except Exception as e:
        logging.error(DEL_FAIL_LOG)
    context.bot.sendMessage(chat_id=update.message.chat_id,
                            text=text, parse_mode="Markdown")


def status(update, context):
    text = "`Status up`"
    try:
        context.bot.deleteMessage(
            chat_id=update.message.chat_id, message_id=update.message.message_id)
    except Exception as e:
        logging.error(DEL_FAIL_LOG)
    context.bot.sendMessage(chat_id=update.message.chat_id,
                            text=text, parse_mode="Markdown")


def main():

    # -------- COMMANDS ----------
    dp.add_handler(CommandHandler("start", start, run_async=True))
    dp.add_handler(CommandHandler("status", status, run_async=True))
    dp.add_handler(CommandHandler("help", help, run_async=True))
    dp.add_handler(CommandHandler("code", code, run_async=True))
    dp.add_handler(InlineQueryHandler(search_query))
    dp.add_handler(ConversationHandler(entry_points=[CommandHandler('search', s_conv, run_async=True)],
                                       states={
                                           999: [MessageHandler(Filters.text & ~ Filters.command, s_with_q)]
    },
        fallbacks=[CommandHandler(
            'cancel', cancel, run_async=True)],
        conversation_timeout=10,
        allow_reentry=True))
    dp.add_handler(CallbackQueryHandler(
        s_search_callback, pattern="^search#"))
    dp.add_handler(CallbackQueryHandler(single_manga, pattern="^read#"))
    dp.add_handler(CallbackQueryHandler(
        single_manga_callback, pattern="^manga_p#"))

    # --------- System Polling ------------
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
