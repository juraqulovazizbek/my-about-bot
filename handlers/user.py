from telegram import Update
from telegram.ext import ContextTypes

from config import Config
from database import (
    get_last_posts,
    get_all_posts,
    get_post,
    get_all_channels,
    get_all_services,
    get_setting,
    add_rating,
    add_message,
    get_user_lang,
    update_user_lang,
)
from keyboards.user_keyboards import (
    get_all_posts_button,
    get_posts_keyboard,
    get_channels_keyboard,
    get_rating_reply_keyboard,
    get_user_main_keyboard,
    get_back_keyboard,
    get_language_keyboard,
)
from texts import TEXTS


def t(user_id: int):
    lang = get_user_lang(user_id)
    return TEXTS.get(lang, TEXTS["uz"]), lang


def rating_text(lang: str, rating: int) -> str:
    return TEXTS[lang][f"rating_{rating}"]


def format_post_preview(post) -> str:
    return (
        "📰 <b>POST</b>\n\n"
        "━━━━━━━━━━\n"
        f"<b>📌 Nomi:</b>\n{post['title']}\n\n"
        f"<b>📝 Tavsif:</b>\n{post['body']}\n"
        "━━━━━━━━━━"
    )


def format_about(title: str, text: str, instagram_url: str, instagram_label: str) -> str:
    result = (
        f"{title}\n\n"
        "━━━━━━━━━━\n"
        f"{text}\n"
    )

    if instagram_url and instagram_url.strip():
        result += f"\n<b>{instagram_label}:</b>\n{instagram_url}\n"

    result += "━━━━━━━━━━"
    return result


def format_service(service) -> str:
    return (
        "🛠 <b>XIZMAT</b>\n\n"
        "━━━━━━━━━━\n"
        f"<b>📌 Nomi:</b>\n{service['title']}\n\n"
        f"<b>📝 Tavsif:</b>\n{service['body']}\n"
        "━━━━━━━━━━"
    )


async def send_post_item(target_message, context, post):
    caption = format_post_preview(post)

    if post["media_type"] == "photo" and post["file_id"]:
        await context.bot.send_photo(
            chat_id=target_message.chat_id,
            photo=post["file_id"],
            caption=caption,
            parse_mode="HTML"
        )
    elif post["media_type"] == "video" and post["file_id"]:
        await context.bot.send_video(
            chat_id=target_message.chat_id,
            video=post["file_id"],
            caption=caption,
            parse_mode="HTML"
        )
    else:
        await context.bot.send_message(
            chat_id=target_message.chat_id,
            text=caption,
            parse_mode="HTML"
        )


async def handle_user_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text
    tr, lang = t(user.id)

    if context.user_data.get("waiting_for_contact_message"):
        if text == tr["back"]:
            context.user_data["waiting_for_contact_message"] = False
            await update.message.reply_text(
                tr["cancelled"],
                reply_markup=get_user_main_keyboard(lang)
            )
            return

        msg = text.strip()

        add_message(
            user_id=user.id,
            full_name=user.full_name,
            username=user.username,
            message=msg,
        )

        username_text = f"@{user.username}" if user.username else "yo‘q"

        admin_text = (
            "📩 <b>Yangi murojaat</b>\n\n"
            f"<b>👤 Ism:</b> {user.full_name}\n"
            f"<b>🔗 Username:</b> {username_text}\n"
            f"<b>🆔 ID:</b> {user.id}\n\n"
            f"<b>💬 Xabar:</b>\n{msg}"
        )

        for admin_id in Config.ADMIN_IDS:
            try:
                await context.bot.send_message(
                    chat_id=admin_id,
                    text=admin_text,
                    parse_mode="HTML"
                )
            except Exception:
                pass

        context.user_data["waiting_for_contact_message"] = False
        await update.message.reply_text(
            tr["contact_sent"],
            reply_markup=get_user_main_keyboard(lang)
        )
        return

    if context.user_data.get("waiting_for_rating"):
        if text == tr["back"]:
            context.user_data["waiting_for_rating"] = False
            await update.message.reply_text(
                tr["cancelled"],
                reply_markup=get_user_main_keyboard(lang)
            )
            return

        rating_map = {
            "⭐ 1": 1,
            "⭐ 2": 2,
            "⭐ 3": 3,
            "⭐ 4": 4,
            "⭐ 5": 5,
        }

        if text in rating_map:
            rating = rating_map[text]
            add_rating(user.id, rating)
            context.user_data["waiting_for_rating"] = False

            await update.message.reply_text(
                rating_text(lang, rating),
                reply_markup=get_user_main_keyboard(lang)
            )
            return

        await update.message.reply_text(tr["invalid_rating"])
        return

    if text == tr["menu_posts"]:
        posts = get_last_posts(3)

        if not posts:
            await update.message.reply_text(tr["no_posts"])
            return

        await update.message.reply_text(
            tr["last_posts"],
            parse_mode="HTML"
        )

        for post in posts:
            await send_post_item(update.message, context, post)

        await update.message.reply_text(
             "📚 Barcha postlarni ko‘rish uchun tugmani bosing.",
         reply_markup=get_all_posts_button(lang)
        )
    elif text == tr["menu_channels"]:
        channels = get_all_channels()
        instagram_url = get_setting("instagram_url", "")

        if not channels and not instagram_url:
            await update.message.reply_text(tr["no_channels"])
            return

        await update.message.reply_text(
            tr["channels_title"],
            parse_mode="HTML",
            reply_markup=get_channels_keyboard(
                channels,
                instagram_url,
                tr["instagram_label"]
            )
        )

    elif text == tr["menu_about"]:
        about_text = get_setting("about_text", tr["no_about"])
        instagram_url = get_setting("instagram_url", "")

        await update.message.reply_text(
            format_about(
                tr["about_title"],
                about_text,
                instagram_url,
                tr["instagram_label"]
            ),
            parse_mode="HTML"
        )

    elif text == tr["menu_services"]:
        services = get_all_services()

        if not services:
            await update.message.reply_text(tr["no_services"])
            return

        await update.message.reply_text(tr["services_title"], parse_mode="HTML")

        for service in services:
            await update.message.reply_text(
                format_service(service),
                parse_mode="HTML"
            )

    elif text == tr["menu_rating"]:
        context.user_data["waiting_for_rating"] = True
        await update.message.reply_text(
            tr["choose_rating"],
            reply_markup=get_rating_reply_keyboard(lang)
        )

    elif text == tr["menu_contact"]:
        context.user_data["waiting_for_contact_message"] = True
        await update.message.reply_text(
            tr["contact_prompt"],
            reply_markup=get_back_keyboard(lang)
        )

    elif text == tr["menu_language"]:
        await update.message.reply_text(
            tr["choose_language"],
            reply_markup=get_language_keyboard()
        )

    else:
        await update.message.reply_text(tr["choose_menu"])


async def handle_user_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    user_id = query.from_user.id
    tr, lang = t(user_id)
    data = query.data

    if data == "all_posts":
        posts = get_all_posts()

        if not posts:
            await query.message.reply_text(tr["no_posts"])
            return

        await query.message.reply_text(
            tr["all_posts"],
            parse_mode="HTML",
            reply_markup=get_posts_keyboard(posts)
        )

    elif data.startswith("post_"):
        post_id = int(data.split("_")[1])
        post = get_post(post_id)

        if not post:
            await query.message.reply_text(tr["post_not_found"])
            return

        await send_post_item(query.message, context, post)

    elif data.startswith("lang_"):
        new_lang = data.split("_")[1]
        update_user_lang(user_id, new_lang)
        tr = TEXTS[new_lang]

        if new_lang == "uz":
            msg = tr["language_changed_uz"]
        elif new_lang == "ru":
            msg = tr["language_changed_ru"]
        else:
            msg = tr["language_changed_en"]

        await query.message.reply_text(
            msg,
            reply_markup=get_user_main_keyboard(new_lang)
        )