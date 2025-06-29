import asyncio
import logging
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from handlers import main_handlers, catalog_handlers, cart_handlers, ai_handlers, order_handlers
from utils.database import init_db

# Завантаження змінних середовища
load_dotenv()

# Налаштування логування
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

async def main():
    """Головна функція запуску бота"""
    
    # Отримання токена бота
    bot_token = os.getenv('BOT_TOKEN')
    if not bot_token:
        logger.error("BOT_TOKEN не знайдено в змінних середовища!")
        return
    
    # Ініціалізація бота та диспетчера
    bot = Bot(
        token=bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    dp = Dispatcher()
    
    # Ініціалізація бази даних
    await init_db()
    
    # Реєстрація роутерів
    dp.include_router(main_handlers.router)
    dp.include_router(catalog_handlers.router)
    dp.include_router(cart_handlers.router)
    dp.include_router(ai_handlers.router)
    dp.include_router(order_handlers.router)
    
    logger.info("🤖 CleanWay бот запущено!")
    
    try:
        # Запуск бота
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Помилка при запуску бота: {e}")
    finally:
        await bot.session.close()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот зупинено користувачем")
    except Exception as e:
        logger.error(f"Критична помилка: {e}")