import { useEffect, useState } from 'react'

export default function LoadingScreen({ onLoadComplete }) {
  const [progress, setProgress] = useState(0)

  useEffect(() => {
    const interval = setInterval(() => {
      setProgress(prev => {
        if (prev >= 100) {
          clearInterval(interval)
          setTimeout(() => onLoadComplete(), 500)
          return 100
        }
        return prev + 2
      })
    }, 30)

    return () => clearInterval(interval)
  }, [onLoadComplete])

  return (
    <div className="loading-screen">
      <div className="loading-content">
        {/* Logo */}
        <div className="loading-logo">
          <div className="logo-icon-large">🔧</div>
          <h1 className="loading-title">AUTOMECH</h1>
          <p className="loading-subtitle">AI DIAGNOSTIC v1.0</p>
        </div>

        {/* Progress Bar */}
        <div className="loading-progress-container">
          <div className="loading-progress-bar">
            <div 
              className="loading-progress-fill" 
              style={{ width: `${progress}%` }}
            />
          </div>
          <div className="loading-progress-text">{progress}%</div>
        </div>

        {/* Status Text */}
        <div className="loading-status">
          {progress < 30 && '⚙️ Initializing AI Engine...'}
          {progress >= 30 && progress < 60 && '🔍 Loading Diagnostic Database...'}
          {progress >= 60 && progress < 90 && '🛠️ Preparing Tools...'}
          {progress >= 90 && '✅ Ready to Diagnose'}
        </div>

        {/* Animated Scanline */}
        <div className="loading-scanline" />
      </div>
    </div>
  )
}
