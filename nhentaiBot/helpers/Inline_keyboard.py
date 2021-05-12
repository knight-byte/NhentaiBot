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
    ],
    [
        InlineKeyboardButton(
            text="About", callback_data="about_com"
        )
    ]
]

about_k = [
    [
        InlineKeyboardButton("Abuanchar's Telegram",
                             url="https://t.me/abunachar"),
        InlineKeyboardButton("Bhaskar's Telegram",
                             url="https://t.me/bhaskar_mahto"),
    ],
    [
        InlineKeyboardButton("Abunachar's Github",
                             url="https://github.com/knight-byte"),
        InlineKeyboardButton("Bhaskar's Github",
                             url="https://github.com/arbkm22"),
    ],
    [
        InlineKeyboardButton("Project Link",
                             url="https://github.com/knight-byte/NhentaiBot"),
    ]
]
