import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { 
  Users, ShoppingBag, Search, CheckCircle, 
  XCircle, TrendingUp, Package, Shield, IndianRupee 
} from 'lucide-react';

export default function AdminDashboard() {

  const navigate = useNavigate();
  const user = JSON.parse(localStorage.getItem('user') || 'null');

  const [stats, setStats] = useState(null);
  const [claims, setClaims] = useState([]);
  const [transactions, setTransactions] = useState([]);
  const [activeSection, setActiveSection] = useState('overview');
  const [loading, setLoading] = useState(true);

  const token = localStorage.getItem('token');
  const headers = { Authorization: `Bearer ${token}` };

  // ✅ Restrict access to Admin only
  useEffect(() => {
    if (!user || user.role !== "Admin") {
      navigate("/");
    }
  }, []);

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

      if (err.response?.status === 403) {
        alert("Admin access required");
        navigate("/");
      }

      if (err.response?.status === 401) {
        localStorage.clear();
        navigate("/login");
      }

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
        <p className="text-slate-500 mt-2">You need admin privileges.</p>
      </div>
    );
  }

  const statCards = [
    { label: 'Total Users', value: stats.users.total, icon: Users, sub: `${stats.users.students} students, ${stats.users.alumni} alumni` },
    { label: 'Lost Reports', value: stats.lost_and_found.total_lost, icon: Search, sub: `${stats.lost_and_found.resolved} resolved` },
    { label: 'Found Reports', value: stats.lost_and_found.total_found, icon: CheckCircle, sub: `${stats.lost_and_found.resolved} recovered` },
    { label: 'Marketplace Items', value: stats.marketplace.total_items, icon: ShoppingBag, sub: `${stats.marketplace.sold} sold` },
    { label: 'Transactions', value: stats.transactions, icon: TrendingUp, sub: 'total completed' },
    { label: 'Platform Revenue', value: `₹${stats.revenue}`, icon: IndianRupee, sub: 'total profit earned' },
  ];

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">

      <div className="mb-10 flex items-center gap-3">
        <Shield className="w-8 h-8 text-blue-600" />
        <h1 className="text-4xl font-bold">Admin Dashboard</h1>
      </div>

      {/* Tabs */}
      <div className="flex bg-red-500 p-1 rounded-xl mb-6 max-w-md">
        {['overview', 'claims', 'transactions'].map(tab => (
          <button 
            key={tab}
            onClick={() => setActiveSection(tab)}
            className={`flex-1 py-2 rounded-lg capitalize ${activeSection === tab ? 'bg-black shadow font-semibold' : ''}`}
          >
            {tab}
          </button>
        ))}
      </div>

      {/* Overview */}
      {activeSection === 'overview' && (
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {statCards.map((card, i) => {
            const Icon = card.icon;
            return (
              <div key={i} className="bg-green-300 p-6 rounded-xl shadow">
                <Icon className="w-6 h-6 mb-2 text-blue-500" />
                <div className="text-2xl font-bold">{card.value}</div>
                <div className="text-sm text-gray-500">{card.label}</div>
                <div className="text-xs text-gray-400">{card.sub}</div>
              </div>
            );
          })}
        </div>
      )}

      {/* Claims */}
      {activeSection === 'claims' && (
        <div className="space-y-4">
          {claims.map(claim => (
            <div key={claim._id} className="bg-zinc-900 p-5 rounded-xl shadow">
              <h3 className="font-bold">{claim.item_name}</h3>
              <p className="text-sm text-gray-500">
                Claimed by: {claim.claimer_name} ({claim.claimer_email})
              </p>
              <p className="text-sm">{claim.verification_details}</p>

              {claim.status === 'Pending' && (
                <div className="flex gap-2 mt-3">
                  <button onClick={() => handleVerifyClaim(claim._id, 'approve')} className="bg-green-600 text-white px-3 py-1 rounded">
                    Approve
                  </button>
                  <button onClick={() => handleVerifyClaim(claim._id, 'reject')} className="bg-red-600 text-white px-3 py-1 rounded">
                    Reject
                  </button>
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      {/* Transactions */}
      {activeSection === 'transactions' && (
        <div className="bg-zinc-700 rounded-xl shadow overflow-x-auto">
          <table className="w-full text-sm">
            <thead className="bg-zinc-500">
              <tr>
                <th className="p-3 text-left">Item</th>
                <th className="p-3 text-left">Buyer</th>
                <th className="p-3 text-left">Seller</th>
                <th className="p-3 text-right">Price</th>
                <th className="p-3 text-right">Fee</th>
                <th className="p-3 text-center">Status</th>
                <th className="p-3 text-right">Date</th>
              </tr>
            </thead>

            <tbody>
              {transactions.map(tx => (
                <tr key={tx._id} className="border-t">

                  <td className="p-3">{tx.item_name}</td>

                  {/* Buyer Info */}
                  <td className="p-3">
                    <div className="font-medium">{tx.buyer_name}</div>
                    <div className="text-xs text-gray-400">{tx.buyer_email}</div>
                    <div className="text-xs text-purple-500">{tx.buyer_anon}</div>
                  </td>

                  {/* Seller Info */}
                  <td className="p-3">
                    <div className="font-medium">{tx.seller_name}</div>
                    <div className="text-xs text-gray-400">{tx.seller_email}</div>
                    <div className="text-xs text-purple-500">{tx.seller_anon}</div>
                  </td>

                  <td className="p-3 text-right">₹{tx.price}</td>
                  <td className="p-3 text-right text-green-600">₹{tx.platform_fee}</td>

                  <td className="p-3 text-center">{tx.status}</td>

                  <td className="p-3 text-right">
                    {new Date(tx.created_at).toLocaleDateString()}
                  </td>

                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}