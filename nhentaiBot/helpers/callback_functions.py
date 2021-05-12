# -------- IMPORTS --------
import os
import re
from telegram import InputMediaPhoto, InlineKeyboardButton
from telegram_bot_pagination import InlineKeyboardPaginator
from nhentaiBot.helpers.constants import SINGLE_MANGA_DATA, S_SEARCH_DATA
from telegram.ext import ConversationHandler
from nhentaiBot.pyfunc.Image_to_pdf import image_pdf
from nhentaiBot.pyfunc.searcher import id_search_q

# -------- FUNCTIONS-------


# function to delete a message after sometime
def callback_alarm(context):
    context.job.context.delete()


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
    # print(img_list)
    title = "".join(re.findall(r"[\w]+", string=title))

    state = image_pdf(img_list=img_list, title=title)
    if state:
        manga_file = open(f'nhentaiBot/tempdir/{title}.pdf', 'rb')

        response = context.bot.sendDocument(
            chat_id=update.callback_query.message.chat_id, document=manga_file)

        os.remove(f'nhentaiBot/tempdir/{title}.pdf')
