import React, { useState } from 'react';
import { Save, Bot, MessageSquare, Mic, CreditCard, Gift, MapPin } from 'lucide-react';

const BotSettings = () => {
  const [settings, setSettings] = useState({
    botToken: 'YOUR_BOT_TOKEN',
    adminId: '123456789',
    geminiApiKey: 'YOUR_GEMINI_API_KEY',
    whisperApiKey: 'YOUR_WHISPER_API_KEY',
    liqpayPublicKey: 'YOUR_LIQPAY_PUBLIC_KEY',
    liqpayPrivateKey: 'YOUR_LIQPAY_PRIVATE_KEY',
    wayforpayMerchantAccount: 'YOUR_WAYFORPAY_ACCOUNT',
    wayforpaySecretKey: 'YOUR_WAYFORPAY_SECRET',
    shopAddress: 'вул. Руська, 15, Тернопіль',
    shopPhone: '+380 67 123 45 67',
    loyaltyRate: 5,
    welcomeMessage: 'Вітаємо в CleanWay! 🧼\n\nВаш надійний помічник у світі чистоти та гігієни. Оберіть потрібний розділ з меню нижче.',
    aiPersonality: 'Ви - турботливий консультант магазину побутової хімії CleanWay. Завжди допомагаєте клієнтам знайти найкращі рішення для їхніх потреб у прибиранні та гігієні.'
  });

  const handleSave = () => {
    // Here you would save settings to backend
    alert('Налаштування збережено!');
  };

  return (
    <div className="space-y-8">
      <div className="flex justify-between items-center">
        <h2 className="text-2xl font-bold text-gray-900">Налаштування бота</h2>
        <button
          onClick={handleSave}
          className="bg-gradient-to-r from-blue-600 to-purple-600 text-white px-6 py-2 rounded-lg hover:shadow-lg transition-all duration-200 flex items-center space-x-2"
        >
          <Save className="h-5 w-5" />
          <span>Зберегти</span>
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Bot Configuration */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <div className="flex items-center space-x-3 mb-6">
            <Bot className="h-6 w-6 text-blue-600" />
            <h3 className="text-lg font-semibold text-gray-900">Основні налаштування</h3>
          </div>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Токен бота
              </label>
              <input
                type="password"
                value={settings.botToken}
                onChange={(e) => setSettings({...settings, botToken: e.target.value})}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                ID адміністратора
              </label>
              <input
                type="text"
                value={settings.adminId}
                onChange={(e) => setSettings({...settings, adminId: e.target.value})}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Привітальне повідомлення
              </label>
              <textarea
                value={settings.welcomeMessage}
                onChange={(e) => setSettings({...settings, welcomeMessage: e.target.value})}
                rows={4}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>
        </div>

        {/* AI Configuration */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <div className="flex items-center space-x-3 mb-6">
            <MessageSquare className="h-6 w-6 text-purple-600" />
            <h3 className="text-lg font-semibold text-gray-900">AI налаштування</h3>
          </div>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Gemini API ключ
              </label>
              <input
                type="password"
                value={settings.geminiApiKey}
                onChange={(e) => setSettings({...settings, geminiApiKey: e.target.value})}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Whisper API ключ
              </label>
              <input
                type="password"
                value={settings.whisperApiKey}
                onChange={(e) => setSettings({...settings, whisperApiKey: e.target.value})}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Особистість AI
              </label>
              <textarea
                value={settings.aiPersonality}
                onChange={(e) => setSettings({...settings, aiPersonality: e.target.value})}
                rows={3}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>
        </div>

        {/* Payment Configuration */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <div className="flex items-center space-x-3 mb-6">
            <CreditCard className="h-6 w-6 text-green-600" />
            <h3 className="text-lg font-semibold text-gray-900">Платіжні системи</h3>
          </div>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                LiqPay Public Key
              </label>
              <input
                type="text"
                value={settings.liqpayPublicKey}
                onChange={(e) => setSettings({...settings, liqpayPublicKey: e.target.value})}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                LiqPay Private Key
              </label>
              <input
                type="password"
                value={settings.liqpayPrivateKey}
                onChange={(e) => setSettings({...settings, liqpayPrivateKey: e.target.value})}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                WayForPay Merchant Account
              </label>
              <input
                type="text"
                value={settings.wayforpayMerchantAccount}
                onChange={(e) => setSettings({...settings, wayforpayMerchantAccount: e.target.value})}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                WayForPay Secret Key
              </label>
              <input
                type="password"
                value={settings.wayforpaySecretKey}
                onChange={(e) => setSettings({...settings, wayforpaySecretKey: e.target.value})}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>
        </div>

        {/* Shop Information */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <div className="flex items-center space-x-3 mb-6">
            <MapPin className="h-6 w-6 text-red-600" />
            <h3 className="text-lg font-semibold text-gray-900">Інформація про магазин</h3>
          </div>
          
          <div className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Адреса магазину
              </label>
              <input
                type="text"
                value={settings.shopAddress}
                onChange={(e) => setSettings({...settings, shopAddress: e.target.value})}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Телефон магазину
              </label>
              <input
                type="text"
                value={settings.shopPhone}
                onChange={(e) => setSettings({...settings, shopPhone: e.target.value})}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Відсоток кешбеку (%)
              </label>
              <input
                type="number"
                min="0"
                max="100"
                value={settings.loyaltyRate}
                onChange={(e) => setSettings({...settings, loyaltyRate: parseInt(e.target.value)})}
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
              />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BotSettings;