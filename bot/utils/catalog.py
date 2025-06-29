"""Робота з каталогом товарів"""
import json
import os

CATALOG_FILE = "catalog.json"

def load_catalog():
    """Завантаження каталогу товарів"""
    try:
        with open(CATALOG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
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