# Structured Diagnostics Feature

## Overview

AutoMech AI now supports **Structured Diagnostics** - an intelligent guided flow that asks follow-up questions to provide more accurate diagnoses with product recommendations including images from online stores.

## Features

### 1. Guided Diagnostic Flow
- AI analyzes initial symptom and generates relevant follow-up questions
- Collects structured information through conversational interface
- Provides more accurate diagnosis based on detailed answers

### 2. Product Recommendations with Images
- Automatically scrapes parts from Amazon India and Flipkart
- Displays product images, prices, and direct purchase links
- Shows top 3-5 relevant products for each diagnosis

### 3. Two Diagnostic Modes

#### Quick Mode (Default)
- User describes symptom in one message
- AI provides immediate diagnosis
- Best for simple issues or experienced users

#### Guided Mode (Structured)
- Triggered by keywords: "detailed", "step by step", "guide me"
- AI asks 3-5 targeted questions
- Collects answers sequentially
- Generates comprehensive diagnosis with parts

## How to Use

### For Users

#### Quick Diagnosis
```
User: "engine overheating"
AI: [Provides immediate diagnosis]
```

#### Guided Diagnosis
```
User: "detailed diagnosis for engine overheating"
AI: "I'll ask you a few questions to diagnose this better:
     1. When did this problem start?
     2. Does it happen all the time or only in certain conditions?
     3. Have you noticed any other symptoms?"

User: "started yesterday"
AI: "2. Does it happen all the time or only in certain conditions?"

User: "only when driving uphill"
AI: "3. Have you noticed any other symptoms?"

User: "temperature gauge goes to red"
AI: [Provides comprehensive diagnosis with parts and images]
```

### API Endpoints

#### Start Structured Diagnostic
```http
POST /diagnose/structured/start
Content-Type: application/json

{
  "symptom": "engine overheating",
  "vehicle_id": 1  // optional
}

Response:
{
  "symptom": "engine overheating",
  "category": "cooling",
  "severity": "high",
  "initial_assessment": "Cooling system issue detected",
  "questions": [
    "When did this problem start?",
    "Does it happen all the time or only in certain conditions?",
    "Have you noticed any other symptoms?"
  ],
  "vehicle_context": "2019 Maruti Swift"
}
```

#### Complete Structured Diagnostic
```http
POST /diagnose/structured/complete
Content-Type: application/json

{
  "symptom": "engine overheating",
  "answers": {
    "When did this problem start?": "yesterday",
    "Does it happen all the time or only in certain conditions?": "only uphill",
    "Have you noticed any other symptoms?": "temperature gauge red"
  },
  "vehicle_id": 1  // optional
}

Response:
{
  "diagnosis_text": "Formatted diagnosis text",
  "diagnosis_data": {
    "diagnosis": "Coolant leak or thermostat failure",
    "causes": ["Damaged radiator", "Faulty thermostat", "Low coolant"],
    "fix_steps": ["Check coolant level", "Inspect radiator", "Test thermostat"],
    "parts_needed": ["Coolant", "Thermostat"],
    "cost_estimate": "₹2,000 - ₹5,000",
    "labor_hours": "1-2 hours",
    "safety_warning": "Do not drive with overheating engine",
    "urgency": "immediate",
    "products": [
      {
        "name": "Maruti Swift Thermostat",
        "price": "₹450",
        "seller": "Amazon India",
        "link": "https://amazon.in/...",
        "image": "https://m.media-amazon.com/..."
      }
    ]
  },
  "vehicle_context": "2019 Maruti Swift"
}
```

## Technical Implementation

### Backend Components

#### `structured_diagnostic.py`
- `analyze_initial_symptom()` - Analyzes symptom and generates questions
- `generate_diagnosis_with_parts()` - Creates diagnosis with product recommendations
- `format_structured_response()` - Formats output for display

#### `parts_scraper.py` (Enhanced)
- Now extracts product images from Amazon and Flipkart
- Returns structured data with image URLs
- Handles image loading errors gracefully

#### `main.py` (New Endpoints)
- `/diagnose/structured/start` - Initiates guided flow
- `/diagnose/structured/complete` - Generates final diagnosis

### Frontend Components

#### `Chat.jsx` (Enhanced)
- State management for structured mode
- Question/answer tracking
- Automatic mode detection
- Product display integration

#### `ProductCard.jsx` (New)
- Displays product with image
- Shows price and seller
- Direct purchase link
- Fallback for missing images

### State Management

```javascript
{
  structuredMode: boolean,           // Is guided mode active?
  currentQuestions: string[],        // Questions to ask
  currentAnswers: object,            // Collected answers
  currentSymptom: string            // Original symptom
}
```

## Styling

### Product Cards
- Grid layout (responsive)
- Image container with fallback
- Orange accent on hover
- Direct purchase button

### Guided Mode Badge
- Shows current question number
- Orange theme matching design
- Positioned above input field

## Benefits

### For Users
- More accurate diagnoses through structured questions
- Visual product recommendations with images
- Direct purchase links to trusted sellers
- Kerala market pricing

### For Mechanics
- Systematic diagnostic approach
- Parts availability information
- Cost estimation for customers
- Professional workflow

## Future Enhancements

1. **Multi-language Support** - Malayalam, Hindi, Tamil
2. **Local Shop Integration** - Kerala auto parts shops
3. **Price Comparison** - Multiple sellers side-by-side
4. **Diagnostic History** - Save and review past diagnoses
5. **Video Tutorials** - Embedded repair guides
6. **AR Integration** - Point camera at part for identification

## Testing

### Test Scenarios

1. **Quick Diagnosis**
   - Input: "brake noise"
   - Expected: Immediate diagnosis

2. **Guided Diagnosis**
   - Input: "detailed diagnosis for brake noise"
   - Expected: 3-5 questions, then comprehensive diagnosis

3. **Product Display**
   - Expected: Products with images, prices, links
   - Fallback: Graceful handling of missing images

4. **Error Handling**
   - Network errors
   - Scraping failures
   - Invalid responses

## Configuration

### Environment Variables
```bash
GROQ_API_KEY=your_groq_api_key  # Required for AI
```

### Scraping Settings
- Timeout: 10 seconds per site
- Max products: 10 total (5 per site)
- Retry: 3 attempts with exponential backoff

## Troubleshooting

### Products Not Showing
- Check internet connection
- Verify scraping sites are accessible
- Check backend logs for errors

### Images Not Loading
- CORS issues - images load from external domains
- Fallback: Image container hides automatically

### Questions Not Appearing
- Check keyword triggers: "detailed", "guide me", "step by step"
- Verify backend endpoint is responding
- Check browser console for errors

## Performance

- Initial question generation: ~2-3 seconds
- Final diagnosis with products: ~5-8 seconds
- Product scraping: ~3-5 seconds per site
- Total guided flow: ~15-20 seconds

## Security

- No user data stored in scraping
- External links open in new tab
- Input sanitization on all endpoints
- Rate limiting recommended for production
