# --------- IMPORTS ---------
from typing import Text
from telegram import InlineKeyboardButton

# --------- KEYBOARD LAYOUT -----
search_k = [
    [
        InlineKeyboardButton(
            text="Search here", switch_inline_query_current_chat=""),
        InlineKeyboardButton(
            text="Share", switch_inline_query="")
    ]
]
