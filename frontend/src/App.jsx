import { useState, useEffect } from 'react'
import Chat from './components/Chat'
import VehicleProfile from './components/VehicleProfile'
import LoadingScreen from './components/LoadingScreen'
import LoginPage from './components/LoginPage'

const TABS = [
  { id: 'chat',     label: 'Diagnose', icon: '💬' },
  { id: 'vehicles', label: 'Vehicles', icon: '🚗' },
]

export default function App() {
  const [isLoading, setIsLoading] = useState(true)
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [username, setUsername] = useState('')
  const [tab, setTab] = useState('chat')
  const [selectedVehicle, setSelectedVehicle] = useState(null)

  // Check if user is already logged in
  useEffect(() => {
    const savedUser = localStorage.getItem('automech_user')
    if (savedUser) {
      setUsername(savedUser)
      setIsLoggedIn(true)
    }
  }, [])

  const handleLoadComplete = () => {
    setIsLoading(false)
  }

  const handleLogin = (user) => {
    setUsername(user)
    setIsLoggedIn(true)
  }

  const handleLogout = () => {
    localStorage.removeItem('automech_user')
    localStorage.removeItem('automech_user_email')
    localStorage.removeItem('automech_user_picture')
    setIsLoggedIn(false)
    setUsername('')
  }

  // Get user profile picture if available
  const userPicture = localStorage.getItem('automech_user_picture')

  // Show loading screen
  if (isLoading) {
    return <LoadingScreen onLoadComplete={handleLoadComplete} />
  }

  // Show login page
  if (!isLoggedIn) {
    return <LoginPage onLogin={handleLogin} />
  }

  // Show main app
  return (
    <div className="app">
      {/* ── Header ── */}
      <header className="header">
        <div className="header-left">
          <div className="logo-icon">🔧</div>
          <div>
            <div className="header-title">AutoMech AI</div>
            <div className="header-sub">Kerala Auto Diagnostics</div>
          </div>
        </div>
        <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
          {userPicture && (
            <img 
              src={userPicture} 
              alt="Profile"
              style={{
                width: '32px',
                height: '32px',
                borderRadius: '50%',
                border: '2px solid var(--accent)',
                objectFit: 'cover'
              }}
            />
          )}
          <span style={{ fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
            {userPicture ? '' : '👤 '}{username}
          </span>
          <button 
            onClick={handleLogout}
            style={{
              background: 'rgba(239,68,68,0.1)',
              border: '1px solid var(--danger)',
              color: 'var(--danger)',
              padding: '6px 12px',
              borderRadius: '6px',
              fontSize: '0.75rem',
              cursor: 'pointer',
              fontFamily: 'Barlow Condensed, sans-serif',
              fontWeight: 600,
              textTransform: 'uppercase',
              letterSpacing: '0.05em'
            }}
            title="Logout"
          >
            Logout
          </button>
          <div className="status-dot" title="Backend connected" />
        </div>
      </header>

      {/* ── Tab Bar ── */}
      <nav className="tab-bar">
        {TABS.map(t => (
          <button
            key={t.id}
            id={`tab-${t.id}`}
            className={tab === t.id ? 'active' : ''}
            onClick={() => setTab(t.id)}
          >
            {t.icon} {t.label}
          </button>
        ))}
      </nav>

      {/* ── Active vehicle bar ── */}
      {selectedVehicle && (
        <div className="vehicle-bar">
          <span className="vehicle-bar-icon">🚗</span>
          <span>Active:</span>
          <span className="vehicle-bar-name">
            {selectedVehicle.year} {selectedVehicle.make} {selectedVehicle.model}
          </span>
          <button
            style={{ marginLeft: 'auto', background: 'none', border: 'none', color: 'var(--text-muted)', cursor: 'pointer', fontSize: '0.75rem' }}
            onClick={() => setSelectedVehicle(null)}
            title="Clear vehicle"
          >
            ✕
          </button>
        </div>
      )}

      {/* ── Content ── */}
      <main className="content">
        {tab === 'chat'
          ? <Chat selectedVehicle={selectedVehicle} />
          : <VehicleProfile selectedVehicle={selectedVehicle} onSelect={setSelectedVehicle} />
        }
      </main>
    </div>
  )
}
