"""Робота з кошиком користувача"""
from typing import List, Dict, Optional
from .database import load_data, save_data, CART_FILE
from .catalog import get_product_by_id

def get_user_cart(user_id: int) -> List[Dict]:
    """Отримання кошика користувача"""
    cart_data = load_data(CART_FILE)
    user_key = str(user_id)
    
    return cart_data.get(user_key, [])

def add_to_cart(user_id: int, product_id: int, quantity: int = 1) -> bool:
    """Додавання товару до кошика"""
    try:
        cart_data = load_data(CART_FILE)
        user_key = str(user_id)
        
        if user_key not in cart_data:
            cart_data[user_key] = []
        
        user_cart = cart_data[user_key]
        
        # Перевіряємо чи товар вже є в кошику
        for item in user_cart:
            if item['product_id'] == product_id:
                item['quantity'] += quantity
                save_data(CART_FILE, cart_data)
                return True
        
        # Додаємо новий товар
        user_cart.append({
            'product_id': product_id,
            'quantity': quantity
        })
        
        save_data(CART_FILE, cart_data)
        return True
        
    except Exception:
        return False

def update_cart_item(user_id: int, product_id: int, quantity: int) -> bool:
    """Оновлення кількості товару в кошику"""
    try:
        cart_data = load_data(CART_FILE)
        user_key = str(user_id)
        
        if user_key not in cart_data:
            return False
        
        user_cart = cart_data[user_key]
        
        for item in user_cart:
            if item['product_id'] == product_id:
                if quantity <= 0:
                    user_cart.remove(item)
                else:
                    item['quantity'] = quantity
                
                save_data(CART_FILE, cart_data)
                return True
        
        return False
        
    except Exception:
        return False

def remove_from_cart(user_id: int, product_id: int) -> bool:
    """Видалення товару з кошика"""
    try:
        cart_data = load_data(CART_FILE)
        user_key = str(user_id)
        
        if user_key not in cart_data:
            return False
        
        user_cart = cart_data[user_key]
        
        for item in user_cart:
            if item['product_id'] == product_id:
                user_cart.remove(item)
                save_data(CART_FILE, cart_data)
                return True
        
        return False
        
    except Exception:
        return False

def clear_cart(user_id: int) -> bool:
    """Очищення кошика користувача"""
    try:
        cart_data = load_data(CART_FILE)
        user_key = str(user_id)
        
        cart_data[user_key] = []
        save_data(CART_FILE, cart_data)
        return True
        
    except Exception:
        return False

def get_cart_total(user_id: int) -> float:
    """Розрахунок загальної суми кошика"""
    cart_items = get_user_cart(user_id)
    total = 0.0
    
    for item in cart_items:
        product = get_product_by_id(item['product_id'])
        if product:
            total += product['price'] * item['quantity']
    
    return total