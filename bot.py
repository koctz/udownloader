import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from dotenv import load_dotenv  # Добавь эту строку
from aiogram.utils.keyboard import InlineKeyboardBuilder
from downloader import get_video_info, download_video

# Загрузка конфигов из .env
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
CHANNEL_ID = os.getenv("CHANNEL_ID")
CHANNEL_URL = os.getenv("CHANNEL_URL")

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Проверка подписки
async def check_subscription(user_id):
    try:
        member = await bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status != 'left'
    except Exception:
        return False

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(f"Привет! Чтобы пользоваться ботом, подпишись на канал: {CHANNEL_URL}\n\nЗатем просто пришли мне ссылку на YouTube видео!")

@dp.message()
async def handle_message(message: types.Message):
    if "youtube.com" in message.text or "youtu.be" in message.text:
        await message.answer("Обрабатываю ссылку, подождите...")
        try:
            # ТУТ ДОБАВЛЕН AWAIT
            info = await get_video_info(message.text)
            title = info.get('title', 'Video')
            formats = info.get('formats', [])
            
            # Далее ваш код создания кнопок...
            await message.answer(f"Что скачать из '{title}'?", reply_markup=keyboard)
        except Exception as e:
            await message.answer(f"Ошибка: {e}")

@dp.callback_query(F.data.startswith("dl|"))
async def callbacks_download(callback: types.CallbackQuery):
    _, format_id, url = callback.data.split("|")
    await callback.message.edit_text("🚀 Начинаю загрузку... Это может занять время.")
    
    try:
        file_path = await download_video(url, format_id)
        video = types.FSInputFile(file_path)
        await callback.message.answer_video(video, caption="Ваше видео готово! ✅")
        os.remove(file_path) # Удаляем файл после отправки
        await callback.message.delete()
    except Exception as e:
        await callback.message.answer(f"❌ Ошибка при скачивании: {str(e)}")

async def main():
    print("Бот успешно запущен и готов к работе!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
