import { useState } from 'react'

export default function VoiceInput({ onResult }) {
  const [listening, setListening] = useState(false)

  const startListening = () => {
    const SpeechRecognition =
      window.SpeechRecognition || window.webkitSpeechRecognition

    if (!SpeechRecognition) {
      alert('Voice input is not supported in this browser. Try Chrome or Edge.')
      return
    }

    const recognition = new SpeechRecognition()
    recognition.lang = 'en-IN'
    recognition.interimResults = false
    recognition.maxAlternatives = 1

    recognition.onstart = () => setListening(true)
    recognition.onend = () => setListening(false)
    recognition.onerror = () => setListening(false)

    recognition.onresult = (e) => {
      const transcript = e.results[0][0].transcript
      onResult(transcript)
    }

    recognition.start()
  }

  return (
    <button
      id="btn-voice-input"
      className={`btn-voice ${listening ? 'listening' : ''}`}
      onClick={startListening}
      title={listening ? 'Listening… speak now' : 'Click to use voice input'}
      aria-label="Voice input"
    >
      {listening ? '🔴' : '🎤'}
    </button>
  )
}
