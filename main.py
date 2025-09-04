#!/usr/bin/env python3
"""
CleanWay Telegram Bot - Main Entry Point for Render
"""
import asyncio
import logging
import os
import sys
from pathlib import Path

# Додаємо bot директорію до Python path
bot_dir = Path(__file__).parent / "bot"
sys.path.insert(0, str(bot_dir))

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

# Імпортуємо обробники
from handlers import main_handlers, catalog_handlers, cart_handlers, ai_handlers, order_handlers
from utils.database import init_db

# Завантаження змінних середовища
env_path = bot_dir / ".env"
if env_path.exists():
    load_dotenv(env_path)

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

async def main():
    """Головна функція запуску бота"""
    
    # Отримання токена бота
    bot_token = os.getenv('BOT_TOKEN')
    if not bot_token:
        logger.error("BOT_TOKEN не знайдено в змінних середовища!")
        return
    
    logger.info(f"🤖 Запуск CleanWay бота...")
    logger.info(f"📁 Робоча директорія: {os.getcwd()}")
    logger.info(f"🔧 Bot директорія: {bot_dir}")
    
    # Ініціалізація бота та диспетчера
    bot = Bot(
        token=bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    dp = Dispatcher()
    
    try:
        # Ініціалізація бази даних
        await init_db()
        logger.info("✅ База даних ініціалізована")
        
        # Реєстрація роутерів
        dp.include_router(main_handlers.router)
        dp.include_router(catalog_handlers.router)
        dp.include_router(cart_handlers.router)
        dp.include_router(ai_handlers.router)
        dp.include_router(order_handlers.router)
        
        logger.info("✅ Роутери зареєстровані")
        
        # Перевірка підключення до Telegram
        bot_info = await bot.get_me()
        logger.info(f"✅ Підключено до Telegram як @{bot_info.username}")
        
        logger.info("🚀 CleanWay бот запущено успішно!")
        
        # Запуск бота
        await dp.start_polling(bot)
        
    except Exception as e:
        logger.error(f"❌ Помилка при запуску бота: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await bot.session.close()
        logger.info("🛑 Бот зупинено")

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Бот зупинено користувачем")
    except Exception as e:
        logger.error(f"💥 Критична помилка: {e}")
        import traceback
        traceback.print_exc()