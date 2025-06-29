from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_payment_keyboard():
    """Клавіатура способів оплати"""
    keyboard = [
        [
            InlineKeyboardButton(text="💳 LiqPay", callback_data="pay_LiqPay"),
            InlineKeyboardButton(text="💰 WayForPay", callback_data="pay_WayForPay")
        ],
        [
            InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_order")
        ]
    ]
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_order_confirmation_keyboard():
    """Клавіатура підтвердження замовлення"""
    keyboard = [
        [
            InlineKeyboardButton(text="✅ Підтвердити замовлення", callback_data="confirm_order")
        ],
        [
            InlineKeyboardButton(text="✏️ Редагувати", callback_data="edit_order"),
            InlineKeyboardButton(text="❌ Скасувати", callback_data="cancel_order")
        ]
    ]
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)