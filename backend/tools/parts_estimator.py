import os
from langchain.tools import tool
from langchain_community.chat_models import ChatOllama
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import requests
from requests.exceptions import RequestException, Timeout

env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(env_path)

def get_llm():
    """Get LLM with Ollama (primary) or Groq (fallback)."""
    try:
        # Check if Ollama is available
        response = requests.get("http://localhost:11434/api/tags", timeout=4)
        if response.status_code == 200:
            return ChatOllama(
                model="llama3",
                base_url="http://localhost:11434",
                temperature=0.2,
            )
    except (RequestException, Timeout):
        pass
    
    # Fallback to Groq
    groq_key = os.getenv("GROQ_API_KEY")
    if groq_key and groq_key != "your_groq_api_key_here":
        return ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.2,
            groq_api_key=groq_key,
        )
    
    # If both fail, return Ollama anyway (will error with helpful message)
    return ChatOllama(
        model="llama3",
        base_url="http://localhost:11434",
        temperature=0.2,
    )


@tool
def parts_estimator(parts_query: str) -> str:
    """
    Estimate parts and labor cost for automotive repairs in the Indian (Kerala) market in INR.
    Provide the repair description and optionally the vehicle make/model for more accurate pricing.
    """
    llm = get_llm()
    
    prompt = f"""You are an automotive parts cost estimator for Kerala, India.
You have deep knowledge of both authorized dealerships and local spare parts markets (like Broadway, Ernakulam).

Repair query: {parts_query}

Provide a structured cost estimate with:
1. **Parts Required** — list each part with OEM price range (INR) and aftermarket alternative
2. **Labor Cost** — estimated mechanic labor in INR (Kerala workshop rates)
3. **Total Estimated Cost** — range (best case / typical case)
4. **Best Source** — authorized dealer / local market / online (CarDekho, Amazon, Flipkart auto)
5. **Time Required** — approximate repair time
6. **Important Notes / Safety Warnings** — any cautions the owner must know

Be realistic for 2024 Kerala market prices. Always give ranges, not fixed prices. Use INR (₹) symbol.
If the repair is safety-critical (brakes, steering, airbags), strongly recommend authorized service center.
"""
    response = llm.invoke(prompt)
    return response.content
