# Quick Start: Structured Diagnostics

## 🚀 Getting Started

### System is Already Running!
- ✅ Backend: http://localhost:8000
- ✅ Frontend: http://localhost:5174 (or 5173)

## 📝 How to Use

### Method 1: Quick Diagnosis (Default)
Just type your symptom normally:

```
"tyre puncture"
"engine overheating"
"brake noise"
"check engine light on"
```

You'll get an immediate diagnosis with:
- Problem description
- Possible causes
- Fix steps
- Cost estimate (Kerala market)

### Method 2: Guided Diagnosis (Structured)
For complex issues, trigger guided mode by including these keywords:

```
"detailed diagnosis for engine noise"
"step by step help with brake problem"
"guide me through transmission issue"
```

The AI will:
1. Ask 3-5 targeted questions
2. Collect your answers one by one
3. Generate comprehensive diagnosis
4. Show available parts with images and prices

## 🎯 Example Conversation

### Quick Mode
```
You: tyre puncture
AI: 🔍 DIAGNOSIS: Tyre puncture...
    📋 CAUSES: Sharp object, wear and tear...
    🛠️ FIX: Remove object, patch or replace...
    💰 COST: ₹200 - ₹500
```

### Guided Mode
```
You: detailed diagnosis for engine overheating

AI: 📋 I'll ask you a few questions to diagnose this better:
    1. When did this problem start?
    2. Does it happen all the time or only in certain conditions?
    3. Have you noticed any other symptoms?
    
    Please answer each question.

You: started yesterday

AI: 2. Does it happen all the time or only in certain conditions?

You: only when driving uphill

AI: 3. Have you noticed any other symptoms?

You: temperature gauge goes to red zone

AI: 🔍 DIAGNOSIS: Coolant system failure...
    📋 CAUSES: Low coolant, thermostat failure...
    🛠️ FIX: Check coolant level, inspect radiator...
    💰 COST: ₹2,000 - ₹5,000
    
    🛒 AVAILABLE PARTS ONLINE:
    [Product cards with images, prices, and buy links]
```

## 🎨 Features You'll See

### Product Cards
- 📸 Product image
- 💰 Price in INR
- 🏪 Seller (Amazon India / Flipkart)
- 🔗 "View Product →" button

### Guided Mode Indicator
When in guided mode, you'll see:
```
📋 Guided Mode: Question 2/5
```

### Smart Placeholder
The input field changes based on context:
- Normal: "Describe symptoms... (type 'detailed' for guided diagnosis)"
- Guided: "Your answer..."

## 🔧 Other Features

### Upload Image
Click 📸 button to upload vehicle damage photos for AI analysis

### Upload Document
Click 📄 button to upload service reports, manuals (PDF, DOCX, TXT)

### OBD Code
Enter diagnostic codes in the OBD field at the top:
```
P0301 - Cylinder 1 Misfire
P0420 - Catalyst System Efficiency
```

### Vehicle Profile
Switch to "VEHICLES" tab to:
- Add your vehicle details
- Get personalized diagnostics
- Track repair history

## 💡 Tips

1. **For Simple Issues**: Use quick mode - just describe the problem
2. **For Complex Issues**: Use guided mode - type "detailed" or "guide me"
3. **Be Specific**: More details = better diagnosis
4. **Check Products**: Click product links to buy parts online
5. **Save Vehicle**: Add vehicle profile for better recommendations

## 🎯 Keywords that Trigger Guided Mode

- "detailed"
- "step by step"
- "guide me"
- "detailed diagnosis"
- "help me diagnose"

## 📱 Access the App

Open your browser and go to:
- http://localhost:5174
- or http://localhost:5173

## 🆘 Troubleshooting

### Backend Not Responding
```bash
cd backend
python main.py
```

### Frontend Not Loading
```bash
cd frontend
npm run dev
```

### Products Not Showing
- Check internet connection
- Products load from Amazon India and Flipkart
- May take 3-5 seconds to scrape

### Images Not Loading
- Some products may not have images
- Cards will still show price and link
- Try different search terms

## 🎉 You're Ready!

Start chatting with AutoMech AI and try both modes:
1. Quick: "brake noise"
2. Guided: "detailed diagnosis for brake noise"

Enjoy the enhanced diagnostic experience! 🚗🔧
