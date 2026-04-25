import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { loadStripe } from '@stripe/stripe-js';
import { Search, PlusCircle, AlertCircle, CheckCircle, MapPin, Tag, Clock, Filter, X } from 'lucide-react';
import { addNotification } from '../components/NotificationBell';

// Publishable key is safe to expose in frontend — it's not the secret key
const stripePromise = loadStripe(import.meta.env.VITE_STRIPE_PUBLISHABLE_KEY);


export default function LostAndFound() {
  const [activeTab, setActiveTab] = useState('browse');
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(true);
  const [typeFilter, setTypeFilter] = useState(''); // '', 'lost', 'found'
  const [claimModal, setClaimModal] = useState(null); // report object or null
  const [verificationText, setVerificationText] = useState('');
  const backendUrl = import.meta.env.VITE_API_URL || 'http://localhost:5000';
  const user = JSON.parse(localStorage.getItem('user') || 'null');

  const [formData, setFormData] = useState({
    type: 'lost',
    item_name: '',
    category: 'General',
    location: '',
    date: new Date().toISOString().split('T')[0],
    description: '',
    image: null,
  });

  const [rewardAmount, setRewardAmount] = useState('');

  useEffect(() => {
    if (activeTab === 'browse') {
      fetchReports();
    }
  }, [activeTab, typeFilter]);

  useEffect(() => {
    if (query.get("canceled")) {
      alert("Action was canceled.");
      window.history.replaceState({}, document.title, "/lost-found");
    }
  }, []);

  const fetchReports = async () => {
    setLoading(true);
    try {
      let url = `${backendUrl}/api/lostandfound/reports`;
      if (typeFilter) url += `?type=${typeFilter}`;
      const res = await axios.get(url);
      setReports(res.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleInputChange = (e) => {
    if (e.target.name === 'image') {
      setFormData({ ...formData, image: e.target.files[0] });
    } else {
      setFormData({ ...formData, [e.target.name]: e.target.value });
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const token = localStorage.getItem('token');
    if (!token) {
      alert("Please log in to submit a report.");
      return;
    }
    
    const submitData = new FormData();
    Object.keys(formData).forEach(key => {
      if (formData[key] !== null) {
        submitData.append(key, formData[key]);
      }
    });

    try {
      const res = await axios.post(`${backendUrl}/api/lostandfound/report`, submitData, {
        headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'multipart/form-data' }
      });
      
      if (res.data.matches && res.data.matches.length > 0) {
        const bestMatch = res.data.matches[0];
        const methodLabel = bestMatch.match_method === 'text+image' ? '📸 Text + Image AI' : '📝 Text AI';
        addNotification('match', '🎯 Possible Match Found!', 
          `${res.data.match_count} match(es) for "${formData.item_name}" via ${methodLabel}. Check Found items.`
        );
        alert(`Report submitted! 🎯 ${res.data.match_count} possible match(es) found!\n\nBest match: "${bestMatch.item_name}"\nCheck your notifications & Found items.`);
      } else {
        alert('Report submitted successfully!');
      }
      
      setFormData({
        type: 'lost', item_name: '', category: 'General', location: '',
        date: new Date().toISOString().split('T')[0], description: '', image: null
      });
      setActiveTab('browse');
    } catch (err) {
      console.error(err);
      alert('Error submitting report. Make sure you are logged in.');
    }
  };



  const handleClaim = async () => {
    const token = localStorage.getItem('token');
    if (!token) {
      alert("Please log in to claim an item.");
      return;
    }

    try {
      const res = await axios.post(`${backendUrl}/api/lostandfound/claim`, {
        report_id: claimModal._id,
        verification_details: verificationText,
        reward_amount: parseFloat(rewardAmount) || 0
      }, {
        headers: { Authorization: `Bearer ${token}` }
      });

      const reward = res.data.reward_amount || 0;
      addNotification('claim', '🙋 Claim Submitted!', `Your claim for "${claimModal.item_name}" is pending admin review.${ reward > 0 ? ` You offered ₹${reward} reward to the finder.` : ''}`);
      alert(`Claim submitted! ✅\nAdmin will verify your ownership.\n${ reward > 0 ? `🎁 ₹${reward} will be rewarded to the honest finder upon approval.` : ''}`);
      setClaimModal(null);
      setVerificationText('');
      setRewardAmount('');
    } catch (err) {
      console.error(err);
      alert(err.response?.data?.message || 'Error submitting claim.');
    }
  };

  return (
    <div className="max-w-6xl mx-auto px-4 py-8 animate-in fade-in zoom-in duration-500">
      <div className="flex flex-col md:flex-row justify-between items-center mb-10">
        <div>
          <h1 className="text-4xl font-extrabold text-slate-900 dark:text-white mb-2">
            Lost & Found
          </h1>
          <p className="text-slate-500 dark:text-slate-400">
            Reclaim what's yours or help others find theirs.
          </p>
        </div>
        
        <div className="flex mt-4 md:mt-0 bg-slate-100 dark:bg-slate-800 p-1 rounded-xl shadow-inner">
          <button 
            onClick={() => setActiveTab('browse')}
            className={`px-6 py-2.5 rounded-lg font-medium transition-all ${activeTab === 'browse' ? 'bg-white dark:bg-slate-700 shadow-sm text-blue-600 dark:text-blue-400' : 'text-slate-600 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700/50'}`}
          >
            <Search className="inline w-4 h-4 mr-2"/> Browse
          </button>
          {user?.role !== 'Admin' && (
            <button 
              onClick={() => setActiveTab('report')}
              className={`px-6 py-2.5 rounded-lg font-medium transition-all ${activeTab === 'report' ? 'bg-white dark:bg-slate-700 shadow-sm text-blue-600 dark:text-blue-400' : 'text-slate-600 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700/50'}`}
            >
              <PlusCircle className="inline w-4 h-4 mr-2"/> Report Item
            </button>
          )}
        </div>
      </div>

      {activeTab === 'browse' ? (
        <div className="space-y-6">
          {/* Type filter tabs */}
          <div className="flex items-center gap-3 flex-wrap">
            <Filter className="w-4 h-4 text-slate-400" />
            {['', 'lost', 'found'].map(t => (
              <button
                key={t}
                onClick={() => setTypeFilter(t)}
                className={`px-4 py-1.5 rounded-full text-sm font-semibold border transition-all ${
                  typeFilter === t
                    ? t === 'lost' ? 'border-red-500 bg-red-50 text-red-700 dark:bg-red-900/20 dark:text-red-400'
                      : t === 'found' ? 'border-emerald-500 bg-emerald-50 text-emerald-700 dark:bg-emerald-900/20 dark:text-emerald-400'
                      : 'border-blue-500 bg-blue-50 text-blue-700 dark:bg-blue-900/20 dark:text-blue-400'
                    : 'border-slate-200 dark:border-slate-700 text-slate-500 hover:border-slate-300'
                }`}
              >
                {t === '' ? 'All' : t === 'lost' ? '🔴 Lost' : '🟢 Found'}
              </button>
            ))}
          </div>

          {loading ? (
             <div className="flex justify-center p-12">
               <div className="animate-spin rounded-full h-12 w-12 border-b-4 border-blue-600"></div>
             </div>
          ) : reports.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {reports.map((report) => (
                <div key={report._id} className="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-2xl overflow-hidden shadow-sm hover:shadow-lg transition-all duration-300 group hover:-translate-y-1">
                  <div className={`h-2 ${report.type === 'lost' ? 'bg-red-500' : 'bg-emerald-500'}`}></div>
                  
                  {/* Image display */}
                  {report.image_url && (
                    <div className="h-48 bg-slate-100 dark:bg-slate-700/50 overflow-hidden">
                      <img src={report.image_url} alt={report.item_name} className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300" onError={(e) => e.target.style.display='none'} />
                    </div>
                  )}
                  
                  <div className="p-6">
                    <div className="flex justify-between items-start mb-4">
                      <span className={`px-3 py-1 rounded-full text-xs font-bold uppercase tracking-wider ${report.type === 'lost' ? 'bg-red-100 text-red-700 dark:bg-red-900/30 dark:text-red-400' : 'bg-emerald-100 text-emerald-700 dark:bg-emerald-900/30 dark:text-emerald-400'}`}>
                        {report.type === 'lost' ? <AlertCircle className="inline w-3 h-3 mr-1" /> : <CheckCircle className="inline w-3 h-3 mr-1" />}
                        {report.type}
                      </span>
                      <span className="text-xs text-slate-400 flex items-center">
                        <Clock className="w-3 h-3 mr-1" />
                        {report.date || new Date(report.created_at).toLocaleDateString()}
                      </span>
                    </div>
                    <h3 className="text-xl font-bold mb-2 group-hover:text-blue-600 dark:group-hover:text-blue-400 transition-colors">{report.item_name}</h3>
                    <p className="text-slate-600 dark:text-slate-300 text-sm mb-4 line-clamp-2">
                       {report.description || 'No description provided.'}
                    </p>
                    <div className="flex flex-col gap-2 text-sm text-slate-500 dark:text-slate-400 mb-6">
                       {report.user_anon_name && (
                         <span className="flex items-center text-blue-500 font-semibold italic">
                           <Clock className="w-4 h-4 mr-2 text-slate-400"/> Reported by: {report.user_anon_name}
                         </span>
                       )}
                       <span className="flex items-center"><Tag className="w-4 h-4 mr-2"/> {report.category}</span>
                       {report.location && <span className="flex items-center"><MapPin className="w-4 h-4 mr-2"/> {report.location}</span>}
                    </div>
                    
                    {report.type === 'found' && (
                       user?.role === 'Admin' ? (
                        <div className="w-full mt-2 py-2 px-3 bg-amber-50 dark:bg-amber-900/20 border border-amber-200 dark:border-amber-800 rounded-xl text-xs text-amber-700 dark:text-amber-400 font-medium text-center">
                           Admin restricted from claiming items
                        </div>
                       ) : (
                        <button 
                          onClick={() => setClaimModal(report)}
                          className="w-full py-2.5 bg-blue-600 text-white rounded-xl font-medium hover:bg-blue-700 transition-all shadow-sm hover:shadow-md active:scale-95"
                        >
                          🙋 Claim This Item
                        </button>
                       )
                    )}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-24 bg-white dark:bg-slate-800 rounded-2xl border border-dashed border-slate-300 dark:border-slate-700">
               <AlertCircle className="w-16 h-16 text-slate-400 mx-auto mb-4" />
               <h3 className="text-xl font-medium text-slate-600 dark:text-slate-300">No reports found</h3>
               <p className="text-slate-500 mt-2">Be the first to report an item.</p>
            </div>
          )}
        </div>
      ) : (
        <div className="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 p-8 rounded-2xl max-w-2xl mx-auto shadow-sm">
          <h2 className="text-2xl font-bold mb-6">Report an Item</h2>
          
          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="grid grid-cols-2 gap-4">
              <button 
                type="button"
                onClick={() => setFormData({...formData, type: 'lost'})}
                className={`py-3 rounded-xl font-medium border-2 transition-all ${formData.type === 'lost' ? 'border-red-500 bg-red-50 text-red-700 dark:bg-red-900/20 dark:text-red-400' : 'border-slate-200 dark:border-slate-700 text-slate-500 hover:border-slate-300'}`}
              >
                🔴 I lost something
              </button>
              <button 
                type="button"
                onClick={() => setFormData({...formData, type: 'found'})}
                className={`py-3 rounded-xl font-medium border-2 transition-all ${formData.type === 'found' ? 'border-emerald-500 bg-emerald-50 text-emerald-700 dark:bg-emerald-900/20 dark:text-emerald-400' : 'border-slate-200 dark:border-slate-700 text-slate-500 hover:border-slate-300'}`}
              >
                🟢 I found something
              </button>
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Item Name *</label>
              <input required type="text" name="item_name" value={formData.item_name} onChange={handleInputChange} className="w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-600 bg-transparent focus:ring-2 focus:ring-blue-500 outline-none transition-all dark:text-white" placeholder="e.g. Blue Hydro Flask" />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
               <div>
                  <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Category</label>
                  <select name="category" value={formData.category} onChange={handleInputChange} className="w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-blue-500 outline-none transition-all">
                    <option>Electronics</option>
                    <option>Books</option>
                    <option>Keys & Wallets</option>
                    <option>Clothing</option>
                    <option>ID Cards</option>
                    <option>General</option>
                  </select>
               </div>
               <div>
                  <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Date Lost/Found</label>
                  <input type="date" name="date" value={formData.date} onChange={handleInputChange} className="w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-blue-500 outline-none transition-all" />
               </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Location</label>
              <input type="text" name="location" value={formData.location} onChange={handleInputChange} className="w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-600 bg-transparent focus:ring-2 focus:ring-blue-500 outline-none transition-all dark:text-white" placeholder="e.g. Library 2nd Floor" />
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Description</label>
              <textarea name="description" value={formData.description} onChange={handleInputChange} rows="4" className="w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-600 bg-transparent focus:ring-2 focus:ring-blue-500 outline-none transition-all dark:text-white" placeholder="Provide details like color, brand, distinct marks..."></textarea>
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Image Upload</label>
              <input type="file" name="image" accept="image/*" onChange={handleInputChange} className="w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-600 bg-transparent focus:ring-2 focus:ring-blue-500 outline-none transition-all dark:text-white" />
              {formData.image && (
                <div className="text-sm mt-2 text-blue-600 font-medium">{formData.image.name}</div>
              )}
            </div>

            <button type="submit" className="w-full py-4 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-xl shadow-lg shadow-blue-500/30 transition-all hover:-translate-y-1">
              Submit Report
            </button>
          </form>
        </div>
      )}

      {/* Claim Modal */}
      {claimModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4 animate-in fade-in">
          <div className="bg-white dark:bg-slate-900 rounded-3xl w-full max-w-md overflow-hidden shadow-2xl relative">
            <button onClick={() => {setClaimModal(null); setVerificationText(''); setRewardAmount('');}} className="absolute top-4 right-4 p-2 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 transition-colors">
              <X className="w-5 h-5" />
            </button>
            <div className="p-8">
              <h2 className="text-2xl font-extrabold mb-1 text-slate-900 dark:text-white">Claim Item</h2>
              <p className="text-slate-500 mb-2">Claiming: <strong>{claimModal.item_name}</strong></p>

              {/* Reward Banner */}
              <div className="flex items-start gap-3 bg-emerald-50 dark:bg-emerald-900/20 border border-emerald-200 dark:border-emerald-800 rounded-xl p-3 mb-6">
                <span className="text-2xl">🎁</span>
                <div>
                  <p className="text-sm font-bold text-emerald-700 dark:text-emerald-400">Reward the honest finder!</p>
                  <p className="text-xs text-emerald-600 dark:text-emerald-500 mt-0.5">The platform charges <strong>zero fees</strong>. Any reward you offer goes <strong>100% to the person who found your item.</strong></p>
                </div>
              </div>

              <div className="mb-5">
                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Prove it's yours *</label>
                <textarea
                  value={verificationText}
                  onChange={(e) => setVerificationText(e.target.value)}
                  rows="3"
                  className="w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-600 bg-transparent focus:ring-2 focus:ring-blue-500 outline-none transition-all dark:text-white"
                  placeholder="e.g. It has a scratch on the back, serial number XYZ123, initials written inside..."
                  required
                />
              </div>

              <div className="mb-6">
                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">
                  🎁 Thank You Reward for Finder <span className="text-slate-400 font-normal">(optional)</span>
                </label>
                <div className="relative">
                  <span className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-500 font-bold">₹</span>
                  <input
                    type="number"
                    value={rewardAmount}
                    onChange={(e) => setRewardAmount(e.target.value)}
                    min="0"
                    placeholder="e.g. 50"
                    className="w-full pl-8 pr-4 py-3 rounded-xl border border-slate-300 dark:border-slate-600 bg-transparent focus:ring-2 focus:ring-emerald-500 outline-none transition-all dark:text-white"
                  />
                </div>
                {parseFloat(rewardAmount) > 0 ? (
                  <div className="mt-2 text-sm text-emerald-600 dark:text-emerald-400 font-semibold">
                    ✅ ₹{parseFloat(rewardAmount)} will go entirely to the finder. Platform fee: ₹0.
                  </div>
                ) : (
                  <div className="mt-2 text-xs text-slate-400">No reward offered — that's okay too!</div>
                )}
              </div>

              <button
                onClick={handleClaim}
                disabled={!verificationText.trim()}
                className="w-full py-3.5 bg-blue-600 hover:bg-blue-700 disabled:bg-slate-300 disabled:cursor-not-allowed text-white font-bold rounded-xl shadow-lg shadow-blue-500/30 transition-all"
              >
                {parseFloat(rewardAmount) > 0 ? `Submit Claim + 🎁 ₹${parseFloat(rewardAmount)} Reward` : 'Submit Claim Request'}
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
