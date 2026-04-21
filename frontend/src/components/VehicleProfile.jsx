import { useState, useEffect } from 'react'
import axios from 'axios'
import { API_URL } from '../config'

const API = API_URL

const MAKES = ['Maruti Suzuki', 'Hyundai', 'Tata', 'Honda', 'Toyota', 'Mahindra', 'Hero', 'Bajaj', 'TVS', 'Kia', 'MG', 'Other']
const FUELS = ['Petrol', 'Diesel', 'CNG', 'Electric', 'Hybrid']

// Map makes to emoji icons
const MAKE_ICON = {
  'Maruti Suzuki': '🚙', 'Hyundai': '🚗', 'Tata': '🚛', 'Honda': '🏍️',
  'Toyota': '🚐', 'Mahindra': '🛻', 'Hero': '🏍️', 'Bajaj': '🏍️',
  'TVS': '🏍️', 'Kia': '🚗', 'MG': '🚗', 'Other': '🚘',
}

const EMPTY_FORM = { name: '', make: 'Maruti Suzuki', model: '', year: '', mileage: '', fuel_type: 'Petrol' }

export default function VehicleProfile({ selectedVehicle, onSelect }) {
  const [vehicles, setVehicles] = useState([])
  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState(EMPTY_FORM)
  const [saving, setSaving] = useState(false)
  const [error, setError] = useState('')

  useEffect(() => { fetchVehicles() }, [])

  const fetchVehicles = async () => {
    try {
      const res = await axios.get(`${API}/vehicles/`)
      setVehicles(res.data)
    } catch {
      setError('Could not load vehicles. Is the backend running?')
    }
  }

  const update = (field, value) => setForm(f => ({ ...f, [field]: value }))

  const addVehicle = async () => {
    if (!form.name.trim()) return setError('Customer name is required.')
    if (!form.model.trim()) return setError('Model is required.')
    if (!form.year || isNaN(form.year) || form.year < 1980 || form.year > new Date().getFullYear() + 1)
      return setError('Enter a valid year (1980 – present).')

    setSaving(true)
    setError('')
    try {
      await axios.post(`${API}/vehicles/`, {
        ...form,
        year: parseInt(form.year),
        mileage: parseFloat(form.mileage) || 0,
      })
      setForm(EMPTY_FORM)
      setShowForm(false)
      fetchVehicles()
    } catch (e) {
      setError(e.response?.data?.detail || 'Failed to save vehicle.')
    } finally {
      setSaving(false)
    }
  }

  const deleteVehicle = async (id, e) => {
    e.stopPropagation()
    if (!window.confirm('Delete this vehicle? Its diagnostic history will remain.')) return
    await axios.delete(`${API}/vehicles/${id}`)
    if (selectedVehicle?.id === id) onSelect(null)
    fetchVehicles()
  }

  return (
    <div className="vehicle-section">
      {/* Header */}
      <div className="section-header">
        <span className="section-title">Saved Vehicles</span>
        {vehicles.length > 0 && (
          <span className="vehicle-count">{vehicles.length}</span>
        )}
      </div>

      {/* Error */}
      {error && (
        <div style={{ background: 'rgba(239,68,68,0.1)', border: '1px solid rgba(239,68,68,0.3)', borderRadius: 'var(--radius-sm)', padding: '8px 12px', fontSize: '0.8rem', color: '#fca5a5', marginBottom: '10px' }}>
          {error}
        </div>
      )}

      {/* Empty state */}
      {!vehicles.length && !showForm && (
        <div className="empty-state">
          <div className="empty-state-icon">🚗</div>
          <div>No vehicles saved yet.</div>
          <div style={{ fontSize: '0.75rem', marginTop: '4px', color: 'var(--text-muted)' }}>
            Add one below to enable vehicle-specific diagnostics.
          </div>
        </div>
      )}

      {/* Vehicle cards */}
      {vehicles.map((v, i) => (
        <div
          key={v.id}
          id={`vehicle-card-${v.id}`}
          className={`vehicle-card ${selectedVehicle?.id === v.id ? 'selected' : ''}`}
          style={{ animation: `formSlideDown 0.4s cubic-bezier(0.16, 1, 0.3, 1) ${i * 0.08}s both` }}
          onClick={() => onSelect(selectedVehicle?.id === v.id ? null : v)}
          title={selectedVehicle?.id === v.id ? 'Click to deselect' : 'Click to select for diagnostics'}
        >
          <div className="vehicle-make-icon">{MAKE_ICON[v.make] || '🚘'}</div>
          <div className="vehicle-info">
            <div className="vehicle-name">{v.make} {v.model}</div>
            <div className="vehicle-meta">
              <span className="meta-chip">{v.year}</span>
              <span className="meta-chip">{v.fuel_type}</span>
              {v.mileage > 0 && <span className="meta-chip">{Number(v.mileage).toLocaleString()} km</span>}
              <span style={{ color: 'var(--text-muted)', fontSize: '0.72rem' }}>👤 {v.name}</span>
              {selectedVehicle?.id === v.id && <span className="selected-chip">Active</span>}
            </div>
          </div>
          <button
            className="btn-delete"
            onClick={(e) => deleteVehicle(v.id, e)}
            title="Delete vehicle"
            id={`btn-delete-${v.id}`}
          >
            🗑
          </button>
        </div>
      ))}

      {/* Add vehicle toggle */}
      <button
        id="btn-toggle-add-vehicle"
        className="btn-add-toggle"
        onClick={() => { setShowForm(s => !s); setError('') }}
      >
        {showForm ? '✕ Cancel' : '+ Add Vehicle'}
      </button>

      {/* Add vehicle form */}
      {showForm && (
        <div className="add-vehicle-form">
          <div className="form-row">
            <input
              id="form-customer-name"
              className="form-input"
              placeholder="Customer Name *"
              value={form.name}
              onChange={e => update('name', e.target.value)}
            />
          </div>
          <div className="form-row">
            <select
              id="form-make"
              className="form-select"
              value={form.make}
              onChange={e => update('make', e.target.value)}
            >
              {MAKES.map(m => <option key={m}>{m}</option>)}
            </select>
            <input
              id="form-model"
              className="form-input"
              placeholder="Model *  (e.g. Swift)"
              value={form.model}
              onChange={e => update('model', e.target.value)}
            />
          </div>
          <div className="form-row">
            <input
              id="form-year"
              className="form-input"
              placeholder="Year *"
              type="number"
              min="1980"
              max={new Date().getFullYear() + 1}
              value={form.year}
              onChange={e => update('year', e.target.value)}
            />
            <input
              id="form-mileage"
              className="form-input"
              placeholder="Mileage (km)"
              type="number"
              min="0"
              value={form.mileage}
              onChange={e => update('mileage', e.target.value)}
            />
          </div>
          <div className="form-row">
            <select
              id="form-fuel"
              className="form-select"
              value={form.fuel_type}
              onChange={e => update('fuel_type', e.target.value)}
            >
              {FUELS.map(f => <option key={f}>{f}</option>)}
            </select>
          </div>
          <button
            id="btn-save-vehicle"
            className="btn-save"
            onClick={addVehicle}
            disabled={saving}
          >
            {saving ? 'Saving…' : '✅ Save Vehicle'}
          </button>
        </div>
      )}
    </div>
  )
}
