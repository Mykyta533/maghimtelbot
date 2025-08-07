from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards.main_keyboards import get_main_menu, get_back_to_menu_keyboard
from utils.messages import WELCOME_MESSAGE, CONTACT_INFO
from utils.cart import get_user_cart, get_cart_total
from utils.database import update_user_data, get_user_data
from keyboards.cart_keyboards import get_checkout_keyboard

router = Router()

class UserRegistrationState(StatesGroup):
    waiting_for_phone = State()

class UserProfileState(StatesGroup):
    waiting_for_phone = State()
    waiting_for_name = State()
    waiting_for_address = State()

@router.message(CommandStart())
async def start_command(message: Message, state: FSMContext):
    """Обробка команди /start - запит номера телефону"""
    await state.clear()
    
    # Створюємо клавіатуру для передачі номера телефону
    phone_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 Поділитися номером", request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    
    await message.answer(
        "👋 <b>Розпочати роботу з CleanWay</b>\n\n"
        "Для початку роботи, будь ласка, поділіться своїм номером телефону.\n"
        "Це допоможе нам краще обслуговувати вас та повідомляти про статус замовлень.",
        reply_markup=phone_keyboard,
        parse_mode="HTML"
    )
    
    await state.set_state(UserRegistrationState.waiting_for_phone)

@router.message(UserRegistrationState.waiting_for_phone, F.contact)
async def process_phone_contact(message: Message, state: FSMContext):
    """Обробка отриманого номера телефону"""
    phone_number = message.contact.phone_number
    user_id = message.from_user.id
    
    # Зберігаємо номер телефону користувача
    user_data = {
        'phone': phone_number,
        'first_name': message.from_user.first_name or '',
        'last_name': message.from_user.last_name or '',
        'username': message.from_user.username or ''
    }
    update_user_data(user_id, user_data)
    
    # Повідомляємо адміністратора про нового користувача
    import os
    admin_id = int(os.getenv('ADMIN_ID', '8095681158'))
    
    admin_text = (
        "👤 <b>Новий користувач зареєстрований!</b>\n\n"
        f"🆔 ID: {user_id}\n"
        f"👤 Ім'я: {message.from_user.first_name or 'Невідомо'} {message.from_user.last_name or ''}\n"
        f"📱 Username: @{message.from_user.username or 'немає'}\n"
        f"📞 Телефон: {phone_number}"
    )
    
    try:
        await message.bot.send_message(chat_id=admin_id, text=admin_text, parse_mode="HTML")
        print(f"✅ Повідомлення про нового користувача надіслано адміну")
    except Exception as e:
        print(f"❌ Не вдалося надіслати повідомлення адміну: {e}")
    
    await state.clear()
    
    # Показуємо вітальне повідомлення та головне меню
    await message.answer(
        WELCOME_MESSAGE,
        reply_markup=get_main_menu(),
        parse_mode="HTML"
    )

@router.message(UserRegistrationState.waiting_for_phone)
async def invalid_phone_input(message: Message):
    """Обробка некоректного вводу номера телефону"""
    phone_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 Поділитися номером", request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    
    await message.answer(
        "📱 Будь ласка, натисніть кнопку \"📱 Поділитися номером\" для передачі вашого номера телефону.",
        reply_markup=phone_keyboard
    )

@router.message(F.text == "🔙 Повернутися в меню")
async def back_to_menu(message: Message, state: FSMContext):
    """Повернення в головне меню"""
    await state.clear()
    
    await message.answer(
        "🏠 <b>Головне меню</b>\n\n"
        "Оберіть потрібний розділ:",
        reply_markup=get_main_menu(),
        parse_mode="HTML"
    )

@router.message(F.text == "📞 Контакти")
async def contact_info(message: Message):
    """Повна контактна інформація"""
    await message.answer(
        CONTACT_INFO,
        reply_markup=get_back_to_menu_keyboard(),
        parse_mode="HTML"
    )

@router.message(F.text == "👤 Моє")
async def my_profile(message: Message, state: FSMContext):
    """Профіль користувача - редагування даних"""
    user_id = message.from_user.id
    user_data = get_user_data(user_id)
    
    current_phone = user_data.get('phone', 'Не вказано')
    current_name = user_data.get('name', 'Не вказано')
    current_address = user_data.get('address', 'Не вказано')
    
    profile_text = (
        "👤 <b>Мій профіль</b>\n\n"
        f"📞 Телефон: {current_phone}\n"
        f"👤 Ім'я: {current_name}\n"
        f"📍 Адреса: {current_address}\n\n"
        "Введіть ваш номер телефону:"
    )
    
    await message.answer(
        profile_text,
        reply_markup=get_back_to_menu_keyboard(),
        parse_mode="HTML"
    )
    
    await state.set_state(UserProfileState.waiting_for_phone)

@router.message(UserProfileState.waiting_for_phone)
async def update_phone(message: Message, state: FSMContext):
    """Оновлення номера телефону"""
    phone = message.text.strip()
    
    if not phone or phone == "🔙 Повернутися в меню":
        await back_to_menu(message, state)
        return
    
    await state.update_data(phone=phone)
    
    await message.answer(
        "👤 Тепер введіть ваше повне ім'я:",
        reply_markup=get_back_to_menu_keyboard()
    )
    
    await state.set_state(UserProfileState.waiting_for_name)

@router.message(UserProfileState.waiting_for_name)
async def update_name(message: Message, state: FSMContext):
    """Оновлення імені"""
    name = message.text.strip()
    
    if not name or name == "🔙 Повернутися в меню":
        await back_to_menu(message, state)
        return
    
    await state.update_data(name=name)
    
    await message.answer(
        "📍 Тепер введіть адресу доставки:\n\n"
        "Наприклад:\n"
        "• Нова Пошта №5, Тернопіль\n"
        "• Укрпошта, вул. Руська 10, Тернопіль\n"
        "• Самовивіз з магазину",
        reply_markup=get_back_to_menu_keyboard()
    )
    
    await state.set_state(UserProfileState.waiting_for_address)

@router.message(UserProfileState.waiting_for_address)
async def update_address(message: Message, state: FSMContext):
    """Оновлення адреси"""
    address = message.text.strip()
    
    if not address or address == "🔙 Повернутися в меню":
        await back_to_menu(message, state)
        return
    
    # Отримуємо всі дані
    data = await state.get_data()
    phone = data.get('phone')
    name = data.get('name')
    
    # Зберігаємо дані користувача
    user_id = message.from_user.id
    update_user_data(user_id, {
        'phone': phone,
        'name': name,
        'address': address
    })
    
    await state.clear()
    
    success_text = (
        "✅ <b>Профіль оновлено!</b>\n\n"
        f"📞 Телефон: {phone}\n"
        f"👤 Ім'я: {name}\n"
        f"📍 Адреса: {address}\n\n"
        "Тепер ви можете швидко оформляти замовлення!"
    )
    
    await message.answer(
        success_text,
        reply_markup=get_main_menu(),
        parse_mode="HTML"
    )

@router.message(F.text == "🧾 Швидке замовлення")
async def quick_order(message: Message):
    """Швидке оформлення замовлення"""
    user_id = message.from_user.id
    cart_items = get_user_cart(user_id)
    
    if not cart_items:
        await message.answer(
            "🛒 Ваш кошик порожній!\n\n"
            "Спочатку додайте товари до кошика через каталог.",
            reply_markup=get_back_to_menu_keyboard()
        )
        return
    
    # Перевіряємо чи є дані користувача
    user_data = get_user_data(user_id)
    if not user_data.get('phone') or not user_data.get('name') or not user_data.get('address'):
        await message.answer(
            "⚠️ <b>Заповніть профіль</b>\n\n"
            "Для швидкого замовлення спочатку заповніть ваші дані в розділі \"👤 Моє\".",
            reply_markup=get_back_to_menu_keyboard(),
            parse_mode="HTML"
        )
        return
    
    total = get_cart_total(user_id)
    
    checkout_text = (
        "📋 <b>Швидке оформлення замовлення</b>\n\n"
        f"👤 Ім'я: {user_data.get('name')}\n"
        f"📞 Телефон: {user_data.get('phone')}\n"
        f"📍 Адреса: {user_data.get('address')}\n\n"
        f"💳 Сума до оплати: <b>{total} грн</b>\n\n"
        "Оберіть спосіб оплати:"
    )
    
    await message.answer(
        checkout_text,
        reply_markup=get_checkout_keyboard(),
        parse_mode="HTML"
    )