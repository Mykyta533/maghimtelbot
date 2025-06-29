from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InputMediaPhoto
from aiogram.fsm.context import FSMContext

from keyboards.catalog_keyboards import get_catalog_menu, get_product_keyboard, get_categories_keyboard
from keyboards.main_keyboards import get_back_to_menu_keyboard
from utils.catalog import get_products_by_category, get_product_by_id, get_all_categories
from utils.cart import add_to_cart

router = Router()

@router.message(F.text == "🧼 Каталог")
async def show_catalog(message: Message):
    """Показ каталогу товарів"""
    categories = get_all_categories()
    
    await message.answer(
        "🛍 <b>Каталог товарів CleanWay</b>\n\n"
        "Оберіть категорію товарів:",
        reply_markup=get_categories_keyboard(categories)
    )

@router.callback_query(F.data.startswith("category_"))
async def show_category_products(callback: CallbackQuery):
    """Показ товарів категорії"""
    category_id = callback.data.split("_")[1]
    products = get_products_by_category(category_id)
    
    if not products:
        await callback.answer("В цій категорії поки немає товарів", show_alert=True)
        return
    
    # Показуємо перший товар
    product = products[0]
    
    text = (
        f"🧼 <b>{product['name']}</b>\n\n"
        f"📝 {product['description']}\n\n"
        f"💰 <b>Ціна: {product['price']} грн</b>\n"
        f"📦 В наявності: {product['stock']} шт."
    )
    
    try:
        await callback.message.edit_media(
            InputMediaPhoto(
                media=product['image'],
                caption=text
            ),
            reply_markup=get_product_keyboard(product['id'], 0, len(products))
        )
    except:
        await callback.message.edit_text(
            text,
            reply_markup=get_product_keyboard(product['id'], 0, len(products))
        )
    
    await callback.answer()

@router.callback_query(F.data.startswith("product_"))
async def show_product_details(callback: CallbackQuery):
    """Показ деталей товару"""
    product_id = int(callback.data.split("_")[1])
    product = get_product_by_id(product_id)
    
    if not product:
        await callback.answer("Товар не знайдено", show_alert=True)
        return
    
    text = (
        f"🧼 <b>{product['name']}</b>\n\n"
        f"📝 {product['description']}\n\n"
        f"💰 <b>Ціна: {product['price']} грн</b>\n"
        f"📦 В наявності: {product['stock']} шт."
    )
    
    try:
        await callback.message.edit_media(
            InputMediaPhoto(
                media=product['image'],
                caption=text
            ),
            reply_markup=get_product_keyboard(product['id'])
        )
    except:
        await callback.message.edit_text(
            text,
            reply_markup=get_product_keyboard(product['id'])
        )
    
    await callback.answer()

@router.callback_query(F.data.startswith("add_to_cart_"))
async def add_product_to_cart(callback: CallbackQuery):
    """Додавання товару до кошика"""
    product_id = int(callback.data.split("_")[3])
    user_id = callback.from_user.id
    
    product = get_product_by_id(product_id)
    if not product:
        await callback.answer("Товар не знайдено", show_alert=True)
        return
    
    success = add_to_cart(user_id, product_id, 1)
    
    if success:
        await callback.answer(
            f"✅ {product['name']} додано до кошика!",
            show_alert=True
        )
    else:
        await callback.answer(
            "❌ Помилка при додаванні до кошика",
            show_alert=True
        )

@router.callback_query(F.data == "back_to_catalog")
async def back_to_catalog(callback: CallbackQuery):
    """Повернення до каталогу"""
    categories = get_all_categories()
    
    await callback.message.edit_text(
        "🛍 <b>Каталог товарів CleanWay</b>\n\n"
        "Оберіть категорію товарів:",
        reply_markup=get_categories_keyboard(categories)
    )
    
    await callback.answer()