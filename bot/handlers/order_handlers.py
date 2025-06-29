from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards.main_keyboards import get_back_to_menu_keyboard
from keyboards.order_keyboards import get_payment_keyboard, get_order_confirmation_keyboard
from utils.orders import create_order, get_user_orders, process_payment
from utils.cart import get_user_cart, clear_cart, get_cart_total
from utils.loyalty import add_loyalty_points, get_user_loyalty_points

router = Router()

class OrderStates(StatesGroup):
    waiting_contact = State()
    waiting_address = State()
    payment_processing = State()

@router.message(F.text == "🧾 Замовити")
async def start_order_process(message: Message, state: FSMContext):
    """Початок процесу замовлення"""
    user_id = message.from_user.id
    cart_items = get_user_cart(user_id)
    
    if not cart_items:
        await message.answer(
            "🛒 Ваш кошик порожній!\n\n"
            "Додайте товари до кошика перед оформленням замовлення.",
            reply_markup=get_back_to_menu_keyboard()
        )
        return
    
    total = get_cart_total(user_id)
    
    await state.set_state(OrderStates.waiting_contact)
    await state.update_data(total=total)
    
    await message.answer(
        "📋 <b>Оформлення замовлення</b>\n\n"
        f"💳 Сума замовлення: <b>{total} грн</b>\n\n"
        "📞 Будь ласка, надішліть ваш номер телефону для зв'язку:\n"
        "(наприклад: +380671234567)",
        reply_markup=get_back_to_menu_keyboard()
    )

@router.message(OrderStates.waiting_contact, F.text)
async def process_contact(message: Message, state: FSMContext):
    """Обробка контактних даних"""
    if message.text == "🔙 Повернутися в меню":
        await state.clear()
        return
    
    # Простая валідація номера телефону
    phone = message.text.strip()
    if not phone.startswith('+380') or len(phone) != 13:
        await message.answer(
            "❌ Некоректний формат номера телефону.\n\n"
            "Будь ласка, введіть номер у форматі: +380671234567"
        )
        return
    
    await state.update_data(phone=phone)
    await state.set_state(OrderStates.waiting_address)
    
    await message.answer(
        "📍 Тепер введіть адресу доставки:\n"
        "(наприклад: вул. Шевченка, 15, кв. 10, Тернопіль)"
    )

@router.message(OrderStates.waiting_address, F.text)
async def process_address(message: Message, state: FSMContext):
    """Обробка адреси доставки"""
    if message.text == "🔙 Повернутися в меню":
        await state.clear()
        return
    
    address = message.text.strip()
    if len(address) < 10:
        await message.answer(
            "❌ Адреса занадто коротка.\n\n"
            "Будь ласка, введіть повну адресу доставки."
        )
        return
    
    data = await state.get_data()
    await state.update_data(address=address)
    
    # Показуємо підтвердження замовлення
    user_id = message.from_user.id
    cart_items = get_user_cart(user_id)
    
    order_text = "📋 <b>Підтвердження замовлення</b>\n\n"
    
    for item in cart_items:
        from utils.catalog import get_product_by_id
        product = get_product_by_id(item['product_id'])
        if product:
            item_total = product['price'] * item['quantity']
            order_text += f"🧼 {product['name']} × {item['quantity']} = {item_total} грн\n"
    
    order_text += f"\n💳 <b>Загальна сума: {data['total']} грн</b>\n"
    order_text += f"📞 Телефон: {data['phone']}\n"
    order_text += f"📍 Адреса: {address}\n\n"
    order_text += "Підтвердіть замовлення та оберіть спосіб оплати:"
    
    await message.answer(
        order_text,
        reply_markup=get_order_confirmation_keyboard()
    )

@router.callback_query(F.data == "confirm_order")
async def confirm_order(callback: CallbackQuery, state: FSMContext):
    """Підтвердження замовлення"""
    await callback.message.edit_text(
        "💳 <b>Оплата замовлення</b>\n\n"
        "Оберіть зручний для вас спосіб оплати:",
        reply_markup=get_payment_keyboard()
    )
    
    await callback.answer()

@router.callback_query(F.data.startswith("pay_"))
async def process_payment_method(callback: CallbackQuery, state: FSMContext):
    """Обробка способу оплати"""
    payment_method = callback.data.split("_")[1]
    user_id = callback.from_user.id
    data = await state.get_data()
    
    # Створюємо замовлення
    order_id = create_order(
        user_id=user_id,
        phone=data['phone'],
        address=data['address'],
        total=data['total'],
        payment_method=payment_method
    )
    
    if order_id:
        # Нараховуємо бали лояльності (5% від суми)
        loyalty_points = int(data['total'] * 0.05)
        add_loyalty_points(user_id, loyalty_points)
        
        # Очищаємо кошик
        clear_cart(user_id)
        
        # Повідомляємо про успішне замовлення
        success_text = (
            "✅ <b>Замовлення успішно оформлено!</b>\n\n"
            f"📋 Номер замовлення: <b>#{order_id}</b>\n"
            f"💳 Сума: <b>{data['total']} грн</b>\n"
            f"💰 Способ оплати: <b>{payment_method}</b>\n\n"
            f"🎁 Нараховано балів лояльності: <b>{loyalty_points}</b>\n\n"
            "📞 Наш менеджер зв'яжеться з вами найближчим часом для підтвердження замовлення.\n\n"
            "Дякуємо за покупку в CleanWay! 😊"
        )
        
        await callback.message.edit_text(
            success_text,
            reply_markup=get_back_to_menu_keyboard()
        )
        
        # Повідомляємо адміністратора
        admin_id = os.getenv('ADMIN_ID')
        if admin_id:
            admin_text = (
                "🔔 <b>Нове замовлення!</b>\n\n"
                f"📋 Замовлення: #{order_id}\n"
                f"👤 Користувач: @{callback.from_user.username or 'без username'}\n"
                f"📞 Телефон: {data['phone']}\n"
                f"📍 Адреса: {data['address']}\n"
                f"💳 Сума: {data['total']} грн\n"
                f"💰 Оплата: {payment_method}"
            )
            
            try:
                await callback.bot.send_message(admin_id, admin_text)
            except:
                pass  # Ігноруємо помилки відправки адміну
        
        await state.clear()
    else:
        await callback.answer(
            "❌ Помилка при створенні замовлення. Спробуйте ще раз.",
            show_alert=True
        )

@router.message(F.text == "🧮 Мої чеки")
async def show_user_orders(message: Message):
    """Показ історії замовлень користувача"""
    user_id = message.from_user.id
    orders = get_user_orders(user_id)
    
    if not orders:
        await message.answer(
            "📋 У вас поки немає замовлень.\n\n"
            "Оформіть перше замовлення через каталог товарів!",
            reply_markup=get_back_to_menu_keyboard()
        )
        return
    
    orders_text = "🧮 <b>Ваші замовлення:</b>\n\n"
    
    for order in orders[-5:]:  # Показуємо останні 5 замовлень
        status_emoji = {
            'pending': '⏳',
            'processing': '🔄',
            'shipped': '🚚',
            'completed': '✅',
            'cancelled': '❌'
        }
        
        orders_text += (
            f"{status_emoji.get(order['status'], '📋')} <b>Замовлення #{order['id']}</b>\n"
            f"💳 Сума: {order['total']} грн\n"
            f"📅 Дата: {order['created_at']}\n"
            f"📊 Статус: {order['status']}\n\n"
        )
    
    # Показуємо бали лояльності
    loyalty_points = get_user_loyalty_points(user_id)
    orders_text += f"🎁 <b>Ваші бали лояльності: {loyalty_points}</b>\n"
    orders_text += "💡 Використовуйте бали для знижок на наступні покупки!"
    
    await message.answer(
        orders_text,
        reply_markup=get_back_to_menu_keyboard()
    )

@router.message(F.text == "🧧 Відмова від паперового чека")
async def toggle_paperless_receipts(message: Message):
    """Перемикання режиму електронних чеків"""
    user_id = message.from_user.id
    
    # Тут би була логіка збереження налаштувань користувача
    # Поки що просто повідомляємо про активацію
    
    await message.answer(
        "✅ <b>Електронні чеки активовано!</b>\n\n"
        "🌱 Дякуємо за турботу про довкілля!\n"
        "📧 Тепер всі ваші чеки будуть надходити в електронному вигляді.\n\n"
        "💚 Разом ми робимо світ чистішим!",
        reply_markup=get_back_to_menu_keyboard()
    )