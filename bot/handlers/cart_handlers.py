from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from keyboards.cart_keyboards import get_cart_keyboard, get_checkout_keyboard
from keyboards.main_keyboards import get_back_to_menu_keyboard
from utils.cart import (
    get_user_cart,
    update_cart_item,
    remove_from_cart,
    clear_cart,
    get_cart_total
)
from utils.catalog import get_product_by_id

router = Router()


@router.message(F.text == "🛒 Кошик")
async def show_cart(message: Message):
    user_id = message.from_user.id
    cart_items = get_user_cart(user_id)

    if not cart_items:
        await message.answer(
            "🛒 Ваш кошик порожній\n\n"
            "Перейдіть до каталогу, щоб додати товари!",
            reply_markup=get_back_to_menu_keyboard()
        )
        return

    await send_cart_message(message, cart_items)


@router.callback_query(F.data.startswith("cart_increase_"))
async def increase_cart_item(callback: CallbackQuery):
    try:
        product_id = int(callback.data.split("_")[2])
        user_id = callback.from_user.id

        cart_items = get_user_cart(user_id)
        current_item = next((item for item in cart_items if item['product_id'] == product_id), None)

        if current_item:
            new_quantity = current_item['quantity'] + 1
            # Додаємо перевірку максимальної кількості
            if new_quantity <= 99:  # Обмеження для запобігання проблемам
                update_cart_item(user_id, product_id, new_quantity)
                await update_cart_display(callback)
            else:
                await callback.answer("Досягнуто максимальну кількість товару", show_alert=True)
                return
        else:
            await callback.answer("Товар не знайдено в кошику", show_alert=True)
            return

        await callback.answer()
    except (ValueError, IndexError) as e:
        await callback.answer("Помилка обробки запиту", show_alert=True)


@router.callback_query(F.data.startswith("cart_decrease_"))
async def decrease_cart_item(callback: CallbackQuery):
    try:
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

            await update_cart_display(callback)
        else:
            await callback.answer("Товар не знайдено в кошику", show_alert=True)
            return

        await callback.answer()
    except (ValueError, IndexError) as e:
        await callback.answer("Помилка обробки запиту", show_alert=True)


@router.callback_query(F.data.startswith("cart_remove_"))
async def remove_cart_item(callback: CallbackQuery):
    try:
        product_id = int(callback.data.split("_")[2])
        user_id = callback.from_user.id

        remove_from_cart(user_id, product_id)
        await update_cart_display(callback)

        await callback.answer("Товар видалено з кошика")
    except (ValueError, IndexError) as e:
        await callback.answer("Помилка видалення товару", show_alert=True)


@router.callback_query(F.data == "clear_cart")
async def clear_cart_handler(callback: CallbackQuery):
    user_id = callback.from_user.id
    clear_cart(user_id)

    await callback.message.edit_text(
        "🗑 Ваш кошик очищено!",
        reply_markup=get_back_to_menu_keyboard()
    )
    await callback.answer("Кошик очищено")


@router.callback_query(F.data == "checkout")
async def start_checkout(callback: CallbackQuery):
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
        reply_markup=get_checkout_keyboard(),
        parse_mode="HTML"
    )

    await callback.answer()


@router.callback_query(F.data == "back_to_cart")
async def back_to_cart(callback: CallbackQuery):
    user_id = callback.from_user.id
    cart_items = get_user_cart(user_id)

    if not cart_items:
        await callback.message.edit_text(
            "🛒 Ваш кошик порожній\n\n"
            "Перейдіть до каталогу, щоб додати товари!",
            reply_markup=get_back_to_menu_keyboard()
        )
    else:
        await update_cart_display(callback)

    await callback.answer()


@router.callback_query(F.data == "pay_liqpay")
async def pay_liqpay(callback: CallbackQuery):
    await callback.message.edit_text(
        "🔄 Оплата через LiqPay наразі в розробці.\nСкоро буде доступна!",
        reply_markup=get_back_to_menu_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "pay_wayforpay")
async def pay_wayforpay(callback: CallbackQuery):
    await callback.message.edit_text(
        "🔄 Оплата через WayForPay наразі в розробці.\nСкоро буде доступна!",
        reply_markup=get_back_to_menu_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery):
    await callback.message.edit_text(
        "📂 Головне меню:",
        reply_markup=get_back_to_menu_keyboard()
    )
    await callback.answer()


async def update_cart_display(callback: CallbackQuery):
    user_id = callback.from_user.id
    cart_items = get_user_cart(user_id)

    if not cart_items:
        await callback.message.edit_text(
            "🛒 Ваш кошик порожній\n\n"
            "Перейдіть до каталогу, щоб додати товари!",
            reply_markup=get_back_to_menu_keyboard()
        )
        return

    await send_cart_message(callback, cart_items)


async def send_cart_message(message_or_callback, cart_items):
    cart_text = "🛒 <b>Ваш кошик:</b>\n\n"
    total = 0

    for item in cart_items:
        product = get_product_by_id(item['product_id'])
        if product:
            item_total = product['price'] * item['quantity']
            total += item_total
            cart_text += (
                f"📦 <b>{product['name']}</b>\n"  # Змінено емодзі
                f"💰 {product['price']} грн × {item['quantity']} шт = {item_total} грн\n\n"
            )
        else:
            # Обробка випадку, коли товар не знайдено
            cart_text += (
                f"❌ <b>Товар не знайдено</b>\n"
                f"ID: {item['product_id']} × {item['quantity']} шт\n\n"
            )

    cart_text += f"💳 <b>Загальна сума: {total} грн</b>"

    try:
        if isinstance(message_or_callback, CallbackQuery):
            await message_or_callback.message.edit_text(
                cart_text,
                reply_markup=get_cart_keyboard(cart_items),
                parse_mode="HTML"
            )
        else:
            await message_or_callback.answer(
                cart_text,
                reply_markup=get_cart_keyboard(cart_items),
                parse_mode="HTML"
            )
    except Exception as e:
        # Логування помилки (додайте свій logger)
        print(f"Помилка відправки повідомлення кошика: {e}")
        
        # Відправка простого повідомлення у випадку помилки
        error_text = "❌ Помилка відображення кошика"
        if isinstance(message_or_callback, CallbackQuery):
            await message_or_callback.message.edit_text(
                error_text,
                reply_markup=get_back_to_menu_keyboard()
            )
        else:
            await message_or_callback.answer(
                error_text,
                reply_markup=get_back_to_menu_keyboard()
            )
