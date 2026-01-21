import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from downloader import get_formats

TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer(f"Привет! Пришли ссылку на YouTube видео, и я скачаю его.")

@dp.message(F.text.contains("youtube.com") | F.text.contains("youtu.be"))
async def process_link(message: types.Message):
    url = message.text
    await message.answer("🔍 Получаю список форматов...")
    
    try:
        title, formats = get_formats(url)
        builder = InlineKeyboardBuilder()
        
        for f in formats:
            builder.button(
                text=f"{f['res']}p ({f['ext']})", 
                callback_data=f"dl_{f['id']}" # В реальном боте тут еще нужен URL
            )
        builder.adjust(2)
        
        await message.answer(f"🎬 {title}\nВыбери качество:", reply_markup=builder.as_markup())
    except Exception as e:
        await message.answer(f"Ошибка: {str(e)}")

async def main():
    print("Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
EOF
