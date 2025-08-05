from typing import List, Dict, Optional
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from utils.catalog import get_product_by_id


def get_cart_keyboard(cart_items: List[Dict[str, int]]) -> InlineKeyboardMarkup:
    """
    Клавіатура для кошика користувача.
    :param cart_items: список товарів у кошику (product_id, quantity)
    :return: клавіатура з кнопками зміни кількості, видалення, оформлення і очищення
    """
    keyboard: List[List[InlineKeyboardButton]] = []
    
    # Перевіряємо чи є товари в кошику
    if not cart_items:
        return InlineKeyboardMarkup(inline_keyboard=[[
            InlineKeyboardButton(text="🔙 Повернутися до меню", callback_data="back_to_menu")
        ]])
    
    # Кнопки для кожного товару
    for item in cart_items:
        try:
            product_id = item.get("product_id")
            quantity = item.get("quantity", 0)
            
            # Перевіряємо валідність даних
            if product_id is None or quantity <= 0:
                continue
                
            # Отримуємо інформацію про товар для відображення назви
            product = get_product_by_id(product_id)
            if not product:
                continue
                
            # Обмежуємо довжину назви товару
            product_name = product.get('name', f'Товар #{product_id}')
            if len(product_name) > 25:
                product_name = product_name[:22] + "..."
            
            # Рядок з назвою товару
            keyboard.append([
                InlineKeyboardButton(
                    text=f"📦 {product_name}", 
                    callback_data=f"product_info_{product_id}"
                )
            ])
            
            # Рядок з кнопками управління кількістю
            row_buttons = []
            
            # Кнопка зменшення
            row_buttons.append(
                InlineKeyboardButton(text="➖", callback_data=f"cart_decrease_{product_id}")
            )
            
            # Кнопка з кількістю
            row_buttons.append(
                InlineKeyboardButton(
                    text=f"{quantity} шт", 
                    callback_data=f"cart_quantity_{product_id}"
                )
            )
            
            # Кнопка збільшення
            row_buttons.append(
                InlineKeyboardButton(text="➕", callback_data=f"cart_increase_{product_id}")
            )
            
            # Кнопка видалення
            row_buttons.append(
                InlineKeyboardButton(text="🗑", callback_data=f"cart_remove_{product_id}")
            )
            
            keyboard.append(row_buttons)
                
        except (KeyError, TypeError, ValueError) as e:
            # Логуємо помилку та пропускаємо некоректний товар
            print(f"Помилка обробки товару в кошику: {e}")
            continue
    
    # Додаємо розділювач перед кнопками дій
    keyboard.append([
        InlineKeyboardButton(text="━━━━━━━━━━━━━", callback_data="separator_main")
    ])
    
    # Кнопка оформлення замовлення
    keyboard.append([
        InlineKeyboardButton(text="🧾 Оформити замовлення", callback_data="checkout")
    ])
    
    # Рядок з додатковими діями
    keyboard.append([
        InlineKeyboardButton(text="🗑 Очистити кошик", callback_data="clear_cart")
    ])
    
    # Кнопка повернення до меню
    keyboard.append([
        InlineKeyboardButton(text="🔙 Головне меню", callback_data="back_to_menu")
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_checkout_keyboard() -> InlineKeyboardMarkup:
    """
    Клавіатура для вибору способу оплати
    :return: клавіатура з варіантами оплати і кнопкою назад
    """
    keyboard: List[List[InlineKeyboardButton]] = [
        # Способи оплати
        [
            InlineKeyboardButton(text="💳 LiqPay", callback_data="pay_liqpay"),
            InlineKeyboardButton(text="💰 WayForPay", callback_data="pay_wayforpay")
        ],
        [
            InlineKeyboardButton(text="💵 При отриманні", callback_data="pay_cash")
        ],
        # Навігаційні кнопки
        [
            InlineKeyboardButton(text="🔙 Назад до кошика", callback_data="back_to_cart"),
            InlineKeyboardButton(text="🏠 Головне меню", callback_data="back_to_menu")
        ]
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
            InlineKeyboardButton(text="💳 Змінити оплату", callback_data="checkout")
        ],
        # Кнопки навігації
        [
            InlineKeyboardButton(text="🔙 Назад до кошика", callback_data="back_to_cart"),
            InlineKeyboardButton(text="❌ Скасувати замовлення", callback_data="cancel_order")
        ]
    ]
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_order_cancel_confirmation_keyboard() -> InlineKeyboardMarkup:
    """Клавіатура підтвердження скасування замовлення"""
    keyboard = [
        [
            InlineKeyboardButton(text="⚠️ Ви впевнені?", callback_data="cancel_warning")
        ],
        [
            InlineKeyboardButton(text="✅ Так, скасувати", callback_data="confirm_cancel_order"),
            InlineKeyboardButton(text="❌ Ні, повернутися", callback_data="back_to_cart")
        ]
    ]
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
