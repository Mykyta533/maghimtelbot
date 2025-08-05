from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from typing import List, Optional


def get_payment_keyboard() -> InlineKeyboardMarkup:
    """Клавіатура способів оплати"""
    keyboard = [
        # Електронні платіжні системи
        [
            InlineKeyboardButton(text="💳 LiqPay", callback_data="pay_liqpay"),
            InlineKeyboardButton(text="💰 WayForPay", callback_data="pay_wayforpay")
        ],
        # Додаткові способи оплати
        [
            InlineKeyboardButton(text="💵 При отриманні", callback_data="pay_cash"),
            InlineKeyboardButton(text="🏦 Переказ на карту", callback_data="pay_card_transfer")
        ],
        # Навігація
        [
    ]
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_order_confirmation_keyboard(payment_method: Optional[str] = None) -> InlineKeyboardMarkup:
    """
    Клавіатура підтвердження замовлення
    :param payment_method: обраний спосіб оплати
    """
    keyboard = [
        # Основна кнопка підтвердження
        [
            InlineKeyboardButton(
                text="✅ Підтвердити замовлення", 
                callback_data=f"confirm_order_{payment_method}" if payment_method else "confirm_order"
            )
        ],
        # Кнопки редагування
        [
            InlineKeyboardButton(text="✏️ Змінити дані", callback_data="edit_order_data"),
            InlineKeyboardButton(text="💳 Змінити оплату", callback_data="change_payment")
        ],
        # Кнопки навігації
        [
            InlineKeyboardButton(text="🔙 Назад до кошика", callback_data="back_to_cart"),
            InlineKeyboardButton(text="❌ Скасувати замовлення", callback_data="cancel_order")
        ]
    ]
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_order_edit_keyboard() -> InlineKeyboardMarkup:
    """Клавіатура для редагування замовлення"""
    keyboard = [
        [
            InlineKeyboardButton(text="📝 Змінити контактні дані", callback_data="edit_contact_info")
        ],
        [
            InlineKeyboardButton(text="🚚 Змінити адресу доставки", callback_data="edit_delivery_address")
        ],
        [
            InlineKeyboardButton(text="⏰ Змінити час доставки", callback_data="edit_delivery_time")
        ],
        [
            InlineKeyboardButton(text="💬 Додати коментар", callback_data="add_order_comment")
        ],
        # Розділювач
        [
            InlineKeyboardButton(text="═════════════", callback_data="separator")
        ],
        [
            InlineKeyboardButton(text="🔙 Назад до підтвердження", callback_data="back_to_confirmation"),
            InlineKeyboardButton(text="❌ Скасувати", callback_data="cancel_order")
        ]
    ]
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_payment_method_keyboard(current_method: str) -> InlineKeyboardMarkup:
    """
    Клавіатура для зміни способу оплати
    :param current_method: поточний спосіб оплати
    """
    keyboard = []
    
    # Заголовок
    keyboard.append([
        InlineKeyboardButton(text=f"Поточний: {get_payment_name(current_method)}", callback_data="current_payment")
    ])
    
    # Розділювач
    keyboard.append([
        InlineKeyboardButton(text="═════════════", callback_data="separator")
    ])
    
    # Всі доступні способи оплати (крім поточного)
    payment_methods = [
        ("pay_liqpay", "💳 LiqPay"),
        ("pay_wayforpay", "💰 WayForPay"),
        ("pay_cash", "💵 При отриманні"),
        ("pay_card_transfer", "🏦 Переказ на карту")
    ]
    
    for method_code, method_name in payment_methods:
        if method_code != current_method:
            keyboard.append([
                InlineKeyboardButton(text=method_name, callback_data=method_code)
            ])
    
    # Навігація
    keyboard.extend([
        [
            InlineKeyboardButton(text="🔙 Назад до підтвердження", callback_data="back_to_confirmation")
        ]
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_order_cancel_confirmation_keyboard() -> InlineKeyboardMarkup:
    """Клавіатура підтвердження скасування замовлення"""
    keyboard = [
        [
            InlineKeyboardButton(text="⚠️ Ви впевнені?", callback_data="cancel_warning")
        ],
        [
            InlineKeyboardButton(text="✅ Так, скасувати", callback_data="confirm_cancel_order"),
            InlineKeyboardButton(text="❌ Ні, повернутися", callback_data="back_to_confirmation")
        ]
    ]
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_order_success_keyboard(order_id: str) -> InlineKeyboardMarkup:
    """
    Клавіатура після успішного оформлення замовлення
    :param order_id: номер замовлення
    """
    keyboard = [
        [
            InlineKeyboardButton(text=f"📄 Деталі замовлення #{order_id}", callback_data=f"order_details_{order_id}")
        ],
        [
            InlineKeyboardButton(text="🛍 Нове замовлення", callback_data="show_catalog"),
            InlineKeyboardButton(text="📞 Зв'язатися з нами", callback_data="contact_support")
        ],
        [
            InlineKeyboardButton(text="🏠 Головне меню", callback_data="back_to_menu")
        ]
    ]
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_payment_processing_keyboard(payment_url: Optional[str] = None) -> InlineKeyboardMarkup:
    """
    Клавіатура під час обробки платежу
    :param payment_url: посилання для оплати (якщо є)
    """
    keyboard = []
    
    if payment_url:
        keyboard.append([
            InlineKeyboardButton(text="💳 Перейти до оплати", url=payment_url)
        ])
        keyboard.append([
            InlineKeyboardButton(text="🔄 Перевірити статус", callback_data="check_payment_status")
        ])
    
    keyboard.extend([
        [
            InlineKeyboardButton(text="❓ Проблеми з оплатою?", callback_data="payment_help")
        ],
        [
            InlineKeyboardButton(text="🔙 Повернутися", callback_data="back_to_confirmation"),
            InlineKeyboardButton(text="❌ Скасувати", callback_data="cancel_order")
        ]
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_contact_edit_keyboard() -> InlineKeyboardMarkup:
    """Клавіатура для редагування контактних даних"""
    keyboard = [
        [
            InlineKeyboardButton(text="📱 Змінити телефон", callback_data="edit_phone")
        ],
        [
            InlineKeyboardButton(text="👤 Змінити ім'я", callback_data="edit_name")
        ],
        [
            InlineKeyboardButton(text="📧 Змінити email", callback_data="edit_email")
        ],
        [
            InlineKeyboardButton(text="🔙 Назад", callback_data="edit_order_data")
        ]
    ]
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_payment_name(payment_method: str) -> str:
    """Отримання читабельної назви способу оплати"""
    payment_names = {
        "pay_liqpay": "💳 LiqPay",
        "pay_wayforpay": "💰 WayForPay", 
        "pay_cash": "💵 При отриманні",
        "pay_card_transfer": "🏦 Переказ на карту"
    }
    return payment_names.get(payment_method, "Невідомий спосіб")


# Функції для швидкого створення простих клавіатур
def get_back_button(callback_data: str = "back") -> InlineKeyboardMarkup:
    """Проста клавіатура з кнопкою назад"""
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="🔙 Назад", callback_data=callback_data)
    ]])


def get_continue_button(callback_data: str = "continue") -> InlineKeyboardMarkup:
    """Проста клавіатура з кнопкою продовжити"""
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="➡️ Продовжити", callback_data=callback_data)
    ]])
