from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

from utils.cart import get_user_cart, get_cart_total, clear_cart
from utils.order_storage import save_order_to_json

router = Router()

class CheckoutState(StatesGroup):
    waiting_for_phone = State()
    waiting_for_address = State()
    waiting_for_payment_method = State()

@router.callback_query(F.data == "checkout")
async def start_checkout(callback: CallbackQuery, state: FSMContext):
    await callback.message.answer("📞 Введіть ваш номер телефону:", reply_markup=ReplyKeyboardRemove())
    await state.set_state(CheckoutState.waiting_for_phone)

@router.message(StateFilter(CheckoutState.waiting_for_phone))
async def get_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer("📍 Введіть вашу адресу доставки:")
    await state.set_state(CheckoutState.waiting_for_address)

@router.message(StateFilter(CheckoutState.waiting_for_address))
async def get_address(message: Message, state: FSMContext):
    await state.update_data(address=message.text)
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="💳 LiqPay"), KeyboardButton(text="💰 WayForPay")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await message.answer("💳 Оберіть спосіб оплати:", reply_markup=keyboard)
    await state.set_state(CheckoutState.waiting_for_payment_method)

@router.message(StateFilter(CheckoutState.waiting_for_payment_method))
async def confirm_order(message: Message, state: FSMContext):
    payment_method = message.text
    user_id = message.from_user.id
    cart_items = get_user_cart(user_id)
    total = get_cart_total(user_id)

    data = await state.get_data()
    data.update({
        "payment_method": payment_method,
        "cart": cart_items,
        "total": total,
        "user_id": user_id
    })

    order_id = save_order_to_json(data)
    clear_cart(user_id)

    # Повідомлення клієнту
    await message.answer(
        f"✅ Замовлення #{order_id} прийнято!\n"
        f"📞 Телефон: {data['phone']}\n"
        f"📍 Адреса: {data['address']}\n"
        f"💰 Оплата: {payment_method}\n"
        f"💳 Сума: {total} грн",
        reply_markup=ReplyKeyboardRemove()
    )

    # Повідомлення адміну
    admin_id = 7888882860  # ← Встав сюди свій Telegram ID
    admin_text = (
        "🔔 <b>Нове замовлення!</b>\n\n"
        f"📋 Замовлення: #{order_id}\n"
        f"👤 Користувач: @{message.from_user.username or 'без username'}\n"
        f"🆔 ID: {user_id}\n"
        f"📞 Телефон: {data['phone']}\n"
        f"📍 Адреса: {data['address']}\n"
        f"💰 Оплата: {payment_method}\n"
        f"💳 Сума: {total} грн"
    )

    try:
        await message.bot.send_message(chat_id=admin_id, text=admin_text, parse_mode="HTML")
    except Exception as e:
        print(f"❌ Не вдалося надіслати повідомлення адміну: {e}")

    await state.clear()
