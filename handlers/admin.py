from telegram import Update
from telegram.ext import ContextTypes

from filters import is_admin
from database import (
    add_post,
    get_all_posts,
    delete_post,
    add_channel,
    get_all_channels,
    delete_channel,
    add_service,
    get_all_services,
    delete_service,
    update_setting,
    get_user_count,
    get_rating_stats,
)
from keyboards.admin_keyboards import get_admin_keyboard
from keyboards.user_keyboards import get_user_main_keyboard


async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not is_admin(user_id):
        await update.message.reply_text("⛔ Sizda admin huquqi yo‘q.")
        return

    context.user_data.clear()

    await update.message.reply_text(
        "🛠 Admin panelga xush kelibsiz.",
        reply_markup=get_admin_keyboard()
    )


async def handle_admin_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    text = update.message.text.strip()

    if not is_admin(user_id):
        return False

    state = context.user_data.get("admin_state")

    if text == "🏠 User menyu":
        context.user_data.clear()
        await update.message.reply_text(
            "🏠 User menyuga qaytdingiz.",
            reply_markup=get_user_main_keyboard("uz")
        )
        return True

    if text == "➕ Post qo‘shish":
        context.user_data.clear()
        context.user_data["admin_state"] = "add_post_title"
        await update.message.reply_text("📝 Post sarlavhasini yuboring:")
        return True

    if state == "add_post_title":
        context.user_data["new_post_title"] = text
        context.user_data["admin_state"] = "add_post_body"
        await update.message.reply_text("✍️ Endi post matnini yuboring:")
        return True

    if state == "add_post_body":
        context.user_data["new_post_body"] = text
        context.user_data["admin_state"] = "add_post_media"
        await update.message.reply_text(
            "🖼 Endi post uchun rasm yoki video yuboring.\n"
            "Agar media kerak bo‘lmasa, 'skip' deb yozing."
        )
        return True

    if state == "add_post_media" and text.lower() == "skip":
        add_post(
            context.user_data["new_post_title"],
            context.user_data["new_post_body"],
            None,
            None
        )
        context.user_data.clear()
        await update.message.reply_text(
            "✅ Post muvaffaqiyatli qo‘shildi.",
            reply_markup=get_admin_keyboard()
        )
        return True

    if text == "🗑 Post o‘chirish":
        posts = get_all_posts()

        if not posts:
            await update.message.reply_text("📰 O‘chirish uchun post yo‘q.")
            return True

        lines = ["🗑 O‘chirish uchun post ID sini yuboring:\n"]
        for post in posts:
            lines.append(f"{post['id']}. {post['title']}")

        context.user_data.clear()
        context.user_data["admin_state"] = "delete_post"
        await update.message.reply_text("\n".join(lines))
        return True

    if state == "delete_post":
        if not text.isdigit():
            await update.message.reply_text("❗ Iltimos, post ID ni raqamda yuboring.")
            return True

        success = delete_post(int(text))
        context.user_data.clear()

        if success:
            await update.message.reply_text(
                "✅ Post o‘chirildi.",
                reply_markup=get_admin_keyboard()
            )
        else:
            await update.message.reply_text(
                "❌ Post topilmadi.",
                reply_markup=get_admin_keyboard()
            )
        return True

    if text == "➕ Kanal qo‘shish":
        context.user_data.clear()
        context.user_data["admin_state"] = "add_channel_name"
        await update.message.reply_text("📢 Kanal nomini yuboring:")
        return True

    if state == "add_channel_name":
        context.user_data["new_channel_name"] = text
        context.user_data["admin_state"] = "add_channel_url"
        await update.message.reply_text(
            "🔗 Endi kanal linkini yuboring:\n"
            "Masalan:\nhttps://t.me/username\n"
            "yoki\n@username"
        )
        return True

    if state == "add_channel_url":
        add_channel(context.user_data["new_channel_name"], text)
        context.user_data.clear()

        await update.message.reply_text(
            "✅ Kanal qo‘shildi.",
            reply_markup=get_admin_keyboard()
        )
        return True

    if text == "🗑 Kanal o‘chirish":
        channels = get_all_channels()

        if not channels:
            await update.message.reply_text("📢 O‘chirish uchun kanal yo‘q.")
            return True

        lines = ["🗑 O‘chirish uchun kanal ID sini yuboring:\n"]
        for channel in channels:
            lines.append(f"{channel['id']}. {channel['name']}")

        context.user_data.clear()
        context.user_data["admin_state"] = "delete_channel"
        await update.message.reply_text("\n".join(lines))
        return True

    if state == "delete_channel":
        if not text.isdigit():
            await update.message.reply_text("❗ Iltimos, kanal ID ni raqamda yuboring.")
            return True

        success = delete_channel(int(text))
        context.user_data.clear()

        if success:
            await update.message.reply_text(
                "✅ Kanal o‘chirildi.",
                reply_markup=get_admin_keyboard()
            )
        else:
            await update.message.reply_text(
                "❌ Kanal topilmadi.",
                reply_markup=get_admin_keyboard()
            )
        return True

    if text == "➕ Xizmat qo‘shish":
        context.user_data.clear()
        context.user_data["admin_state"] = "add_service_title"
        await update.message.reply_text("🛠 Xizmat nomini yuboring:")
        return True

    if state == "add_service_title":
        context.user_data["new_service_title"] = text
        context.user_data["admin_state"] = "add_service_body"
        await update.message.reply_text("✍️ Xizmat tavsifini yuboring:")
        return True

    if state == "add_service_body":
        add_service(context.user_data["new_service_title"], text)
        context.user_data.clear()

        await update.message.reply_text(
            "✅ Xizmat qo‘shildi.",
            reply_markup=get_admin_keyboard()
        )
        return True

    if text == "🗑 Xizmat o‘chirish":
        services = get_all_services()

        if not services:
            await update.message.reply_text("🛠 O‘chirish uchun xizmat yo‘q.")
            return True

        lines = ["🗑 O‘chirish uchun xizmat ID sini yuboring:\n"]
        for service in services:
            lines.append(f"{service['id']}. {service['title']}")

        context.user_data.clear()
        context.user_data["admin_state"] = "delete_service"
        await update.message.reply_text("\n".join(lines))
        return True

    if state == "delete_service":
        if not text.isdigit():
            await update.message.reply_text("❗ Iltimos, xizmat ID ni raqamda yuboring.")
            return True

        success = delete_service(int(text))
        context.user_data.clear()

        if success:
            await update.message.reply_text(
                "✅ Xizmat o‘chirildi.",
                reply_markup=get_admin_keyboard()
            )
        else:
            await update.message.reply_text(
                "❌ Xizmat topilmadi.",
                reply_markup=get_admin_keyboard()
            )
        return True

    if text == "✏️ About ni o‘zgartirish":
        context.user_data.clear()
        context.user_data["admin_state"] = "update_about"
        await update.message.reply_text("👤 Yangi about matnini yuboring:")
        return True

    if state == "update_about":
        update_setting("about_text", text)
        context.user_data.clear()

        await update.message.reply_text(
            "✅ About matni yangilandi.",
            reply_markup=get_admin_keyboard()
        )
        return True

    if text == "📸 Instagramni o‘zgartirish":
        context.user_data.clear()
        context.user_data["admin_state"] = "update_instagram"
        await update.message.reply_text(
            "📸 Instagram linkini yuboring.\nMasalan:\nhttps://instagram.com/username"
        )
        return True

    if state == "update_instagram":
        update_setting("instagram_url", text.strip())
        context.user_data.clear()

        await update.message.reply_text(
            "✅ Instagram link yangilandi.",
            reply_markup=get_admin_keyboard()
        )
        return True

    if text == "📊 Statistika":
        user_count = get_user_count()
        stats = get_rating_stats()

        lines = [
            "📊 Statistika",
            f"👥 Foydalanuvchilar soni: {user_count}",
            "",
            "⭐ Baholar:"
        ]

        if stats:
            for item in stats:
                lines.append(f"{item['rating']} baho — {item['total']} ta")
        else:
            lines.append("Hozircha baholar yo‘q.")

        await update.message.reply_text(
            "\n".join(lines),
            reply_markup=get_admin_keyboard()
        )
        return True

    return False


async def handle_admin_media(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id

    if not is_admin(user_id):
        return False

    state = context.user_data.get("admin_state")

    if state != "add_post_media":
        return False

    title = context.user_data.get("new_post_title")
    body = context.user_data.get("new_post_body")

    if update.message.photo:
        file_id = update.message.photo[-1].file_id
        add_post(title, body, "photo", file_id)
    elif update.message.video:
        file_id = update.message.video.file_id
        add_post(title, body, "video", file_id)
    else:
        await update.message.reply_text("❗ Rasm, video yoki 'skip' yuboring.")
        return True

    context.user_data.clear()
    await update.message.reply_text(
        "✅ Media bilan post qo‘shildi.",
        reply_markup=get_admin_keyboard()
    )
    return True