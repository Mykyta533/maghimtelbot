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
            
            # Кнопка зменшення (неактивна якщо кількість = 1)
            if quantity > 1:
                row_buttons.append(
                    InlineKeyboardButton(text="➖", callback_data=f"cart_decrease_{product_id}")
                )
            else:
                row_buttons.append(
                    InlineKeyboardButton(text="🚫", callback_data=f"cart_min_{product_id}")
                )
            
            # Кнопка з кількістю (можна клікнути для ручного введення)
            row_buttons.append(
                InlineKeyboardButton(
                    text=f"{quantity} шт", 
                    callback_data=f"cart_quantity_{product_id}"
                )
            )
            
            # Кнопка збільшення (неактивна якщо кількість = 99)
            if quantity < 99:
                row_buttons.append(
                    InlineKeyboardButton(text="➕", callback_data=f"cart_increase_{product_id}")
                )
            else:
                row_buttons.append(
                    InlineKeyboardButton(text="🚫", callback_data=f"cart_max_{product_id}")
                )
            
            # Кнопка видалення
            row_buttons.append(
                InlineKeyboardButton(text="🗑", callback_data=f"cart_remove_{product_id}")
            )
            
            keyboard.append(row_buttons)
            
            # Додаємо порожній рядок для розділення товарів (якщо товарів більше 1)
            if len(cart_items) > 1:
                keyboard.append([
                    InlineKeyboardButton(text="━━━━━━━━━━", callback_data="separator")
                ])
                
        except (KeyError, TypeError, ValueError) as e:
            # Логуємо помилку та пропускаємо некоректний товар
            print(f"Помилка обробки товару в кошику: {e}")
            continue
    
    # Видаляємо останній розділювач якщо він є
    if keyboard and keyboard[-1][0].text == "━━━━━━━━━━":
        keyboard.pop()
    
    # Додаємо розділювач перед кнопками дій
    keyboard.append([
        InlineKeyboardButton(text="═════════════", callback_data="separator_main")
    ])
    
    # Кнопка оформлення замовлення
    keyboard.append([
        InlineKeyboardButton(text="🧾 Оформити замовлення", callback_data="checkout")
    ])
    
    # Рядок з додатковими діями
    keyboard.append([
        InlineKeyboardButton(text="🗑 Очистити кошик", callback_data="clear_cart"),
        InlineKeyboardButton(text="🛍 Продовжити покупки", callback_data="continue_shopping")
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
        # Заголовок
        [
            InlineKeyboardButton(text="💳 Оберіть спосіб оплати:", callback_data="payment_header")
        ],
        # Розділювач
        [
            InlineKeyboardButton(text="═════════════", callback_data="separator")
        ],
        # Способи оплати
        [
            InlineKeyboardButton(text="💳 LiqPay", callback_data="pay_liqpay")
        ],
        [
            InlineKeyboardButton(text="💰 WayForPay", callback_data="pay_wayforpay")
        ],
        [
            InlineKeyboardButton(text="💵 При отриманні", callback_data="pay_cash")
        ],
        # Розділювач
        [
            InlineKeyboardButton(text="═════════════", callback_data="separator")
        ],
        # Навігаційні кнопки
        [
            InlineKeyboardButton(text="🔙 Назад до кошика", callback_data="back_to_cart"),
            InlineKeyboardButton(text="🏠 Головне меню", callback_data="back_to_menu")
        ]
    ]
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_payment_confirmation_keyboard(payment_method: str) -> InlineKeyboardMarkup:
    """
    Клавіатура для підтвердження оплати
    :param payment_method: спосіб оплати
    :return: клавіатура з кнопками підтвердження
    """
    keyboard: List[List[InlineKeyboardButton]] = [
        [
            InlineKeyboardButton(text="✅ Підтвердити замовлення", callback_data=f"confirm_order_{payment_method}")
        ],
        [
            InlineKeyboardButton(text="✏️ Змінити спосіб оплати", callback_data="checkout"),
            InlineKeyboardButton(text="🔙 До кошика", callback_data="back_to_cart")
        ]
    ]
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_empty_cart_keyboard() -> InlineKeyboardMarkup:
    """
    Клавіатура для порожнього кошика
    :return: клавіатура з кнопкою переходу до каталогу
    """
    keyboard: List[List[InlineKeyboardButton]] = [
        [
            InlineKeyboardButton(text="🛍 Перейти до каталогу", callback_data="show_catalog")
        ],
        [
            InlineKeyboardButton(text="🏠 Головне меню", callback_data="back_to_menu")
        ]
    ]
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_quantity_input_keyboard(product_id: int, current_quantity: int) -> InlineKeyboardMarkup:
    """
    Клавіатура для швидкого вибору кількості товару
    :param product_id: ID товару
    :param current_quantity: поточна кількість
    :return: клавіатура з кнопками швидкого вибору
    """
    keyboard: List[List[InlineKeyboardButton]] = []
    
    # Заголовок
    keyboard.append([
        InlineKeyboardButton(
            text=f"Поточна кількість: {current_quantity} шт", 
            callback_data="current_quantity"
        )
    ])
    
    # Швидкий вибір кількості
    quick_amounts = [1, 2, 3, 5, 10]
    row = []
    
    for amount in quick_amounts:
        if amount != current_quantity:  # Не показуємо поточну кількість
            row.append(
                InlineKeyboardButton(
                    text=f"{amount}", 
                    callback_data=f"set_quantity_{product_id}_{amount}"
                )
            )
            
            # По 3 кнопки в рядку
            if len(row) == 3:
                keyboard.append(row)
                row = []
    
    # Додаємо останній рядок якщо є залишкові кнопки
    if row:
        keyboard.append(row)
    
    # Кнопки управління
    keyboard.append([
        InlineKeyboardButton(text="🔙 Назад до кошика", callback_data="back_to_cart")
    ])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
