import { useState } from 'react'
import axios from 'axios'
import { API_URL } from '../config'

const API = API_URL

export default function LoginPage({ onLogin }) {
  const [isRegisterMode, setIsRegisterMode] = useState(false)
  const [username, setUsername] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [fullName, setFullName] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState('')

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')

    if (!username.trim() || !password.trim()) {
      setError('Please enter both username and password')
      return
    }

    if (isRegisterMode) {
      // Registration validation
      if (!email.trim()) {
        setError('Please enter your email')
        return
      }
      if (password.length < 8) {
        setError('Password must be at least 8 characters long')
        return
      }
      if (password !== confirmPassword) {
        setError('Passwords do not match')
        return
      }
    }

    setIsLoading(true)

    try {
      const endpoint = isRegisterMode ? '/api/auth/register' : '/api/auth/login'
      const payload = isRegisterMode 
        ? { username, email, password, full_name: fullName || null }
        : { username, password }

      const response = await axios.post(`${API}${endpoint}`, payload)
      
      // Store token and user info
      localStorage.setItem('automech_token', response.data.access_token)
      localStorage.setItem('automech_user', response.data.user.username)
      localStorage.setItem('automech_user_email', response.data.user.email)
      localStorage.setItem('automech_user_id', response.data.user.id)
      
      onLogin(response.data.user.username)
    } catch (err) {
      const errorMsg = err.response?.data?.detail || 'Authentication failed'
      setError(errorMsg)
      setIsLoading(false)
    }
  }

  const toggleMode = () => {
    setIsRegisterMode(!isRegisterMode)
    setError('')
    setPassword('')
    setConfirmPassword('')
    setEmail('')
    setFullName('')
  }

  return (
    <div className="login-page">
      <div className="login-container">
        {/* Left Side - Branding */}
        <div className="login-branding">
          <div className="login-logo">
            <div className="logo-icon-large">🔧</div>
            <h1 className="login-brand-title">AUTOMECH</h1>
            <p className="login-brand-subtitle">AI DIAGNOSTIC SYSTEM</p>
          </div>
          
          <div className="login-features">
            <div className="login-feature">
              <span className="feature-icon">🔍</span>
              <span>AI-Powered Diagnostics</span>
            </div>
            <div className="login-feature">
              <span className="feature-icon">🛠️</span>
              <span>Expert Repair Guidance</span>
            </div>
            <div className="login-feature">
              <span className="feature-icon">💰</span>
              <span>Kerala Market Pricing</span>
            </div>
            <div className="login-feature">
              <span className="feature-icon">🛒</span>
              <span>Parts Recommendations</span>
            </div>
          </div>
        </div>

        {/* Right Side - Login/Register Form */}
        <div className="login-form-container">
          <div className="login-form-wrapper">
            <h2 className="login-form-title">
              {isRegisterMode ? 'CREATE ACCOUNT' : 'SYSTEM ACCESS'}
            </h2>
            <p className="login-form-subtitle">
              {isRegisterMode 
                ? 'Register to access AutoMech AI' 
                : 'Enter your credentials to continue'}
            </p>

            <form onSubmit={handleSubmit} className="login-form">
              <div className="login-input-group">
                <label className="login-label">USERNAME</label>
                <input
                  type="text"
                  className="login-input"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  placeholder="Enter username"
                  disabled={isLoading}
                  autoComplete="username"
                />
              </div>

              {isRegisterMode && (
                <>
                  <div className="login-input-group">
                    <label className="login-label">EMAIL</label>
                    <input
                      type="email"
                      className="login-input"
                      value={email}
                      onChange={(e) => setEmail(e.target.value)}
                      placeholder="Enter email"
                      disabled={isLoading}
                      autoComplete="email"
                    />
                  </div>

                  <div className="login-input-group">
                    <label className="login-label">FULL NAME (OPTIONAL)</label>
                    <input
                      type="text"
                      className="login-input"
                      value={fullName}
                      onChange={(e) => setFullName(e.target.value)}
                      placeholder="Enter full name"
                      disabled={isLoading}
                      autoComplete="name"
                    />
                  </div>
                </>
              )}

              <div className="login-input-group">
                <label className="login-label">PASSWORD</label>
                <input
                  type="password"
                  className="login-input"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder={isRegisterMode ? "Min 8 characters" : "Enter password"}
                  disabled={isLoading}
                  autoComplete={isRegisterMode ? "new-password" : "current-password"}
                />
              </div>

              {isRegisterMode && (
                <div className="login-input-group">
                  <label className="login-label">CONFIRM PASSWORD</label>
                  <input
                    type="password"
                    className="login-input"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    placeholder="Confirm password"
                    disabled={isLoading}
                    autoComplete="new-password"
                  />
                </div>
              )}

              {error && (
                <div className="login-error">
                  ⚠️ {error}
                </div>
              )}

              <button 
                type="submit" 
                className="login-button"
                disabled={isLoading}
              >
                {isLoading ? (
                  <>
                    <span className="login-spinner" />
                    {isRegisterMode ? 'CREATING ACCOUNT...' : 'AUTHENTICATING...'}
                  </>
                ) : (
                  <>
                    <span>→</span>
                    {isRegisterMode ? 'REGISTER' : 'LOGIN'}
                  </>
                )}
              </button>

              <div className="login-toggle">
                <button 
                  type="button"
                  onClick={toggleMode}
                  disabled={isLoading}
                  className="login-toggle-button"
                >
                  {isRegisterMode 
                    ? 'Already have an account? Login' 
                    : "Don't have an account? Register"}
                </button>
              </div>
            </form>

            <div className="login-footer">
              <p>🔒 Secure Authentication with Password Encryption</p>
              <p style={{ fontSize: '11px', marginTop: '4px', color: 'var(--text-dim)' }}>
                For Kerala Mechanics & Vehicle Owners
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Animated Background Elements */}
      <div className="login-bg-grid" />
      <div className="login-bg-glow" />
    </div>
  )
}
