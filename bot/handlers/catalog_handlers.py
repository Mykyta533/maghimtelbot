from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
import logging

from keyboards.catalog_keyboards import get_product_keyboard, get_categories_keyboard
from keyboards.main_keyboards import get_back_to_menu_keyboard
from utils.catalog import get_products_by_category, get_product_by_id, get_all_categories
from utils.cart import add_to_cart

router = Router()
logger = logging.getLogger(__name__)

@router.message(F.text == "🧼 Каталог")
async def show_catalog(message: Message):
    try:
        categories = get_all_categories()
        
        if not categories:
            await message.answer(
                "😔 Каталог товарів поки порожній",
                reply_markup=get_back_to_menu_keyboard()
            )
            return

        await message.answer(
            "🛍 <b>Каталог товарів CleanWay</b>\n\n"
            "Оберіть категорію товарів:",
            reply_markup=get_categories_keyboard(categories)
        )
    except Exception as e:
        logger.error(f"Error showing catalog: {e}")
        await message.answer(
            "❌ Помилка при завантаженні каталогу",
            reply_markup=get_back_to_menu_keyboard()
        )

@router.callback_query(F.data.startswith("category_"))
async def show_category_products(callback: CallbackQuery):
    try:
        category_id = callback.data.split("_", 1)[1]
    except (ValueError, IndexError):
        await callback.answer("❌ Невірний ID категорії", show_alert=True)
        return

    try:
        products = get_products_by_category(category_id)

        if not products:
            await callback.answer("В цій категорії поки немає товарів", show_alert=True)
            return

        await show_product_in_category(callback, products, 0)

    except Exception as e:
        logger.error(f"Error showing category products: {e}")
        await callback.answer("❌ Помилка при завантаженні товарів", show_alert=True)

@router.callback_query(F.data.startswith("product_"))
async def show_product_details(callback: CallbackQuery):
    try:
        product_id = int(callback.data.split("_")[1])
    except (ValueError, IndexError):
        await callback.answer("❌ Невірний ID товару", show_alert=True)
        return

    try:
        product = get_product_by_id(product_id)

        if not product:
            await callback.answer("Товар не знайдено", show_alert=True)
            return

        await show_single_product(callback, product)

    except Exception as e:
        logger.error(f"Error showing product details: {e}")
        await callback.answer("❌ Помилка при завантаженні товару", show_alert=True)

@router.callback_query(F.data.startswith("nav_"))
async def navigate_products(callback: CallbackQuery):
    try:
        _, category_id, index = callback.data.split("_")
        index = int(index)
    except (ValueError, IndexError):
        await callback.answer("❌ Невірні дані навігації", show_alert=True)
        return

    try:
        products = get_products_by_category(category_id)

        if not products or index < 0 or index >= len(products):
            await callback.answer("❌ Товар не знайдено", show_alert=True)
            return

        await show_product_in_category(callback, products, index)

    except Exception as e:
        logger.error(f"Error navigating products: {e}")
        await callback.answer("❌ Помилка навігації", show_alert=True)

@router.callback_query(F.data.startswith("add_to_cart_"))
async def add_product_to_cart(callback: CallbackQuery):
    try:
        # callback_data виглядає як "add_to_cart_5"
        product_id = int(callback.data.split("_")[-1])
    except (ValueError, IndexError):
        await callback.answer("❌ Невірний ID товару", show_alert=True)
        return

    try:
        user_id = callback.from_user.id
        product = get_product_by_id(product_id)

        if not product:
            await callback.answer("Товар не знайдено", show_alert=True)
            return

        if product.get('stock', 0) <= 0:
            await callback.answer("❌ Товар закінчився", show_alert=True)
            return

        success = add_to_cart(user_id, product_id, 1)

        if success:
            await callback.answer(f"✅ {product['name']} додано до кошика!", show_alert=True)
        else:
            await callback.answer("❌ Помилка при додаванні до кошика", show_alert=True)

    except Exception as e:
        logger.error(f"Error adding to cart: {e}")
        await callback.answer("❌ Помилка при додаванні до кошика", show_alert=True)

@router.callback_query(F.data.startswith("order_now_"))
async def order_now_from_catalog(callback: CallbackQuery):
    """Швидке замовлення товару з каталогу"""
    try:
        product_id = int(callback.data.split("_")[-1])
    except (ValueError, IndexError):
        await callback.answer("❌ Невірний ID товару", show_alert=True)
        return

    try:
        user_id = callback.from_user.id
        product = get_product_by_id(product_id)

        if not product:
            await callback.answer("Товар не знайдено", show_alert=True)
            return

        if product.get('stock', 0) <= 0:
            await callback.answer("❌ Товар закінчився", show_alert=True)
            return

        # Додаємо товар до кошика
        from utils.cart import add_to_cart, get_cart_total
        success = add_to_cart(user_id, product_id, 1)

        if not success:
            await callback.answer("❌ Помилка при додаванні до кошика", show_alert=True)
            return

        # Перевіряємо чи є дані користувача
        from utils.database import get_user_data
        user_data = get_user_data(user_id)
        
        if not user_data.get('phone') or not user_data.get('name') or not user_data.get('address'):
            await callback.message.edit_text(
                "⚠️ <b>Заповніть профіль</b>\n\n"
                "Для швидкого замовлення спочатку заповніть ваші дані в розділі \"👤 Моє\".",
                reply_markup=InlineKeyboardMarkup(inline_keyboard=[[
                    InlineKeyboardButton(text="👤 Заповнити профіль", callback_data="fill_profile"),
                    InlineKeyboardButton(text="🔙 Назад", callback_data=f"product_{product_id}")
                ]]),
                parse_mode="HTML"
            )
            return

        total = get_cart_total(user_id)
        
        from keyboards.cart_keyboards import get_checkout_keyboard
        checkout_text = (
            f"📋 <b>Швидке замовлення товару</b>\n\n"
            f"📦 Товар: {product['name']}\n"
            f"👤 Ім'я: {user_data.get('name')}\n"
            f"📞 Телефон: {user_data.get('phone')}\n"
            f"📍 Адреса: {user_data.get('address')}\n\n"
            f"💳 Сума до оплати: <b>{total} грн</b>\n\n"
            "Оберіть спосіб оплати:"
        )
        
        await callback.message.edit_text(
            checkout_text,
            reply_markup=get_checkout_keyboard(),
            parse_mode="HTML"
        )
        await callback.answer("✅ Товар додано до кошика!")

    except Exception as e:
        logger.error(f"Error in order now: {e}")
        await callback.answer("❌ Помилка при оформленні замовлення", show_alert=True)

@router.callback_query(F.data == "back_to_catalog")
async def back_to_catalog(callback: CallbackQuery):
    try:
        categories = get_all_categories()

        if not categories:
            await callback.message.edit_text(
                "😔 Каталог товарів поки порожній",
                reply_markup=get_back_to_menu_keyboard()
            )
            return

        await callback.message.edit_text(
            "🛌 <b>Каталог товарів CleanWay</b>\n\n"
            "Оберіть категорію товарів:",
            reply_markup=get_categories_keyboard(categories)
        )

        await callback.answer()

    except Exception as e:
        logger.error(f"Error returning to catalog: {e}")
        await callback.answer("❌ Помилка при поверненні до каталогу", show_alert=True)

async def show_product_in_category(callback: CallbackQuery, products: list, index: int):
    product = products[index]
    category_id = product.get('category')  # Ось тут правильний ключ

    text = (
        f"🧼 <b>{product['name']}</b>\n\n"
        f"📝 {product['description']}\n\n"
        f"💰 <b>Ціна: {product['price']} грн</b>\n"
        f"📦 В наявності: {product['stock']} шт.\n\n"
        f"📄 Товар {index + 1} з {len(products)}"
    )

    keyboard = get_product_keyboard(product['id'], index, len(products), category_id=category_id)
    await edit_message_with_media(callback, product, text, keyboard)

async def show_single_product(callback: CallbackQuery, product: dict):
    text = (
        f"🧼 <b>{product['name']}</b>\n\n"
        f"📝 {product['description']}\n\n"
        f"💰 <b>Ціна: {product['price']} грн</b>\n"
        f"📦 В наявності: {product['stock']} шт."
    )

    keyboard = get_product_keyboard(product['id'])
    await edit_message_with_media(callback, product, text, keyboard)

async def edit_message_with_media(callback: CallbackQuery, product: dict, text: str, keyboard):
    try:
        if product.get('image'):
            await callback.message.edit_media(
                InputMediaPhoto(
                    media=product['image'],
                    caption=text
                ),
                reply_markup=keyboard
            )
        else:
            await callback.message.edit_text(text, reply_markup=keyboard)
    except Exception as e:
        logger.error(f"Error editing message with media: {e}")
        try:
            await callback.message.edit_text(text, reply_markup=keyboard)
        except Exception as e2:
            logger.error(f"Error editing message text: {e2}")
            await callback.message.answer(text, reply_markup=keyboard)

    await callback.answer()
