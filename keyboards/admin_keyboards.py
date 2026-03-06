from telegram import ReplyKeyboardMarkup


def get_admin_keyboard():
    keyboard = [
        ["➕ Post qo‘shish", "🗑 Post o‘chirish"],
        ["➕ Kanal qo‘shish", "🗑 Kanal o‘chirish"],
        ["➕ Xizmat qo‘shish", "🗑 Xizmat o‘chirish"],
        ["✏️ About ni o‘zgartirish", "📸 Instagramni o‘zgartirish"],
        ["📊 Statistika", "🏠 User menyu"],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)