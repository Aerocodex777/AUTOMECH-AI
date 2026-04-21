# 🇮🇳 Malayalam Language Support

## Overview
AutoMech AI now supports **Malayalam (മലയാളം)** language for Kerala users! You can ask questions in Malayalam and get responses in Malayalam.

## Features

### ✅ What's Supported

1. **Malayalam Input**
   - Type your questions in Malayalam script
   - System automatically detects Malayalam language
   - No need to switch language manually

2. **Malayalam Output**
   - AI responds in Malayalam when you ask in Malayalam
   - Technical terms in Malayalam with English in brackets
   - Example: ബാറ്ററി (Battery), ബ്രേക്ക് പാഡ് (Brake Pad)

3. **Kerala Context**
   - All costs in Indian Rupees (₹)
   - Kerala market pricing
   - Local mechanic recommendations
   - Monsoon-specific advice

4. **Bilingual Support**
   - Switch between Malayalam and English anytime
   - Mixed language queries supported
   - Conversation memory works across languages

## Example Queries

### Malayalam Examples

**Starting Issues:**
```
എന്റെ കാർ സ്റ്റാർട്ട് ആകുന്നില്ല. ക്ലിക്ക് ശബ്ദം വരുന്നു
```

**Brake Problems:**
```
ബ്രേക്ക് അമർത്തുമ്പോൾ ഗ്രൈൻഡിംഗ് ശബ്ദം വരുന്നു
```

**Engine Light:**
```
ചെക്ക് എഞ്ചിൻ ലൈറ്റ് കത്തിയിരിക്കുന്നു
```

**Oil Leak:**
```
എഞ്ചിനിൽ നിന്ന് ഓയിൽ ചോർന്നു പോകുന്നു
```

**Maintenance:**
```
എന്റെ കാറിന് 45,000 കിലോമീറ്റർ ആയി. എന്ത് മെയിന്റനൻസ് വേണം?
```

**Cost Inquiry:**
```
ബ്രേക്ക് പാഡ് മാറ്റാൻ എത്ര ചിലവ് വരും?
```

**DIY Help:**
```
സ്പാർക്ക് പ്ലഗ് എങ്ങനെ മാറ്റാം?
```

## How It Works

### 1. Language Detection
```python
# System automatically detects Malayalam
detected_lang = detect_language(user_input)
# Returns 'ml' for Malayalam, 'en' for English
```

### 2. Response Generation
- If Malayalam detected → AI responds in Malayalam
- If English detected → AI responds in English
- Mixed input → AI responds in dominant language

### 3. Technical Terms
- Common parts: ബാറ്ററി (Battery), എഞ്ചിൻ (Engine)
- Actions: അറ്റകുറ്റപ്പണി (Repair), പരിശോധിക്കുക (Check)
- Symptoms: ശബ്ദം (Noise), ചോർച്ച (Leak)

## Malayalam Automotive Vocabulary

### Common Parts (സാധാരണ ഭാഗങ്ങൾ)
- എഞ്ചിൻ (Engine)
- ബ്രേക്ക് (Brake)
- ബാറ്ററി (Battery)
- ടയർ (Tire)
- ക്ലച്ച് (Clutch)
- ഗിയർ (Gear)
- സ്റ്റിയറിംഗ് (Steering)
- ഹെഡ്‌ലൈറ്റ് (Headlight)
- റേഡിയേറ്റർ (Radiator)
- സ്പാർക്ക് പ്ലഗ് (Spark Plug)

### Symptoms (ലക്ഷണങ്ങൾ)
- ശബ്ദം (Noise/Sound)
- ചോർച്ച (Leak)
- പുക (Smoke)
- വൈബ്രേഷൻ (Vibration)
- പ്രശ്നം (Problem)
- കേടുപാട് (Damage)

### Actions (പ്രവർത്തനങ്ങൾ)
- അറ്റകുറ്റപ്പണി (Repair)
- മാറ്റിസ്ഥാപിക്കുക (Replace)
- ശരിയാക്കുക (Fix)
- പരിശോധിക്കുക (Check)
- സർവീസ് (Service)

## Technical Implementation

### Backend Files
- `backend/language_support.py` - Language detection and translation
- `backend/main.py` - Language detection in API
- `backend/agentic_agent.py` - Malayalam response generation

### Key Functions
```python
# Detect language
detect_language(text: str) -> str

# Enhance prompt for Malayalam
enhance_prompt_for_malayalam(prompt: str, lang: str) -> str

# Get Malayalam greeting
get_malayalam_greeting() -> str
```

## Demo Examples

### Example 1: Battery Issue
**User (Malayalam):**
```
എന്റെ കാർ സ്റ്റാർട്ട് ആകുന്നില്ല. ക്ലിക്ക് ശബ്ദം മാത്രം വരുന്നു
```

**AI Response (Malayalam):**
```
🔧 രോഗനിർണയം:

നിങ്ങളുടെ കാറിന്റെ ബാറ്ററി (Battery) തീർന്നിരിക്കാം. ക്ലിക്ക് ശബ്ദം വരുന്നത് 
സ്റ്റാർട്ടർ മോട്ടോറിന് വേണ്ടത്ര പവർ കിട്ടാത്തതിനാലാണ്.

പരിശോധിക്കേണ്ടവ:
1. ബാറ്ററി ടെർമിനലുകൾ വൃത്തിയാണോ എന്ന്
2. ബാറ്ററി വോൾട്ടേജ് (12V ഉണ്ടായിരിക്കണം)
3. ബാറ്ററി പഴക്കം (3-4 വർഷത്തിൽ കൂടുതലാണോ)

ആവശ്യമായ ഭാഗങ്ങൾ:
- പുതിയ ബാറ്ററി (New Battery)

വില: ₹3,500 - ₹6,500 (കേരള വിപണി)

ശുപാർശ: ബാറ്ററി ടെസ്റ്റ് ചെയ്യാൻ അടുത്തുള്ള മെക്കാനിക്കിനെ സമീപിക്കുക.
```

### Example 2: Follow-up in Malayalam
**User:**
```
എത്ര വില വരും?
```

**AI Response:**
```
ബാറ്ററി മാറ്റിസ്ഥാപിക്കാനുള്ള ചിലവ്:

ബാറ്ററി വില: ₹3,500 - ₹6,500
- Amaron: ₹4,200 - ₹5,500
- Exide: ₹3,800 - ₹5,000
- SF Sonic: ₹4,000 - ₹5,200

ലേബർ ചാർജ്: ₹200 - ₹500

മൊത്തം: ₹3,700 - ₹7,000

കേരളയിലെ വിശ്വസനീയമായ കടകളിൽ നിന്ന് വാങ്ങുക. വാറന്റി ഉറപ്പാക്കുക.
```

## Limitations

### Current Limitations
1. **UI Language**: Frontend UI is still in English (Malayalam UI coming soon)
2. **Voice Input**: Malayalam voice recognition not yet implemented
3. **OCR**: Malayalam text in images not yet supported
4. **Full Translation**: Some technical terms remain in English

### Future Enhancements
- [ ] Full Malayalam UI
- [ ] Malayalam voice input/output
- [ ] Malayalam OCR for documents
- [ ] More comprehensive Malayalam vocabulary
- [ ] Regional dialect support (Malabar, Kochi, Trivandrum)

## Testing Malayalam Support

### Test Queries
Try these Malayalam queries to test the system:

1. **Simple Query:**
   ```
   എന്റെ കാർ എന്താണ് പ്രശ്നം?
   ```

2. **Specific Issue:**
   ```
   ബ്രേക്ക് പാഡ് മാറ്റണം. എവിടെ കിട്ടും?
   ```

3. **Cost Question:**
   ```
   സർവീസിന് എത്ര ചിലവ് വരും?
   ```

4. **Maintenance:**
   ```
   മഴക്കാലത്തിന് മുമ്പ് എന്ത് ചെയ്യണം?
   ```

## Benefits for Kerala Users

✅ **Accessibility**: No English knowledge required
✅ **Comfort**: Ask in your native language
✅ **Clarity**: Better understanding of technical issues
✅ **Local Context**: Kerala-specific recommendations
✅ **Cultural Fit**: Familiar terminology and examples

## Technical Notes

### Language Detection Algorithm
- Checks for Malayalam Unicode characters (U+0D00 to U+0D7F)
- If >30% Malayalam characters → Detected as Malayalam
- Otherwise → Detected as English

### Response Generation
- LLM (Llama 3.3) has native Malayalam support
- System prompts LLM to respond in Malayalam
- Technical terms provided in both languages

### Performance
- No performance impact from language detection
- Same response time for Malayalam and English
- Conversation memory works across languages

## For Demo

### Demo Script (Malayalam)
**Show Malayalam capability:**

1. Type: `എന്റെ കാർ സ്റ്റാർട്ട് ആകുന്നില്ല`
2. Show AI responds in Malayalam
3. Follow-up: `എത്ര വില വരും?`
4. Show conversation memory works in Malayalam

**Talking Point:**
"AutoMech AI is truly Kerala-friendly - you can ask questions in Malayalam and get responses in Malayalam. This makes automotive diagnostics accessible to everyone in Kerala, regardless of English proficiency."

## Summary

🇮🇳 **Malayalam Support Status: ACTIVE**

- ✅ Malayalam input detection
- ✅ Malayalam response generation
- ✅ Kerala-specific context
- ✅ Bilingual technical terms
- ✅ Conversation memory across languages
- ⏳ Malayalam UI (coming soon)
- ⏳ Malayalam voice (coming soon)

AutoMech AI is now truly a Kerala-first automotive assistant! 🚗💚
