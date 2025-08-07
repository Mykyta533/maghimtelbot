import os
import asyncio
from aiogram import Router, F
from aiogram.types import Message, Voice
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from keyboards.main_keyboards import get_back_to_menu_keyboard
from utils.ai_assistant import process_text_query, process_voice_query
from utils.voice_processing import voice_to_text, text_to_voice

router = Router()

class AIStates(StatesGroup):
    waiting_query = State()
    choosing_mode = State()

@router.message(F.text == "🤖 AI-помічник")
async def start_ai_assistant(message: Message, state: FSMContext):
    """Запуск AI-помічника"""
    from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
    
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="💬 Текстовий режим", callback_data="ai_text_mode"),
                InlineKeyboardButton(text="🎙 Голосовий режим", callback_data="ai_voice_mode")
            ],
            [
                InlineKeyboardButton(text="🔙 Назад в меню", callback_data="back_to_menu")
            ]
        ]
    )
    
    await message.answer(
        "🤖 <b>AI-помічник CleanWay</b>\n\n"
        "Привіт! Я ваш персональний консультант з питань прибирання та гігієни.\n\n"
        "Оберіть режим роботи:\n\n"
        "💬 <b>Текстовий</b> - пишіть запитання текстом\n"
        "🎙 <b>Голосовий</b> - надсилайте голосові повідомлення\n\n"
        "Приклади запитань:\n"
        "• Чим краще мити дзеркала без розводів?\n"
        "• Який засіб підійде для чутливої шкіри?\n"
        "• Як видалити плями з килима?",
        reply_markup=keyboard,
        parse_mode="HTML"
    )
    
    await state.set_state(AIStates.choosing_mode)

@router.callback_query(F.data == "ai_text_mode")
async def start_text_mode(callback: CallbackQuery, state: FSMContext):
    """Запуск текстового режиму"""
    await state.update_data(mode="text")
    await state.set_state(AIStates.waiting_query)
    
    await callback.message.edit_text(
        "💬 <b>Текстовий режим AI-помічника</b>\n\n"
        "Напишіть ваше запитання, і я дам детальну пораду та порекомендую підходящі товари! 😊",
        reply_markup=get_back_to_menu_keyboard()
    )
    await callback.answer()

@router.callback_query(F.data == "ai_voice_mode")
async def start_voice_mode(callback: CallbackQuery, state: FSMContext):
    """Запуск голосового режиму"""
    await state.update_data(mode="voice")
    await state.set_state(AIStates.waiting_query)
    
    await callback.message.edit_text(
        "🎙 <b>Голосовий режим AI-помічника</b>\n\n"
        "Надішліть голосове повідомлення з вашим запитанням, і я:\n"
        "• Розпізнаю вашу мову\n"
        "• Дам детальну відповідь\n"
        "• Порекомендую товари\n"
        "• Відповім голосом\n\n"
        "Говоріть чітко та не поспішайте! 🎯",
        reply_markup=get_back_to_menu_keyboard()
    )
    await callback.answer()

@router.message(AIStates.waiting_query, F.text)
async def handle_text_query(message: Message, state: FSMContext):
    """Обробка текстового запиту до AI"""
    if message.text == "🔙 Повернутися в меню":
        await state.clear()
        return
    
    # Показуємо, що бот обробляє запит
    processing_msg = await message.answer("🤔 Обробляю ваш запит...")
    
    try:
        # Обробка запиту через AI
        response = await process_text_query(message.text, message.from_user.id)
        
        # Видаляємо повідомлення про обробку
        await processing_msg.delete()
        
        # Надсилаємо відповідь
        await message.answer(
            response,
            reply_markup=get_back_to_menu_keyboard()
        )
        
    except Exception as e:
        await processing_msg.delete()
        await message.answer(
            "😔 Вибачте, сталася помилка при обробці вашого запиту.\n"
            "Спробуйте ще раз або зверніться до адміністратора.",
            reply_markup=get_back_to_menu_keyboard()
        )

@router.message(AIStates.waiting_query, F.voice)
async def handle_voice_query(message: Message, state: FSMContext):
    """Обробка голосового запиту до AI"""
    data = await state.get_data()
    mode = data.get('mode', 'voice')
    
    if mode != 'voice':
        await message.answer(
            "💬 Ви в текстовому режимі. Надішліть текстове повідомлення або поверніться в меню для зміни режиму.",
            reply_markup=get_back_to_menu_keyboard()
        )
        return
    
    processing_msg = await message.answer("🎙 Обробляю голосове повідомлення...")
    
    try:
        # Завантажуємо голосове повідомлення
        voice_file = await message.bot.get_file(message.voice.file_id)
        voice_path = f"temp_voice_{message.from_user.id}.ogg"
        
        await message.bot.download_file(voice_file.file_path, voice_path)
        
        # Конвертуємо голос у текст
        await processing_msg.edit_text("🔄 Розпізнаю мову...")
        text_query = await voice_to_text(voice_path)
        
        if not text_query:
            await processing_msg.delete()
            await message.answer(
                "😔 Не вдалося розпізнати мову. Спробуйте ще раз, говоріть чіткіше.",
                reply_markup=get_back_to_menu_keyboard()
            )
            return
        
        # Показуємо розпізнаний текст
        await processing_msg.edit_text(f"✅ Розпізнано: \"{text_query}\"\n\n🤖 Готую відповідь...")
        
        # Обробляємо запит через AI
        response = await process_voice_query(text_query, message.from_user.id)
        
        # Видаляємо повідомлення про обробку
        await processing_msg.delete()
        
        # Надсилаємо текстову відповідь
        await message.answer(
            f"🎙 <b>Ваш запит:</b> {text_query}\n\n"
            f"🤖 <b>Відповідь:</b>\n{response}",
            reply_markup=get_back_to_menu_keyboard()
        )
        
        # Генеруємо голосову відповідь
        voice_response_path = await text_to_voice(response, message.from_user.id)
        if voice_response_path and os.path.exists(voice_response_path):
            with open(voice_response_path, 'rb') as voice_file:
                await message.answer_voice(
                    voice_file,
                    caption="🔊 Голосова відповідь"
                )
            
            # Видаляємо тимчасовий файл
            os.remove(voice_response_path)
        
        # Видаляємо тимчасовий файл голосового запиту
        if os.path.exists(voice_path):
            os.remove(voice_path)
            
    except Exception as e:
        await processing_msg.delete()
        await message.answer(
            "😔 Вибачте, сталася помилка при обробці голосового повідомлення.\n"
            "Спробуйте ще раз або скористайтеся текстовим режимом.",
            reply_markup=get_back_to_menu_keyboard()
        )
        
        # Очищаємо тимчасові файли
        if os.path.exists(voice_path):
            os.remove(voice_path)

@router.message(AIStates.waiting_query)
async def invalid_text_input(message: Message):
    """Обробка некоректного вводу"""
    await message.answer(
        "💬 Будь ласка, надішліть текстове повідомлення або голосове (залежно від обраного режиму).\n\n"
        "Або натисніть кнопку \"🔙 Повернутися в меню\" для виходу.",
        reply_markup=get_back_to_menu_keyboard()
    )