from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.fsm.context import FSMContext

from keyboards.main_keyboards import get_main_menu, get_back_to_menu_keyboard
from utils.messages import WELCOME_MESSAGE, SHOP_ADDRESS, CONTACT_INFO

router = Router()

@router.message(CommandStart())
async def start_command(message: Message, state: FSMContext):
    """Обробка команди /start"""
    await state.clear()
    
    await message.answer(
        WELCOME_MESSAGE,
        reply_markup=get_main_menu()
    )

@router.message(F.text == "🔙 Повернутися в меню")
async def back_to_menu(message: Message, state: FSMContext):
    """Повернення в головне меню"""
    await state.clear()
    
    await message.answer(
        "Головне меню:",
        reply_markup=get_main_menu()
    )

@router.message(F.text == "📍 Адреса магазину")
async def shop_address(message: Message):
    """Показ адреси магазину"""
    await message.answer(
        SHOP_ADDRESS,
        reply_markup=get_back_to_menu_keyboard()
    )

@router.message(F.text == "📞 Зв'язатися")
async def contact_info(message: Message):
    """Контактна інформація"""
    await message.answer(
        CONTACT_INFO,
        reply_markup=get_back_to_menu_keyboard()
    )