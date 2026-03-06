from telegram import Update
from telegram.ext import ContextTypes

from keyboards import get_main_keyboard, get_language_keyboard
from texts import TEXTS

# vaqtinchalik foydalanuvchi tili saqlash
user_languages = {}

# vaqtinchalik admin id
# shu yerga o'zingning telegram id'ingni yozasan
ADMIN_ID = 7276398332


def get_user_lang(user_id: int) -> str:
    return user_languages.get(user_id, "uz")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_user_lang(user_id)

    await update.message.reply_text(
        TEXTS[lang]["welcome"],
        reply_markup=get_main_keyboard()
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    lang = get_user_lang(user_id)
    text = update.message.text

    if text == "📝 Postlar":
        await update.message.reply_text(TEXTS[lang]["posts"])

    elif text == "📢 Kanallar":
        await update.message.reply_text(TEXTS[lang]["channels"])

    elif text == "ℹ️ About":
        await update.message.reply_text(TEXTS[lang]["about"])

    elif text == "🛠 Xizmatlar":
        await update.message.reply_text(TEXTS[lang]["services"])

    elif text == "🌐 Tillarni tanlash":
        await update.message.reply_text(
            TEXTS[lang]["choose_language"],
            reply_markup=get_language_keyboard()
        )

    elif text == "🇺🇿 O'zbek":
        user_languages[user_id] = "uz"
        await update.message.reply_text(
            TEXTS["uz"]["language_changed_uz"],
            reply_markup=get_main_keyboard()
        )

    elif text == "🇷🇺 Русский":
        user_languages[user_id] = "ru"
        await update.message.reply_text(
            TEXTS["ru"]["language_changed_ru"],
            reply_markup=get_main_keyboard()
        )

    elif text == "🇬🇧 English":
        user_languages[user_id] = "en"
        await update.message.reply_text(
            TEXTS["en"]["language_changed_en"],
            reply_markup=get_main_keyboard()
        )

    elif text == "⭐ Botni baholash":
        context.user_data["waiting_for_rating"] = True
        context.user_data["waiting_for_message"] = False
        await update.message.reply_text(TEXTS[lang]["rate_bot"])

    elif text == "✉️ Menga xabar yuborish":
        context.user_data["waiting_for_message"] = True
        context.user_data["waiting_for_rating"] = False
        await update.message.reply_text(TEXTS[lang]["send_message"])

    elif context.user_data.get("waiting_for_rating"):
        if text.isdigit() and 1 <= int(text) <= 5:
            await update.message.reply_text(f"✅ Rahmat, siz {text} baho berdingiz!")
            context.user_data["waiting_for_rating"] = False
        else:
            await update.message.reply_text("1 dan 5 gacha son yuboring.")

    elif context.user_data.get("waiting_for_message"):
        full_name = update.effective_user.full_name
        username = update.effective_user.username or "username yo'q"

        admin_text = (
            f"📩 Yangi xabar!\n\n"
            f"👤 Ism: {full_name}\n"
            f"🔗 Username: @{username}\n"
            f"🆔 ID: {user_id}\n\n"
            f"✉️ Xabar:\n{text}"
        )

        await context.bot.send_message(chat_id=ADMIN_ID, text=admin_text)
        await update.message.reply_text(TEXTS[lang]["message_sent"])
        context.user_data["waiting_for_message"] = False

    else:
        await update.message.reply_text(TEXTS[lang]["unknown"])