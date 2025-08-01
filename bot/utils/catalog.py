import json
import os
import logging

logger = logging.getLogger(__name__)

# Визначаємо базову директорію проєкту (корінь)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))

# Повний шлях до файлу catalog.json у корені проєкту
CATALOG_FILE = os.path.join(BASE_DIR, "catalog.json")

def load_catalog():
    """Завантаження каталогу товарів"""
    try:
        with open(CATALOG_FILE, 'r', encoding='utf-8') as f:
            catalog = json.load(f)
            logger.info(f"Каталог завантажено: {len(catalog.get('products', []))} товарів, {len(catalog.get('categories', []))} категорій")
            return catalog
    except FileNotFoundError:
        logger.error(f"Файл {CATALOG_FILE} не знайдено!")
        return {"categories": [], "products": []}
    except json.JSONDecodeError as e:
        logger.error(f"Помилка декодування JSON: {e}")
        return {"categories": [], "products": []}

def get_all_categories():
    """Отримання всіх категорій"""
    catalog = load_catalog()
    return catalog.get("categories", [])

def get_products_by_category(category_id: str):
    """Отримання товарів за категорією"""
    catalog = load_catalog()
    products = catalog.get("products", [])
    
    if category_id == "all":
        return products
    
    # category_id - рядок, наприклад "cleaning"
    return [p for p in products if p.get("category") == category_id]

def get_product_by_id(product_id: int):
    """Отримання товару за ID"""
    catalog = load_catalog()
    products = catalog.get("products", [])
    
    for product in products:
        if product.get("id") == product_id:
            return product
    
    return None

def search_products(query: str):
    """Пошук товарів за запитом"""
    catalog = load_catalog()
    products = catalog.get("products", [])
    
    query = query.lower()
    results = []
    
    for product in products:
        if (query in product.get("name", "").lower() or 
            query in product.get("description", "").lower() or
            query in product.get("tags", "").lower()):
            results.append(product)
    
    return results
