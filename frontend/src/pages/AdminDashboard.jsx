import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import {
  Users, ShoppingBag, Search, CheckCircle,
  XCircle, TrendingUp, Shield, IndianRupee,
  Package, AlertCircle, Clock, ArrowUpRight,
  ArrowDownRight, BarChart2, Activity
} from 'lucide-react';
import {
  AreaChart, Area, BarChart, Bar, PieChart, Pie, Cell,
  XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend
} from 'recharts';

const backendUrl = import.meta.env.VITE_API_URL || 'http://localhost:5000';

/* ── Helpers ─────────────────────────────────────────────────── */

// Generate sparkline-style mock trend data from a single value
function makeTrend(total, points = 7) {
  const arr = [];
  let rem = total;
  for (let i = 0; i < points - 1; i++) {
    const v = Math.floor(Math.random() * (rem / (points - i)) * 1.5);
    arr.push(v);
    rem -= v;
  }
  arr.push(Math.max(0, rem));
  return arr.map((v, i) => ({ day: `D${i + 1}`, v }));
}

const CLAIM_STATUS_COLORS = {
  Pending: '#f59e0b',
  Approved: '#22c55e',
  Rejected: '#ef4444',
};

const PIE_COLORS = ['#3b82f6', '#8b5cf6', '#22c55e', '#f59e0b', '#ef4444', '#06b6d4'];

/* ── Sub-components ──────────────────────────────────────────── */

function StatCard({ label, value, icon: Icon, sub, trend, accentColor, delta }) {
  const trendData = trend || makeTrend(typeof value === 'number' ? value : 100);
  const isUp = delta === undefined ? true : delta >= 0;

  return (
    <div style={{ background: '#0f172a', border: '1px solid #1e293b', borderRadius: 16, padding: '1.5rem', position: 'relative', overflow: 'hidden' }}>
      {/* Glow accent */}
      <div style={{ position: 'absolute', top: 0, left: 0, right: 0, height: 3, background: accentColor, borderRadius: '16px 16px 0 0' }} />

      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '1rem' }}>
        <div style={{ padding: '0.5rem', background: `${accentColor}22`, borderRadius: 10 }}>
          <Icon style={{ width: 20, height: 20, color: accentColor }} />
        </div>
        <span style={{ display: 'flex', alignItems: 'center', gap: 4, fontSize: '0.72rem', fontWeight: 600, color: isUp ? '#22c55e' : '#ef4444', background: isUp ? '#22c55e18' : '#ef444418', padding: '2px 8px', borderRadius: 20 }}>
          {isUp ? <ArrowUpRight style={{ width: 12, height: 12 }} /> : <ArrowDownRight style={{ width: 12, height: 12 }} />}
          {delta !== undefined ? `${Math.abs(delta)}%` : 'Live'}
        </span>
      </div>

      <div style={{ fontSize: '2rem', fontWeight: 800, color: '#f1f5f9', letterSpacing: '-0.03em', lineHeight: 1 }}>{value}</div>
      <div style={{ fontSize: '0.8rem', color: '#64748b', marginTop: '0.3rem', fontWeight: 500 }}>{label}</div>
      {sub && <div style={{ fontSize: '0.72rem', color: '#475569', marginTop: '0.2rem' }}>{sub}</div>}

      {/* Sparkline */}
      <div style={{ marginTop: '1rem', height: 40 }}>
        <ResponsiveContainer width="100%" height={40}>
          <AreaChart data={trendData} margin={{ top: 0, right: 0, left: 0, bottom: 0 }}>
            <defs>
              <linearGradient id={`grad-${label}`} x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor={accentColor} stopOpacity={0.3} />
                <stop offset="95%" stopColor={accentColor} stopOpacity={0} />
              </linearGradient>
            </defs>
            <Area type="monotone" dataKey="v" stroke={accentColor} strokeWidth={2} fill={`url(#grad-${label})`} dot={false} />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}

function SectionHeader({ icon: Icon, title, subtitle }) {
  return (
    <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '1.25rem' }}>
      <div style={{ padding: '0.45rem', background: '#1e293b', borderRadius: 10 }}>
        <Icon style={{ width: 18, height: 18, color: '#60a5fa' }} />
      </div>
      <div>
        <div style={{ fontSize: '1rem', fontWeight: 700, color: '#f1f5f9' }}>{title}</div>
        {subtitle && <div style={{ fontSize: '0.75rem', color: '#64748b' }}>{subtitle}</div>}
      </div>
    </div>
  );
}

function ClaimCard({ claim, onApprove, onReject }) {
  return (
    <div style={{ background: '#0f172a', border: '1px solid #1e293b', borderRadius: 14, padding: '1.25rem', display: 'flex', flexDirection: 'column', gap: '0.6rem' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
        <div>
          <div style={{ fontWeight: 700, color: '#f1f5f9', fontSize: '0.95rem' }}>{claim.item_name}</div>
          <div style={{ fontSize: '0.75rem', color: '#64748b' }}>
            {claim.claimer_name} · {claim.claimer_email}
          </div>
        </div>
        <span style={{
          padding: '3px 10px', borderRadius: 20, fontSize: '0.7rem', fontWeight: 600,
          background: claim.status === 'Pending' ? '#f59e0b22' : claim.status === 'Approved' ? '#22c55e22' : '#ef444422',
          color: claim.status === 'Pending' ? '#f59e0b' : claim.status === 'Approved' ? '#22c55e' : '#ef4444',
        }}>
          {claim.status}
        </span>
      </div>

      {claim.verification_details && (
        <div style={{ fontSize: '0.8rem', color: '#94a3b8', background: '#1e293b', borderRadius: 8, padding: '0.6rem 0.8rem', borderLeft: '3px solid #3b82f6' }}>
          {claim.verification_details}
        </div>
      )}

      {claim.reward_amount > 0 && (
        <div style={{ fontSize: '0.75rem', color: '#22c55e', display: 'flex', alignItems: 'center', gap: 4 }}>
          🎁 ₹{claim.reward_amount} reward offered to finder
        </div>
      )}

      {claim.status === 'Pending' && (
        <div style={{ display: 'flex', gap: '0.5rem', marginTop: '0.25rem' }}>
          <button
            onClick={() => onApprove(claim._id)}
            style={{ flex: 1, padding: '0.55rem', background: '#22c55e', color: 'white', border: 'none', borderRadius: 8, fontWeight: 600, fontSize: '0.8rem', cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 4, transition: 'opacity 0.2s' }}
            onMouseEnter={e => e.currentTarget.style.opacity = '0.85'}
            onMouseLeave={e => e.currentTarget.style.opacity = '1'}
          >
            <CheckCircle style={{ width: 14, height: 14 }} /> Approve
          </button>
          <button
            onClick={() => onReject(claim._id)}
            style={{ flex: 1, padding: '0.55rem', background: '#ef4444', color: 'white', border: 'none', borderRadius: 8, fontWeight: 600, fontSize: '0.8rem', cursor: 'pointer', display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 4, transition: 'opacity 0.2s' }}
            onMouseEnter={e => e.currentTarget.style.opacity = '0.85'}
            onMouseLeave={e => e.currentTarget.style.opacity = '1'}
          >
            <XCircle style={{ width: 14, height: 14 }} /> Reject
          </button>
        </div>
      )}
    </div>
  );
}

const CustomTooltip = ({ active, payload, label }) => {
  if (!active || !payload?.length) return null;
  return (
    <div style={{ background: '#1e293b', border: '1px solid #334155', borderRadius: 10, padding: '0.6rem 1rem', fontSize: '0.8rem', color: '#f1f5f9' }}>
      <div style={{ color: '#94a3b8', marginBottom: 4 }}>{label}</div>
      {payload.map((p, i) => (
        <div key={i} style={{ color: p.color, fontWeight: 600 }}>{p.name}: {p.value}</div>
      ))}
    </div>
  );
};

/* ── Main Dashboard ──────────────────────────────────────────── */

export default function AdminDashboard() {
  const navigate = useNavigate();
  const user = JSON.parse(localStorage.getItem('user') || 'null');

  const [stats, setStats] = useState(null);
  const [claims, setClaims] = useState([]);
  const [transactions, setTransactions] = useState([]);
  const [activeSection, setActiveSection] = useState('overview');
  const [loading, setLoading] = useState(true);
  const [claimFilter, setClaimFilter] = useState('All');

  const token = localStorage.getItem('token');
  const headers = { Authorization: `Bearer ${token}` };

  useEffect(() => {
    if (!user || user.role !== 'Admin') navigate('/');
  }, []);

  useEffect(() => {
    fetchDashboard();
  }, []);

  const fetchDashboard = async () => {
    setLoading(true);
    try {
      const [statsRes, claimsRes, txRes] = await Promise.all([
        axios.get(`${backendUrl}/api/admin/dashboard`, { headers }),
        axios.get(`${backendUrl}/api/admin/claims`, { headers }),
        axios.get(`${backendUrl}/api/admin/transactions`, { headers }),
      ]);
      setStats(statsRes.data);
      setClaims(claimsRes.data);
      const unique = txRes.data.filter((v, i, a) => a.findIndex(t => t._id === v._id) === i);
      setTransactions(unique);
    } catch (err) {
      if (err.response?.status === 403) { alert('Admin access required'); navigate('/'); }
      if (err.response?.status === 401) { localStorage.clear(); navigate('/login'); }
    } finally {
      setLoading(false);
    }
  };

  const handleVerifyClaim = async (claimId, action) => {
    try {
      await axios.post(`${backendUrl}/api/admin/claims/${claimId}/verify`, { action }, { headers });
      fetchDashboard();
    } catch (err) {
      alert(err.response?.data?.message || 'Error');
    }
  };

  if (loading) {
    return (
      <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', minHeight: '60vh', gap: '1rem' }}>
        <div style={{ width: 48, height: 48, border: '3px solid #1e293b', borderTop: '3px solid #3b82f6', borderRadius: '50%', animation: 'spin 0.8s linear infinite' }} />
        <style>{`@keyframes spin { to { transform: rotate(360deg); } }`}</style>
        <div style={{ color: '#64748b', fontSize: '0.85rem' }}>Loading dashboard...</div>
      </div>
    );
  }

  if (!stats) return (
    <div style={{ textAlign: 'center', padding: '6rem 2rem' }}>
      <Shield style={{ width: 48, height: 48, color: '#ef4444', margin: '0 auto 1rem' }} />
      <div style={{ color: '#f1f5f9', fontSize: '1.25rem', fontWeight: 700 }}>Access Denied</div>
    </div>
  );

  /* ── Derived chart data ── */
  const lnfPieData = [
    { name: 'Lost', value: stats.lost_and_found.total_lost },
    { name: 'Found', value: stats.lost_and_found.total_found },
    { name: 'Resolved', value: stats.lost_and_found.resolved },
  ];

  const claimStatusData = [
    { name: 'Pending', value: claims.filter(c => c.status === 'Pending').length },
    { name: 'Approved', value: claims.filter(c => c.status === 'Approved').length },
    { name: 'Rejected', value: claims.filter(c => c.status === 'Rejected').length },
  ];

  // Revenue bars — last 6 months simulated from transactions
  const revenueByMonth = (() => {
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    const map = {};
    transactions.forEach(tx => {
      const d = new Date(tx.created_at);
      const key = months[d.getMonth()];
      map[key] = (map[key] || 0) + (tx.platform_fee || 0);
    });
    const recent = months.slice(Math.max(0, new Date().getMonth() - 5), new Date().getMonth() + 1);
    return recent.map(m => ({ month: m, revenue: map[m] || 0, transactions: transactions.filter(tx => months[new Date(tx.created_at).getMonth()] === m).length }));
  })();

  // Category breakdown from transactions
  const categoryData = (() => {
    const map = {};
    transactions.forEach(tx => {
      const cat = tx.category || 'General';
      map[cat] = (map[cat] || 0) + 1;
    });
    return Object.entries(map).map(([name, value]) => ({ name, value }));
  })();

  const statCards = [
    { label: 'Total Users', value: stats.users.total, icon: Users, sub: `${stats.users.students || 0} students`, accentColor: '#3b82f6', delta: 12 },
    { label: 'Lost Reports', value: stats.lost_and_found.total_lost, icon: Search, sub: `${stats.lost_and_found.resolved} resolved`, accentColor: '#ef4444', delta: -3 },
    { label: 'Found Reports', value: stats.lost_and_found.total_found, icon: CheckCircle, sub: 'items recovered', accentColor: '#22c55e', delta: 8 },
    { label: 'Marketplace Items', value: stats.marketplace.total_items, icon: ShoppingBag, sub: `${stats.marketplace.sold} sold`, accentColor: '#8b5cf6', delta: 5 },
    { label: 'Transactions', value: stats.transactions, icon: TrendingUp, sub: 'total completed', accentColor: '#06b6d4', delta: 21 },
    { label: 'Platform Revenue', value: `₹${stats.revenue}`, icon: IndianRupee, sub: 'total earned', accentColor: '#f59e0b', delta: 15 },
  ];

  const filteredClaims = claimFilter === 'All' ? claims : claims.filter(c => c.status === claimFilter);
  const tabs = ['overview', 'analytics', 'claims', 'transactions'];

  return (
    <div style={{ background: '#020817', minHeight: '100vh', padding: '2rem 1.5rem', fontFamily: 'system-ui, sans-serif', color: '#f1f5f9' }}>
      <div style={{ maxWidth: 1280, margin: '0 auto' }}>

        {/* ── Header ── */}
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '2rem', flexWrap: 'wrap', gap: '1rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <div style={{ padding: '0.6rem', background: '#3b82f622', borderRadius: 12, border: '1px solid #3b82f633' }}>
              <Shield style={{ width: 24, height: 24, color: '#3b82f6' }} />
            </div>
            <div>
              <div style={{ fontSize: '1.5rem', fontWeight: 800, letterSpacing: '-0.02em' }}>Admin Dashboard</div>
              <div style={{ fontSize: '0.75rem', color: '#64748b' }}>CampusConnect Control Panel</div>
            </div>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', padding: '0.4rem 0.8rem', background: '#22c55e18', border: '1px solid #22c55e33', borderRadius: 20 }}>
            <div style={{ width: 7, height: 7, borderRadius: '50%', background: '#22c55e', animation: 'pulse 2s infinite' }} />
            <span style={{ fontSize: '0.75rem', color: '#22c55e', fontWeight: 600 }}>System Live</span>
          </div>
        </div>

        {/* ── Tabs ── */}
        <div style={{ display: 'flex', gap: '0.25rem', background: '#0f172a', padding: '0.3rem', borderRadius: 12, marginBottom: '2rem', width: 'fit-content', border: '1px solid #1e293b' }}>
          {tabs.map(tab => (
            <button
              key={tab}
              onClick={() => setActiveSection(tab)}
              style={{
                padding: '0.5rem 1.25rem', borderRadius: 9, border: 'none', cursor: 'pointer',
                fontWeight: 600, fontSize: '0.82rem', textTransform: 'capitalize', transition: 'all 0.2s',
                background: activeSection === tab ? '#3b82f6' : 'transparent',
                color: activeSection === tab ? 'white' : '#64748b',
              }}
            >
              {tab}
            </button>
          ))}
        </div>

        <style>{`
          @keyframes pulse { 0%,100%{opacity:1} 50%{opacity:0.4} }
          @keyframes spin { to{transform:rotate(360deg)} }
        `}</style>

        {/* ══════════════════════════════════════
            OVERVIEW
        ══════════════════════════════════════ */}
        {activeSection === 'overview' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '2rem' }}>

            {/* Stat cards grid */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '1rem' }}>
              {statCards.map((card, i) => <StatCard key={i} {...card} />)}
            </div>

            {/* Quick summary row */}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>

              {/* Lost vs Found Pie */}
              <div style={{ background: '#0f172a', border: '1px solid #1e293b', borderRadius: 16, padding: '1.5rem' }}>
                <SectionHeader icon={Activity} title="Lost & Found Breakdown" subtitle="Current status distribution" />
                <ResponsiveContainer width="100%" height={220}>
                  <PieChart>
                    <Pie data={lnfPieData} cx="50%" cy="50%" innerRadius={55} outerRadius={85} paddingAngle={4} dataKey="value">
                      {lnfPieData.map((_, i) => <Cell key={i} fill={['#ef4444', '#22c55e', '#3b82f6'][i]} />)}
                    </Pie>
                    <Tooltip content={<CustomTooltip />} />
                    <Legend wrapperStyle={{ fontSize: '0.75rem', color: '#94a3b8' }} />
                  </PieChart>
                </ResponsiveContainer>
              </div>

              {/* Claims status */}
              <div style={{ background: '#0f172a', border: '1px solid #1e293b', borderRadius: 16, padding: '1.5rem' }}>
                <SectionHeader icon={Package} title="Claims Status" subtitle="Pending · Approved · Rejected" />
                <ResponsiveContainer width="100%" height={220}>
                  <BarChart data={claimStatusData} barSize={36}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                    <XAxis dataKey="name" tick={{ fill: '#64748b', fontSize: 12 }} axisLine={false} tickLine={false} />
                    <YAxis tick={{ fill: '#64748b', fontSize: 12 }} axisLine={false} tickLine={false} />
                    <Tooltip content={<CustomTooltip />} />
                    <Bar dataKey="value" radius={[6, 6, 0, 0]}>
                      {claimStatusData.map((entry, i) => (
                        <Cell key={i} fill={CLAIM_STATUS_COLORS[entry.name] || '#64748b'} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Recent claims preview */}
            <div style={{ background: '#0f172a', border: '1px solid #1e293b', borderRadius: 16, padding: '1.5rem' }}>
              <SectionHeader icon={Clock} title="Recent Pending Claims" subtitle="Needs your attention" />
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '0.75rem' }}>
                {claims.filter(c => c.status === 'Pending').slice(0, 3).map(claim => (
                  <ClaimCard key={claim._id} claim={claim}
                    onApprove={(id) => handleVerifyClaim(id, 'approve')}
                    onReject={(id) => handleVerifyClaim(id, 'reject')}
                  />
                ))}
                {claims.filter(c => c.status === 'Pending').length === 0 && (
                  <div style={{ color: '#64748b', fontSize: '0.85rem', padding: '1rem' }}>No pending claims 🎉</div>
                )}
              </div>
            </div>
          </div>
        )}

        {/* ══════════════════════════════════════
            ANALYTICS
        ══════════════════════════════════════ */}
        {activeSection === 'analytics' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>

            {/* Revenue + Transaction trend */}
            <div style={{ background: '#0f172a', border: '1px solid #1e293b', borderRadius: 16, padding: '1.5rem' }}>
              <SectionHeader icon={TrendingUp} title="Revenue & Transactions" subtitle="Monthly platform performance" />
              <ResponsiveContainer width="100%" height={280}>
                <AreaChart data={revenueByMonth} margin={{ top: 10, right: 10, left: 0, bottom: 0 }}>
                  <defs>
                    <linearGradient id="revGrad" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#f59e0b" stopOpacity={0.3} />
                      <stop offset="95%" stopColor="#f59e0b" stopOpacity={0} />
                    </linearGradient>
                    <linearGradient id="txGrad" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3} />
                      <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
                  <XAxis dataKey="month" tick={{ fill: '#64748b', fontSize: 12 }} axisLine={false} tickLine={false} />
                  <YAxis tick={{ fill: '#64748b', fontSize: 12 }} axisLine={false} tickLine={false} />
                  <Tooltip content={<CustomTooltip />} />
                  <Legend wrapperStyle={{ fontSize: '0.75rem', color: '#94a3b8' }} />
                  <Area type="monotone" dataKey="revenue" name="Revenue (₹)" stroke="#f59e0b" strokeWidth={2} fill="url(#revGrad)" dot={{ fill: '#f59e0b', r: 4 }} />
                  <Area type="monotone" dataKey="transactions" name="Transactions" stroke="#3b82f6" strokeWidth={2} fill="url(#txGrad)" dot={{ fill: '#3b82f6', r: 4 }} />
                </AreaChart>
              </ResponsiveContainer>
            </div>

            {/* Category breakdown + User split */}
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>

              <div style={{ background: '#0f172a', border: '1px solid #1e293b', borderRadius: 16, padding: '1.5rem' }}>
                <SectionHeader icon={BarChart2} title="Listings by Category" subtitle="Marketplace category split" />
                {categoryData.length > 0 ? (
                  <ResponsiveContainer width="100%" height={220}>
                    <BarChart data={categoryData} layout="vertical" barSize={14}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" horizontal={false} />
                      <XAxis type="number" tick={{ fill: '#64748b', fontSize: 11 }} axisLine={false} tickLine={false} />
                      <YAxis type="category" dataKey="name" tick={{ fill: '#94a3b8', fontSize: 11 }} axisLine={false} tickLine={false} width={80} />
                      <Tooltip content={<CustomTooltip />} />
                      <Bar dataKey="value" name="Items" radius={[0, 6, 6, 0]}>
                        {categoryData.map((_, i) => <Cell key={i} fill={PIE_COLORS[i % PIE_COLORS.length]} />)}
                      </Bar>
                    </BarChart>
                  </ResponsiveContainer>
                ) : (
                  <div style={{ color: '#64748b', fontSize: '0.85rem', paddingTop: '1rem' }}>No transaction data yet.</div>
                )}
              </div>

              <div style={{ background: '#0f172a', border: '1px solid #1e293b', borderRadius: 16, padding: '1.5rem' }}>
                <SectionHeader icon={Users} title="User Distribution" subtitle="Role breakdown" />
                <ResponsiveContainer width="100%" height={220}>
                  <PieChart>
                    <Pie
                      data={[
                        { name: 'Students', value: stats.users.students || 0 },
                        { name: 'Alumni', value: stats.users.alumni || 0 },
                        { name: 'Admins', value: stats.users.admins || 1 },
                      ]}
                      cx="50%" cy="50%" outerRadius={80} paddingAngle={3} dataKey="value"
                    >
                      {['#3b82f6', '#8b5cf6', '#f59e0b'].map((c, i) => <Cell key={i} fill={c} />)}
                    </Pie>
                    <Tooltip content={<CustomTooltip />} />
                    <Legend wrapperStyle={{ fontSize: '0.75rem', color: '#94a3b8' }} />
                  </PieChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Key metrics row */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '1rem' }}>
              {[
                { label: 'Avg. Platform Fee', value: transactions.length ? `₹${(transactions.reduce((s, t) => s + (t.platform_fee || 0), 0) / transactions.length).toFixed(1)}` : '₹0', color: '#f59e0b' },
                { label: 'Claim Approval Rate', value: claims.length ? `${Math.round((claims.filter(c => c.status === 'Approved').length / claims.length) * 100)}%` : '0%', color: '#22c55e' },
                { label: 'Resolution Rate', value: stats.lost_and_found.total_lost ? `${Math.round((stats.lost_and_found.resolved / stats.lost_and_found.total_lost) * 100)}%` : '0%', color: '#3b82f6' },
                { label: 'Avg. Reward Offered', value: (() => { const r = claims.filter(c => c.reward_amount > 0); return r.length ? `₹${Math.round(r.reduce((s, c) => s + c.reward_amount, 0) / r.length)}` : '₹0'; })(), color: '#8b5cf6' },
              ].map((m, i) => (
                <div key={i} style={{ background: '#0f172a', border: `1px solid ${m.color}33`, borderRadius: 14, padding: '1.25rem', textAlign: 'center' }}>
                  <div style={{ fontSize: '1.75rem', fontWeight: 800, color: m.color }}>{m.value}</div>
                  <div style={{ fontSize: '0.75rem', color: '#64748b', marginTop: '0.3rem' }}>{m.label}</div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* ══════════════════════════════════════
            CLAIMS
        ══════════════════════════════════════ */}
        {activeSection === 'claims' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>

            {/* Filter pills */}
            <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
              {['All', 'Pending', 'Approved', 'Rejected'].map(f => (
                <button
                  key={f}
                  onClick={() => setClaimFilter(f)}
                  style={{
                    padding: '0.4rem 1rem', borderRadius: 20, border: 'none', cursor: 'pointer',
                    fontSize: '0.8rem', fontWeight: 600, transition: 'all 0.2s',
                    background: claimFilter === f ? (f === 'Pending' ? '#f59e0b' : f === 'Approved' ? '#22c55e' : f === 'Rejected' ? '#ef4444' : '#3b82f6') : '#1e293b',
                    color: claimFilter === f ? 'white' : '#94a3b8',
                  }}
                >
                  {f} {f !== 'All' && `(${claims.filter(c => c.status === f).length})`}
                </button>
              ))}
            </div>

            {filteredClaims.length === 0 ? (
              <div style={{ textAlign: 'center', padding: '4rem', color: '#64748b' }}>
                <AlertCircle style={{ width: 40, height: 40, margin: '0 auto 1rem', color: '#334155' }} />
                No {claimFilter !== 'All' ? claimFilter.toLowerCase() : ''} claims found.
              </div>
            ) : (
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))', gap: '0.75rem' }}>
                {filteredClaims.map(claim => (
                  <ClaimCard key={claim._id} claim={claim}
                    onApprove={(id) => handleVerifyClaim(id, 'approve')}
                    onReject={(id) => handleVerifyClaim(id, 'reject')}
                  />
                ))}
              </div>
            )}
          </div>
        )}

        {/* ══════════════════════════════════════
            TRANSACTIONS
        ══════════════════════════════════════ */}
        {activeSection === 'transactions' && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>

            {/* Summary pills */}
            <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap' }}>
              {[
                { label: 'Total', value: transactions.length, color: '#3b82f6' },
                { label: 'Revenue', value: `₹${transactions.reduce((s, t) => s + (t.platform_fee || 0), 0)}`, color: '#f59e0b' },
                { label: 'Avg Price', value: transactions.length ? `₹${Math.round(transactions.reduce((s, t) => s + (t.price || 0), 0) / transactions.length)}` : '₹0', color: '#8b5cf6' },
              ].map((p, i) => (
                <div key={i} style={{ background: '#0f172a', border: `1px solid ${p.color}33`, borderRadius: 12, padding: '0.6rem 1.25rem', display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
                  <span style={{ fontSize: '1.1rem', fontWeight: 800, color: p.color }}>{p.value}</span>
                  <span style={{ fontSize: '0.75rem', color: '#64748b' }}>{p.label}</span>
                </div>
              ))}
            </div>

            {/* Table */}
            <div style={{ background: '#0f172a', border: '1px solid #1e293b', borderRadius: 16, overflow: 'hidden' }}>
              <div style={{ overflowX: 'auto' }}>
                <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.82rem' }}>
                  <thead>
                    <tr style={{ background: '#020817', borderBottom: '1px solid #1e293b' }}>
                      {['Item', 'Buyer', 'Seller', 'Price', 'Fee', 'Status', 'Date'].map(h => (
                        <th key={h} style={{ padding: '0.9rem 1rem', textAlign: h === 'Item' || h === 'Buyer' || h === 'Seller' ? 'left' : 'right', color: '#475569', fontWeight: 600, whiteSpace: 'nowrap' }}>
                          {h}
                        </th>
                      ))}
                    </tr>
                  </thead>
                  <tbody>
                    {transactions.map((tx, i) => (
                      <tr key={tx._id} style={{ borderBottom: '1px solid #1e293b', background: i % 2 === 0 ? 'transparent' : '#0f172a55', transition: 'background 0.15s' }}
                        onMouseEnter={e => e.currentTarget.style.background = '#1e293b'}
                        onMouseLeave={e => e.currentTarget.style.background = i % 2 === 0 ? 'transparent' : '#0f172a55'}
                      >
                        <td style={{ padding: '0.85rem 1rem', color: '#f1f5f9', fontWeight: 600 }}>{tx.item_name}</td>
                        <td style={{ padding: '0.85rem 1rem' }}>
                          <div style={{ color: '#cbd5e1', fontWeight: 500 }}>{tx.buyer_name}</div>
                          <div style={{ color: '#475569', fontSize: '0.72rem' }}>{tx.buyer_email}</div>
                        </td>
                        <td style={{ padding: '0.85rem 1rem' }}>
                          <div style={{ color: '#cbd5e1', fontWeight: 500 }}>{tx.seller_name}</div>
                          <div style={{ color: '#475569', fontSize: '0.72rem' }}>{tx.seller_email}</div>
                        </td>
                        <td style={{ padding: '0.85rem 1rem', textAlign: 'right', color: '#94a3b8' }}>₹{tx.price}</td>
                        <td style={{ padding: '0.85rem 1rem', textAlign: 'right' }}>
                          <span style={{ color: '#22c55e', fontWeight: 700 }}>₹{tx.platform_fee}</span>
                        </td>
                        <td style={{ padding: '0.85rem 1rem', textAlign: 'right' }}>
                          <span style={{ padding: '3px 10px', borderRadius: 20, fontSize: '0.7rem', fontWeight: 600, background: '#22c55e22', color: '#22c55e' }}>
                            {tx.status}
                          </span>
                        </td>
                        <td style={{ padding: '0.85rem 1rem', textAlign: 'right', color: '#475569', whiteSpace: 'nowrap' }}>
                          {new Date(tx.created_at).toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: '2-digit' })}
                        </td>
                      </tr>
                    ))}
                    {transactions.length === 0 && (
                      <tr>
                        <td colSpan={7} style={{ textAlign: 'center', padding: '3rem', color: '#475569' }}>No transactions yet.</td>
                      </tr>
                    )}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}