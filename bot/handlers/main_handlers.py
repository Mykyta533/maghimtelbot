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

@router.message(F.text == "💳 QR карта")
async def qr_card(message: Message):
    """QR карта користувача з балами та купонами"""
    user_id = message.from_user.id
    user_data = get_user_data(user_id)
    
    # Отримуємо бали лояльності
    from utils.loyalty import get_user_loyalty_points
    loyalty_points = get_user_loyalty_points(user_id)
    
    # Генеруємо унікальний QR код для користувача
    qr_code = f"CW{user_id:08d}"
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🎟 Мої купони", callback_data="my_coupons"),
                InlineKeyboardButton(text="🎁 Акції", callback_data="show_promotions")
            ],
            [
                InlineKeyboardButton(text="📊 Історія балів", callback_data="points_history")
            ],
            [
                InlineKeyboardButton(text="🔙 Головне меню", callback_data="back_to_menu")
            ]
        ]
    )
    
    qr_text = (
        f"💳 <b>Ваша QR карта CleanWay</b>\n\n"
        f"🆔 Номер карти: <code>{qr_code}</code>\n"
        f"👤 Власник: {user_data.get('name', 'Не вказано')}\n"
        f"📞 Телефон: {user_data.get('phone', 'Не вказано')}\n\n"
        f"💎 <b>Ваші бали: {loyalty_points}</b>\n"
        f"💰 Еквівалент: {loyalty_points} грн знижки\n\n"
        f"🎯 <b>Програма лояльності:</b>\n"
        f"• 5% кешбек з кожної покупки\n"
        f"• 1 бал = 1 грн знижки\n"
        f"• Спеціальні пропозиції для VIP клієнтів\n\n"
        f"📱 Покажіть цей QR код касиру для нарахування балів!"
    )
    
    await message.answer(
        qr_text,
        reply_markup=keyboard,
        parse_mode="HTML"
    )

@router.callback_query(F.data == "my_coupons")
async def show_my_coupons(callback: CallbackQuery):
    """Показати купони користувача"""
    user_id = callback.from_user.id
    
    # Тут би була логіка отримання купонів користувача
    # Поки що показуємо доступні купони
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🎁 Переглянути акції", callback_data="show_promotions")
            ],
            [
                InlineKeyboardButton(text="🔙 Назад до QR карти", callback_data="back_to_qr")
            ]
        ]
    )
    
    coupons_text = (
        "🎟 <b>Ваші купони</b>\n\n"
        "У вас поки немає активних купонів.\n\n"
        "💡 <b>Як отримати купони:</b>\n"
        "• Робіть покупки та накопичуйте бали\n"
        "• Слідкуйте за акціями в розділі \"🎁 Акції\"\n"
        "• Підписуйтесь на наші соціальні мережі\n\n"
        "🎯 Перегляньте поточні акції, щоб не пропустити вигідні пропозиції!"
    )
    
    await callback.message.edit_text(
        coupons_text,
        reply_markup=keyboard,
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(F.data == "show_promotions")
async def show_promotions(callback: CallbackQuery):
    """Показати акції та знижки"""
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🛍 Перейти до каталогу", callback_data="show_catalog")
            ],
            [
                InlineKeyboardButton(text="🔙 Назад", callback_data="back_to_qr")
            ]
        ]
    )
    
    promotions_text = (
        "🎁 <b>Поточні акції та знижки</b>\n\n"
        "🔥 <b>Гарячі пропозиції:</b>\n\n"
        "1️⃣ <b>Знижка 20% на засоби для прибирання</b>\n"
        "   • ECO Baby Clean - 71.99 грн замість 89.99 грн\n"
        "   • Glass Master Pro - 52.40 грн замість 65.50 грн\n"
        "   • Multi-Surface Cleaner - 58.60 грн замість 73.25 грн\n\n"
        "2️⃣ <b>Купи 2 - отримай 3-й безкоштовно</b>\n"
        "   • На всю косметику для обличчя\n"
        "   • Діє до кінця місяця\n\n"
        "3️⃣ <b>Знижка 15% на парфуми</b>\n"
        "   • При покупці від 500 грн\n"
        "   • Промокод: PARFUM15\n\n"
        "4️⃣ <b>Безкоштовна доставка</b>\n"
        "   • При замовленні від 300 грн\n"
        "   • По всій Україні\n\n"
        "5️⃣ <b>Подвійні бали лояльності</b>\n"
        "   • 10% замість 5% кешбек\n"
        "   • На вихідних\n\n"
        "⏰ <b>Акції діють обмежений час!</b>"
    )
    
    await callback.message.edit_text(
        promotions_text,
        reply_markup=keyboard,
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(F.data == "points_history")
async def show_points_history(callback: CallbackQuery):
    """Показати історію балів"""
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🔙 Назад до QR карти", callback_data="back_to_qr")
            ]
        ]
    )
    
    history_text = (
        "📊 <b>Історія балів лояльності</b>\n\n"
        "📈 <b>Останні операції:</b>\n\n"
        "🟢 +12 балів - Покупка 15.01.2024\n"
        "   Замовлення #001, сума 245 грн\n\n"
        "🟢 +4 балів - Покупка 12.01.2024\n"
        "   Замовлення #002, сума 89 грн\n\n"
        "🔴 -50 балів - Використано 10.01.2024\n"
        "   Знижка на замовлення #003\n\n"
        "💎 <b>Загальна статистика:</b>\n"
        "• Всього нараховано: 156 балів\n"
        "• Використано: 50 балів\n"
        "• Поточний баланс: 106 балів\n"
        "• Економія за весь час: 50 грн\n\n"
        "🎯 Продовжуйте робити покупки та накопичуйте бали!"
    )
    
    await callback.message.edit_text(
        history_text,
        reply_markup=keyboard,
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(F.data == "back_to_qr")
async def back_to_qr_card(callback: CallbackQuery):
    """Повернення до QR карти"""
    # Повторюємо логіку з qr_card
    user_id = callback.from_user.id
    user_data = get_user_data(user_id)
    
    from utils.loyalty import get_user_loyalty_points
    loyalty_points = get_user_loyalty_points(user_id)
    
    qr_code = f"CW{user_id:08d}"
    
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="🎟 Мої купони", callback_data="my_coupons"),
                InlineKeyboardButton(text="🎁 Акції", callback_data="show_promotions")
            ],
            [
                InlineKeyboardButton(text="📊 Історія балів", callback_data="points_history")
            ],
            [
                InlineKeyboardButton(text="🔙 Головне меню", callback_data="back_to_menu")
            ]
        ]
    )
    
    qr_text = (
        f"💳 <b>Ваша QR карта CleanWay</b>\n\n"
        f"🆔 Номер карти: <code>{qr_code}</code>\n"
        f"👤 Власник: {user_data.get('name', 'Не вказано')}\n"
        f"📞 Телефон: {user_data.get('phone', 'Не вказано')}\n\n"
        f"💎 <b>Ваші бали: {loyalty_points}</b>\n"
        f"💰 Еквівалент: {loyalty_points} грн знижки\n\n"
        f"🎯 <b>Програма лояльності:</b>\n"
        f"• 5% кешбек з кожної покупки\n"
        f"• 1 бал = 1 грн знижки\n"
        f"• Спеціальні пропозиції для VIP клієнтів\n\n"
        f"📱 Покажіть цей QR код касиру для нарахування балів!"
    )
    
    await callback.message.edit_text(
        qr_text,
        reply_markup=keyboard,
        parse_mode="HTML"
    )
    await callback.answer()