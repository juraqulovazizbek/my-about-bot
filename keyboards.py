from telegram import ReplyKeyboardMarkup


def get_main_keyboard():
    keyboard = [
        ["📝 Postlar", "📢 Kanallar"],
        ["ℹ️ About", "🛠 Xizmatlar"],
        ["🌐 Tillarni tanlash", "⭐ Botni baholash"],
        ["✉️ Menga xabar yuborish"],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True
    )


def get_language_keyboard():
    keyboard = [
        ["🇺🇿 O'zbek", "🇷🇺 Русский"],
        ["🇬🇧 English"],
    ]
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        one_time_keyboard=True
    )