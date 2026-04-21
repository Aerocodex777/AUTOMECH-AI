import { useState, useEffect } from 'react'
import './AgentThinking.css'

export default function AgentThinking({ steps, isThinking }) {
  const [visibleSteps, setVisibleSteps] = useState([])

  useEffect(() => {
    if (steps && steps.length > 0) {
      // Animate steps appearing one by one
      steps.forEach((step, index) => {
        setTimeout(() => {
          setVisibleSteps(prev => [...prev, step])
        }, index * 500)
      })
    }
  }, [steps])

  if (!isThinking && (!steps || steps.length === 0)) {
    return null
  }

  return (
    <div className="agent-thinking-container">
      <div className="agent-thinking-header">
        <span className="thinking-icon">🤖</span>
        <span className="thinking-title">Agentic AI Processing</span>
        {isThinking && (
          <div className="thinking-spinner">
            <div className="spinner"></div>
          </div>
        )}
      </div>

      <div className="thinking-steps">
        {visibleSteps.map((step, index) => (
          <div key={index} className="thinking-step" style={{ animationDelay: `${index * 0.1}s` }}>
            <div className="step-icon">
              {step.type === 'thought' && '💭'}
              {step.type === 'action' && '🔧'}
              {step.type === 'observation' && '👁️'}
              {step.type === 'final' && '✅'}
            </div>
            <div className="step-content">
              <div className="step-type">{step.type.toUpperCase()}</div>
              <div className="step-text">{step.text}</div>
              {step.tool && (
                <div className="step-tool">Tool: {step.tool}</div>
              )}
            </div>
          </div>
        ))}

        {isThinking && (
          <div className="thinking-step thinking-active">
            <div className="step-icon">⏳</div>
            <div className="step-content">
              <div className="step-text">Processing...</div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
