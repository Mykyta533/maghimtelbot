from typing import List, Dict
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_cart_keyboard(cart_items: List[Dict]) -> InlineKeyboardMarkup:
    """
    Клавіатура для кошика
    
    :param cart_items: список товарів у кошику, кожен елемент - словник з 'product_id' та 'quantity'
    :return: InlineKeyboardMarkup з кнопками для керування кошиком
    """
    keyboard = []
    
    # Кнопки для кожного товару в кошику: - | кількість | + | видалити
    for item in cart_items:
        product_id = item['product_id']
        quantity = item['quantity']
        
        keyboard.append([
            InlineKeyboardButton(text="➖", callback_data=f"cart_decrease_{product_id}"),
            InlineKeyboardButton(text=f"{quantity}", callback_data=f"cart_quantity_{product_id}"),
            InlineKeyboardButton(text="➕", callback_data=f"cart_increase_{product_id}"),
            InlineKeyboardButton(text="🗑", callback_data=f"cart_remove_{product_id}")
        ])
    
    # Кнопка оформлення замовлення
    keyboard.append([
        InlineKeyboardButton(text="🧾 Оформити замовлення", callback_data="checkout")
    ])
    
    # Кнопка очищення кошика
    keyboard.append([
        InlineKeyboardButton(text="🗑 Очистити кошик", callback_data="clear_cart")
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_checkout_keyboard() -> InlineKeyboardMarkup:
    """
    Клавіатура для вибору способу оплати
    
    :return: InlineKeyboardMarkup з кнопками оплати і повернення до кошика
    """
    keyboard = [
        [
            InlineKeyboardButton(text="💳 LiqPay", callback_data="pay_liqpay"),
            InlineKeyboardButton(text="💰 WayForPay", callback_data="pay_wayforpay")
        ],
        [
            InlineKeyboardButton(text="🔙 Назад до кошика", callback_data="back_to_cart")
        ]
    ]
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
