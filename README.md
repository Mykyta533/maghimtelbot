# CleanWay - Telegram Bot з React Admin Panel

Повноцінна система для магазину побутової хімії CleanWay з Telegram-ботом та веб-панеллю адміністратора.

## 🚀 Особливості

### Telegram Bot
- 🤖 AI-помічник (текстовий та голосовий)
- 🛒 Повноцінний інтернет-магазин
- 💳 Інтеграція з LiqPay та WayForPay
- 🎁 Програма лояльності з кешбеком 5%
- 📱 Голосові команди через Whisper API
- 🧾 Електронні чеки

### Admin Panel
- 📊 Дашборд з аналітикою
- 📦 Управління каталогом товарів
- 👥 Управління користувачами
- 🛍 Відстеження замовлень
- ⚙️ Налаштування бота

## 🛠 Технології

### Frontend (Admin Panel)
- React 18 + TypeScript
- Tailwind CSS
- Recharts для графіків
- Lucide React для іконок

### Backend (Telegram Bot)
- Python 3.9+
- aiogram 3.x
- Google Gemini API
- OpenAI Whisper
- gTTS для озвучення

## 📦 Встановлення

### 1. Клонування репозиторію
```bash
git clone <repository-url>
cd cleanway-system
```

### 2. Налаштування Admin Panel
```bash
npm install
npm run dev
```

### 3. Налаштування Telegram Bot
```bash
cd bot
pip install -r requirements.txt
```

### 4. Налаштування змінних середовища
Створіть файл `bot/.env` на основі `bot/.env.example`:

```env
BOT_TOKEN=your_telegram_bot_token
ADMIN_ID=your_telegram_user_id
GEMINI_API_KEY=your_gemini_api_key
WHISPER_API_KEY=your_whisper_api_key
LIQPAY_PUBLIC_KEY=your_liqpay_public_key
LIQPAY_PRIVATE_KEY=your_liqpay_private_key
WAYFORPAY_MERCHANT_ACCOUNT=your_wayforpay_account
WAYFORPAY_SECRET_KEY=your_wayforpay_secret
```

### 5. Запуск бота
```bash
cd bot
python bot.py
```

## 🎯 Функціональність бота

### Головне меню
- 🧼 Каталог товарів
- 🎁 Акції та знижки
- 🛒 Кошик покупок
- 🤖 AI-помічник (текстовий)
- 🎙 AI-помічник (голосовий)
- 🧾 Оформлення замовлення
- 🧮 Історія покупок
- 🧧 Електронні чеки
- 📍 Адреса магазину
- 📞 Контакти

### AI-помічник
- Розпізнавання голосових команд
- Персоналізовані рекомендації товарів
- Консультації з прибирання та гігієни
- Голосові відповіді

### Система замовлень
- Онлайн-оплата через LiqPay/WayForPay
- Автоматичні повідомлення адміністратору
- Відстеження статусу замовлення
- Електронні чеки

### Програма лояльності
- 5% кешбек з кожної покупки
- Накопичення та використання балів
- Персональні знижки

## 🔧 Розробка

### Структура проекту
```
cleanway-system/
├── src/                    # React Admin Panel
│   ├── components/         # React компоненти
│   └── ...
├── bot/                    # Telegram Bot
│   ├── handlers/          # Обробники команд
│   ├── keyboards/         # Клавіатури бота
│   ├── utils/            # Утиліти
│   └── bot.py            # Головний файл бота
├── catalog.json          # Каталог товарів
└── README.md
```

### Додавання нових товарів
Редагуйте файл `catalog.json` або використовуйте Admin Panel.

### Налаштування AI
Змініть системний промпт у файлі `bot/utils/ai_assistant.py`.

## 🚀 Деплой

### Admin Panel
```bash
npm run build
# Деплой на Netlify, Vercel або інший хостинг
```

### Telegram Bot
Рекомендовані платформи:
- Railway
- Render
- Heroku
- VPS сервер

## 📞 Підтримка

Для питань та підтримки звертайтеся:
- Email: support@cleanway.te.ua
- Telegram: @cleanway_support

## 📄 Ліцензія

MIT License - деталі в файлі LICENSE.