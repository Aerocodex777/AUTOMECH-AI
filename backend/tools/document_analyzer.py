"""
Document analysis for vehicle manuals, receipts, reports
"""
import os
from pathlib import Path
import PyPDF2
from docx import Document
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

def analyze_document(file_path: str, query: str = "") -> str:
    """
    Analyze uploaded document (PDF, DOCX, TXT)
    
    Args:
        file_path: Path to the document
        query: Optional specific question about the document
    
    Returns:
        Summary and analysis of the document
    """
    try:
        # Extract text based on file type
        file_ext = Path(file_path).suffix.lower()
        
        if file_ext == '.pdf':
            text = extract_pdf_text(file_path)
        elif file_ext == '.docx':
            text = extract_docx_text(file_path)
        elif file_ext == '.txt':
            with open(file_path, 'r', encoding='utf-8') as f:
                text = f.read()
        else:
            return f"⚠️ Unsupported file type: {file_ext}. Please upload PDF, DOCX, or TXT files."
        
        if not text.strip():
            return "⚠️ Could not extract text from document. Please ensure it's not a scanned image."
        
        # Analyze with Groq
        groq_key = os.getenv("GROQ_API_KEY")
        if not groq_key or groq_key == "your_groq_api_key_here":
            return "⚠️ Groq API key not configured."
        
        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.2,
            groq_api_key=groq_key,
        )
        
        prompt = f"""You are an automotive document analyst. Analyze this vehicle-related document.

Document Content:
{text[:4000]}  # Limit to first 4000 chars

{"User Question: " + query if query else ""}

Provide:

📄 **DOCUMENT SUMMARY:**
[Brief overview of what this document is about]

🔍 **KEY INFORMATION:**
- Important details, specifications, or findings
- Dates, mileage, costs mentioned
- Vehicle details if present

🛠️ **ACTIONABLE INSIGHTS:**
- What does this mean for the vehicle owner?
- Any repairs or maintenance needed?
- Cost implications?

⚠️ **WARNINGS/CONCERNS:**
- Any red flags or issues mentioned?
- Safety concerns?

💡 **RECOMMENDATIONS:**
- What should be done based on this document?
- Next steps for the vehicle owner?

Keep it practical for Kerala vehicle owners and mechanics."""

        response = llm.invoke(prompt)
        return f"📄 **Document Analysis:**\n\n{response.content}"
        
    except Exception as e:
        return f"⚠️ **Document Analysis Error**: {str(e)}"


def extract_pdf_text(file_path: str) -> str:
    """Extract text from PDF"""
    text = ""
    try:
        with open(file_path, 'rb') as file:
            pdf_reader = PyPDF2.PdfReader(file)
            for page in pdf_reader.pages:
                text += page.extract_text() + "\n"
    except Exception as e:
        print(f"PDF extraction error: {e}")
    return text


def extract_docx_text(file_path: str) -> str:
    """Extract text from DOCX"""
    text = ""
    try:
        doc = Document(file_path)
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
    except Exception as e:
        print(f"DOCX extraction error: {e}")
    return text


def save_uploaded_document(file_data: bytes, filename: str) -> str:
    """
    Save uploaded document to disk
    
    Args:
        file_data: Binary file data
        filename: Original filename
    
    Returns:
        Path to saved file
    """
    # Create uploads directory
    upload_dir = Path("backend/uploads/documents")
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate unique filename
    import time
    timestamp = int(time.time())
    file_ext = Path(filename).suffix
    new_filename = f"doc_{timestamp}{file_ext}"
    
    file_path = upload_dir / new_filename
    
    # Save file
    with open(file_path, 'wb') as f:
        f.write(file_data)
    
    return str(file_path)
