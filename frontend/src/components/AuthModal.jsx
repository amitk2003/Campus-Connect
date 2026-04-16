import React, { useState } from 'react';
import axios from 'axios';
import { X } from 'lucide-react';

export default function AuthModal({ isOpen, onClose, onLogin }) {
  const [activeView, setActiveView] = useState('login'); // login, register, forgot
  const [formData, setFormData] = useState({
    name: '',
    email: '',
    password: '',
    role: 'Student'
  });
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);

  if (!isOpen) return null;

  const handleInputChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setLoading(true);
    
    try {
      if (activeView === 'forgot') {
        const res = await axios.post('/api/auth/forgot-password', { email: formData.email });
        setSuccess(res.data.message);
        return;
      }

      const endpoint = activeView === 'login' ? '/api/auth/login' : '/api/auth/register';
      const res = await axios.post(`${endpoint}`, formData);
      
      if (activeView === 'login') {
        localStorage.setItem('token', res.data.access_token);
        localStorage.setItem('user', JSON.stringify({ 
          id: res.data.user_id, 
          name: res.data.name, 
          role: res.data.role 
        }));
        onLogin(res.data.name);
        onClose();
      } else {
        alert('Registration successful! Please login.');
        setActiveView('login');
      }
    } catch (err) {
      setError(err.response?.data?.message || 'An error occurred');
    } finally {
      setLoading(false);
    }
  };

  const handleGoogleLogin = async () => {
    // Mocking Google Auth flow
    // In real app: use Google SDK to get user info
    const mockGoogleData = {
      email: prompt("Enter Google Email:", formData.email),
      name: "Google User",
      google_id: "google_12345",
      role: formData.role
    };

    if (!mockGoogleData.email) return;

    try {
      const res = await axios.post('/api/auth/google-login', mockGoogleData);
      localStorage.setItem('token', res.data.access_token);
      localStorage.setItem('user', JSON.stringify({ 
        id: res.data.user_id, 
        name: res.data.name, 
        role: res.data.role 
      }));
      onLogin(res.data.name);
      onClose();
    } catch (err) {
      setError(err.response?.data?.message || 'Google login failed');
    }
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 backdrop-blur-sm p-4 animate-in fade-in">
      <div className="bg-white dark:bg-slate-900 rounded-3xl w-full max-w-md overflow-hidden shadow-2xl relative">
        <button onClick={onClose} className="absolute top-4 right-4 p-2 text-slate-400 hover:text-slate-600 dark:hover:text-slate-200 transition-colors">
          <X className="w-5 h-5" />
        </button>
        
        <div className="p-8">
          <h2 className="text-3xl font-extrabold mb-1 text-slate-900 dark:text-white">
            {activeView === 'login' ? 'Welcome Back' : activeView === 'register' ? 'Create Account' : 'Reset Password'}
          </h2>
          <p className="text-slate-500 mb-8">
            {activeView === 'login' ? 'Login to continue to CampusConnect.' : 
             activeView === 'register' ? 'Join your campus community.' : 
             'Enter your email to receive reset instructions.'}
          </p>

          {error && <div className="mb-4 p-3 bg-red-100 dark:bg-red-900/30 text-red-700 dark:text-red-400 text-sm font-medium rounded-xl">{error}</div>}
          {success && <div className="mb-4 p-3 bg-green-100 dark:bg-green-900/30 text-green-700 dark:text-green-400 text-sm font-medium rounded-xl">{success}</div>}

          <form onSubmit={handleSubmit} className="space-y-4">
            {activeView === 'register' && (
              <div>
                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Full Name</label>
                <input required type="text" name="name" value={formData.name} onChange={handleInputChange} className="w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-700 bg-transparent focus:ring-2 focus:ring-blue-500 outline-none transition-all dark:text-white" placeholder="John Doe" />
              </div>
            )}
            
            <div>
              <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">College Email</label>
              <input required type="email" name="email" value={formData.email} onChange={handleInputChange} className="w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-700 bg-transparent focus:ring-2 focus:ring-blue-500 outline-none transition-all dark:text-white" placeholder="you@university.edu" />
            </div>

            {activeView !== 'forgot' && (
              <div>
                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">Password</label>
                <input required type="password" name="password" value={formData.password} onChange={handleInputChange} className="w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-700 bg-transparent focus:ring-2 focus:ring-blue-500 outline-none transition-all dark:text-white" placeholder="••••••••" />
                {activeView === 'login' && (
                   <button type="button" onClick={() => setActiveView('forgot')} className="text-xs text-blue-600 hover:underline mt-1 block">
                     Forgot password?
                   </button>
                )}
              </div>
            )}

            {activeView === 'register' && (
              <div>
                <label className="block text-sm font-medium text-slate-700 dark:text-slate-300 mb-1">I am a...</label>
                <select name="role" value={formData.role} onChange={handleInputChange} className="w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-900 text-slate-900 dark:text-white focus:ring-2 focus:ring-blue-500 outline-none transition-all">
                  <option>Student</option>
                  <option>Alumni</option>
                  <option>Admin</option>
                </select>
              </div>
            )}

            <button 
              disabled={loading}
              type="submit" 
              className="w-full py-3.5 mt-2 bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-xl shadow-lg shadow-blue-500/30 transition-all disabled:opacity-50"
            >
              {loading ? 'Processing...' : activeView === 'login' ? 'Log In' : activeView === 'register' ? 'Sign Up' : 'Send Reset Link'}
            </button>
          </form>

          {activeView !== 'forgot' && (
            <>
              <div className="relative my-6">
                <div className="absolute inset-0 flex items-center"><div className="w-full border-t border-slate-200 dark:border-slate-800"></div></div>
                <div className="relative flex justify-center text-xs uppercase"><span className="bg-white dark:bg-slate-900 px-2 text-slate-500">Or continue with</span></div>
              </div>

              <button 
                onClick={handleGoogleLogin}
                className="w-full py-3 border border-slate-300 dark:border-slate-700 rounded-xl flex items-center justify-center gap-2 hover:bg-slate-50 dark:hover:bg-slate-800 transition-all font-medium text-slate-700 dark:text-slate-200"
              >
                <svg className="w-5 h-5" viewBox="0 0 24 24">
                  <path fill="currentColor" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" />
                  <path fill="currentColor" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" />
                  <path fill="currentColor" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l2.85-2.22.81-.62z" />
                  <path fill="currentColor" d="M12 5.38c1.62 0 3.06.56 4.21 1.66l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" />
                </svg>
                Google
              </button>
            </>
          )}

          <div className="mt-6 text-center text-sm font-medium text-slate-500">
            {activeView === 'login' ? "Don't have an account? " : activeView === 'register' ? "Already have an account? " : ""}
            <button 
              onClick={() => setActiveView(activeView === 'login' ? 'register' : 'login')} 
              className="text-blue-600 hover:underline dark:text-blue-400"
            >
              {activeView === 'login' ? 'Sign up' : 'Back to login'}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
