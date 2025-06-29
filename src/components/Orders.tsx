import React, { useState } from 'react';
import { Eye, Package, Truck, CheckCircle, Clock, Filter } from 'lucide-react';

const Orders = () => {
  const [statusFilter, setStatusFilter] = useState('all');

  const orders = [
    {
      id: '#ORD-001',
      customer: '@maria_k',
      items: 3,
      total: 245.50,
      status: 'pending',
      date: '2024-01-15 14:30',
      paymentMethod: 'LiqPay'
    },
    {
      id: '#ORD-002',
      customer: '@anna_t',
      items: 1,
      total: 89.99,
      status: 'processing',
      date: '2024-01-15 13:15',
      paymentMethod: 'WayForPay'
    },
    {
      id: '#ORD-003',
      customer: '@oksana_m',
      items: 5,
      total: 456.75,
      status: 'completed',
      date: '2024-01-15 11:45',
      paymentMethod: 'LiqPay'
    },
    {
      id: '#ORD-004',
      customer: '@natalia_s',
      items: 2,
      total: 134.00,
      status: 'shipped',
      date: '2024-01-15 10:20',
      paymentMethod: 'WayForPay'
    }
  ];

  const statusConfig = {
    pending: { label: 'Очікує', color: 'bg-yellow-100 text-yellow-800', icon: Clock },
    processing: { label: 'Обробляється', color: 'bg-blue-100 text-blue-800', icon: Package },
    shipped: { label: 'Відправлено', color: 'bg-purple-100 text-purple-800', icon: Truck },
    completed: { label: 'Завершено', color: 'bg-green-100 text-green-800', icon: CheckCircle }
  };

  const filteredOrders = statusFilter === 'all' 
    ? orders 
    : orders.filter(order => order.status === statusFilter);

  return (
    <div className="space-y-6">
      {/* Header */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <h2 className="text-2xl font-bold text-gray-900">Замовлення</h2>
        <div className="flex items-center space-x-4">
          <select
            value={statusFilter}
            onChange={(e) => setStatusFilter(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
          >
            <option value="all">Всі статуси</option>
            <option value="pending">Очікує</option>
            <option value="processing">Обробляється</option>
            <option value="shipped">Відправлено</option>
            <option value="completed">Завершено</option>
          </select>
        </div>
      </div>

      {/* Orders List */}
      <div className="bg-white rounded-xl shadow-lg overflow-hidden">
        <div className="overflow-x-auto">
          <table className="min-w-full divide-y divide-gray-200">
            <thead className="bg-gray-50">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Замовлення
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Клієнт
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Товари
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Сума
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Статус
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Дата
                </th>
                <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                  Дії
                </th>
              </tr>
            </thead>
            <tbody className="bg-white divide-y divide-gray-200">
              {filteredOrders.map((order) => {
                const StatusIcon = statusConfig[order.status].icon;
                return (
                  <tr key={order.id} className="hover:bg-gray-50 transition-colors duration-200">
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium text-gray-900">{order.id}</div>
                      <div className="text-sm text-gray-500">{order.paymentMethod}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-medium text-gray-900">{order.customer}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm text-gray-900">{order.items} товарів</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <div className="text-sm font-bold text-gray-900">₴{order.total}</div>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap">
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${statusConfig[order.status].color}`}>
                        <StatusIcon className="h-3 w-3 mr-1" />
                        {statusConfig[order.status].label}
                      </span>
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                      {order.date}
                    </td>
                    <td className="px-6 py-4 whitespace-nowrap text-sm font-medium">
                      <button className="text-blue-600 hover:text-blue-900 flex items-center space-x-1">
                        <Eye className="h-4 w-4" />
                        <span>Переглянути</span>
                      </button>
                    </td>
                  </tr>
                );
              })}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Orders;