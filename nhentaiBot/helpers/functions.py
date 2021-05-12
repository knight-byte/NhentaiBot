from nhentaiBot.helpers.Inline_keyboard import about_k
from telegram import InlineKeyboardMarkup, parsemode


def about(update, context):
    text = """`Hey!
Bot Name     : nHentai BOT
Username     : @nhenyai_xbot
Inline Mode  : True
Group ( add ): True
Developed by : Abunachar, Bhaskar
Contack us :-`
"""
    chat_id = ""
    if update.callback_query != None:
        chat_id = update.callback_query.message.chat_id
    else:
        chat_id = update.message.chat_id
    reply_markup = InlineKeyboardMarkup(about_k)
    context.bot.sendMessage(chat_id=chat_id, text=text,
                            reply_markup=reply_markup, parse_mode="Markdown")
