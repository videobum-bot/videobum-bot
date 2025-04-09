import os
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils import executor

API_TOKEN = os.getenv("API_TOKEN")
OWNER_ID = int(os.getenv("OWNER_ID"))

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Главное меню
def main_menu():
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton("📦 Каталог"), KeyboardButton("❓ Частые вопросы"))
    kb.add(KeyboardButton("🛒 Заказ / Консультация"), KeyboardButton("🌐 Перейти на сайт"))
    return kb

@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    text = (
        "Привет 👋\n"
        "Я — виртуальный продавец магазина ВидеоБум 🎥\n"
        "Помогу выбрать товар, расскажу о доставке и приму заказ прямо здесь в Telegram.\n\n"
        "Выберите, что вас интересует 👇"
    )
    await message.answer(text, reply_markup=main_menu())

@dp.message_handler(lambda m: m.text == "📦 Каталог")
async def catalog(message: types.Message):
    text = (
        "Выберите нужный раздел 👇\n\n"
        "📸 Камеры наблюдения\n🔗 https://videobum.shop/ua/g127647150-kameri\n\n"
        "🎥 Автоматика для ворот\n🔗 https://videobum.shop/ua/g127647151-avtomatika-vorit\n\n"
        "💾 Умные Wi-Fi выключатели\n🔗 https://videobum.shop/ua/g127647160-rozumni-vimikachi\n\n"
        "🎯 Всё оборудование\n🔗 https://videobum.shop"
    )
    await message.answer(text)

@dp.message_handler(lambda m: m.text == "❓ Частые вопросы")
async def faq(message: types.Message):
    text = (
        "📦 *Доставка:* по всей Украине, 1–3 рабочих дня\n"
        "💳 *Оплата:* при получении или по предоплате\n"
        "🛠 *Установка:* возможна, уточняйте у менеджера\n"
        "📞 *Поддержка:* бесплатно — поможем с выбором оборудования"
    )
    await message.answer(text, parse_mode="Markdown")

user_data = {}

@dp.message_handler(lambda m: m.text == "🛒 Заказ / Консультация")
async def order_start(message: types.Message):
    await message.answer("1️⃣ Напишите, как вас зовут:")
    user_data[message.chat.id] = {}
    dp.register_message_handler(get_name, content_types=types.ContentTypes.TEXT, state=None)

async def get_name(message: types.Message):
    user_data[message.chat.id]["name"] = message.text
    await message.answer("2️⃣ Укажите номер телефона (Viber/Telegram):")
    dp.register_message_handler(get_phone, content_types=types.ContentTypes.TEXT, state=None)

async def get_phone(message: types.Message):
    user_data[message.chat.id]["phone"] = message.text
    await message.answer("3️⃣ Что вас интересует? Можете отправить ссылку или описать нужное:")
    dp.register_message_handler(get_interest, content_types=types.ContentTypes.TEXT, state=None)

async def get_interest(message: types.Message):
    user_data[message.chat.id]["interest"] = message.text
    data = user_data[message.chat.id]
    username = f"@{message.from_user.username}" if message.from_user.username else f"ID: {message.from_user.id}"

    text = (
        "📥 Новая заявка от клиента:\n\n"
        f"👤 Имя: {data['name']}\n"
        f"📞 Телефон: {data['phone']}\n"
        f"💬 Интересует: {data['interest']}\n"
        f"🔗 Telegram: {username}"
    )
    await bot.send_message(OWNER_ID, text)
    await message.answer("✅ Спасибо! Мы скоро с вами свяжемся.")

@dp.message_handler(lambda m: m.text == "🌐 Перейти на сайт")
async def go_to_site(message: types.Message):
    await message.answer("🔗 Перейдите на наш сайт: https://videobum.shop")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)