"""
Simple diagnostic agent (fallback)
"""
import os
import requests
from groq import Groq
from dotenv import load_dotenv

load_dotenv()


def check_ollama_available(timeout: int = 2) -> bool:
    """Check if Ollama is running"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=timeout)
        return response.status_code == 200
    except:
        return False


def run_diagnostic(symptoms: str, vehicle_context: str = "") -> str:
    """Simple diagnostic function"""
    try:
        # Use Groq API directly
        groq_key = os.getenv("GROQ_API_KEY")
        if not groq_key or groq_key == "your_groq_api_key_here":
            return "⚠️ GROQ_API_KEY not configured"
        
        client = Groq(api_key=groq_key)
        
        prompt = f"""You are an automotive diagnostic expert for Kerala, India.

Vehicle: {vehicle_context or 'Not specified'}
Symptoms: {symptoms}

Provide a clear diagnosis with:
1. Most likely cause
2. Parts needed (if any)
3. Estimated cost in INR
4. Repair recommendations

Be specific and practical."""

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        return f"⚠️ Diagnostic error: {str(e)}"
