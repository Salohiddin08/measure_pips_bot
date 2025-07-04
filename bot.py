import asyncio
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, KeyboardButton, ReplyKeyboardMarkup
from aiogram.filters import CommandStart

TOKEN = "7512686350:AAGM5NrtPQXkr_Fqh890o5um32wRWsDSQ18"

bot = Bot(token=TOKEN)
dp = Dispatcher()

# 🔘 Asosiy menyu
main_menu = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="📏 Pips hisoblash")],
        [KeyboardButton(text="💰 Profit hisoblash")],
        [KeyboardButton(text="ℹ️ Bot haqida")]
    ],
    resize_keyboard=True
)

# ⌨️ Foydalanuvchi rejimini saqlovchi
user_mode = {}

@dp.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(
        "Assalomu alaykum, Trader! 👋\n\n"
        "Quyidagi funksiyalardan birini tanlang:",
        reply_markup=main_menu
    )

@dp.message(F.text == "📏 Pips hisoblash")
async def set_pips_mode(message: Message):
    user_mode[message.from_user.id] = "pips"
    await message.answer("✍️ Entry va exit narxlarni yuboring (masalan: `3299.087, 3310.614`):", parse_mode="Markdown")

@dp.message(F.text == "💰 Profit hisoblash")
async def set_profit_mode(message: Message):
    user_mode[message.from_user.id] = "profit"
    await message.answer("✍️ Entry, exit va lot miqdorini yuboring (masalan: `3299.087, 3310.614, 0.1`):", parse_mode="Markdown")

@dp.message(F.text == "ℹ️ Bot haqida")
async def bot_info(message: Message):
    await message.answer(
        "🤖 *Bot haqida:*\n\n"
        "Bu bot sizga quyidagi savdo (trading) hisob-kitoblarida yordam beradi:\n"
        "1️⃣ Pips hisoblash (entry va exit orasidagi farq)\n"
        "2️⃣ Profit hisoblash (pips asosida foyda)\n\n"
        "XAUUSD uchun pip o‘lchami: 0.01\n"
        "0.1 lot = 1 USD/pip\n\n"
        "Dasturchi: @codersdepartament\n",
        parse_mode="Markdown"
    )

@dp.message(F.text)
async def handle_calc(message: Message):
    mode = user_mode.get(message.from_user.id)

    if mode == "pips":
        try:
            entry_str, exit_str = message.text.replace(" ", "").split(",")
            entry = float(entry_str)
            exit = float(exit_str)

            pip_size = 0.01  # XAUUSD uchun
            pips = abs(exit - entry) / pip_size
            pips = round(pips, 1)

            await message.answer(
                f"📊 Pips hisob:\n\n"
                f"🔹 Kirish: `{entry}`\n"
                f"🔹 Chiqish: `{exit}`\n"
                f"🔹 Natija: *{pips} pips*",
                parse_mode="Markdown"
            )

        except:
            await message.answer("❗️Format xato. To‘g‘ri format: `entry, exit`")

    elif mode == "profit":
        try:
            entry_str, exit_str, lot_str = message.text.replace(" ", "").split(",")
            entry = float(entry_str)
            exit = float(exit_str)
            lot = float(lot_str)

            pip_size = 0.01
            pips = abs(exit - entry) / pip_size
            profit_per_pip = 1 * lot / 0.1  # 0.1 lot uchun 1$, 1 lot uchun 10$
            profit = round(pips * profit_per_pip, 2)
            pips = round(pips, 1)

            await message.answer(
                f"💰 Profit hisob:\n\n"
                f"🔹 Kirish: `{entry}`\n"
                f"🔹 Chiqish: `{exit}`\n"
                f"🔹 Lot: `{lot}`\n"
                f"🔹 Pips: *{pips}*\n"
                f"🔹 Foyda: *{profit} USD*",
                parse_mode="Markdown"
            )

        except:
            await message.answer("❗️Format xato. To‘g‘ri format: `entry, exit, lot`")

    else:
        await message.answer("❗️Iltimos, oldin menyudan funksiyani tanlang.")

async def main():
    bot_info = await bot.get_me()
    print("📡 Bot muvaffaqiyatli ishga tushdi!")
    print("🤖 Bot nomi:", bot_info.first_name)
    print("🔗 Username:", f"@{bot_info.username}")
    print("🆔 Telegram ID:", bot_info.id)
    print("🚀 Polling boshlanmoqda...\n")

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
