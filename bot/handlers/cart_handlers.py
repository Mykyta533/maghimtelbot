from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards.cart_keyboards import get_cart_keyboard, get_checkout_keyboard
from keyboards.main_keyboards import get_back_to_menu_keyboard
from utils.cart import get_user_cart, update_cart_item, remove_from_cart, clear_cart, get_cart_total
from utils.catalog import get_product_by_id

router = Router()

@router.message(F.text == "🛒 Кошик")
async def show_cart(message: Message):
    """Показ кошика користувача"""
    user_id = message.from_user.id
    cart_items = get_user_cart(user_id)
    
    if not cart_items:
        await message.answer(
            "🛒 Ваш кошик порожній\n\n"
            "Перейдіть до каталогу, щоб додати товари!",
            reply_markup=get_back_to_menu_keyboard()
        )
        return
    
    cart_text = "🛒 <b>Ваш кошик:</b>\n\n"
    total = 0
    
    for item in cart_items:
        product = get_product_by_id(item['product_id'])
        if product:
            item_total = product['price'] * item['quantity']
            total += item_total
            
            cart_text += (
                f"🧼 <b>{product['name']}</b>\n"
                f"💰 {product['price']} грн × {item['quantity']} шт = {item_total} грн\n\n"
            )
    
    cart_text += f"💳 <b>Загальна сума: {total} грн</b>"
    
    await message.answer(
        cart_text,
        reply_markup=get_cart_keyboard(cart_items)
    )

@router.callback_query(F.data.startswith("cart_increase_"))
async def increase_cart_item(callback: CallbackQuery):
    """Збільшення кількості товару в кошику"""
    product_id = int(callback.data.split("_")[2])
    user_id = callback.from_user.id
    
    cart_items = get_user_cart(user_id)
    current_item = next((item for item in cart_items if item['product_id'] == product_id), None)
    
    if current_item:
        new_quantity = current_item['quantity'] + 1
        update_cart_item(user_id, product_id, new_quantity)
        
        # Оновлюємо відображення кошика
        await update_cart_display(callback)
    
    await callback.answer()

@router.callback_query(F.data.startswith("cart_decrease_"))
async def decrease_cart_item(callback: CallbackQuery):
    """Зменшення кількості товару в кошику"""
    product_id = int(callback.data.split("_")[2])
    user_id = callback.from_user.id
    
    cart_items = get_user_cart(user_id)
    current_item = next((item for item in cart_items if item['product_id'] == product_id), None)
    
    if current_item:
        if current_item['quantity'] > 1:
            new_quantity = current_item['quantity'] - 1
            update_cart_item(user_id, product_id, new_quantity)
        else:
            remove_from_cart(user_id, product_id)
        
        # Оновлюємо відображення кошика
        await update_cart_display(callback)
    
    await callback.answer()

@router.callback_query(F.data.startswith("cart_remove_"))
async def remove_cart_item(callback: CallbackQuery):
    """Видалення товару з кошика"""
    product_id = int(callback.data.split("_")[2])
    user_id = callback.from_user.id
    
    remove_from_cart(user_id, product_id)
    await update_cart_display(callback)
    
    await callback.answer("Товар видалено з кошика")

@router.callback_query(F.data == "checkout")
async def start_checkout(callback: CallbackQuery):
    """Початок оформлення замовлення"""
    user_id = callback.from_user.id
    cart_items = get_user_cart(user_id)
    
    if not cart_items:
        await callback.answer("Кошик порожній", show_alert=True)
        return
    
    total = get_cart_total(user_id)
    
    checkout_text = (
        "📋 <b>Оформлення замовлення</b>\n\n"
        f"💳 Сума до оплати: <b>{total} грн</b>\n\n"
        "Оберіть спосіб оплати:"
    )
    
    await callback.message.edit_text(
        checkout_text,
        reply_markup=get_checkout_keyboard()
    )
    
    await callback.answer()

async def update_cart_display(callback: CallbackQuery):
    """Оновлення відображення кошика"""
    user_id = callback.from_user.id
    cart_items = get_user_cart(user_id)
    
    if not cart_items:
        await callback.message.edit_text(
            "🛒 Ваш кошик порожній\n\n"
            "Перейдіть до каталогу, щоб додати товари!",
            reply_markup=get_back_to_menu_keyboard()
        )
        return
    
    cart_text = "🛒 <b>Ваш кошик:</b>\n\n"
    total = 0
    
    for item in cart_items:
        product = get_product_by_id(item['product_id'])
        if product:
            item_total = product['price'] * item['quantity']
            total += item_total
            
            cart_text += (
                f"🧼 <b>{product['name']}</b>\n"
                f"💰 {product['price']} грн × {item['quantity']} шт = {item_total} грн\n\n"
            )
    
    cart_text += f"💳 <b>Загальна сума: {total} грн</b>"
    
    await callback.message.edit_text(
        cart_text,
        reply_markup=get_cart_keyboard(cart_items)
    )