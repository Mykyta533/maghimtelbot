from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def get_main_menu():
    """Головне меню бота (Reply клавіатура)"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="🧼 Каталог"),
                KeyboardButton(text="🎁 Акції")
            ],
            [
                KeyboardButton(text="🛒 Кошик"),
                KeyboardButton(text="👤 Моє")
            ],
            [
                KeyboardButton(text="🤖 AI-помічник"),
                KeyboardButton(text="💳 QR карта")
            ],
            [
                KeyboardButton(text="🧮 Мої чеки"),
                KeyboardButton(text="🧧 Відмова від паперового чека")
            ],
            [
                KeyboardButton(text="📞 Контакти")
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard


def get_back_to_menu_keyboard():
    """Кнопка повернення в меню (Reply клавіатура)"""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🔙 Повернутися в меню")]
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
    return keyboard


# ДОДАЙТЕ ЦІ НОВІ ФУНКЦІЇ:

def get_back_to_menu_inline():
    """Кнопка повернення в меню (Inline клавіатура)"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔙 Повернутися в меню", callback_data="back_to_menu")]
        ]
    )
    return keyboard


def get_main_menu_inline():
    """Головне меню бота (Inline клавіатура)"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🧼 Каталог", callback_data="show_catalog"),
                InlineKeyboardButton(text="🎁 Акції", callback_data="show_promotions")
            ],
            [
                InlineKeyboardButton(text="🛒 Кошик", callback_data="show_cart"),
                InlineKeyboardButton(text="🧾 Замовити", callback_data="quick_order")
            ],
            [
                InlineKeyboardButton(text="🤖 AI-помічник", callback_data="ai_assistant")
            ],
            [
                InlineKeyboardButton(text="🧮 Мої чеки", callback_data="my_receipts"),
                InlineKeyboardButton(text="📍 Адреса", callback_data="store_address")
            ],
            [
                InlineKeyboardButton(text="📞 Зв'язатися", callback_data="contact_us")
            ]
        ]
    )
    return keyboard


def get_catalog_inline():
    """Inline клавіатура каталогу"""
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🧼 Миючі засоби", callback_data="category_cleaning"),
                InlineKeyboardButton(text="🧴 Косметика", callback_data="category_cosmetics")
            ],
            [
                InlineKeyboardButton(text="🍭 Солодощі", callback_data="category_sweets"),
                InlineKeyboardButton(text="🥤 Напої", callback_data="category_drinks")
            ],
            [
                InlineKeyboardButton(text="🍞 Хліб", callback_data="category_bread"),
                InlineKeyboardButton(text="🥛 Молочні", callback_data="category_dairy")
            ],
            [
                InlineKeyboardButton(text="🔙 Назад в меню", callback_data="back_to_menu")
            ]
        ]
    )
    return keyboard
