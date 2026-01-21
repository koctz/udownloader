import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
from downloader import get_video_info, download_video
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start(message: types.Message):
    await message.answer("Привет! Пришли мне ссылку на YouTube видео, и я помогу его скачать.")

@dp.message(F.text.contains("youtube.com") | F.text.contains("youtu.be"))
async def handle_url(message: types.Message):
    url = message.text
    await message.answer("🔍 Получаю информацию о видео...")
    
    try:
        info = await get_video_info(url)
        title = info.get('title', 'Видео')
        
        # Собираем кнопки для выбора качества (только видео с аудио)
        builder = InlineKeyboardBuilder()
        
        # Берем несколько популярных форматов
        formats = [f for f in info.get('formats', []) if f.get('vcodec') != 'none' and f.get('acodec') != 'none']
        
        for f in formats[:5]: # Ограничим до 5 кнопок
            res = f.get('height', 'unknown')
            ext = f.get('ext', 'mp4')
            f_id = f.get('format_id')
            builder.button(
                text=f"{res}p .{ext}", 
                callback_data=f"dl|{f_id}|{url}"
            )
        
        builder.adjust(2)
        await message.answer(f"🎬 {title}\n\nВыберите качество:", reply_markup=builder.as_markup())
        
    except Exception as e:
        await message.answer(f"❌ Ошибка при получении инфо: {e}")

@dp.callback_query(F.data.startswith("dl|"))
async def process_download(callback: types.Callback_query):
    _, format_id, url = callback.data.split("|")
    await callback.message.edit_text("⏳ Начинаю скачивание... это может занять время.")
    
    try:
        file_path = await download_video(url, format_id)
        
        if os.path.exists(file_path):
            await callback.message.answer("✅ Скачивание завершено! Отправляю файл...")
            video_file = types.FSInputFile(file_path)
            await bot.send_video(callback.message.chat.id, video_file)
            # Опционально: удалить файл после отправки
            # os.remove(file_path)
        else:
            await callback.message.answer("❌ Файл не найден после скачивания.")
            
    except Exception as e:
        await callback.message.answer(f"❌ Ошибка при скачивании: {e}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
