"""Робота з кошиком користувача"""
from typing import List, Dict, Optional
from .database import load_data, save_data, CART_FILE
from .catalog import get_product_by_id


def get_user_cart(user_id: int) -> List[Dict]:
    """Отримання кошика користувача"""
    try:
        cart_data = load_data(CART_FILE)
        user_key = str(user_id)
        return cart_data.get(user_key, [])
    except Exception as e:
        print(f"Помилка отримання кошика: {e}")
        return []


def add_to_cart(user_id: int, product_id: int, quantity: int = 1) -> bool:
    """Додавання товару до кошика"""
    if quantity <= 0:
        return False
    
    # Перевіряємо чи існує товар
    product = get_product_by_id(product_id)
    if not product:
        print(f"Товар з ID {product_id} не знайдено")
        return False
    
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
                # Обмежуємо максимальну кількість
                if item['quantity'] > 99:
                    item['quantity'] = 99
                save_data(CART_FILE, cart_data)
                return True
        
        # Додаємо новий товар
        user_cart.append({
            'product_id': product_id,
            'quantity': min(quantity, 99)  # Обмежуємо кількість
        })
        
        save_data(CART_FILE, cart_data)
        return True
        
    except Exception as e:
        print(f"Помилка додавання до кошика: {e}")
        return False


def update_cart_item(user_id: int, product_id: int, quantity: int) -> bool:
    """Оновлення кількості товару в кошику"""
    try:
        cart_data = load_data(CART_FILE)
        user_key = str(user_id)
        
        if user_key not in cart_data:
            return False
        
        user_cart = cart_data[user_key]
        
        # Безпечне видалення - створюємо новий список
        for i, item in enumerate(user_cart):
            if item['product_id'] == product_id:
                if quantity <= 0:
                    # Видаляємо товар з кошика
                    user_cart.pop(i)
                else:
                    # Обмежуємо максимальну кількість
                    item['quantity'] = min(quantity, 99)
                
                save_data(CART_FILE, cart_data)
                return True
        
        return False
        
    except Exception as e:
        print(f"Помилка оновлення кошика: {e}")
        return False


def remove_from_cart(user_id: int, product_id: int) -> bool:
    """Видалення товару з кошика"""
    try:
        cart_data = load_data(CART_FILE)
        user_key = str(user_id)
        
        if user_key not in cart_data:
            return False
        
        user_cart = cart_data[user_key]
        
        # Безпечне видалення
        for i, item in enumerate(user_cart):
            if item['product_id'] == product_id:
                user_cart.pop(i)
                save_data(CART_FILE, cart_data)
                return True
        
        return False
        
    except Exception as e:
        print(f"Помилка видалення з кошика: {e}")
        return False


def clear_cart(user_id: int) -> bool:
    """Очищення кошика користувача"""
    try:
        cart_data = load_data(CART_FILE)
        user_key = str(user_id)
        
        cart_data[user_key] = []
        save_data(CART_FILE, cart_data)
        return True
        
    except Exception as e:
        print(f"Помилка очищення кошика: {e}")
        return False


def get_cart_total(user_id: int) -> int:
    """Розрахунок загальної суми кошика"""
    cart_items = get_user_cart(user_id)
    total = 0
    
    for item in cart_items:
        product = get_product_by_id(item['product_id'])
        if product:
            # Переконуємося що price та quantity є числами
            try:
                price = int(product['price']) if isinstance(product['price'], (int, float, str)) else 0
                quantity = int(item['quantity']) if isinstance(item['quantity'], (int, float, str)) else 0
                total += price * quantity
            except (ValueError, TypeError):
                print(f"Помилка обчислення для товару {product.get('name', 'Unknown')}")
                continue
    
    return total


def get_cart_item_count(user_id: int) -> int:
    """Отримання кількості різних товарів в кошику"""
    cart_items = get_user_cart(user_id)
    return len(cart_items)


def get_cart_total_quantity(user_id: int) -> int:
    """Отримання загальної кількості товарів в кошику"""
    cart_items = get_user_cart(user_id)
    total_quantity = 0
    
    for item in cart_items:
        try:
            quantity = int(item['quantity']) if isinstance(item['quantity'], (int, float, str)) else 0
            total_quantity += quantity
        except (ValueError, TypeError):
            continue
    
    return total_quantity


def is_product_in_cart(user_id: int, product_id: int) -> bool:
    """Перевірка чи є товар в кошику"""
    cart_items = get_user_cart(user_id)
    return any(item['product_id'] == product_id for item in cart_items)


def get_cart_item_quantity(user_id: int, product_id: int) -> int:
    """Отримання кількості конкретного товару в кошику"""
    cart_items = get_user_cart(user_id)
    
    for item in cart_items:
        if item['product_id'] == product_id:
            try:
                return int(item['quantity']) if isinstance(item['quantity'], (int, float, str)) else 0
            except (ValueError, TypeError):
                return 0
    
    return 0


def validate_cart(user_id: int) -> bool:
    """Валідація кошика - видалення неіснуючих товарів"""
    try:
        cart_data = load_data(CART_FILE)
        user_key = str(user_id)
        
        if user_key not in cart_data:
            return True
        
        user_cart = cart_data[user_key]
        valid_items = []
        
        for item in user_cart:
            product = get_product_by_id(item['product_id'])
            if product:
                # Перевіряємо та виправляємо кількість
                try:
                    quantity = int(item['quantity'])
                    if 1 <= quantity <= 99:
                        valid_items.append({
                            'product_id': item['product_id'],
                            'quantity': quantity
                        })
                except (ValueError, TypeError):
                    continue
        
        # Оновлюємо кошик тільки валідними товарами
        cart_data[user_key] = valid_items
        save_data(CART_FILE, cart_data)
        
        return True
        
    except Exception as e:
        print(f"Помилка валідації кошика: {e}")
        return False
