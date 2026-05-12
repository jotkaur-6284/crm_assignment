
import { useEffect, useState } from 'react'
import { useDispatch } from 'react-redux'
import { updateField, setInteraction } from '../store/interactionSlice'

const BACKEND_URL = 'http://127.0.0.1:8001'

export default function InteractionForm({ data }) {
  const dispatch = useDispatch()
  const [sentiment, setSentiment] = useState(data?.sentiment || '')
  const [status, setStatus] = useState('')

  useEffect(() => {
    setSentiment(data?.sentiment || '')
  }, [data?.sentiment])

  const handleSave = async () => {
    setStatus('Saving...')
    try {
      const response = await fetch(`${BACKEND_URL}/api/log-interaction`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          id: data.id,
          hcp_name: data.name,
          interaction_type: data.type,
          date: data.date,
          time: data.time,
          topics: data.topic,
          materials_shared: data.material,
          sample_distributed: data.sample,
          sentiment: data.sentiment,
          outcomes: data.outcomes,
        }),
      })

      if (!response.ok) {
        throw new Error('Save failed')
      }

      const result = await response.json()
      dispatch(
        setInteraction({
          id: result.id || data.id,
          name: result.hcp_name || data.name,
          type: result.interaction_type || data.type,
          date: result.date || data.date,
          time: result.time || data.time,
          topic: result.topics || data.topic,
          material: result.materials_shared || data.material,
          sample: result.sample_distributed || data.sample,
          sentiment: result.sentiment || data.sentiment,
          outcomes: result.outcomes || data.outcomes,
        })
      )
      setStatus('Saved successfully ✅')
    } catch (err) {
      setStatus('Save failed. Please try again.')
    }
  }

  const onFieldChange = (field, value) => {
    dispatch(updateField({ field, value }))
  }

  return (
    <div>
      <h1>Log HCP Interaction</h1>

      <div className="section">
        <div className="grid">
          <div>
            <label>HCP Name</label>
            <input value={data.name} readOnly placeholder="Search or select HCP..." />
          </div>

          <div>
            <label>Interaction Type</label>
            <select value={data.type} readOnly>
              <option value="">Select Type</option>
              <option>Meeting</option>
            </select>
          </div>
        </div>

        <div className="grid">
          <div>
            <label>Date</label>
            <input value={data.date} readOnly />
          </div>

          <div>
            <label>Time</label>
            <input value={data.time} readOnly />
          </div>
        </div>

        <div>
          <label>Topics Discussed</label>
          <textarea
            rows="5"
            value={data.topic}
            readOnly
            placeholder="Enter key discussion points..."
          />
          <a className="no-underline-link" href="#">Summarize from Voice note (Require Consent)</a>
        </div>

        <div>
          <label>Materials Shared</label>
          <div className="search-input-wrapper">
            <input value={data.material} readOnly placeholder="Search materials..." />
            <button type="button" className="search-button">🔍 Search/Add</button>
          </div>
        </div>

        <div className="spaced-section">
          <label>Sample Distributed</label>
          <div className="search-input-wrapper">
            <input
              value={data.sample || ''}
              onChange={(e) => onFieldChange('sample', e.target.value)}
              placeholder="Search sample..."
            />
            <button type="button" className="search-button">➕ Add Sample</button>
          </div>
        </div>

        <div className="sentiment-section">
          <label>Observed HCP Sentiment</label>
          <div className="radio-group">
            <button
              type="button"
              className={sentiment === 'Positive' ? 'sentiment-button active' : 'sentiment-button'}
              onClick={() => {
                setSentiment('Positive')
                onFieldChange('sentiment', 'Positive')
              }}
            >🙂 Positive</button>
            <button
              type="button"
              className={sentiment === 'Neutral' ? 'sentiment-button active' : 'sentiment-button'}
              onClick={() => {
                setSentiment('Neutral')
                onFieldChange('sentiment', 'Neutral')
              }}
            >😐 Neutral</button>
            <button
              type="button"
              className={sentiment === 'Negative' ? 'sentiment-button active' : 'sentiment-button'}
              onClick={() => {
                setSentiment('Negative')
                onFieldChange('sentiment', 'Negative')
              }}
            >☹️ Negative</button>
          </div>
        </div>

        <div>
          <label>Outcomes</label>
          <textarea
            rows="4"
            value={data.outcomes || ''}
            onChange={(e) => onFieldChange('outcomes', e.target.value)}
            placeholder="Key outcomes or agreements..."
          />
        </div>

        <div style={{ marginTop: '20px' }}>
          <button type="button" onClick={handleSave}>Save Interaction</button>
          {status && <div style={{ marginTop: '10px', color: '#333' }}>{status}</div>}
        </div>
      </div>
    </div>
  )
}
