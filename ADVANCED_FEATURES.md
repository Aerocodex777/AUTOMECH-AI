# AutoMech AI — Advanced Features

## New Capabilities Added

### 1. 🛒 Web Scraping for Parts

**What it does:**
- Searches Amazon India and Flipkart for automotive parts
- Returns prices, sellers, and direct purchase links
- Filters by vehicle make/model

**API Endpoint:**
```
GET /parts/search?part_name=spark+plug&make=Maruti&model=Swift
```

**Response:**
```json
{
  "results": [
    {
      "name": "NGK Spark Plug for Maruti Swift",
      "price": "₹450",
      "seller": "Amazon India",
      "link": "https://amazon.in/..."
    }
  ],
  "formatted": "🛒 Available Parts Online:\n\n1. NGK Spark Plug..."
}
```

**How to use from frontend:**
- Add "Search Parts" button
- Call API with part name from diagnosis
- Display results with buy links

---

### 2. 📸 Image Upload & Damage Analysis

**What it does:**
- Analyzes vehicle damage from photos
- Uses Groq Vision AI (llama-3.2-11b-vision-preview)
- Provides damage assessment, repair recommendations, cost estimates

**API Endpoint:**
```
POST /analyze/image
Content-Type: multipart/form-data
Body: file (image/jpeg or image/png)
```

**Response:**
```json
{
  "analysis": "📸 Image Analysis Results:\n\n1. DAMAGE ASSESSMENT:...",
  "file_path": "backend/uploads/images/vehicle_1234567890.jpg"
}
```

**What it analyzes:**
- Damage type (dent, scratch, crack, etc.)
- Severity level (Minor/Moderate/Severe)
- Affected components
- Repair recommendations
- Cost estimates in INR
- Safety concerns

**How to use from frontend:**
- Add image upload button in chat
- Send image to `/analyze/image`
- Display analysis in chat bubble

---

### 3. 📄 Document Upload & Analysis

**What it does:**
- Analyzes vehicle documents (service reports, manuals, receipts)
- Extracts key information
- Provides actionable insights
- Supports PDF, DOCX, TXT

**API Endpoint:**
```
POST /analyze/document
Content-Type: multipart/form-data
Body: 
  - file (PDF/DOCX/TXT)
  - query (optional specific question)
```

**Response:**
```json
{
  "analysis": "📄 Document Analysis:\n\nDOCUMENT SUMMARY:...",
  "file_path": "backend/uploads/documents/doc_1234567890.pdf"
}
```

**What it extracts:**
- Document summary
- Key information (dates, costs, mileage)
- Vehicle details
- Actionable insights
- Warnings/concerns
- Recommendations

**How to use from frontend:**
- Add document upload button
- Send PDF/DOCX to `/analyze/document`
- Optionally include specific question
- Display analysis in chat

---

## Installation

### 1. Install new dependencies:
```bash
cd backend
pip install -r requirements.txt
```

New packages added:
- `beautifulsoup4` - Web scraping
- `selenium` - Advanced scraping (optional)
- `Pillow` - Image processing
- `opencv-python` - Image analysis
- `pypdf2` - PDF extraction
- `python-docx` - DOCX extraction

### 2. Create upload directories:
```bash
mkdir -p backend/uploads/images
mkdir -p backend/uploads/documents
```

### 3. Restart backend:
```bash
python main.py
```

---

## Frontend Integration

### Add Upload Buttons to Chat.jsx

```jsx
// Add to input area
<input
  type="file"
  accept="image/*"
  onChange={handleImageUpload}
  style={{display: 'none'}}
  ref={imageInputRef}
/>
<button onClick={() => imageInputRef.current.click()}>
  📸 Upload Image
</button>

<input
  type="file"
  accept=".pdf,.docx,.txt"
  onChange={handleDocumentUpload}
  style={{display: 'none'}}
  ref={docInputRef}
/>
<button onClick={() => docInputRef.current.click()}>
  📄 Upload Document
</button>
```

### Handle Uploads

```jsx
const handleImageUpload = async (e) => {
  const file = e.target.files[0];
  if (!file) return;
  
  const formData = new FormData();
  formData.append('file', file);
  
  setLoading(true);
  try {
    const res = await axios.post(`${API}/analyze/image`, formData, {
      headers: {'Content-Type': 'multipart/form-data'}
    });
    setMessages(prev => [...prev, 
      {role: 'user', text: `📸 Uploaded: ${file.name}`},
      {role: 'bot', text: res.data.analysis}
    ]);
  } catch (err) {
    console.error(err);
  } finally {
    setLoading(false);
  }
};

const handleDocumentUpload = async (e) => {
  const file = e.target.files[0];
  if (!file) return;
  
  const formData = new FormData();
  formData.append('file', file);
  formData.append('query', ''); // Optional question
  
  setLoading(true);
  try {
    const res = await axios.post(`${API}/analyze/document`, formData, {
      headers: {'Content-Type': 'multipart/form-data'}
    });
    setMessages(prev => [...prev,
      {role: 'user', text: `📄 Uploaded: ${file.name}`},
      {role: 'bot', text: res.data.analysis}
    ]);
  } catch (err) {
    console.error(err);
  } finally {
    setLoading(false);
  }
};
```

---

## Testing

### Test Parts Search:
```bash
curl "http://localhost:8000/parts/search?part_name=brake+pad&make=Maruti&model=Swift"
```

### Test Image Analysis:
```bash
curl -X POST http://localhost:8000/analyze/image \
  -F "file=@damage_photo.jpg"
```

### Test Document Analysis:
```bash
curl -X POST http://localhost:8000/analyze/document \
  -F "file=@service_report.pdf" \
  -F "query=What repairs were done?"
```

---

## Features Summary

| Feature | Status | API Endpoint | Frontend Integration |
|---------|--------|--------------|---------------------|
| Parts Search | ✅ Ready | `/parts/search` | Need to add button |
| Image Analysis | ✅ Ready | `/analyze/image` | Need to add upload |
| Document Analysis | ✅ Ready | `/analyze/document` | Need to add upload |

---

## Next Steps

1. **Install dependencies**: `pip install -r requirements.txt`
2. **Test backend endpoints**: Use curl or Postman
3. **Add frontend UI**: Upload buttons in Chat component
4. **Test with real data**: Upload actual vehicle images/documents

---

## Notes

- **Image Analysis** requires Groq API key (uses vision model)
- **Web Scraping** may need updates if site structures change
- **Document Analysis** works best with text-based PDFs (not scanned images)
- **Upload limits**: Default 10MB per file (configurable in FastAPI)

---

**Status**: ✅ Backend implementation complete
**Next**: Frontend integration needed
