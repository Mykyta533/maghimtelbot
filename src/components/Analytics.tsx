import React from 'react';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, LineChart, Line, PieChart, Pie, Cell } from 'recharts';
import { TrendingUp, DollarSign, ShoppingCart, Users } from 'lucide-react';

const Analytics = () => {
  const salesData = [
    { name: 'Пн', sales: 1200, orders: 15 },
    { name: 'Вт', sales: 1900, orders: 23 },
    { name: 'Ср', sales: 3000, orders: 35 },
    { name: 'Чт', sales: 2800, orders: 32 },
    { name: 'Пт', sales: 3900, orders: 45 },
    { name: 'Сб', sales: 4200, orders: 48 },
    { name: 'Нд', sales: 3100, orders: 38 }
  ];

  const categoryData = [
    { name: 'Засоби для прибирання', value: 45, color: '#3B82F6' },
    { name: 'Гігієна', value: 25, color: '#10B981' },
    { name: 'Миття посуду', value: 20, color: '#8B5CF6' },
    { name: 'Побутові дрібниці', value: 10, color: '#F59E0B' }
  ];

  const aiUsageData = [
    { name: 'Пн', textQueries: 45, voiceQueries: 23 },
    { name: 'Вт', textQueries: 52, voiceQueries: 31 },
    { name: 'Ср', textQueries: 67, voiceQueries: 42 },
    { name: 'Чт', textQueries: 58, voiceQueries: 38 },
    { name: 'Пт', textQueries: 73, voiceQueries: 45 },
    { name: 'Сб', textQueries: 81, voiceQueries: 52 },
    { name: 'Нд', textQueries: 64, voiceQueries: 39 }
  ];

  return (
    <div className="space-y-8">
      <h2 className="text-2xl font-bold text-gray-900">Аналітика</h2>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="bg-white rounded-xl shadow-lg p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Продажі за тиждень</p>
              <p className="text-2xl font-bold text-gray-900 mt-2">₴20,200</p>
              <p className="text-sm text-green-600 font-medium mt-1">+15.3%</p>
            </div>
            <div className="bg-blue-500 p-3 rounded-lg">
              <DollarSign className="h-6 w-6 text-white" />
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-lg p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Замовлення за тиждень</p>
              <p className="text-2xl font-bold text-gray-900 mt-2">236</p>
              <p className="text-sm text-green-600 font-medium mt-1">+8.7%</p>
            </div>
            <div className="bg-green-500 p-3 rounded-lg">
              <ShoppingCart className="h-6 w-6 text-white" />
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-lg p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">Нові користувачі</p>
              <p className="text-2xl font-bold text-gray-900 mt-2">47</p>
              <p className="text-sm text-green-600 font-medium mt-1">+23.1%</p>
            </div>
            <div className="bg-purple-500 p-3 rounded-lg">
              <Users className="h-6 w-6 text-white" />
            </div>
          </div>
        </div>

        <div className="bg-white rounded-xl shadow-lg p-6">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-sm font-medium text-gray-600">AI запити</p>
              <p className="text-2xl font-bold text-gray-900 mt-2">440</p>
              <p className="text-sm text-green-600 font-medium mt-1">+12.4%</p>
            </div>
            <div className="bg-yellow-500 p-3 rounded-lg">
              <TrendingUp className="h-6 w-6 text-white" />
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Sales Chart */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Продажі за тиждень</h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={salesData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip formatter={(value, name) => [
                name === 'sales' ? `₴${value}` : value,
                name === 'sales' ? 'Продажі' : 'Замовлення'
              ]} />
              <Bar dataKey="sales" fill="#3B82F6" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        {/* Category Distribution */}
        <div className="bg-white rounded-xl shadow-lg p-6">
          <h3 className="text-lg font-semibold text-gray-900 mb-4">Розподіл за категоріями</h3>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={categoryData}
                cx="50%"
                cy="50%"
                outerRadius={100}
                dataKey="value"
                label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
              >
                {categoryData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* AI Usage Chart */}
      <div className="bg-white rounded-xl shadow-lg p-6">
        <h3 className="text-lg font-semibold text-gray-900 mb-4">Використання AI-помічника</h3>
        <ResponsiveContainer width="100%" height={300}>
          <LineChart data={aiUsageData}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="name" />
            <YAxis />
            <Tooltip />
            <Line 
              type="monotone" 
              dataKey="textQueries" 
              stroke="#3B82F6" 
              strokeWidth={2}
              name="Текстові запити"
            />
            <Line 
              type="monotone" 
              dataKey="voiceQueries" 
              stroke="#10B981" 
              strokeWidth={2}
              name="Голосові запити"
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
};

export default Analytics;