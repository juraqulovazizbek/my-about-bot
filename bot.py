from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from config import Config
from callbacks import (
    start,
    send_about,
    change_language,
    handle_language,
    sendFeedback,
    send_cart,
    send_partnership_info,
    send_feedback_response5,
    send_feedback_response4,
    send_feedback_response3,
    send_feedback_response2,
    send_feedback_response1,
    send_delivery_terms,
    send_contacts
)

def main():
    application = Application.builder().token(Config.TOKEN).build()

    application.add_handler(CommandHandler("start", start))

    application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'^📥 Savat$'), send_cart))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'^💼 Hamkorlik$'), send_partnership_info))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r"^ℹ️ Ma'lumot$"), send_about))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'^🌐 Tilni tanlash$'), change_language))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'^🏠 Bosh menyu$'), start))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'^✍️ Izoh qoldirish$'), sendFeedback))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'^🚀 Yetkazib berish shartlari$'), send_delivery_terms))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'^☎️ Kontaktlar$'), send_contacts))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'^😊 Menga hamma narsa yoqdi, 5 ❤️$'), send_feedback_response5))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'^☺️ Yaxshi, 4 ⭐️⭐️⭐️⭐️$'), send_feedback_response4))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r"^😐 Qo'niqarli, 3⭐️⭐️⭐️$"), send_feedback_response3))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'^☹️ Yoqmadi, 2 ⭐️⭐️$'), send_feedback_response2))
    application.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'^😤 Men shikoyat qilmoqchiman 👎🏻$'), send_feedback_response1))

    application.add_handler(CallbackQueryHandler(handle_language))

    application.run_polling()

if __name__ == '__main__':
    main()