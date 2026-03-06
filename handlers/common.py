from telegram import Update
from telegram.ext import ContextTypes

from database import add_user, get_user_lang
from keyboards.user_keyboards import get_user_main_keyboard
from texts import TEXTS


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    add_user(
        user_id=user.id,
        full_name=user.full_name,
        username=user.username,
    )

    lang = get_user_lang(user.id)
    context.user_data.clear()

    await update.message.reply_text(
        TEXTS[lang]["welcome"],
        reply_markup=get_user_main_keyboard(lang)
    )