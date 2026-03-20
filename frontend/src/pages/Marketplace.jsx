import React, { useState, useEffect } from 'react';
import axios from 'axios';
import { ShoppingBag, Tag, ShoppingCart, IndianRupee, MapPin, Search, SlidersHorizontal, X } from 'lucide-react';
import { addNotification } from '../components/NotificationBell';

export default function Marketplace() {
  const [activeTab, setActiveTab] = useState('browse');
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [submitting,setSubmitting] = useState(false);

  // Filters
  const [category, setCategory] = useState('');
  const [minPrice, setMinPrice] = useState('');
  const [maxPrice, setMaxPrice] = useState('');
  const [searchQuery, setSearchQuery] = useState('');

  // Sell form states
  const [formData, setFormData] = useState({
    title: '',
    category: 'General',
    price: '',
    description: '',
    location: '',
    image: null
  });

  const [editingItem, setEditingItem] = useState(null);
  const user = JSON.parse(localStorage.getItem('user') || 'null');

  // Payment modal
  const [paymentModal, setPaymentModal] = useState(null); // item object or null

  useEffect(() => {
    if (activeTab === 'browse') {
      fetchItems();
    }
  }, [activeTab, category]);

  useEffect(() => {
    const query = new URLSearchParams(window.location.search);
    if (query.get("success")) {
      const sessionId = query.get("session_id");
      const itemId = query.get("item_id");
      if (sessionId && itemId) {
         verifyStripePayment(sessionId, itemId);
      }
    }
    if (query.get("canceled")) {
      alert("Payment was canceled.");
      // Clean up URL
      window.history.replaceState({}, document.title, "/marketplace");
    }
  }, []);

  const verifyStripePayment = async (sessionId, itemId) => {
    const token = localStorage.getItem('token');
    if (!token) return;
    try {
      await axios.post(`/api/marketplace/buy/${itemId}`, { session_id: sessionId }, {
        headers: { Authorization: `Bearer ${token}` }
      });
      alert('Payment Successful!');
      fetchItems();
      window.history.replaceState({}, document.title, "/marketplace");
    } catch (err) {
      console.error(err);
      alert("Payment verification failed.");
    }
  };

  const fetchItems = async () => {
  setLoading(true);
  try {
    const params = new URLSearchParams();

    if (category) params.append('category', category);
    if (minPrice !== undefined && minPrice !== null && minPrice !=='')
      params.append('min_price', minPrice);
    if (maxPrice !== undefined && maxPrice !== null && maxPrice !=='')
      params.append('max_price', maxPrice);
    if (searchQuery) params.append('search', searchQuery);

    const query = params.toString();
    const url = query
      ? `/api/marketplace/items?${query}`
      : `/api/marketplace/items`;

    console.log("URL:", url);

    const res = await axios.get(url);
    setItems(res.data);
  } catch (err) {
    console.error(err);
  } finally {
    setLoading(false);
  }
};
  const handleSearch = (e) => {
    e.preventDefault();
    fetchItems();
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
    addNotification('marketplace', 'Error', 'Please log in to list items.');
    return;
  }

  if (!formData.title || !formData.price) {
    alert("Title and Price are required");
    return;
  }

  if (isNaN(formData.price)) {
    alert("Price must be a number");
    return;
  }

  setSubmitting(true);

  const submitData = new FormData();

  submitData.append('title', formData.title);
  submitData.append('price', formData.price);
  submitData.append('category', formData.category);
  submitData.append('description', formData.description);
  submitData.append('location', formData.location);

  if (formData.image) {
    submitData.append('image', formData.image);
  }

  try {
    const config = {
      headers: {
        Authorization: `Bearer ${token}`
      }
    };

    if (editingItem) {
      await axios.put(`/api/marketplace/items/${editingItem._id}`, submitData, config);
      alert('Item updated successfully!');
    } else {
      await axios.post('/api/marketplace/items', submitData, config);
      alert('Item listed successfully!');
    }

  } catch (err) {
    console.error("Error:", err.response?.data || err.message);
    alert(err.response?.data?.message || 'Error saving item');
  } finally {
    setSubmitting(false);
  }
};
  const handleDelete = async (itemId) => {
    if(!window.confirm("Are you sure you want to delete this item?")) return;
    const token = localStorage.getItem('token');
    try {
      await axios.delete(`/api/marketplace/items/${itemId}`, {
        headers: { Authorization: `Bearer ${token}` }
      });
      fetchItems();
    } catch (err) {
      console.error(err);
      alert('Error deleting item');
    }
  };

  const handleEdit = (item) => {
    setEditingItem(item);
    setFormData({
      title: item.title,
      category: item.category,
      price: item.price,
      description: item.description,
      location: item.pickup_location,
      image: null
    });
    setActiveTab('sell');
  };

  const openPaymentModal = (item) => {
    const token = localStorage.getItem('token');
    if (!token) {
      alert("Please log in to buy items.");
      return;
    }
    setPaymentModal(item);
  };



  const handlePayAndBuy = async () => {
    const token = localStorage.getItem('token');
    if (!token) return;

    try {
      // Create order
      const res = await axios.post(`/api/marketplace/buy/${paymentModal._id}`, {}, {
        headers: { Authorization: `Bearer ${token}` }
      });

      const orderData = res.data;
      if (orderData.key === 'mock' || !orderData.url) {
        // Mock success (No real stripe key provided)
        addNotification('purchase', '🎉 Purchase Successful!', `You bought "${paymentModal.title}" for ₹${orderData.total_charged}. Meet the seller on campus for pickup.`);
        alert(`✅ Mock Payment Successful!\n\nItem: ${paymentModal.title}\nTotal Charged: ₹${orderData.total_charged}\n\nMeet the seller on campus.`);
        setPaymentModal(null);
        fetchItems();
        return;
      }

      // Redirect to Stripe Checkout
      window.location.href = orderData.url;

    } catch (err) {
      console.error(err);
      alert(err.response?.data?.message || 'Error processing purchase');
    }
  };

  const itemPrice = paymentModal ? parseFloat(paymentModal.price) : 0;
  const platformFee = paymentModal ? Math.round(itemPrice * 0.05 * 100) / 100 : 0;
  const totalAmount = itemPrice + platformFee;

  return (
    <div className="max-w-6xl mx-auto px-4 py-8 animate-in fade-in zoom-in duration-500">
      <div className="flex flex-col md:flex-row justify-between items-center mb-10">
        <div>
          <h1 className="text-4xl font-extrabold text-slate-900 dark:text-white mb-2">
            Campus Marketplace
          </h1>
          <p className="text-slate-500 dark:text-slate-400">
            Buy and sell used books, electronics, and more on campus.
          </p>
        </div>
        
        <div className="flex mt-4 md:mt-0 bg-slate-100 dark:bg-slate-800 p-1 rounded-xl shadow-inner">
          <button 
            onClick={() => setActiveTab('browse')}
            className={`px-6 py-2.5 rounded-lg font-medium transition-all ${activeTab === 'browse' ? 'bg-white dark:bg-slate-700 shadow-sm text-purple-600 dark:text-purple-400' : 'text-slate-600 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700/50'}`}
          >
            <ShoppingBag className="inline w-4 h-4 mr-2"/> Browse
          </button>
          <button 
            onClick={() => setActiveTab('sell')}
            className={`px-6 py-2.5 rounded-lg font-medium transition-all ${activeTab === 'sell' ? 'bg-white dark:bg-slate-700 shadow-sm text-purple-600 dark:text-purple-400' : 'text-slate-600 dark:text-slate-300 hover:bg-slate-200 dark:hover:bg-slate-700/50'}`}
          >
            <Tag className="inline w-4 h-4 mr-2"/> Sell an Item
          </button>
        </div>
      </div>

      {activeTab === 'browse' ? (
        <div className="space-y-6">
          {/* Filters Bar */}
          <div className="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 rounded-2xl p-4">
            <form onSubmit={handleSearch} className="flex flex-col md:flex-row gap-4 items-end">
              <div className="flex-grow">
                <label className="block text-xs font-medium text-slate-500 mb-1"><Search className="inline w-3 h-3 mr-1"/>Search</label>
                <input 
                  type="text" value={searchQuery} onChange={(e) => setSearchQuery(e.target.value)}
                  className="w-full px-3 py-2 rounded-lg border border-slate-300 dark:border-slate-600 bg-transparent focus:ring-2 focus:ring-purple-500 outline-none text-sm dark:text-white"
                  placeholder="Search items..."
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-slate-500 mb-1"><Tag className="inline w-3 h-3 mr-1"/>Category</label>
                <select 
                  value={category} onChange={(e) => setCategory(e.target.value)} 
                  className="px-3 py-2 rounded-lg border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 focus:ring-2 focus:ring-purple-500 outline-none text-sm"
                >
                  <option value="">All</option>
                  <option value="Electronics">Electronics</option>
                  <option value="Books">Books</option>
                  <option value="Furniture">Furniture</option>
                  <option value="Hostel Items">Hostel Items</option>
                  <option value="General">General</option>
                </select>
              </div>
              <div>
                <label className="block text-xs font-medium text-slate-500 mb-1"><IndianRupee className="inline w-3 h-3 mr-1"/>Min Price</label>
                <input 
                  type="number" value={minPrice} onChange={(e) => setMinPrice(e.target.value)} min="0"
                  className="w-24 px-3 py-2 rounded-lg border border-slate-300 dark:border-slate-600 bg-transparent focus:ring-2 focus:ring-purple-500 outline-none text-sm dark:text-white"
                  placeholder="₹0"
                />
              </div>
              <div>
                <label className="block text-xs font-medium text-slate-500 mb-1"><IndianRupee className="inline w-3 h-3 mr-1"/>Max Price</label>
                <input 
                  type="number" value={maxPrice} onChange={(e) => setMaxPrice(e.target.value)} min="0"
                  className="w-24 px-3 py-2 rounded-lg border border-slate-300 dark:border-slate-600 bg-transparent focus:ring-2 focus:ring-purple-500 outline-none text-sm dark:text-white"
                  placeholder="₹∞"
                />
              </div>
              <button type="submit" className="px-5 py-2 bg-purple-600 text-white rounded-lg font-medium hover:bg-purple-700 transition-all text-sm shadow-sm flex items-center gap-1">
                <SlidersHorizontal className="w-4 h-4"/> Apply
              </button>
            </form>
          </div>

          {loading ? (
             <div className="flex justify-center p-12">
               <div className="animate-spin rounded-full h-12 w-12 border-b-4 border-purple-600"></div>
             </div>
          ) : items.length > 0 ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
              {items.map((item) => (
                <div key={item._id} className="bg-white dark:bg-slate-800 rounded-2xl overflow-hidden shadow-sm hover:shadow-xl transition-all duration-300 group hover:-translate-y-2 border border-slate-200 dark:border-slate-700 flex flex-col">
                  {/* Image or placeholder */}
                  <div className="h-48 bg-slate-100 dark:bg-slate-700/50 flex items-center justify-center text-slate-300 relative overflow-hidden">
                     {item.image_url ? (
                       <img src={item.image_url} alt={item.title} className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-300" onError={(e) => { e.target.style.display='none'; e.target.nextSibling.style.display='flex'; }} />
                     ) : null}
                     <div className={`${item.image_url ? 'hidden' : 'flex'} items-center justify-center w-full h-full`}>
                       <ShoppingBag className="w-16 h-16 opacity-30"/>
                     </div>
                     <span className="absolute top-2 right-2 bg-purple-600 text-white text-xs font-bold px-3 py-1 rounded-full shadow-md">
                        {item.category}
                     </span>
                  </div>
                  
                  <div className="p-5 flex flex-col flex-grow">
                    <h3 className="text-lg font-bold mb-1 truncate group-hover:text-purple-600 dark:group-hover:text-purple-400 transition-colors">{item.title}</h3>
                    <div className="flex items-center text-xl font-extrabold text-slate-900 dark:text-white mb-1">
                       <IndianRupee className="w-5 h-5 mr-1 text-slate-400" />
                       {item.price}
                    </div>
                    <div className="text-xs text-slate-400 mb-3">+ ₹{Math.round(item.price * 0.05)} platform fee</div>
                    <p className="text-slate-500 dark:text-slate-400 text-sm mb-4 line-clamp-2 flex-grow">
                       {item.description || "No description provided."}
                    </p>
                    {item.pickup_location && (
                      <div className="text-xs text-slate-400 mb-3 flex items-center">
                        <MapPin className="w-3 h-3 mr-1"/> {item.pickup_location}
                      </div>
                    )}
                    
                    {user && user.id === item.seller_id ? (
                      <div className="flex gap-2 w-full mt-2">
                         <button 
                            onClick={() => handleEdit(item)}
                            className="flex-1 py-2 bg-slate-100 text-slate-700 dark:bg-slate-700 dark:text-slate-200 rounded-xl font-bold hover:bg-slate-200 dark:hover:bg-slate-600 transition-all text-sm"
                         >
                            Edit
                         </button>
                         <button 
                            onClick={() => handleDelete(item._id)}
                            className="flex-1 py-2 bg-red-100 text-red-600 dark:bg-red-900/30 dark:text-red-400 rounded-xl font-bold hover:bg-red-200 dark:hover:bg-red-900/50 transition-all text-sm"
                         >
                            Delete
                         </button>
                      </div>
                    ) : (
                      <button 
                        onClick={() => openPaymentModal(item)}
                        className="w-full mt-2 py-2.5 bg-purple-600 text-white rounded-xl font-bold hover:bg-purple-700 shadow-lg shadow-purple-500/30 transition-all active:scale-95 flex items-center justify-center"
                      >
                        <ShoppingCart className="w-4 h-4 mr-2" /> Buy Now
                      </button>
                    )}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="text-center py-24 bg-white dark:bg-slate-800 rounded-2xl border border-dashed border-slate-300 dark:border-slate-700">
               <Tag className="w-16 h-16 text-slate-300 dark:text-slate-600 mx-auto mb-4" />
               <h3 className="text-xl font-medium text-slate-600 dark:text-slate-300">No items available</h3>
               <p className="text-slate-500 mt-2">Check back later or change filters.</p>
            </div>
          )}
        </div>
      ) : (
        <div className="bg-white dark:bg-slate-800 border border-slate-200 dark:border-slate-700 p-8 rounded-2xl max-w-2xl mx-auto shadow-sm">
          <h2 className="text-2xl font-bold mb-6">{editingItem ? 'Edit Item' : 'List an Item for Sale'}</h2>
          
          <form onSubmit={handleSubmit} className="space-y-6">
            <div>
              <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Item Name *</label>
              <input required type="text" name="title" value={formData.title} onChange={handleInputChange} className="w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-600 bg-transparent focus:ring-2 focus:ring-purple-500 outline-none transition-all dark:text-white" placeholder="e.g. Engineering Mathematics Book" />
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
               <div>
                  <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Category</label>
                  <select name="category" value={formData.category} onChange={handleInputChange} className="w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-600 bg-white dark:bg-slate-800 text-slate-900 dark:text-white focus:ring-2 focus:ring-purple-500 outline-none transition-all">
                    <option>Electronics</option>
                    <option>Books</option>
                    <option>Furniture</option>
                    <option>Hostel Items</option>
                    <option>General</option>
                  </select>
               </div>
               <div>
                  <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Price (₹) *</label>
                  <input required type="number" name="price" value={formData.price} onChange={handleInputChange} min="0" className="w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-600 bg-transparent focus:ring-2 focus:ring-purple-500 outline-none transition-all dark:text-white" placeholder="e.g. 500" />
               </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Description</label>
              <textarea name="description" value={formData.description} onChange={handleInputChange} rows="4" className="w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-600 bg-transparent focus:ring-2 focus:ring-purple-500 outline-none transition-all dark:text-white" placeholder="Condition, specs, reason for selling..."></textarea>
            </div>

            <div>
              <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Image Upload</label>
              <input type="file" name="image" accept="image/*" onChange={handleInputChange} className="w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-600 bg-transparent focus:ring-2 focus:ring-purple-500 outline-none transition-all dark:text-white" />
              {formData.image && (
                <div className="text-sm mt-2 text-purple-600 font-medium">{formData.image.name}</div>
              )}
            </div>
            
            <div>
              <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-2">Pickup Location</label>
              <input type="text" name="location" value={formData.location} onChange={handleInputChange} className="w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-600 bg-transparent focus:ring-2 focus:ring-purple-500 outline-none transition-all dark:text-white" placeholder="e.g. Meet at Main Gate" />
            </div>

            {formData.price && (
              <div className="bg-purple-50 dark:bg-purple-900/20 border border-purple-200 dark:border-purple-800 rounded-xl p-4 text-sm">
                <div className="flex justify-between mb-1"><span className="text-slate-600 dark:text-slate-400">Your price:</span> <span className="font-bold">₹{formData.price}</span></div>
                <div className="flex justify-between mb-1"><span className="text-slate-600 dark:text-slate-400">Platform fee (5%):</span> <span className="font-bold text-purple-600">₹{Math.round(parseFloat(formData.price || 0) * 0.05)}</span></div>
                <hr className="border-purple-200 dark:border-purple-800 my-2"/>
                <div className="flex justify-between"><span className="font-semibold">Buyer pays:</span> <span className="font-extrabold text-purple-700 dark:text-purple-400">₹{parseFloat(formData.price || 0) + Math.round(parseFloat(formData.price || 0) * 0.05)}</span></div>
                <p className="text-xs text-slate-400 mt-2">You receive ₹{formData.price}. Platform keeps the fee.</p>
              </div>
            )}

            <button type="submit" className="w-full py-4 bg-purple-600 hover:bg-purple-700 text-white font-bold rounded-xl shadow-lg shadow-purple-500/30 transition-all hover:-translate-y-1">
              {editingItem ? 'Update Item' : 'List Item'}
            </button>
          </form>
        </div>
      )}

      {/* Payment / Checkout Modal (simulates Razorpay/Stripe flow) */}
      {paymentModal && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4 animate-in fade-in">
          <div className="bg-white dark:bg-slate-900 rounded-3xl w-full max-w-md overflow-hidden shadow-2xl relative">
            <button onClick={() => setPaymentModal(null)} className="absolute top-4 right-4 p-2 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 transition-colors z-10">
              <X className="w-5 h-5" />
            </button>
            
            {/* Simulated Payment Gateway Header */}
            <div className="bg-gradient-to-r from-purple-600 to-indigo-600 p-6 text-white">
              <div className="flex items-center gap-2 mb-1">
                <div className="w-8 h-8 bg-white/20 rounded-lg flex items-center justify-center">
                  <IndianRupee className="w-5 h-5" />
                </div>
                <span className="font-bold text-lg">CampusConnect Pay</span>
              </div>
              <p className="text-purple-200 text-sm">Secure campus payment gateway</p>
            </div>

            <div className="p-6">
              {/* Order Summary */}
              <div className="mb-6">
                <h3 className="font-bold text-lg mb-4 text-slate-900 dark:text-white">Order Summary</h3>
                <div className="bg-slate-50 dark:bg-slate-800 rounded-xl p-4 space-y-3 border border-slate-200 dark:border-slate-700">
                  <div className="flex justify-between items-start">
                    <div>
                      <div className="font-bold text-slate-900 dark:text-white">{paymentModal.title}</div>
                      <div className="text-xs text-slate-400">{paymentModal.category}</div>
                    </div>
                    {paymentModal.image_url && (
                      <img src={paymentModal.image_url} alt="" className="w-12 h-12 rounded-lg object-cover" />
                    )}
                  </div>
                  <hr className="border-slate-200 dark:border-slate-700"/>
                  <div className="flex justify-between text-sm"><span className="text-slate-500">Item Price</span><span className="font-medium">₹{itemPrice}</span></div>
                  <div className="flex justify-between text-sm"><span className="text-slate-500">Platform Fee (5%)</span><span className="font-medium text-purple-600">₹{platformFee}</span></div>
                  <hr className="border-slate-200 dark:border-slate-700"/>
                  <div className="flex justify-between text-base"><span className="font-bold">Total</span><span className="font-extrabold text-lg text-purple-700 dark:text-purple-400">₹{totalAmount}</span></div>
                </div>
              </div>

              {/* Proceed to Payment */}

              <button 
                onClick={handlePayAndBuy}
                className="w-full py-3.5 bg-gradient-to-r from-purple-600 to-indigo-600 hover:from-purple-700 hover:to-indigo-700 text-white font-bold rounded-xl shadow-lg shadow-purple-500/30 transition-all active:scale-95 flex items-center justify-center gap-2"
              >
                <ShoppingCart className="w-5 h-5" />
                Pay ₹{totalAmount}
              </button>
              <p className="text-center text-xs text-slate-400 mt-3">🔒 Secured by CampusConnect Pay · Stripe Integration</p>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
