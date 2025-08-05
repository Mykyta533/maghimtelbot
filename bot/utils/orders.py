"""Робота з замовленнями"""
from typing import List, Dict, Optional
from datetime import datetime
from .database import load_data, save_data, ORDERS_FILE, get_next_order_id, update_user_data, get_user_data
from .cart import get_user_cart, get_cart_total

def create_order(user_id: int, phone: str, address: str, total: float, payment_method: str) -> Optional[int]:
    """Створення нового замовлення"""
    try:
        orders_data = load_data(ORDERS_FILE)
        user_key = str(user_id)
        
        if user_key not in orders_data:
            orders_data[user_key] = []
        
        order_id = get_next_order_id()
        cart_items = get_user_cart(user_id)
        
        order = {
            'id': order_id,
            'user_id': user_id,
            'phone': phone,
            'address': address,
            'total': total,
            'payment_method': payment_method,
            'status': 'pending',
            'items': cart_items,
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        orders_data[user_key].append(order)
        save_data(ORDERS_FILE, orders_data)
        
        print(f"✅ Замовлення #{order_id} створено успішно для користувача {user_id}")
        
        # Оновлюємо статистику користувача
        user_data = get_user_data(user_id)
        update_user_data(user_id, {
            'total_orders': user_data.get('total_orders', 0) + 1,
            'total_spent': user_data.get('total_spent', 0) + total
        })
        
        return order_id
        
    except Exception as e:
        print(f"❌ Помилка створення замовлення: {e}")
        import traceback
        traceback.print_exc()
        return None

def get_user_orders(user_id: int) -> List[Dict]:
    """Отримання замовлень користувача"""
    orders_data = load_data(ORDERS_FILE)
    user_key = str(user_id)
    
    return orders_data.get(user_key, [])

def get_order_by_id(order_id: int) -> Optional[Dict]:
    """Отримання замовлення за ID"""
    orders_data = load_data(ORDERS_FILE)
    
    for user_orders in orders_data.values():
        for order in user_orders:
            if order['id'] == order_id:
                return order
    
    return None

def update_order_status(order_id: int, status: str) -> bool:
    """Оновлення статусу замовлення"""
    try:
        orders_data = load_data(ORDERS_FILE)
        
        for user_key, user_orders in orders_data.items():
            for order in user_orders:
                if order['id'] == order_id:
                    order['status'] = status
                    order['updated_at'] = datetime.now().isoformat()
                    save_data(ORDERS_FILE, orders_data)
                    return True
        
        return False
        
    except Exception:
        return False

def process_payment(order_id: int, payment_data: Dict) -> bool:
    """Обробка платежу"""
    # Тут би була інтеграція з платіжними системами
    # Поки що просто позначаємо як оплачено
    return update_order_status(order_id, 'processing')