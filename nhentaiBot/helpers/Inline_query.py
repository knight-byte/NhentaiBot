from nhentaiBot.pyfunc.searcher import homepage, search_q
from telegram import InlineQueryResultArticle, InputTextMessageContent, InlineQueryResultPhoto, InlineKeyboardButton, InlineKeyboardMarkup


def search_query(update, context):
    query = update.inline_query.query
    results = []
    data = None
    if len(query) != 0:
        results = []
        data = search_q(query)

    else:
        results = []
        data = homepage()

    for single in data:
        single = single.__dict__
        caption = f"""
*Title* : `{single["title"]}`
*ID*    : `#{single["id"]}`
*Lang*  : `{single["lang"]}`
"""
        keyboard = [

            [InlineKeyboardButton("Download",
                                  url="https://t.me/nhentai_xbot"),
                InlineKeyboardButton("Visit",
                                     url=f"https://nhentai.net/g/{single['id']}")],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        temp = InlineQueryResultPhoto(id=single["id"], photo_url=single["cover"], thumb_url=single["cover"], caption=caption,
                                      title=single["title"], description=f"lang : {single['lang']} ", parse_mode="Markdown", reply_markup=reply_markup)
        results.append(temp)
        if len(results) == 0:
            temp = InlineQueryResultArticle(id="xxx",
                                            title="No Result found", input_message_content=InputTextMessageContent(f"No result", parse_mode="Markdown"))

    update.inline_query.answer(results, auto_pagination=True)
