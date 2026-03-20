import React, { useState } from 'react';
import { Bell, X, CheckCircle, ShoppingBag, Search, Info } from 'lucide-react';

export default function NotificationBell() {
  const [isOpen, setIsOpen] = useState(false);

  // In a full app these would come from a backend websocket or polling endpoint.
  // For now we'll use localStorage-based notifications as a demo.
  const [notifications, setNotifications] = useState(() => {
    const saved = localStorage.getItem('campus_notifications');
    if (saved) return JSON.parse(saved);
    return [
      { id: 1, type: 'info', title: 'Welcome to CampusConnect!', message: 'Start by browsing lost items or marketplace.', read: false, time: new Date().toISOString() },
    ];
  });

  const unreadCount = notifications.filter(n => !n.read).length;

  const markAllRead = () => {
    const updated = notifications.map(n => ({ ...n, read: true }));
    setNotifications(updated);
    localStorage.setItem('campus_notifications', JSON.stringify(updated));
  };

  const clearAll = () => {
    setNotifications([]);
    localStorage.removeItem('campus_notifications');
  };

  const iconMap = {
    match: <Search className="w-4 h-4 text-blue-500" />,
    purchase: <ShoppingBag className="w-4 h-4 text-purple-500" />,
    claim: <CheckCircle className="w-4 h-4 text-emerald-500" />,
    info: <Info className="w-4 h-4 text-slate-400" />,
  };

  return (
    <div className="relative">
      <button
        onClick={() => setIsOpen(!isOpen)}
        className="p-2 text-slate-500 hover:text-blue-600 hover:bg-blue-50 dark:hover:bg-blue-900/20 rounded-full transition-all relative"
        title="Notifications"
      >
        <Bell className="w-5 h-5" />
        {unreadCount > 0 && (
          <span className="absolute -top-0.5 -right-0.5 w-4.5 h-4.5 bg-red-500 text-white text-[10px] font-bold rounded-full flex items-center justify-center min-w-[18px] h-[18px] shadow-sm">
            {unreadCount}
          </span>
        )}
      </button>

      {isOpen && (
        <div className="absolute right-0 top-12 w-80 bg-white dark:bg-slate-900 border border-slate-200 dark:border-slate-700 rounded-2xl shadow-2xl z-50 overflow-hidden animate-in slide-in-from-top-2 fade-in duration-200">
          <div className="p-4 border-b border-slate-200 dark:border-slate-700 flex justify-between items-center">
            <h3 className="font-bold text-slate-900 dark:text-white">Notifications</h3>
            <div className="flex gap-2">
              <button onClick={markAllRead} className="text-xs text-blue-600 hover:underline font-medium">Mark all read</button>
              <button onClick={clearAll} className="text-xs text-red-500 hover:underline font-medium">Clear</button>
            </div>
          </div>
          <div className="max-h-72 overflow-y-auto">
            {notifications.length === 0 ? (
              <div className="py-8 text-center text-slate-400 text-sm">No notifications</div>
            ) : (
              notifications.map(n => (
                <div key={n.id} className={`px-4 py-3 flex gap-3 items-start border-b border-slate-100 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-slate-800/50 transition-colors ${!n.read ? 'bg-blue-50/50 dark:bg-blue-900/10' : ''}`}>
                  <div className="mt-0.5">{iconMap[n.type] || iconMap.info}</div>
                  <div className="flex-grow">
                    <div className="font-semibold text-sm text-slate-800 dark:text-slate-200">{n.title}</div>
                    <div className="text-xs text-slate-500 mt-0.5">{n.message}</div>
                  </div>
                  {!n.read && <div className="w-2 h-2 bg-blue-500 rounded-full mt-2 flex-shrink-0"></div>}
                </div>
              ))
            )}
          </div>
        </div>
      )}
    </div>
  );
}

/**
 * Utility function to add a notification programmatically.
 * Call this from anywhere after an event (match found, purchase, claim approved).
 */
export function addNotification(type, title, message) {
  const saved = localStorage.getItem('campus_notifications');
  const notifications = saved ? JSON.parse(saved) : [];
  notifications.unshift({
    id: Date.now(),
    type,
    title,
    message,
    read: false,
    time: new Date().toISOString()
  });
  // Keep max 20
  if (notifications.length > 20) notifications.pop();
  localStorage.setItem('campus_notifications', JSON.stringify(notifications));
}
