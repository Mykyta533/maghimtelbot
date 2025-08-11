"""
Keep Alive модуль для Replit
Запускає простий веб-сервер щоб тримати бота активним
"""
from flask import Flask
from threading import Thread
import logging

app = Flask('')

@app.route('/')
def home():
    return """
    <h1>🧼 CleanWay Telegram Bot</h1>
    <p>✅ Бот працює!</p>
    <p>📱 Знайдіть бота в Telegram: @cleanway_bot</p>
    """

@app.route('/health')
def health():
    return {"status": "ok", "message": "Bot is running"}

def run():
    app.run(host='0.0.0.0', port=8080, debug=False)

def keep_alive():
    t = Thread(target=run)
    t.daemon = True
    t.start()
    logging.info("🌐 Keep-alive сервер запущено на порту 8080")