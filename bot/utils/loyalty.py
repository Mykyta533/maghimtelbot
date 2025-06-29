"""Система лояльності"""
from typing import Dict
from .database import load_data, save_data, LOYALTY_FILE

def get_user_loyalty_points(user_id: int) -> int:
    """Отримання балів лояльності користувача"""
    loyalty_data = load_data(LOYALTY_FILE)
    user_key = str(user_id)
    
    return loyalty_data.get(user_key, {}).get('points', 0)

def add_loyalty_points(user_id: int, points: int) -> bool:
    """Додавання балів лояльності"""
    try:
        loyalty_data = load_data(LOYALTY_FILE)
        user_key = str(user_id)
        
        if user_key not in loyalty_data:
            loyalty_data[user_key] = {'points': 0, 'total_earned': 0}
        
        loyalty_data[user_key]['points'] += points
        loyalty_data[user_key]['total_earned'] = loyalty_data[user_key].get('total_earned', 0) + points
        
        save_data(LOYALTY_FILE, loyalty_data)
        return True
        
    except Exception:
        return False

def use_loyalty_points(user_id: int, points: int) -> bool:
    """Використання балів лояльності"""
    try:
        loyalty_data = load_data(LOYALTY_FILE)
        user_key = str(user_id)
        
        if user_key not in loyalty_data:
            return False
        
        current_points = loyalty_data[user_key].get('points', 0)
        
        if current_points < points:
            return False
        
        loyalty_data[user_key]['points'] -= points
        save_data(LOYALTY_FILE, loyalty_data)
        return True
        
    except Exception:
        return False

def get_loyalty_discount(points: int) -> float:
    """Розрахунок знижки за бали (1 бал = 1 грн знижки)"""
    return float(points)