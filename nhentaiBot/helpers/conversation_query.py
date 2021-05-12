# ---------- IMPORTS --------
from nhentaiBot.pyfunc.Image_to_pdf import image_pdf
from telegram import ForceReply, InputMediaPhoto, InlineKeyboardButton
from nhentaiBot.pyfunc.searcher import search_q, id_search_q
from telegram_bot_pagination import InlineKeyboardPaginator
from telegram.ext import ConversationHandler
import logging
from nhentaiBot.helpers.constants import DEL_FAIL_LOG
import os

# ------- GLOBAL VAR ----------
S_SEARCH_DATA = {}
SINGLE_MANGA_DATA = {}


# ----------- FUNCTIONS-----

# function to delete a message after sometime
def callback_alarm(context):
    context.job.context.delete()


# End the Conersation
def cancel(update, context):
    context.bot.sendMessage(
        chat_id=update.message.chat_id, text="`You cancelled.`", parse_mode="Markdown")
    # conversationHandle end
    return ConversationHandler.END


# Search callback function
def s_search_callback(update, context):
    global S_SEARCH_DATA

    # creating a UUID by combining unqiue user ID and chat ID
    uuid = f"{update.callback_query.message.chat_id}{update.effective_user.id}"
    query = update.callback_query
    # query.answer("loading")
    page = int(query.data.split('#')[1])

    paginator = InlineKeyboardPaginator(
        len(S_SEARCH_DATA[uuid]),
        current_page=page,
        data_pattern='search#{page}'
    )
    paginator.add_before(
        InlineKeyboardButton(
            'read', callback_data=f'read#{S_SEARCH_DATA[uuid][page-1]["id"]}'),
        InlineKeyboardButton(
            'Download', callback_data=f'download#{S_SEARCH_DATA[uuid][page-1]["id"]}')
    )
    caption = f"""
*Title* : `{S_SEARCH_DATA[uuid][page-1]["title"]}`
*ID*    : `#{S_SEARCH_DATA[uuid][page-1]["id"]}`
*Lang*  : `{S_SEARCH_DATA[uuid][page-1]["lang"]}`
"""

    query.edit_message_media(
        media=InputMediaPhoto(media=S_SEARCH_DATA[uuid][page - 1]["cover"]), reply_markup=paginator.markup)
    query.edit_message_caption(
        caption=caption,
        reply_markup=paginator.markup,
        parse_mode='Markdown')
    return ConversationHandler.END


def s_conv(update, context):
    global S_SEARCH_DATA
    query = " ".join(context.args)
    if len(query) < 1:
        update.message.reply_text("Search here ...",
                                  reply_markup=ForceReply(force_reply=True, selective=True))
        return 999
    else:
        pagination_search_context(update, context, query)
    try:
        context.bot.deleteMessage(
            chat_id=update.message.chat_id, message_id=update.message.message_id)
        return ConversationHandler.END

    except Exception as e:
        logging.error(DEL_FAIL_LOG)


def s_with_q(update, context):
    global S_SEARCH_DATA
    query = update.message.text
    if len(query) < 1:
        update.message.reply_text("Search here ...",
                                  reply_markup=ForceReply(force_reply=True, selective=True))
        return 999
    else:
        pagination_search_context(update, context, query)
    try:
        context.bot.deleteMessage(
            chat_id=update.message.chat_id, message_id=update.message.message_id)
        return ConversationHandler.END

    except Exception as e:
        logging.error(DEL_FAIL_LOG)
        return ConversationHandler.END


def pagination_search_context(update, context, query):
    temp = search_q(query)
    user_chat = update.effective_user.id
    user_grp = update.message.chat_id
    uuid = f"{user_grp}{user_chat}"
    data = [i.__dict__ for i in temp]
    if len(data) > 0:
        S_SEARCH_DATA[uuid] = data
        paginator = InlineKeyboardPaginator(
            len(S_SEARCH_DATA[uuid]),
            data_pattern="search#{page}"
        )
        paginator.add_before(
            InlineKeyboardButton(
                'read', callback_data=f'read#{S_SEARCH_DATA[uuid][0]["id"]}'),
            InlineKeyboardButton(
                'Download', callback_data=f'download#{S_SEARCH_DATA[uuid][0]["id"]}')
        )
        caption = f"""
*Title* : `{S_SEARCH_DATA[uuid][0]["title"]}`
*ID*    : `#{S_SEARCH_DATA[uuid][0]["id"]}`
*Lang*  : `{S_SEARCH_DATA[uuid][0]["lang"]}`
    """
        message = context.bot.send_photo(
            photo=S_SEARCH_DATA[uuid][0]["cover"],
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


# single manga view functiom
def single_manga(update, context):
    global SINGLE_MANGA_DATA
    query = update.callback_query
    id = query.data[5:]
    # print("QUERY : ", id)
    data = id_search_q(id)
    uuid = f"{update.callback_query.message.chat_id}{update.effective_user.id}"
    if len(data.keys()) > 0:
        SINGLE_MANGA_DATA[uuid] = data
        caption = f"""
*Title*: {SINGLE_MANGA_DATA[uuid]['title']}
*ID*   : {SINGLE_MANGA_DATA[uuid]['id']}
*Lang* : {", ".join(SINGLE_MANGA_DATA[uuid]['languages'])}
*Pages*: {SINGLE_MANGA_DATA[uuid]['total_pages']}
"""
        paginator = InlineKeyboardPaginator(
            len(SINGLE_MANGA_DATA[uuid]['images']),
            data_pattern="manga_p#{page}"
        )
        message = context.bot.send_photo(
            photo=SINGLE_MANGA_DATA[uuid]["images"][0],
            chat_id=update.callback_query.message.chat_id,
            caption=caption,
            reply_markup=paginator.markup,
            parse_mode='Markdown',
        )
        context.job_queue.run_once(
            callback_alarm, 600, context=message)
        return ConversationHandler.END
    else:
        context.bot.sendMessage(
            chat_id=update.callback_query.message.chat_id, text="Error loading")
        return ConversationHandler.END


def single_manga_callback(update, context):
    global SINGLE_MANGA_DATA
    query = update.callback_query
    # query.answer("loading")
    temp = query.data.split('#')[1]

    # id = temp.split("_")[0]
    # page = int(temp.split("_")[1])

    page = int(temp)
    # creating a UUID by combining unqiue user ID and chat ID
    uuid = f"{update.callback_query.message.chat_id}{update.effective_user.id}"

    paginator = InlineKeyboardPaginator(
        len(SINGLE_MANGA_DATA[uuid]["images"]),
        current_page=page,
        data_pattern='manga_p#{page}'
    )
    query.edit_message_media(
        media=InputMediaPhoto(media=SINGLE_MANGA_DATA[uuid]["images"][page-1]), reply_markup=paginator.markup)
    return ConversationHandler.END


def download_manga_callback(update, context):
    query = update.callback_query
    text = f"`downloading..,\nthis may take few min depend on the manga`"
    print("downloading...")
    context.bot.sendMessage(
        chat_id=update.callback_query.message.chat_id, text=text, parse_mode="Markdown")
    # query.answer("loading")
    id = query.data.split('#')[1]
    data = id_search_q(id)
    title = data["title"]
    img_list = data["images"]
    print(img_list)
    state = image_pdf(img_list=img_list, title=title)
    if state:
        manga_file = open(f'nhentaiBot/tempdir/{title}.pdf', 'rb')

        response = context.bot.sendDocument(
            chat_id=update.callback_query.message.chat_id, document=manga_file)

        # os.remove(f'nhentaiBot/tempdir/{title}.pdf')
