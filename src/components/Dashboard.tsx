import React from 'react';
import { 
  Users, 
  ShoppingCart, 
  Package, 
  TrendingUp,
  MessageSquare,
  Bot,
  Gift,
  DollarSign
} from 'lucide-react';

const Dashboard = () => {
  const stats = [
    {
      title: 'Активні користувачі',
      value: '1,247',
      change: '+12%',
      icon: Users,
      color: 'bg-blue-500'
    },
    {
      title: 'Замовлення сьогодні',
      value: '89',
      change: '+23%',
      icon: ShoppingCart,
      color: 'bg-green-500'
    },
    {
      title: 'Товарів у каталозі',
      value: '156',
      change: '+5',
      icon: Package,
      color: 'bg-purple-500'
    },
    {
      title: 'Дохід за місяць',
      value: '₴45,230',
      change: '+18%',
      icon: DollarSign,
      color: 'bg-yellow-500'
    }
  ];

  const recentActivity = [
    { type: 'order', message: 'Нове замовлення від @maria_k', time: '2 хв тому' },
    { type: 'user', message: 'Новий користувач зареєстрований', time: '5 хв тому' },
    { type: 'ai', message: 'AI-помічник відповів на 15 запитів', time: '10 хв тому' },
    { type: 'payment', message: 'Оплата ₴850 успішно проведена', time: '15 хв тому' },
  ];

  return (
    <div className="space-y-8">
      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, index) => {
          const Icon = stat.icon;
          return (
            <div key={index} className="bg-white rounded-xl shadow-lg p-6 hover:shadow-xl transition-shadow duration-300">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600">{stat.title}</p>
                  <p className="text-2xl font-bold text-gray-900 mt-2">{stat.value}</p>
                  <p className="text-sm text-green-600 font-medium mt-1">{stat.change}</p>
                </div>
                <div className={`${stat.color} p-3 rounded-lg`}>
                  <Icon className="h-6 w-6 text-white" />
                </div>
              </div>
            </div>
          );
        })}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Recent Activity */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Остання активність</h3>
          <div className="space-y-4">
            {recentActivity.map((activity, index) => (
              <div key={index} className="flex items-center space-x-3 p-3 bg-gray-50 rounded-lg">
                <div className="flex-shrink-0">
                  {activity.type === 'order' && <ShoppingCart className="h-5 w-5 text-green-500" />}
                  {activity.type === 'user' && <Users className="h-5 w-5 text-blue-500" />}
                  {activity.type === 'ai' && <Bot className="h-5 w-5 text-purple-500" />}
                  {activity.type === 'payment' && <DollarSign className="h-5 w-5 text-yellow-500" />}
                </div>
                <div className="flex-1">
                  <p className="text-sm font-medium text-gray-900">{activity.message}</p>
                  <p className="text-xs text-gray-500">{activity.time}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Bot Status */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Статус бота</h3>
          <div className="space-y-4">
            <div className="flex items-center justify-between p-3 bg-green-50 rounded-lg">
              <div className="flex items-center space-x-3">
                <Bot className="h-5 w-5 text-green-500" />
                <span className="font-medium text-gray-900">Основний бот</span>
              </div>
              <span className="px-2 py-1 bg-green-100 text-green-800 text-xs font-medium rounded-full">
                Активний
              </span>
            </div>
            
            <div className="flex items-center justify-between p-3 bg-blue-50 rounded-lg">
              <div className="flex items-center space-x-3">
                <MessageSquare className="h-5 w-5 text-blue-500" />
                <span className="font-medium text-gray-900">AI-помічник</span>
              </div>
              <span className="px-2 py-1 bg-blue-100 text-blue-800 text-xs font-medium rounded-full">
                Працює
              </span>
            </div>

            <div className="flex items-center justify-between p-3 bg-purple-50 rounded-lg">
              <div className="flex items-center space-x-3">
                <Gift className="h-5 w-5 text-purple-500" />
                <span className="font-medium text-gray-900">Програма лояльності</span>
              </div>
              <span className="px-2 py-1 bg-purple-100 text-purple-800 text-xs font-medium rounded-full">
                Активна
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;