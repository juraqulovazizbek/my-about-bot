from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)

from config import Config
from database import init_db
from handlers.common import start
from handlers.user import handle_user_text, handle_user_callback
from handlers.admin import admin_panel, handle_admin_text, handle_admin_media


async def text_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    handled_by_admin = await handle_admin_text(update, context)
    if handled_by_admin:
        return

    await handle_user_text(update, context)


async def media_router(update: Update, context: ContextTypes.DEFAULT_TYPE):
    handled_by_admin = await handle_admin_media(update, context)
    if handled_by_admin:
        return


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    print("Xatolik:", context.error)


def main():
    init_db()

    app = Application.builder().token(Config.TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("admin", admin_panel))
    app.add_handler(CallbackQueryHandler(handle_user_callback))
    app.add_handler(MessageHandler(filters.PHOTO | filters.VIDEO, media_router))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_router))
    app.add_error_handler(error_handler)

    print("Bot ishga tushdi...")
    app.run_polling()


if __name__ == "__main__":
    main()