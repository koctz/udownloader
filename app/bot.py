import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
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

@dp.message(F.text.contains("youtube.com") | F.text.contains("youtu.be"))
async def handle_link(message: types.Message):
    if not await check_subscription(message.from_user.id):
        return await message.answer(f"❌ Ошибка! Сначала подпишитесь на канал: {CHANNEL_URL}")

    wait_msg = await message.answer("⏳ Анализирую видео, подождите...")
    
    try:
        title, formats = get_video_info(message.text)
        builder = InlineKeyboardBuilder()
        
        # Создаем кнопки качества (ограничим 6-ю самыми популярными)
        for f in formats[:6]:
            builder.button(
                text=f"{f['res']}p ({f['ext']})", 
                callback_data=f"dl|{f['id']}|{message.text}"
            )
        builder.adjust(2)
        
        await wait_msg.delete()
        await message.answer(f"🎬 <b>{title}</b>\n\nВыбери желаемое качество:", 
                           reply_markup=builder.as_markup(), parse_mode="HTML")
    except Exception as e:
        await message.answer(f"❌ Произошла ошибка: {str(e)}")

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
