"""Простий файловий менеджер даних (замість БД)"""
import json
import os
from datetime import datetime
from typing import Dict, List, Optional

# Шляхи до файлів даних
DATA_DIR = "data"
USERS_FILE = os.path.join(DATA_DIR, "users.json")
CART_FILE = os.path.join(DATA_DIR, "cart.json")
ORDERS_FILE = os.path.join(DATA_DIR, "orders.json")
LOYALTY_FILE = os.path.join(DATA_DIR, "loyalty.json")

async def init_db():
    """Ініціалізація файлової системи даних"""
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)
    
    # Створюємо файли якщо їх немає
    for file_path in [USERS_FILE, CART_FILE, ORDERS_FILE, LOYALTY_FILE]:
        if not os.path.exists(file_path):
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump({}, f, ensure_ascii=False, indent=2)

def load_data(file_path: str) -> Dict:
    """Завантаження даних з файлу"""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_data(file_path: str, data: Dict):
    """Збереження даних у файл"""
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def get_user_data(user_id: int) -> Dict:
    """Отримання даних користувача"""
    users = load_data(USERS_FILE)
    user_key = str(user_id)
    
    if user_key not in users:
        users[user_key] = {
            'id': user_id,
            'created_at': datetime.now().isoformat(),
            'paperless_receipts': False,
            'total_orders': 0,
            'total_spent': 0.0
        }
        save_data(USERS_FILE, users)
    
    return users[user_key]

def update_user_data(user_id: int, data: Dict):
    """Оновлення даних користувача"""
    users = load_data(USERS_FILE)
    user_key = str(user_id)
    
    if user_key in users:
        users[user_key].update(data)
        save_data(USERS_FILE, users)

def get_next_order_id() -> int:
    """Отримання наступного ID замовлення"""
    orders = load_data(ORDERS_FILE)
    if not orders:
        return 1
    
    max_id = 0
    for order_data in orders.values():
        for order in order_data:
            if order['id'] > max_id:
                max_id = order['id']
    
    return max_id + 1