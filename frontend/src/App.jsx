import { useState, useEffect, useRef } from 'react'
import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import './App.css'

import LostAndFound from './pages/LostAndFound'
import Marketplace from './pages/Marketplace'
import AdminDashboard from './pages/AdminDashboard'
import ResetPassword from './pages/ResetPassword'
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
              <Search className="w-4 h-4 mr-1" /> Lost & Found
            </Link>
            <Link to="/marketplace" className="hover:text-purple-600 dark:hover:text-purple-400 transition-colors flex items-center">
              <ShoppingBag className="w-4 h-4 mr-1" /> Marketplace
            </Link>
            {user && user.role === 'Admin' && (
              <Link to="/admin" className="hover:text-amber-600 dark:hover:text-amber-400 transition-colors flex items-center">
                <Shield className="w-4 h-4 mr-1" /> Admin
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
              <Search className="w-4 h-4 mr-2" /> Lost & Found
            </Link>
            <Link to="/marketplace" onClick={() => setMobileMenuOpen(false)} className="block py-2 font-medium hover:text-purple-600 flex items-center">
              <ShoppingBag className="w-4 h-4 mr-2" /> Marketplace
            </Link>
            {user && user.role === 'Admin' && (
              <Link to="/admin" onClick={() => setMobileMenuOpen(false)} className="block py-2 font-medium hover:text-amber-600 flex items-center">
                <Shield className="w-4 h-4 mr-2" /> Admin Dashboard
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
            <Route path="/reset-password" element={<ResetPassword />} />
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
            const userData = JSON.parse(localStorage.getItem('user'))
            setUser(userData)
          }}
        />
      </div>
    </Router>
  )
}

/* ─── Home Page ─────────────────────────────────────────────────────────────── */

// Counts up from 0 to a target number on mount
function CountUp({ target, suffix = '' }) {
  const ref = useRef(null)
  useEffect(() => {
    const duration = 1400
    const step = target / (duration / 16)
    let cur = 0
    const timer = setInterval(() => {
      cur = Math.min(cur + step, target)
      if (ref.current) ref.current.textContent = Math.round(cur) + suffix
      if (cur >= target) clearInterval(timer)
    }, 16)
    return () => clearInterval(timer)
  }, [target, suffix])
  return <span ref={ref}>0{suffix}</span>
}

// Typewriter that cycles through words
function TypeWriter({ words }) {
  const [index, setIndex] = useState(0)
  const [displayed, setDisplayed] = useState('')
  const [deleting, setDeleting] = useState(false)

  useEffect(() => {
    const word = words[index % words.length]
    let timeout

    if (!deleting && displayed.length < word.length) {
      timeout = setTimeout(() => setDisplayed(word.slice(0, displayed.length + 1)), 80)
    } else if (!deleting && displayed.length === word.length) {
      timeout = setTimeout(() => setDeleting(true), 1800)
    } else if (deleting && displayed.length > 0) {
      timeout = setTimeout(() => setDisplayed(displayed.slice(0, -1)), 45)
    } else if (deleting && displayed.length === 0) {
      setDeleting(false)
      setIndex(i => i + 1)
    }

    return () => clearTimeout(timeout)
  }, [displayed, deleting, index, words])

  return (
    <span>
      {displayed}
      <span
        style={{
          display: 'inline-block',
          width: 3,
          height: '0.85em',
          background: 'currentColor',
          marginLeft: 3,
          verticalAlign: 'middle',
          animation: 'blink 1s step-end infinite',
        }}
      />
    </span>
  )
}

// Single feature card with a stagger reveal on scroll
function FeatureCard({ icon, title, desc, delay }) {
  const ref = useRef(null)
  const [visible, setVisible] = useState(false)

  useEffect(() => {
    const el = ref.current
    if (!el) return
    const obs = new IntersectionObserver(
      ([entry]) => { if (entry.isIntersecting) { setVisible(true); obs.disconnect() } },
      { threshold: 0.2 }
    )
    obs.observe(el)
    return () => obs.disconnect()
  }, [])

  return (
    <div
      ref={ref}
      style={{
        opacity: visible ? 1 : 0,
        transform: visible ? 'translateY(0)' : 'translateY(28px)',
        transition: `opacity 0.55s ${delay}s ease, transform 0.55s ${delay}s ease`,
        background: 'white',
        border: '1px solid #e2e8f0',
        borderRadius: 16,
        padding: '1.75rem',
      }}
      className="dark:bg-slate-800 dark:border-slate-700 group hover:-translate-y-1 hover:shadow-lg transition-[transform,box-shadow] duration-300"
    >
      <div className="w-12 h-12 mb-4 rounded-xl flex items-center justify-center text-2xl bg-slate-50 dark:bg-slate-700 group-hover:scale-110 transition-transform duration-300">
        {icon}
      </div>
      <div className="font-bold text-slate-800 dark:text-white mb-1.5">{title}</div>
      <div className="text-sm text-slate-500 dark:text-slate-400 leading-relaxed">{desc}</div>
    </div>
  )
}

function Home() {
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    // Small delay so CSS transitions actually fire after paint
    const t = setTimeout(() => setMounted(true), 60)
    return () => clearTimeout(t)
  }, [])

  const fadeUp = (delay = 0) => ({
    opacity: mounted ? 1 : 0,
    transform: mounted ? 'translateY(0)' : 'translateY(24px)',
    transition: `opacity 0.6s ${delay}s ease, transform 0.6s ${delay}s ease`,
  })

  return (
    <>
      {/* Keyframes injected once */}
      <style>{`
        @keyframes blink { 0%,100%{opacity:1} 50%{opacity:0} }
        @keyframes float-slow {
          0%,100% { transform: translateY(0px) rotate(0deg); }
          33%      { transform: translateY(-10px) rotate(1deg); }
          66%      { transform: translateY(-5px) rotate(-1deg); }
        }
        @keyframes drift {
          0%,100% { transform: translateX(0) translateY(0); }
          50%      { transform: translateX(6px) translateY(-8px); }
        }
        @keyframes marquee {
          from { transform: translateX(0); }
          to   { transform: translateX(-50%); }
        }
        @keyframes ping-soft {
          0%   { transform: scale(1); opacity: 0.5; }
          80%  { transform: scale(2); opacity: 0; }
          100% { opacity: 0; }
        }
        .marquee-track { animation: marquee 24s linear infinite; }
        .marquee-track:hover { animation-play-state: paused; }
      `}</style>

      <div className="flex flex-col items-center w-full overflow-x-hidden">

        {/* ── HERO ─────────────────────────────────────────── */}
        <section className="w-full min-h-[90vh] flex flex-col items-center justify-center px-6 pt-20 pb-12 relative text-center">

          {/* Subtle background dots — no blur, no gradient blob */}
          <div
            aria-hidden
            style={{
              position: 'absolute', inset: 0, zIndex: 0, pointerEvents: 'none',
              backgroundImage: 'radial-gradient(circle, #cbd5e1 1px, transparent 1px)',
              backgroundSize: '32px 32px',
              opacity: 0.35,
            }}
            className="dark:opacity-10"
          />

          {/* Floating accent shapes — geometry, not blobs */}
          <div aria-hidden style={{ position: 'absolute', top: '12%', left: '7%', width: 48, height: 48, border: '2px solid #3b82f6', borderRadius: 10, animation: 'float-slow 6s ease-in-out infinite', opacity: 0.25, zIndex: 0 }} />
          <div aria-hidden style={{ position: 'absolute', top: '20%', right: '9%', width: 32, height: 32, background: '#8b5cf6', borderRadius: '50%', animation: 'drift 7s ease-in-out infinite', opacity: 0.15, zIndex: 0 }} />
          <div aria-hidden style={{ position: 'absolute', bottom: '18%', left: '12%', width: 20, height: 20, border: '2px solid #10b981', borderRadius: 4, animation: 'float-slow 8s ease-in-out infinite 1s', opacity: 0.2, zIndex: 0 }} />
          <div aria-hidden style={{ position: 'absolute', bottom: '22%', right: '8%', width: 40, height: 40, border: '2px solid #f59e0b', borderRadius: '50%', animation: 'drift 9s ease-in-out infinite 0.5s', opacity: 0.18, zIndex: 0 }} />

          <div className="relative z-10 max-w-4xl w-full flex flex-col items-center gap-6">

            {/* Status pill */}
            <div style={fadeUp(0)} className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full border border-slate-200 dark:border-slate-700 bg-white dark:bg-slate-800 text-sm font-medium text-slate-500 dark:text-slate-400 shadow-sm">
              <span className="relative flex h-2 w-2">
                <span style={{ animation: 'ping-soft 1.5s ease-out infinite' }} className="absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />
                <span className="relative inline-flex h-2 w-2 rounded-full bg-emerald-500" />
              </span>
              Live · Built for students
            </div>

            {/* Headline with typewriter */}
            <h1 style={{ ...fadeUp(0.1), lineHeight: 1.08, letterSpacing: '-0.03em' }} className="text-5xl md:text-7xl font-black text-slate-900 dark:text-white">
              Your campus,<br />
              <span className="text-blue-600 dark:text-blue-400">
                <TypeWriter words={['recovered.', 'connected.', 'simplified.', 'smarter.']} />
              </span>
            </h1>

            <p style={fadeUp(0.2)} className="text-lg md:text-xl text-slate-500 dark:text-slate-400 max-w-2xl leading-relaxed">
              Recover lost items with AI-matching and trade goods safely — all within your campus, all in one place.
            </p>

            {/* CTA buttons */}
            <div style={fadeUp(0.3)} className="flex flex-col sm:flex-row gap-4 mt-2">
              <Link
                to="/lost-found"
                className="px-8 py-3.5 bg-blue-600 text-white font-bold rounded-xl hover:bg-blue-700 hover:-translate-y-0.5 hover:shadow-lg hover:shadow-blue-500/25 transition-all duration-200 flex items-center gap-2"
              >
                <Search className="w-4 h-4" /> Find Lost Items
              </Link>
              <Link
                to="/marketplace"
                className="px-8 py-3.5 bg-white dark:bg-slate-800 text-slate-800 dark:text-white font-bold rounded-xl border border-slate-200 dark:border-slate-700 hover:-translate-y-0.5 hover:shadow-md hover:border-slate-300 dark:hover:border-slate-600 transition-all duration-200 flex items-center gap-2"
              >
                <ShoppingBag className="w-4 h-4" /> Open Marketplace
              </Link>
            </div>

            {/* Stat strip */}
            <div style={fadeUp(0.45)} className="mt-10 grid grid-cols-3 divide-x divide-slate-200 dark:divide-slate-700 border border-slate-200 dark:border-slate-700 rounded-2xl overflow-hidden bg-white dark:bg-slate-800 shadow-sm w-full max-w-lg">
              {[
                { n: 340, s: '+', label: 'Items recovered' },
                { n: 94, s: '%', label: 'Match accuracy' },
                { n: 180, s: '+', label: 'Active listings' },
              ].map(({ n, s, label }) => (
                <div key={label} className="flex flex-col items-center py-4 px-2">
                  <span className="text-2xl font-black text-slate-900 dark:text-white tracking-tight">
                    <CountUp target={n} suffix={s} />
                  </span>
                  <span className="text-xs text-slate-400 mt-0.5">{label}</span>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* ── MARQUEE STRIP ────────────────────────────────── */}
        <div className="w-full overflow-hidden border-y border-slate-100 dark:border-slate-800 bg-slate-50 dark:bg-slate-800/50 py-3 select-none">
          <div className="marquee-track flex gap-10 w-max">
            {[
              '🔐 Secure JWT Auth', '🧠 TF-IDF Smart Match', '🛒 Campus Marketplace',
              '🔔 Real-time Alerts', '🍃 MongoDB Atlas', '🎨 Tailwind UI',
              '🔐 Secure JWT Auth', '🧠 TF-IDF Smart Match', '🛒 Campus Marketplace',
              '🔔 Real-time Alerts', '🍃 MongoDB Atlas', '🎨 Tailwind UI',
            ].map((item, i) => (
              <span key={i} className="text-sm font-semibold text-slate-400 dark:text-slate-500 whitespace-nowrap tracking-wide uppercase">
                {item}
              </span>
            ))}
          </div>
        </div>

        {/* ── FEATURES GRID ────────────────────────────────── */}
        <section className="w-full max-w-5xl px-6 py-24 grid grid-cols-2 md:grid-cols-4 gap-5 text-blue-800">
          {[
            { icon: '🔍', title: 'Smart Lost & Found', desc: 'TF-IDF engine surfaces the closest matches so things get back to their owners fast.', delay: 0 },
            { icon: '🛒', title: 'Campus Marketplace', desc: 'Buy & sell within your campus only. No strangers, no risk.', delay: 0.1 },
            { icon: '🔔', title: 'Live Notifications', desc: 'Instant alerts when a match is found or someone replies to your listing.', delay: 0.2 },
            { icon: '🛡️', title: 'Secure & Verified', desc: 'JWT sessions and admin moderation keep every interaction trustworthy.', delay: 0.3 },
          ].map(f => (
            <FeatureCard key={f.title} {...f} />
          ))}
        </section>

        {/* ── BOTTOM CTA ───────────────────────────────────── */}
        <section className="w-full max-w-5xl px-6 pb-20">
          <div className="rounded-2xl border border-slate-200 dark:border-slate-700 bg-slate-50 dark:bg-slate-800 p-10 md:p-14 flex flex-col md:flex-row items-center justify-between gap-8">
            <div>
              <div className="text-xs font-bold tracking-widest uppercase text-blue-500 mb-2">Get started now</div>
              <h2 className="text-3xl md:text-4xl font-black text-slate-900 dark:text-white leading-tight">
                Lost something?<br />
                <span className="text-slate-400 font-medium">Someone's probably found it.</span>
              </h2>
            </div>
            <div className="flex flex-col sm:flex-row gap-3 shrink-0">
              <Link to="/lost-found" className="px-7 py-3 bg-blue-600 text-white font-bold rounded-xl hover:bg-blue-700 hover:-translate-y-0.5 transition-all duration-200 flex items-center gap-2 justify-center">
                <Search className="w-4 h-4" /> Lost & Found
              </Link>
              <Link to="/marketplace" className="px-7 py-3 border border-slate-300 dark:border-slate-600 font-bold rounded-xl hover:border-slate-400 dark:hover:border-slate-500 hover:-translate-y-0.5 transition-all duration-200 flex items-center gap-2 justify-center text-slate-700 dark:text-white">
                <ShoppingBag className="w-4 h-4" /> Marketplace
              </Link>
            </div>
          </div>
        </section>

      </div>
    </>
  )
}

export default App