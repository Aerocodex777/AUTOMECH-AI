# AutoMech AI — Intelligent Fallback System

## Overview

The system now uses a smart fallback mechanism that automatically switches between local Ollama and cloud Groq API based on availability.

## How It Works

### Primary: Local Ollama (llama3)
- **Checked first** with 4-second timeout
- **Endpoint**: http://localhost:11434
- **Advantages**: 
  - Free, unlimited usage
  - Complete privacy
  - No internet required
  - Fast responses

### Fallback: Groq API (llama-3.3-70b-versatile)
- **Activated when**:
  - Ollama doesn't respond within 4 seconds
  - Ollama is not running
  - Ollama connection fails
- **Advantages**:
  - Always available (cloud-based)
  - Faster than local on slower machines
  - Larger model (70B vs 8B)

## Configuration

### For Ollama Only (Default)
No configuration needed! Just ensure Ollama is running:
```bash
# Check if Ollama is running
ollama list

# If not running, start it
ollama serve
```

### For Groq Fallback
Add your Groq API key to `backend/.env`:
```env
GROQ_API_KEY=gsk_your_actual_key_here
```

Get a free key: https://console.groq.com/keys

## Behavior

### Scenario 1: Ollama Running
```
User Request → Check Ollama (4s timeout) → ✅ Available
             → Use Ollama (llama3)
             → Console: "🏠 Using local Ollama (llama3)"
```

### Scenario 2: Ollama Not Responding
```
User Request → Check Ollama (4s timeout) → ❌ Timeout/Unavailable
             → Check Groq API Key → ✅ Configured
             → Use Groq (llama-3.3-70b-versatile)
             → Console: "🌐 Using Groq API (Ollama unavailable)"
```

### Scenario 3: Both Unavailable
```
User Request → Check Ollama → ❌ Unavailable
             → Check Groq API Key → ❌ Not configured
             → Return Error: "Configuration Error: Please configure GROQ_API_KEY or ensure Ollama is running"
```

## Implementation Details

### Files Modified

1. **backend/agent.py**
   - `check_ollama_available(timeout=4)` - Checks Ollama health
   - `create_agent(use_groq=False)` - Creates agent with fallback logic
   - Prints which service is being used

2. **backend/tools/parts_estimator.py**
   - `get_llm()` - Returns appropriate LLM with fallback
   - Same 4-second timeout for Ollama check

### Health Check Endpoint

The system checks: `http://localhost:11434/api/tags`
- **Success (200)**: Ollama is healthy → use it
- **Timeout/Error**: Ollama unavailable → fallback to Groq

## Monitoring

### Console Output

When a diagnosis is requested, you'll see:
```
🏠 Using local Ollama (llama3)
```
or
```
🌐 Using Groq API (Ollama unavailable)
```

### Logs

Check backend terminal for:
- Ollama connection attempts
- Fallback activations
- Error messages

## Performance

### Ollama (Local)
- First request: ~5-10 seconds (model loading)
- Subsequent: ~2-4 seconds
- No rate limits

### Groq (Cloud)
- All requests: ~2-3 seconds
- Rate limits: Generous free tier
- Requires internet

## Best Practices

### For Development
- Use Ollama for privacy and unlimited testing
- Keep Groq as backup for when Ollama is slow/unavailable

### For Production
- Configure both for maximum reliability
- Ollama handles most traffic (free)
- Groq catches overflow/failures

### For Kerala Workshop
- Primary: Ollama (no internet needed)
- Fallback: Groq (when internet available)
- Best of both worlds!

## Troubleshooting

### "Configuration Error" Message
**Problem**: Both Ollama and Groq unavailable
**Solution**: 
1. Start Ollama: `ollama serve` or open Ollama app
2. OR add Groq API key to `backend/.env`

### Slow Responses
**Problem**: Ollama taking >4 seconds
**Solution**: System automatically falls back to Groq (if configured)

### Always Using Groq
**Problem**: Ollama not being detected
**Solution**: 
1. Check Ollama is running: `ollama list`
2. Verify endpoint: `curl http://localhost:11434/api/tags`
3. Check firewall isn't blocking localhost:11434

## Cost Analysis

### Monthly Usage (100 diagnoses/day)

**Ollama Only**:
- Cost: ₹0 (free)
- Privacy: 100%
- Internet: Not required

**Groq Only**:
- Cost: ₹0 (free tier sufficient)
- Privacy: Data sent to cloud
- Internet: Required

**Hybrid (Recommended)**:
- Cost: ₹0 (Ollama handles 90%+)
- Privacy: 90% local, 10% cloud
- Internet: Optional (fallback only)

## Summary

✅ **Intelligent**: Automatically chooses best available service
✅ **Reliable**: Never fails if either service works
✅ **Fast**: 4-second timeout prevents long waits
✅ **Free**: Both options are free to use
✅ **Private**: Prefers local Ollama when available
✅ **Flexible**: Easy to configure for any scenario

---

**Status**: ✅ Active
**Default**: Ollama (local)
**Fallback**: Groq (cloud)
**Timeout**: 4 seconds
