# AutoMech AI — Testing Checklist

## Pre-Flight Checks

### ✅ Environment Setup
- [ ] Python 3.9+ installed
- [ ] Node.js 18+ installed
- [ ] Groq API key configured in `backend/.env`
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Frontend dependencies installed (`npm install`)

### ✅ File Structure
- [ ] `backend/.env` exists with GROQ_API_KEY
- [ ] `backend/data/obd_codes.json` has 28+ codes
- [ ] `backend/data/manuals/` directory exists
- [ ] `backend/vectorstore/` directory exists (created on first run)
- [ ] `frontend/public/icon-192.png` exists
- [ ] `frontend/public/icon-512.png` exists

## Backend Tests

### 1. Health Check
```bash
curl http://localhost:8000/
```
**Expected**: `{"status": "AutoMech AI is running 🔧", "version": "1.0.0"}`

### 2. Database Initialization
**Check console output on startup**:
- [ ] "✅ Database ready (SQLite)" or "(PostgreSQL)"
- [ ] No database connection errors

### 3. RAG Initialization
**Check console output on startup**:
- [ ] "ℹ️ No PDFs found in data/manuals/" (if no manuals)
- [ ] OR "✅ Ingested X chunks from 'Vehicle_Name'" (if manuals present)

### 4. Vehicle CRUD Operations

**Create Vehicle**:
```bash
curl -X POST http://localhost:8000/vehicles/ \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test Customer",
    "make": "Maruti Suzuki",
    "model": "Swift",
    "year": 2019,
    "mileage": 45000,
    "fuel_type": "Petrol"
  }'
```
**Expected**: JSON with vehicle ID

**List Vehicles**:
```bash
curl http://localhost:8000/vehicles/
```
**Expected**: Array with created vehicle

**Delete Vehicle**:
```bash
curl -X DELETE http://localhost:8000/vehicles/1
```
**Expected**: `{"message": "Vehicle 1 deleted"}`

### 5. OBD Code Lookup

**Test P0301 (Cylinder 1 Misfire)**:
```bash
curl -X POST http://localhost:8000/diagnose/ \
  -H "Content-Type: application/json" \
  -d '{"symptoms": "engine clicking", "obd_code": "P0301"}'
```
**Expected**:
- [ ] Diagnosis includes "Cylinder 1 Misfire"
- [ ] System: "Ignition System"
- [ ] Severity: "High"
- [ ] Causes listed
- [ ] Fix recommendations
- [ ] Cost estimate in INR

**Test Invalid Code**:
```bash
curl -X POST http://localhost:8000/diagnose/ \
  -H "Content-Type: application/json" \
  -d '{"symptoms": "test", "obd_code": "INVALID"}'
```
**Expected**: "Code 'INVALID' not found in database"

### 6. Agent Diagnostic (No OBD Code)

```bash
curl -X POST http://localhost:8000/diagnose/ \
  -H "Content-Type: application/json" \
  -d '{"symptoms": "car makes grinding noise when braking"}'
```
**Expected**:
- [ ] Structured diagnosis with emojis
- [ ] Safety warning (brakes = critical)
- [ ] Cost estimate in INR
- [ ] Kerala-specific advice

### 7. Vehicle-Specific Diagnosis

```bash
# First create vehicle (ID will be 1)
curl -X POST http://localhost:8000/vehicles/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Rajan", "make": "Maruti Suzuki", "model": "Swift", "year": 2019, "mileage": 45000, "fuel_type": "Petrol"}'

# Then diagnose with vehicle context
curl -X POST http://localhost:8000/diagnose/ \
  -H "Content-Type: application/json" \
  -d '{"symptoms": "engine overheating", "vehicle_id": 1}'
```
**Expected**:
- [ ] Diagnosis considers 2019 Maruti Swift context
- [ ] Saved to diagnostic_history table

### 8. Diagnostic History

```bash
curl http://localhost:8000/history/1
```
**Expected**: Array of past diagnoses for vehicle ID 1

## Frontend Tests

### 1. App Load
- [ ] Open http://localhost:5173
- [ ] No console errors
- [ ] Header shows "AutoMech AI"
- [ ] Green status dot visible
- [ ] Two tabs: "Diagnose" and "Vehicles"

### 2. Vehicle Management
- [ ] Click "Vehicles" tab
- [ ] Click "+ Add Vehicle"
- [ ] Fill form:
  - Customer Name: "Test User"
  - Make: "Maruti Suzuki"
  - Model: "Swift"
  - Year: 2019
  - Mileage: 45000
  - Fuel: "Petrol"
- [ ] Click "✅ Save Vehicle"
- [ ] Vehicle card appears
- [ ] Click vehicle card to select
- [ ] Orange border appears on selected vehicle
- [ ] Active vehicle chip shows below tabs

### 3. OBD Code Input
- [ ] Switch to "Diagnose" tab
- [ ] Type "P0301" in OBD input field
- [ ] Orange badge appears with code
- [ ] Click X to clear code
- [ ] Badge disappears

### 4. Chat Diagnosis
- [ ] Type "engine makes clicking sound when cold"
- [ ] Click send button (or press Enter)
- [ ] User message appears (right side, orange gradient)
- [ ] Loading animation shows (three dots)
- [ ] Bot response appears (left side, dark card)
- [ ] DiagnosticResult card renders with sections

### 5. Voice Input
- [ ] Click microphone button
- [ ] Browser asks for mic permission → Allow
- [ ] Button turns red with pulse animation
- [ ] Speak: "check engine light is on"
- [ ] Text appears in input field
- [ ] Send message

### 6. Safety Warnings
- [ ] Send: "brake pedal feels soft"
- [ ] Response includes red safety banner
- [ ] Banner says "Professional mechanic verification required"
- [ ] Banner is not dismissible

### 7. Diagnostic Result Rendering
**Check that bot responses show**:
- [ ] Structured sections with emoji headers
- [ ] 🔍 DIAGNOSIS section
- [ ] 📋 CAUSES section
- [ ] 🛠️ FIX section
- [ ] 💰 COST ESTIMATE (in INR)
- [ ] ⚠️ SAFETY WARNING (if applicable)

### 8. PWA Features
- [ ] Open DevTools → Application → Manifest
- [ ] Manifest loads correctly
- [ ] Icons show (192x192 and 512x512)
- [ ] Theme color: #0f172a
- [ ] Display: standalone

### 9. Responsive Design
- [ ] Resize browser to mobile width (360px)
- [ ] Layout adapts correctly
- [ ] Touch targets are 44px+ height
- [ ] No horizontal scroll

### 10. Error Handling
**Backend Offline**:
- [ ] Stop backend server
- [ ] Try to send message
- [ ] Error message: "Cannot connect to AutoMech backend"

**Invalid API Key**:
- [ ] Set GROQ_API_KEY to "invalid"
- [ ] Restart backend
- [ ] Try diagnosis
- [ ] Error message: "Invalid or missing Groq API key"

## Integration Tests

### End-to-End Flow
1. [ ] Open app
2. [ ] Add vehicle (2019 Maruti Swift)
3. [ ] Select vehicle
4. [ ] Enter OBD code P0301
5. [ ] Type symptom: "engine misfiring"
6. [ ] Send message
7. [ ] Verify response includes:
   - Vehicle context (2019 Maruti Swift)
   - OBD code details
   - Symptom analysis
   - Cost estimate in INR
   - Safety warnings
8. [ ] Go to Vehicles tab
9. [ ] Verify vehicle still selected
10. [ ] Delete vehicle
11. [ ] Confirm deletion
12. [ ] Vehicle removed from list

## Performance Tests

### Backend
- [ ] Startup time < 10 seconds
- [ ] Diagnosis response time < 5 seconds (with Groq)
- [ ] Database queries < 100ms

### Frontend
- [ ] Initial load < 2 seconds
- [ ] Tab switch instant
- [ ] Message send/receive smooth
- [ ] No UI lag or jank

## Browser Compatibility

### Desktop
- [ ] Chrome/Edge (latest)
- [ ] Firefox (latest)
- [ ] Safari (latest)

### Mobile
- [ ] Chrome Android
- [ ] Safari iOS
- [ ] Edge Mobile

### Voice Input
- [ ] Works in Chrome/Edge
- [ ] Shows "not supported" message in Firefox/Safari

## Known Limitations (Expected Behavior)

- [ ] Voice input only works in Chrome/Edge (Web Speech API)
- [ ] RAG returns "No manuals found" if no PDFs added (expected)
- [ ] SQLite used by default (PostgreSQL optional)
- [ ] First diagnosis may be slower (model loading)

## Production Readiness

- [ ] All tests pass
- [ ] No console errors
- [ ] No Python exceptions
- [ ] API key is valid
- [ ] Database persists data
- [ ] PWA installable
- [ ] Responsive on mobile
- [ ] Safety warnings always show

---

## Test Results

**Date**: _____________
**Tester**: _____________
**Environment**: _____________

**Overall Status**: ⬜ PASS  ⬜ FAIL

**Notes**:
_____________________________________________
_____________________________________________
_____________________________________________
