from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

def get_main_menu():
    """Головне меню бота"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🧼 Каталог"),
                KeyboardButton(text="🎁 Акції")
            ],
            [
                KeyboardButton(text="🛒 Кошик"),
                KeyboardButton(text="🧾 Замовити")
            ],
            [
                KeyboardButton(text="🤖 AI-помічник (текстовий)"),
                KeyboardButton(text="🎙 AI-помічник (голосовий)")
            ],
            [
                KeyboardButton(text="🧮 Мої чеки"),
                KeyboardButton(text="🧧 Відмова від паперового чека")
            ],
            [
                KeyboardButton(text="📍 Адреса магазину"),
                KeyboardButton(text="📞 Зв'язатися")
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard

def get_back_to_menu_keyboard():
    """Кнопка повернення в меню"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔙 Повернутися в меню")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard