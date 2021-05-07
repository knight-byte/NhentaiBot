# ---------- IMPORTS --------
from telegram import ForceReply, InputMediaPhoto
from nhentaiBot.pyfunc.searcher import search_q
from telegram_bot_pagination import InlineKeyboardPaginator
from telegram.ext import ConversationHandler
import logging
from nhentaiBot.helpers.constants import DEL_FAIL_LOG
# ------- GLOBAL VAR ----------
s_SEARCH_DATA = {}

# ----------- FUNCTIONS-----

# function to delete a message after sometime


def callback_alarm(context):
    context.job.context.delete()


def cancel(update, context):
    context.bot.sendMessage("You cancelled.")
    # conversationHandle end
    return ConversationHandler.END


def s_search_callback(update, context):
    global s_SEARCH_DATA

    # creating a UUID by combining unqiue user ID and chat ID
    uuid = f"{update.callback_query.message.chat_id}{update.effective_user.id}"
    query = update.callback_query
    # query.answer("loading")
    page = int(query.data.split('#')[1])

    paginator = InlineKeyboardPaginator(
        len(s_SEARCH_DATA[uuid]),
        current_page=page,
        data_pattern='search#{page}'
    )
    caption = f"""
*Title* : `{s_SEARCH_DATA[uuid][page-1]["title"]}`
*ID*    : `#{s_SEARCH_DATA[uuid][page-1]["id"]}`
*Lang*  : `{s_SEARCH_DATA[uuid][page-1]["lang"]}`
"""

    query.edit_message_media(
        media=InputMediaPhoto(media=s_SEARCH_DATA[uuid][page - 1]["cover"]), reply_markup=paginator.markup)
    query.edit_message_caption(
        caption=caption,
        reply_markup=paginator.markup,
        parse_mode='Markdown')


def s_conv(update, context):
    global s_SEARCH_DATA
    try:
        context.bot.deleteMessage(
            chat_id=update.message.chat_id, message_id=update.message.message_id)
    except Exception as e:
        logging.error(DEL_FAIL_LOG)
    query = " ".join(context.args)
    if len(query) < 1:
        update.message.reply_text("Search here ...",
                                  reply_markup=ForceReply(force_reply=True, selective=True))
        return 999
    else:
        temp = search_q(query)
        user_chat = update.effective_user.id
        user_grp = update.message.chat_id
        uuid = f"{user_grp}{user_chat}"
        data = [i.__dict__ for i in temp]
        s_SEARCH_DATA[uuid] = data
        if len(data) > 0:
            paginator = InlineKeyboardPaginator(
                len(s_SEARCH_DATA[uuid]),
                data_pattern="search#{page}"
            )
            caption = f"""
*Title* : `{s_SEARCH_DATA[uuid][0]["title"]}`
*ID*    : `#{s_SEARCH_DATA[uuid][0]["id"]}`
*Lang*  : `{s_SEARCH_DATA[uuid][0]["lang"]}`
    """
            message = context.bot.send_photo(
                photo=s_SEARCH_DATA[uuid][0]["cover"],
                chat_id=update.message.chat_id,
                caption=caption,
                reply_markup=paginator.markup,
                parse_mode='Markdown',
            )
            context.job_queue.run_once(
                callback_alarm, 600, context=message)

        else:
            message = context.bot.sendMessage(
                chat_id=update.message.chat_id, text="No result found :(")
            context.job_queue.run_once(
                callback_alarm, 600, context=message)
            return ConversationHandler.END


def s_with_q(update, context):
    try:
        context.bot.deleteMessage(
            chat_id=update.message.chat_id, message_id=update.message.message_id)
    except Exception as e:
        logging.error(DEL_FAIL_LOG)
    global s_SEARCH_DATA
    query = update.message.text
    if len(query) < 1:
        update.message.reply_text("Search here ...",
                                  reply_markup=ForceReply(force_reply=True, selective=True))
        return 999
    else:
        temp = search_q(query)
        user_chat = update.effective_user.id
        user_grp = update.message.chat_id
        uuid = f"{user_grp}{user_chat}"
        data = [i.__dict__ for i in temp]
        if len(data) > 0:
            s_SEARCH_DATA[uuid] = data
            paginator = InlineKeyboardPaginator(
                len(s_SEARCH_DATA[uuid]),
                data_pattern="search#{page}"
            )
            caption = f"""
    *Title* : `{s_SEARCH_DATA[uuid][0]["title"]}`
    *ID*    : `#{s_SEARCH_DATA[uuid][0]["id"]}`
    *Lang*  : `{s_SEARCH_DATA[uuid][0]["lang"]}`
    """
            message = context.bot.send_photo(
                photo=s_SEARCH_DATA[uuid][0]["cover"],
                chat_id=update.message.chat_id,
                caption=caption,
                reply_markup=paginator.markup,
                parse_mode='Markdown',
            )
            context.job_queue.run_once(
                callback_alarm, 600, context=message)
            return ConversationHandler.END
        else:
            message = context.bot.sendMessage(
                chat_id=update.message.chat_id, text="No result found :(")

            context.job_queue.run_once(
                callback_alarm, 600, context=message)
            return ConversationHandler.END
