"""AI-помічник для консультацій"""
import os
import google.generativeai as genai
from typing import Optional
from .catalog import search_products, get_all_categories

# Налаштування Gemini
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

# Системний промпт для AI
SYSTEM_PROMPT = """
Ви - турботливий консультант магазину побутової хімії CleanWay в Тернополі. 

Ваша мета - допомогти клієнтам знайти найкращі рішення для їхніх потреб у прибиранні та гігієні.

Характеристики вашої комунікації:
- Турботливий та дружелюбний тон
- Фокус на здоров'ї родини та безпеці
- Практичні поради та рекомендації
- Завжди пропонуйте 1-2 конкретні товари з каталогу

Асортимент магазину:
- Засоби для прибирання (підлога, скло, поверхні)
- Гігієнічні товари (мило, шампуні, дезінфектори)
- Миючі засоби для посуду
- Побутові дрібниці (губки, серветки, рукавички)

Завжди відповідайте українською мовою та будьте корисними!
"""

async def process_text_query(query: str, user_id: int) -> str:
    """Обробка текстового запиту через Gemini"""
    try:
        model = genai.GenerativeModel('gemini-pro')
        
        # Шукаємо релевантні товари
        relevant_products = search_products(query)
        
        # Формуємо контекст з товарами
        products_context = ""
        if relevant_products:
            products_context = "\n\nДоступні товари в каталозі:\n"
            for product in relevant_products[:3]:  # Беремо топ-3 товари
                products_context += f"- {product['name']}: {product['description']} - {product['price']} грн\n"
        
        # Формуємо повний промпт
        full_prompt = f"{SYSTEM_PROMPT}\n\nЗапит клієнта: {query}{products_context}\n\nДайте корисну пораду та порекомендуйте товари:"
        
        response = model.generate_content(full_prompt)
        
        if response.text:
            return response.text
        else:
            return get_fallback_response(query)
            
    except Exception as e:
        return get_fallback_response(query)

async def process_voice_query(query: str, user_id: int) -> str:
    """Обробка голосового запиту (аналогічно текстовому)"""
    return await process_text_query(query, user_id)

def get_fallback_response(query: str) -> str:
    """Резервна відповідь при помилці AI"""
    # Простий аналіз ключових слів
    query_lower = query.lower()
    
    if any(word in query_lower for word in ['дзеркало', 'скло', 'вікно']):
        return (
            "🪟 Для миття дзеркал та скла рекомендую:\n\n"
            "✨ Використовуйте спеціальні засоби для скла\n"
            "🧽 Мийте круговими рухами, потім протирайте насухо\n"
            "📰 Для ідеального результату - газетний папір\n\n"
            "💡 Порада: мийте скло в похмуру погоду - воно повільніше сохне і не залишає розводів!"
        )
    
    elif any(word in query_lower for word in ['підлога', 'миття', 'прибирання']):
        return (
            "🏠 Для миття підлоги рекомендую:\n\n"
            "🧼 Використовуйте pH-нейтральні засоби\n"
            "💧 Не заливайте підлогу - вологе прибирання краще\n"
            "🧽 Різні поверхні потребують різних засобів\n\n"
            "👶 Для родин з дітьми - обирайте гіпоалергенні засоби!"
        )
    
    elif any(word in query_lower for word in ['дитина', 'безпечн', 'алергі']):
        return (
            "👶 Для родин з дітьми рекомендую:\n\n"
            "🌿 Екологічні засоби без агресивної хімії\n"
            "🏷  Шукайте позначки 'гіпоалергенно'\n"
            "🚫 Уникайте засобів з сильним запахом\n\n"
            "💚 Здоров'я вашої родини - наш пріоритет!"
        )
    
    else:
        return (
            "😊 Дякую за ваш запит!\n\n"
            "Я готовий допомогти вам з будь-якими питаннями щодо:\n"
            "🧼 Засобів для прибирання\n"
            "🧴 Гігієнічних товарів\n"
            "🍽 Миття посуду\n"
            "🏠 Догляду за домом\n\n"
            "Поставте більш конкретне запитання, і я дам детальну пораду!"
        )