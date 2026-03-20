import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { 
  Users, ShoppingBag, Search, DollarSign, CheckCircle, 
  XCircle, Clock, TrendingUp, Package, Shield, IndianRupee 
} from 'lucide-react';

export default function AdminDashboard() {
  const [stats, setStats] = useState(null);
  const [claims, setClaims] = useState([]);
  const [transactions, setTransactions] = useState([]);
  const [activeSection, setActiveSection] = useState('overview');
  const [loading, setLoading] = useState(true);

  const token = localStorage.getItem('token');
  const headers = { Authorization: `Bearer ${token}` };

  useEffect(() => {
    fetchDashboard();
  }, []);

  const fetchDashboard = async () => {
    setLoading(true);
    try {
      const [statsRes, claimsRes, txRes] = await Promise.all([
        axios.get('/api/admin/dashboard', { headers }),
        axios.get('/api/admin/claims', { headers }),
        axios.get('/api/admin/transactions', { headers })
      ]);
      setStats(statsRes.data);
      setClaims(claimsRes.data);
      setTransactions(txRes.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleVerifyClaim = async (claimId, action) => {
    try {
      await axios.post(`/api/admin/claims/${claimId}/verify`, { action }, { headers });
      alert(`Claim ${action}d successfully!`);
      fetchDashboard();
    } catch (err) {
      alert(err.response?.data?.message || 'Error');
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center min-h-[60vh]">
        <div className="animate-spin rounded-full h-16 w-16 border-b-4 border-blue-600"></div>
      </div>
    );
  }

  if (!stats) {
    return (
      <div className="text-center py-24">
        <Shield className="w-16 h-16 text-red-400 mx-auto mb-4" />
        <h2 className="text-2xl font-bold text-slate-700 dark:text-slate-300">Access Denied</h2>
        <p className="text-slate-500 mt-2">You need admin privileges to view this page.</p>
      </div>
    );
  }

  const statCards = [
    { label: 'Total Users', value: stats.users.total, icon: Users, color: 'blue', sub: `${stats.users.students} students, ${stats.users.alumni} alumni` },
    { label: 'Lost Reports', value: stats.lost_and_found.total_lost, icon: Search, color: 'red', sub: `${stats.lost_and_found.resolved} resolved` },
    { label: 'Found Reports', value: stats.lost_and_found.total_found, icon: CheckCircle, color: 'emerald', sub: `${stats.lost_and_found.resolved} recovered` },
    { label: 'Marketplace Items', value: stats.marketplace.total_items, icon: ShoppingBag, color: 'purple', sub: `${stats.marketplace.sold} sold, ${stats.marketplace.available} available` },
    { label: 'Transactions', value: stats.transactions, icon: TrendingUp, color: 'amber', sub: 'total completed' },
    { label: 'Platform Revenue', value: `₹${stats.revenue}`, icon: IndianRupee, color: 'green', sub: 'from fees' },
  ];

  const colorMap = {
    blue: 'from-blue-500 to-blue-600',
    red: 'from-red-500 to-red-600',
    emerald: 'from-emerald-500 to-emerald-600',
    purple: 'from-purple-500 to-purple-600',
    amber: 'from-amber-500 to-amber-600',
    green: 'from-green-500 to-green-600',
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-8 animate-in fade-in duration-500">
      <div className="mb-10">
        <div className="flex items-center gap-3 mb-2">
          <Shield className="w-8 h-8 text-blue-600" />
          <h1 className="text-4xl font-extrabold text-slate-900 dark:text-white">Admin Dashboard</h1>
        </div>
        <p className="text-slate-500 dark:text-slate-400 ml-11">Monitor platform activity, claims, and revenue.</p>
      </div>

      {/* Tab Navigation */}
      <div className="flex bg-slate-100 dark:bg-slate-800 p-1 rounded-xl mb-8 max-w-lg shadow-inner">
        {['overview', 'claims', 'transactions'].map(tab => (
          <button 
            key={tab}
            onClick={() => setActiveSection(tab)}
            className={`flex-1 px-4 py-2.5 rounded-lg font-medium capitalize transition-all ${activeSection === tab ? 'bg-white dark:bg-slate-700 shadow-sm text-blue-600 dark:text-blue-400' : 'text-slate-600 dark:text-slate-300'}`}
          >
            {tab}
          </button>
        ))}
      </div>

      {/* Overview */}
      {activeSection === 'overview' && (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
          {statCards.map((card, i) => {
            const Icon = card.icon;
            return (
              <div key={i} className="bg-white dark:bg-slate-800 rounded-2xl border border-slate-200 dark:border-slate-700 p-6 hover:shadow-lg transition-all duration-300 hover:-translate-y-1">
                <div className="flex items-start justify-between mb-4">
                  <div className={`p-3 rounded-xl bg-gradient-to-br ${colorMap[card.color]} text-white shadow-lg`}>
                    <Icon className="w-6 h-6" />
                  </div>
                </div>
                <div className="text-3xl font-black text-slate-900 dark:text-white mb-1">{card.value}</div>
                <div className="text-sm font-semibold text-slate-600 dark:text-slate-300">{card.label}</div>
                <div className="text-xs text-slate-400 mt-1">{card.sub}</div>
              </div>
            );
          })}
        </div>
      )}

      {/* Claims Management */}
      {activeSection === 'claims' && (
        <div className="space-y-4">
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-2xl font-bold">Pending Claims ({claims.filter(c => c.status === 'Pending').length})</h2>
          </div>
          {claims.length === 0 ? (
            <div className="text-center py-16 bg-white dark:bg-slate-800 rounded-2xl border border-dashed border-slate-300 dark:border-slate-700">
              <Package className="w-12 h-12 text-slate-300 mx-auto mb-3" />
              <p className="text-slate-500">No claims to review.</p>
            </div>
          ) : (
            claims.map(claim => (
              <div key={claim._id} className="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-2xl p-6 hover:shadow-md transition-all">
                <div className="flex flex-col md:flex-row justify-between gap-4">
                  <div className="flex-grow">
                    <div className="flex items-center gap-3 mb-2">
                      <h3 className="text-lg font-bold">{claim.item_name}</h3>
                      <span className={`px-2.5 py-0.5 rounded-full text-xs font-bold uppercase ${
                        claim.status === 'Pending' ? 'bg-amber-100 text-amber-700 dark:bg-amber-900/30 dark:text-amber-400' :
                        claim.status === 'Approved' ? 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400' :
                        'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400'
                      }`}>
                        {claim.status}
                      </span>
                    </div>
                    <div className="text-sm text-slate-500 space-y-1">
                      <p><span className="font-medium">Category:</span> {claim.item_category}</p>
                      <p><span className="font-medium">Claimed by:</span> {claim.claimer_name} ({claim.claimer_email})</p>
                      <p><span className="font-medium">Verification:</span> {claim.verification_details || 'None provided'}</p>
                      <p><span className="font-medium">Description:</span> {claim.item_description}</p>
                    </div>
                  </div>
                  {claim.status === 'Pending' && (
                    <div className="flex md:flex-col gap-2 justify-end">
                      <button onClick={() => handleVerifyClaim(claim._id, 'approve')} className="px-5 py-2.5 bg-emerald-600 text-white rounded-xl font-medium hover:bg-emerald-700 transition-all flex items-center gap-2 shadow-sm">
                        <CheckCircle className="w-4 h-4" /> Approve
                      </button>
                      <button onClick={() => handleVerifyClaim(claim._id, 'reject')} className="px-5 py-2.5 bg-red-600 text-white rounded-xl font-medium hover:bg-red-700 transition-all flex items-center gap-2 shadow-sm">
                        <XCircle className="w-4 h-4" /> Reject
                      </button>
                    </div>
                  )}
                </div>
              </div>
            ))
          )}
        </div>
      )}

      {/* Transactions */}
      {activeSection === 'transactions' && (
        <div className="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-2xl overflow-hidden">
          <div className="p-6 border-b border-slate-200 dark:border-slate-700">
            <h2 className="text-2xl font-bold">Marketplace Transactions</h2>
          </div>
          {transactions.length > 0 ? (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead className="bg-slate-50 dark:bg-slate-700/50">
                  <tr>
                    <th className="text-left p-4 font-semibold text-slate-600 dark:text-slate-300">Item</th>
                    <th className="text-left p-4 font-semibold text-slate-600 dark:text-slate-300">Buyer</th>
                    <th className="text-left p-4 font-semibold text-slate-600 dark:text-slate-300">Seller</th>
                    <th className="text-right p-4 font-semibold text-slate-600 dark:text-slate-300">Price</th>
                    <th className="text-right p-4 font-semibold text-slate-600 dark:text-slate-300">Fee</th>
                    <th className="text-center p-4 font-semibold text-slate-600 dark:text-slate-300">Status</th>
                    <th className="text-right p-4 font-semibold text-slate-600 dark:text-slate-300">Date</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-100 dark:divide-slate-700">
                  {transactions.map(tx => (
                    <tr key={tx._id} className="hover:bg-slate-50 dark:hover:bg-slate-700/30 transition-colors">
                      <td className="p-4 font-medium">{tx.item_name}</td>
                      <td className="p-4 text-slate-500">{tx.buyer_name}</td>
                      <td className="p-4 text-slate-500">{tx.seller_name}</td>
                      <td className="p-4 text-right font-medium">₹{tx.price}</td>
                      <td className="p-4 text-right text-emerald-600 dark:text-emerald-400 font-medium">₹{tx.platform_fee}</td>
                      <td className="p-4 text-center">
                        <span className="px-2.5 py-0.5 rounded-full text-xs font-bold bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400">
                          {tx.status}
                        </span>
                      </td>
                      <td className="p-4 text-right text-slate-400">{new Date(tx.created_at).toLocaleDateString()}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="text-center py-16">
              <TrendingUp className="w-12 h-12 text-slate-300 mx-auto mb-3" />
              <p className="text-slate-500">No transactions yet.</p>
            </div>
          )}
        </div>
      )}
    </div>
  );
}
