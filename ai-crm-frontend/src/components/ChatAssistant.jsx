
import { useState } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { setInteraction, addMessage } from '../store/interactionSlice'

const BACKEND_URL = 'https://crm-assignment-or1h.onrender.com'

export default function ChatAssistant() {
  const dispatch = useDispatch()
  const messages = useSelector((state) => state.interaction.messages)
  const [message, setMessage] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  const handleSend = async () => {
    if (!message) return

    dispatch(addMessage({ type: 'user', text: message }))
    setIsLoading(true)

    try {
      const response = await fetch(`${BACKEND_URL}/api/parse-chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: message }),
      })

      if (!response.ok) {
        throw new Error('Failed to parse chat')
      }

      const result = await response.json()
      dispatch(
        setInteraction({
          id: result.id || null,
          name: result.hcp_name || '',
          type: result.interaction_type || '',
          date: result.date || new Date().toLocaleDateString(),
          time: result.time || new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
          topic: result.topics || '',
          material: result.materials_shared || '',
          sample: result.sample_distributed || '',
          sentiment: result.sentiment || 'Neutral',
          outcomes: result.outcomes || '',
        })
      )

      dispatch(
        addMessage({
          type: 'ai',
          text:
            result.summary ||
            '✅ Interaction details were extracted and populated on the left. You can save the record once you verify the fields.',
        })
      )
    } catch (error) {
      dispatch(
        addMessage({
          type: 'ai',
          text:
            '⚠️ Unable to parse chat with the backend. Please try again or use the form directly.',
        })
      )
    } finally {
      setIsLoading(false)
      setMessage('')
    }
  }

  return (
    <div className="chat-box">
      <h2>🤖 AI Assistant</h2>
      <p className="small">Log Interaction details here via chat</p>

      <div className="chat-content">
        <div className="message info">
          Log interaction details here (e.g., "Met Dr. Smith, discussed Product-X efficacy, positive sentiment, shared brochure") or ask for help.
        </div>

        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.type}`}>
            {msg.text}
          </div>
        ))}
      </div>

      <div className="input-row">
        <input
          placeholder="Describe Interaction..."
          value={message}
          onChange={(e) => setMessage(e.target.value)}
          disabled={isLoading}
        />
        <button onClick={handleSend} disabled={isLoading}>
          {isLoading ? 'Processing...' : 'AI Log'}
        </button>
      </div>
    </div>
  )
}
