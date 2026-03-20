import { useState, useEffect } from 'react'
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import './App.css'

import LostAndFound from './pages/LostAndFound'
import Marketplace from './pages/Marketplace'
import AdminDashboard from './pages/AdminDashboard'
import AuthModal from './components/AuthModal'
import NotificationBell from './components/NotificationBell'

import { Search, ShoppingBag, LogOut, User, Shield, Menu, X } from 'lucide-react'

function App() {
  const [isAuthOpen, setIsAuthOpen] = useState(false)
  const [user, setUser] = useState(null)
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false)

  useEffect(() => {
    const token = localStorage.getItem('token')
    const userData = localStorage.getItem('user')
    if (token && userData) {
      setUser(JSON.parse(userData))
    }
  }, [])

  const handleLogout = () => {
    localStorage.removeItem('token')
    localStorage.removeItem('user')
    localStorage.removeItem('campus_notifications')
    setUser(null)
  }

  return (
    <Router>
      <div className="min-h-screen bg-white dark:bg-slate-900 text-slate-900 dark:text-white transition-colors duration-300 w-full flex flex-col font-sans">
        
        {/* Navigation Bar */}
        <nav className="border-b dark:border-slate-800 bg-white/80 dark:bg-slate-900/80 backdrop-blur-md py-4 px-6 md:px-12 w-full flex justify-between items-center z-30 sticky top-0 shadow-sm">
          <Link to="/" className="text-2xl font-black tracking-tight bg-clip-text text-transparent bg-gradient-to-r from-blue-600 via-indigo-500 to-purple-600 hover:opacity-80 transition-opacity">
            CampusConnect
          </Link>
          
          {/* Desktop Nav Links */}
          <div className="space-x-8 hidden md:flex font-semibold text-slate-600 dark:text-slate-300 items-center">
            <Link to="/" className="hover:text-blue-600 dark:hover:text-blue-400 transition-colors">Home</Link>
            <Link to="/lost-found" className="hover:text-blue-600 dark:hover:text-blue-400 transition-colors flex items-center">
               <Search className="w-4 h-4 mr-1"/> Lost & Found
            </Link>
            <Link to="/marketplace" className="hover:text-purple-600 dark:hover:text-purple-400 transition-colors flex items-center">
               <ShoppingBag className="w-4 h-4 mr-1"/> Marketplace
            </Link>
            {user && user.role === 'Admin' && (
              <Link to="/admin" className="hover:text-amber-600 dark:hover:text-amber-400 transition-colors flex items-center">
                 <Shield className="w-4 h-4 mr-1"/> Admin
              </Link>
            )}
          </div>

          {/* Right side actions */}
          <div className="flex space-x-3 items-center">
            {user && <NotificationBell />}
            {user ? (
              <div className="flex items-center gap-3">
                 <div className="hidden sm:flex items-center px-3 py-1.5 bg-slate-100 dark:bg-slate-800 rounded-full font-medium text-sm border border-slate-200 dark:border-slate-700">
                    <User className="w-4 h-4 mr-2 text-slate-400" />
                    {user.name}
                    <span className="ml-1.5 px-1.5 py-0.5 bg-blue-100 dark:bg-blue-900/30 text-blue-600 dark:text-blue-400 text-[10px] font-bold rounded uppercase">{user.role}</span>
                 </div>
                 <button onClick={handleLogout} className="p-2 text-slate-400 hover:text-red-500 hover:bg-red-50 dark:hover:bg-red-900/20 rounded-full transition-all" title="Logout">
                   <LogOut className="w-5 h-5" />
                 </button>
              </div>
            ) : (
              <button onClick={() => setIsAuthOpen(true)} className="px-5 py-2.5 bg-blue-600 text-white rounded-xl font-bold hover:bg-blue-700 shadow-lg shadow-blue-500/30 transition-all hover:-translate-y-0.5">
                Sign In
              </button>
            )}
            
            {/* Mobile menu button */}
            <button onClick={() => setMobileMenuOpen(!mobileMenuOpen)} className="md:hidden p-2 text-slate-500 hover:text-slate-700 dark:hover:text-slate-300">
              {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
            </button>
          </div>
        </nav>

        {/* Mobile Menu */}
        {mobileMenuOpen && (
          <div className="md:hidden bg-white dark:bg-slate-900 border-b border-slate-200 dark:border-slate-800 px-6 py-4 space-y-3 z-20 relative animate-in slide-in-from-top-2 duration-200">
            <Link to="/" onClick={() => setMobileMenuOpen(false)} className="block py-2 font-medium hover:text-blue-600">Home</Link>
            <Link to="/lost-found" onClick={() => setMobileMenuOpen(false)} className="block py-2 font-medium hover:text-blue-600 flex items-center">
              <Search className="w-4 h-4 mr-2"/> Lost & Found
            </Link>
            <Link to="/marketplace" onClick={() => setMobileMenuOpen(false)} className="block py-2 font-medium hover:text-purple-600 flex items-center">
              <ShoppingBag className="w-4 h-4 mr-2"/> Marketplace
            </Link>
            {user && user.role === 'Admin' && (
              <Link to="/admin" onClick={() => setMobileMenuOpen(false)} className="block py-2 font-medium hover:text-amber-600 flex items-center">
                <Shield className="w-4 h-4 mr-2"/> Admin Dashboard
              </Link>
            )}
          </div>
        )}

        {/* Main Content Area */}
        <main className="flex-grow w-full relative">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/lost-found" element={<LostAndFound />} />
            <Route path="/marketplace" element={<Marketplace />} />
            <Route path="/admin" element={<AdminDashboard />} />
          </Routes>
        </main>
        
        {/* Footer */}
        <footer className="py-8 px-12 border-t border-slate-200 dark:border-slate-800 text-center text-slate-600 dark:text-slate-500 font-medium">
          <div className="max-w-4xl mx-auto flex flex-col md:flex-row justify-between items-center gap-4 text-sm">
             <div>&copy; {new Date().getFullYear()} CampusConnect. Built for students, by students.</div>
             <div className="flex gap-6">
                <Link to="/lost-found" className="hover:text-blue-500 transition-colors">Lost & Found</Link>
                <Link to="/marketplace" className="hover:text-purple-500 transition-colors">Marketplace</Link>
                <a href="#" className="hover:text-slate-900 dark:hover:text-white transition-colors">Privacy</a>
             </div>
          </div>
        </footer>

        <AuthModal 
          isOpen={isAuthOpen} 
          onClose={() => setIsAuthOpen(false)} 
          onLogin={(name) => {
             const userData = JSON.parse(localStorage.getItem('user'));
             setUser(userData);
          }}
        />
      </div>
    </Router>
  )
}

function Home() {
  return (
    <div className="flex flex-col items-center justify-center min-h-[85vh] px-4 animate-in slide-in-from-bottom-8 duration-700 fade-in">
       
       {/* Background decorative elements */}
       <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-blue-400/20 dark:bg-blue-600/10 rounded-full blur-3xl -z-10 animate-pulse mix-blend-multiply dark:mix-blend-screen"></div>
       <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-purple-400/20 dark:bg-purple-600/10 rounded-full blur-3xl -z-10 animate-pulse mix-blend-multiply dark:mix-blend-screen" style={{animationDelay: '1s'}}></div>
       
       <div className="max-w-4xl text-center space-y-10 relative">
         <div className="inline-block px-4 py-1.5 rounded-full border border-slate-200 dark:border-slate-700 bg-white/50 dark:bg-slate-800/50 backdrop-blur-sm text-sm font-semibold text-slate-600 dark:text-slate-300 shadow-sm mb-4">
            ✨ Smarter. Safer. Connected.
         </div>
         <h1 className="text-5xl md:text-6xl lg:text-8xl font-black tracking-tight leading-tight">
           Your Smart Campus <br/> 
           <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-600 via-indigo-600 to-purple-600">
             Ecosystem
           </span>
         </h1>
         <p className="text-xl md:text-2xl text-slate-600 dark:text-slate-400 max-w-3xl mx-auto leading-relaxed font-medium">
           The all-in-one platform to recover lost items through AI-matching and buy or sell goods safely within your campus.
         </p>
         <div className="flex flex-col sm:flex-row gap-6 justify-center pt-8">
           <Link to="/lost-found" className="px-8 py-4 bg-white dark:bg-slate-800 border-2 border-slate-200 dark:border-slate-700 text-slate-900 dark:text-white rounded-2xl hover:border-blue-500 hover:shadow-[0_0_30px_rgba(59,130,246,0.2)] hover:-translate-y-1 transition-all duration-300 font-bold text-lg flex items-center justify-center gap-3">
              <Search className="w-5 h-5 text-blue-500"/> Reclaim Items
           </Link>
           <Link to="/marketplace" className="px-8 py-4 bg-purple-600 text-white shadow-xl shadow-purple-500/30 border-2 border-purple-600 rounded-2xl hover:bg-purple-700 hover:border-purple-700 hover:-translate-y-1 transition-all duration-300 font-bold text-lg flex items-center justify-center gap-3">
              <ShoppingBag className="w-5 h-5"/> Browse Marketplace
           </Link>
         </div>
         
         {/* Feature highlights */}
         <div className="mt-20 grid grid-cols-2 md:grid-cols-4 gap-8 max-w-3xl mx-auto">
            <div className="text-center group">
              <div className="w-14 h-14 mx-auto mb-3 bg-blue-100 dark:bg-blue-900/30 rounded-2xl flex items-center justify-center text-blue-600 dark:text-blue-400 group-hover:scale-110 transition-transform">🔐</div>
              <div className="font-bold text-sm text-slate-600 dark:text-slate-400">Secure Auth</div>
              <div className="text-xs text-slate-400">JWT Tokens</div>
            </div>
            <div className="text-center group">
              <div className="w-14 h-14 mx-auto mb-3 bg-purple-100 dark:bg-purple-900/30 rounded-2xl flex items-center justify-center text-purple-600 dark:text-purple-400 group-hover:scale-110 transition-transform">🎨</div>
              <div className="font-bold text-sm text-slate-600 dark:text-slate-400">Beautiful UI</div>
              <div className="text-xs text-slate-400">Tailwind CSS</div>
            </div>
            <div className="text-center group">
              <div className="w-14 h-14 mx-auto mb-3 bg-emerald-100 dark:bg-emerald-900/30 rounded-2xl flex items-center justify-center text-emerald-600 dark:text-emerald-400 group-hover:scale-110 transition-transform">🧠</div>
              <div className="font-bold text-sm text-slate-600 dark:text-slate-400">Smart Match</div>
              <div className="text-xs text-slate-400">TF-IDF Similarity</div>
            </div>
            <div className="text-center group">
              <div className="w-14 h-14 mx-auto mb-3 bg-amber-100 dark:bg-amber-900/30 rounded-2xl flex items-center justify-center text-amber-600 dark:text-amber-400 group-hover:scale-110 transition-transform">🍃</div>
              <div className="font-bold text-sm text-slate-600 dark:text-slate-400">MongoDB</div>
              <div className="text-xs text-slate-400">Atlas Cloud</div>
            </div>
         </div>
       </div>
    </div>
  )
}

export default App
