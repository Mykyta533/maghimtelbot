from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_categories_keyboard(categories):
    """Клавіатура категорій товарів"""
    keyboard = []

    for category in categories:
        keyboard.append([
            InlineKeyboardButton(
                text=category['name'],
                callback_data=f"category_{category['id']}"
            )
        ])

    keyboard.append([
        InlineKeyboardButton(text="🔙 Назад в меню", callback_data="back_to_menu")
    ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_product_keyboard(product_id, current_index=0, total_products=1, category_id=None):
    """Клавіатура для товару"""
    keyboard = []

    # Кнопки навігації між товарами (якщо товарів більше одного)
    if total_products > 1 and category_id is not None:
        nav_buttons = []
        if current_index > 0:
            nav_buttons.append(
                InlineKeyboardButton(text="⬅️", callback_data=f"nav_{category_id}_{current_index - 1}")
            )

        nav_buttons.append(
            InlineKeyboardButton(
                text=f"{current_index + 1}/{total_products}",
                callback_data="current_product"
            )
        )

        if current_index < total_products - 1:
            nav_buttons.append(
                InlineKeyboardButton(text="➡️", callback_data=f"nav_{category_id}_{current_index + 1}")
            )

        keyboard.append(nav_buttons)

    # Основні кнопки
    keyboard.extend([
        [
            InlineKeyboardButton(
                text="🛒 Додати до кошика",
                callback_data=f"add_cart_{product_id}"
            )
        ],
        [
            InlineKeyboardButton(
                text="🧾 Замовити зараз",
                callback_data=f"order_{product_id}"
            )
        ]
    ])

    # Кнопка "До каталогу" з поверненням до відповідної категорії
    back_callback = f"category_{category_id}" if category_id else "back_to_catalog"
    keyboard.append([
        InlineKeyboardButton(text="🔙 До каталогу", callback_data=back_callback)
    ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
