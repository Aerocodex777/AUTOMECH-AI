import { useState, useRef, useEffect } from 'react'
import axios from 'axios'
import DiagnosticResult from './DiagnosticResult'
import ProductCard from './ProductCard'
import { API_URL } from '../config'

const API = API_URL

const INITIAL_MESSAGE = {
  role: 'bot',
  text: '👋 Hello! I\'m AutoMech AI.\n\nI can help you in two ways:\n\n🔧 Quick Diagnosis: Just describe your issue\n📋 Guided Diagnosis: Type "detailed" or "guide me" for step-by-step questions\n\nI\'ll provide detailed fixes with Kerala market pricing and show available parts online with images!',
}

export default function Chat({ selectedVehicle }) {
  const [messages, setMessages] = useState([INITIAL_MESSAGE])
  const [input, setInput] = useState('')
  const [obdCode, setObdCode] = useState('')
  const [loading, setLoading] = useState(false)
  const [structuredMode, setStructuredMode] = useState(false)
  const [currentQuestions, setCurrentQuestions] = useState([])
  const [currentAnswers, setCurrentAnswers] = useState({})
  const [currentSymptom, setCurrentSymptom] = useState('')
  const [sessionId, setSessionId] = useState(null)  // Store session ID for conversation continuity
  const bottomRef = useRef(null)
  const textareaRef = useRef(null)
  const imageInputRef = useRef(null)

  // Auto-scroll to bottom on new messages
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  // Auto-resize textarea
  const handleInputChange = (e) => {
    setInput(e.target.value)
    const ta = textareaRef.current
    if (ta) {
      ta.style.height = 'auto'
      ta.style.height = Math.min(ta.scrollHeight, 110) + 'px'
    }
  }

  const sendMessage = async () => {
    const text = input.trim()
    if (!text && !obdCode) return

    // Check if user wants structured diagnostic
    const wantsStructured = text.toLowerCase().includes('detailed') || 
                           text.toLowerCase().includes('step by step') ||
                           text.toLowerCase().includes('guide me')

    const displayText = obdCode ? `[OBD: ${obdCode}] ${text || ''}`.trim() : text
    setMessages(prev => [...prev, { role: 'user', text: displayText }])
    setInput('')
    if (textareaRef.current) textareaRef.current.style.height = 'auto'
    setLoading(true)

    try {
      if (wantsStructured && !structuredMode) {
        // Start structured diagnostic
        const res = await axios.post(`${API}/diagnose/structured/start`, {
          symptom: text,
          vehicle_id: selectedVehicle?.id ?? null,
        })
        
        setStructuredMode(true)
        setCurrentSymptom(text)
        setCurrentQuestions(res.data.questions)
        setCurrentAnswers({})
        
        let botMsg = `📋 **${res.data.initial_assessment}**\n\n`
        botMsg += `I'll ask you a few questions to diagnose this better:\n\n`
        res.data.questions.forEach((q, i) => {
          botMsg += `${i + 1}. ${q}\n`
        })
        botMsg += `\nPlease answer each question.`
        
        setMessages(prev => [...prev, { role: 'bot', text: botMsg }])
      } else if (structuredMode) {
        // Collecting answers for structured diagnostic
        const questionIndex = Object.keys(currentAnswers).length
        if (questionIndex < currentQuestions.length) {
          const newAnswers = { ...currentAnswers, [currentQuestions[questionIndex]]: text }
          setCurrentAnswers(newAnswers)
          
          if (questionIndex + 1 < currentQuestions.length) {
            // Ask next question
            setMessages(prev => [...prev, { 
              role: 'bot', 
              text: `${questionIndex + 2}. ${currentQuestions[questionIndex + 1]}` 
            }])
          } else {
            // All questions answered, generate diagnosis
            const res = await axios.post(`${API}/diagnose/structured/complete`, {
              symptom: currentSymptom,
              answers: newAnswers,
              vehicle_id: selectedVehicle?.id ?? null,
            })
            
            setMessages(prev => [...prev, { 
              role: 'bot', 
              text: res.data.diagnosis_text,
              rich: true,
              products: res.data.diagnosis_data.products 
            }])
            
            // Reset structured mode
            setStructuredMode(false)
            setCurrentQuestions([])
            setCurrentAnswers({})
            setCurrentSymptom('')
          }
        }
      } else {
        // Regular diagnostic
        const res = await axios.post(`${API}/diagnose/`, {
          symptoms: text || 'Diagnose based on the provided OBD code',
          vehicle_id: selectedVehicle?.id ?? null,
          obd_code: obdCode || null,
          session_id: sessionId || null,  // Send session_id for conversation continuity
        })
        
        // Store session_id from response
        if (res.data.session_id) {
          setSessionId(res.data.session_id)
          console.log('💬 Session ID:', res.data.session_id)
        }
        
        setMessages(prev => [...prev, { 
          role: 'bot', 
          text: res.data.diagnosis, 
          rich: true,
          products: res.data.products || []
        }])
        setObdCode('')
      }
    } catch (err) {
      const errMsg = err.response
        ? `⚠️ Server error ${err.response.status}: ${err.response.data?.detail || 'Unknown error'}`
        : '⚠️ Cannot connect to AutoMech backend. Make sure `python main.py` is running on port 8000.'
      setMessages(prev => [...prev, { role: 'bot', text: errMsg }])
    } finally {
      setLoading(false)
    }
  }

  const handleKey = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  const handleImageUpload = async (e) => {
    const file = e.target.files[0]
    if (!file) return

    setMessages(prev => [...prev, { role: 'user', text: `📸 Uploaded image: ${file.name}` }])
    setLoading(true)

    try {
      const formData = new FormData()
      formData.append('file', file)

      const res = await axios.post(`${API}/analyze/image`, formData, {
        headers: { 'Content-Type': 'multipart/form-data' }
      })
      setMessages(prev => [...prev, { role: 'bot', text: res.data.analysis, rich: true }])
    } catch (err) {
      const errMsg = err.response?.data?.detail || 'Failed to analyze image'
      setMessages(prev => [...prev, { role: 'bot', text: `⚠️ ${errMsg}` }])
    } finally {
      setLoading(false)
      e.target.value = '' // Reset input
    }
  }

  return (
    <div className="chat-container">
      {/* OBD code bar */}
      <div className="obd-bar">
        <span className="obd-label">OBD</span>
        <input
          id="obd-code-input"
          className="obd-input-field"
          value={obdCode}
          onChange={e => setObdCode(e.target.value.toUpperCase().replace(/[^A-Z0-9]/g, ''))}
          placeholder="P0300"
          maxLength={6}
          spellCheck={false}
        />
        {obdCode && (
          <button className="obd-clear-btn" onClick={() => setObdCode('')} title="Clear OBD code">✕</button>
        )}
        {obdCode && <span className="obd-badge">{obdCode}</span>}
      </div>

      {/* Messages */}
      <div className="messages" id="chat-messages">
        {messages.map((msg, i) => (
          <div key={i} className={`message-row ${msg.role}`} style={{ animationDelay: `${i * 0.05}s` }}>
            <div className={`avatar ${msg.role}`}>
              {msg.role === 'bot' ? '🔧' : '👤'}
            </div>
            <div className={`bubble ${msg.role} ${msg.role === 'bot' && loading && i === messages.length - 1 ? '' : ''}`}>
              {msg.rich
                ? <DiagnosticResult text={msg.text} />
                : <span style={{ whiteSpace: 'pre-wrap' }}>{msg.text}</span>
              }
              {msg.products && msg.products.length > 0 && (
                <div className="products-container">
                  <div className="products-header">🛒 Available Parts:</div>
                  <div className="products-grid">
                    {msg.products.map((product, idx) => (
                      <ProductCard key={idx} product={product} />
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        ))}

        {loading && (
          <div className="message-row bot">
            <div className="avatar bot">🔧</div>
            <div className="bubble bot loading">
              <div className="typing-dots">
                <span /><span /><span />
              </div>
              <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>Diagnosing…</span>
            </div>
          </div>
        )}

        <div ref={bottomRef} />
      </div>

      {/* Input area */}
      <div className="input-area">
        {/* Hidden file input */}
        <input
          type="file"
          ref={imageInputRef}
          accept="image/*"
          onChange={handleImageUpload}
          style={{ display: 'none' }}
        />

        <div style={{ display: 'flex', gap: '12px', alignItems: 'flex-end', width: '100%' }}>
          {/* Upload button */}
          <button
            className="btn-upload"
            onClick={() => imageInputRef.current?.click()}
            title="Upload vehicle image"
            disabled={loading}
          >
            📸
          </button>

          <div style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '6px' }}>
            {structuredMode && (
              <div className="structured-mode-badge">
                📋 Guided Mode: Question {Object.keys(currentAnswers).length + 1}/{currentQuestions.length}
              </div>
            )}
            <textarea
              id="chat-input"
              ref={textareaRef}
              className="chat-textarea"
              value={input}
              onChange={handleInputChange}
              onKeyDown={handleKey}
              placeholder={structuredMode 
                ? `Your answer...` 
                : "Describe symptoms… (type 'detailed' for guided diagnosis)"}
              rows={1}
            />
          </div>
          
          <button
            id="btn-send"
            className="btn-send"
            onClick={sendMessage}
            disabled={loading}
            title="Send (Enter)"
          >
            ➤
          </button>
        </div>
      </div>
    </div>
  )
}
