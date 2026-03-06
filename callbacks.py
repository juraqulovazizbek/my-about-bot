from telegram import (
    Update,
    ReplyKeyboardMarkup,
    KeyboardButton,
    WebAppInfo,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)
from telegram.ext import ContextTypes

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        text=(
            f"Assalomu Alaykum, ⚡!\n\n"
            "Ijodimizga qiziqish bildirganingiz uchun tashakkur!\n\n"
            "Hozircha siz uchun futbolka, xudi, svitshot, kepka va stikerlar mavjud. "
            "Yaqin orada tanlovni kengaytiramiz. Aytganday, istalgan turdagi kiyim buyurtma qilganlarga "
            "qo‘shimcha ravishda stikerpak sovg‘a qilinadi :)\n\n"
            "Toshkent bo‘yicha yetkazib berish: 1–3 ish kuni\n"
            "O‘zbekiston bo‘yicha yetkazib berish: 3–7 ish kuni\n"
            "O‘zbekiston bo‘yicha jo‘natmalar seshanba va juma kunlari amalga oshiriladi\n\n"
            "450 000 so‘mdan ortiq buyurtmalarni yetkazib berish tekin!\n\n"
            f"Agar bu shartlar sizni qoniqtirsa, “🔥 Mahsulotlar” bo‘limiga o‘tish orqali "
            f"buyurtma berishni boshlashingiz mumkin, {update.message.from_user.first_name}!"
        ),
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [
                    KeyboardButton(
                        text="🔥 Mahsulotlar",
                        web_app=WebAppInfo(url='https://uzum.uz')
                    ),
                    KeyboardButton(text='📥 Savat')
                ],
                [
                    KeyboardButton(text='💼 Hamkorlik'),
                    KeyboardButton(text="ℹ️ Ma'lumot")
                ],
                [
                    KeyboardButton(text="🌐 Tilni tanlash"),
                ]
            ],
            resize_keyboard=True,
        )
    )

async def send_partnership_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Biz sizning kompaniyangiz bilan hamkorlik qilishdan mamnunmiz "
        "va sizning buyurtmangizga asosan futbolkalar, xudi, svitshot va boshqa "
        "ko'p narsalarni tayyorlashimiz mumkin.\n\n"
        "Menejer bilan bog'lanish uchun: @tirik_chilik"
    )

async def send_cart(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Sizning savatingiz bo'sh")

async def send_about(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        text="Kerakli bo'limni tanlang ⬇",
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="✍️ Izoh qoldirish")],
                [
                    KeyboardButton(text="🚀 Yetkazib berish shartlari"),
                    KeyboardButton(text="☎️ Kontaktlar")
                ],
                [KeyboardButton(text='🏠 Bosh menyu')],
            ],
            resize_keyboard=True
        )
    )

async def sendFeedback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        text=(
            "✅ Tirikchilik loyihasini tanlaganingiz uchun rahmat.\n\n"
            "Bizning xizmatlarimiz sifatini yaxshilashga yordam bersangiz juda xursand bo’lar edik :)\n\n"
            "Buning uchun 5 ballik tizim asosida bizni baholang yoki o'z tilaklaringizni yozib jo'nating."
        ),
        reply_markup=ReplyKeyboardMarkup(
            keyboard=[
                [KeyboardButton(text="😊 Menga hamma narsa yoqdi, 5 ❤️")],
                [KeyboardButton(text="☺️ Yaxshi, 4 ⭐️⭐️⭐️⭐️")],
                [KeyboardButton(text="😐 Qo'niqarli, 3⭐️⭐️⭐️")],
                [KeyboardButton(text="☹️ Yoqmadi, 2 ⭐️⭐️")],
                [KeyboardButton(text="😤 Men shikoyat qilmoqchiman 👎🏻")],
                [KeyboardButton(text="🏠 Bosh menyu")]
            ],
            resize_keyboard=True
        )
    )

async def send_feedback_response5(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Mamnun qolganingizdan xursandmiz 😊. Siz va yaqinlaringizni har doim xursand qilishga harakat qilamiz 🤗")

async def send_feedback_response4(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Sizga yoqqanidan xursandmiz 😊. Bot ishlashini yaxshilash uchun qanday maslahatlaringiz bor?👇🏻")

async def send_feedback_response3(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Botimiz sizni qoniqtirmaganidan afsusdamiz 😔.\nBizni yaxshilashga yordam bering,\nsharh va takliflaringizni qoldiring👇🏻.\nYaxshilashga harakat qilamiz🙏🏻.")

async def send_feedback_response2(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Botimiz sizni qoniqtirmaganidan afsusdamiz 😔. Bizni yaxshilashga yordam bering, sharh va takliflaringizni qoldiring👇🏻. Yaxshilashga harakat qilamiz🙏🏻.")

async def send_feedback_response1(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Botimiz sizni qoniqtirmaganidan afsusdamiz 😔. Bizni yaxshilashga yordam bering, sharh va takliflaringizni qoldiring👇🏻. Yaxshilashga harakat qilamiz🙏🏻.")

async def send_contacts(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Teskari aloqa uchun:\n@tirik_chilik")

async def send_delivery_terms(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Yetkazib berish shartlari:\n"
        "Toshkent bo‘yicha yetkazib berish: 1–3 ish kuni\n"
        "O‘zbekiston bo‘yicha yetkazib berish: 3–7 ish kuni\n"
        "O‘zbekiston bo‘yicha jo‘natmalar seshanba va juma kunlari amalga oshiriladi\n\n"
        "Toshkent bo'ylab yetkazib berish - 30 000 so'm.\n"
        "O‘zbekiston bo'ylab yetkazib berish - 40 000 so‘m.\n\n"
        "450 000 so'mdan ortiq buyurtmalarni yetkazib berish - tekin!"
    )

async def change_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        text="Iltimos, tilni tanlang\nПожалуйста, выберите язык ⬇️",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[
                [InlineKeyboardButton(text='🇷🇺 Русский', callback_data='lang_ru')],
                [InlineKeyboardButton(text="🇺🇿 O'zbekcha", callback_data='lang_uz')]
            ]
        )
    )

async def handle_language(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    await query.answer()

    if query.data == "lang_ru":
        await query.message.reply_text("Русский язык выбран 🇷🇺")
    elif query.data == "lang_uz":
        await query.message.reply_text("O'zbek tili tanlandi 🇺🇿")