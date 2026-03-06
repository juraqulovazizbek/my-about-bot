from telegram import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from texts import TEXTS


def get_user_main_keyboard(lang: str):
    t = TEXTS[lang]
    keyboard = [
        [KeyboardButton(t["menu_posts"]), KeyboardButton(t["menu_channels"])],
        [KeyboardButton(t["menu_about"]), KeyboardButton(t["menu_services"])],
        [KeyboardButton(t["menu_language"]), KeyboardButton(t["menu_rating"])],
        [KeyboardButton(t["menu_contact"])],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)


def get_all_posts_button(lang: str):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(TEXTS[lang]["all_posts_btn"], callback_data="all_posts")]
    ])


def get_posts_keyboard(posts):
    buttons = []
    for post in posts:
        buttons.append([
            InlineKeyboardButton(f"📰 {post['title']}", callback_data=f"post_{post['id']}")
        ])
    return InlineKeyboardMarkup(buttons)


def get_channels_keyboard(channels, instagram_url=None, instagram_label="📸 Instagram"):
    buttons = []

    for channel in channels:
        buttons.append([
            InlineKeyboardButton(f"📢 {channel['name']}", url=channel["url"])
        ])

    if instagram_url and instagram_url.strip():
        buttons.append([
            InlineKeyboardButton(instagram_label, url=instagram_url)
        ])

    return InlineKeyboardMarkup(buttons)


def get_rating_reply_keyboard(lang: str):
    t = TEXTS[lang]
    keyboard = [
        [KeyboardButton("⭐ 1"), KeyboardButton("⭐ 2"), KeyboardButton("⭐ 3")],
        [KeyboardButton("⭐ 4"), KeyboardButton("⭐ 5")],
        [KeyboardButton(t["back"])],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)


def get_back_keyboard(lang: str):
    return ReplyKeyboardMarkup(
        [[KeyboardButton(TEXTS[lang]["back"])]],
        resize_keyboard=True,
        one_time_keyboard=True
    )


def get_language_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("🇺🇿 O‘zbek", callback_data="lang_uz"),
            InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
            InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
        ]
    ])