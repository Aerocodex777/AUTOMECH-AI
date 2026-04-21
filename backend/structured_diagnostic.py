"""
Structured diagnostic flow with follow-up questions and product recommendations
"""
from typing import Dict, List, Optional
from langchain_groq import ChatGroq
from tools.parts_scraper import scrape_parts
import os
import json

def analyze_initial_symptom(symptom: str) -> Dict:
    """
    Analyze initial symptom and determine what questions to ask
    
    Returns:
        {
            'category': str,  # engine, brake, electrical, tire, etc.
            'questions': List[str],  # Follow-up questions to ask
            'severity': str  # low, medium, high, critical
        }
    """
    groq_key = os.getenv("GROQ_API_KEY")
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.2,
        groq_api_key=groq_key,
    )
    
    prompt = f"""You are an automotive diagnostic expert. Analyze this symptom and provide structured information.

Symptom: {symptom}

Respond ONLY with valid JSON in this exact format (no markdown, no code blocks):
{{
    "category": "engine",
    "severity": "medium",
    "questions": [
        "When did this problem start?",
        "Does it happen all the time or only in certain conditions?",
        "Have you noticed any other symptoms?"
    ],
    "initial_assessment": "Brief assessment of the issue"
}}

Categories: engine, brake, electrical, tire, transmission, cooling, fuel, suspension, exhaust, other
Severity: low, medium, high, critical

Ask 3-5 specific diagnostic questions that will help narrow down the problem.
Questions should be clear and easy to answer."""

    response = llm.invoke(prompt)
    
    # Clean response - remove markdown code blocks if present
    content = response.content.strip()
    if content.startswith('```'):
        content = content.split('```')[1]
        if content.startswith('json'):
            content = content[4:].strip()
    
    try:
        return json.loads(content)
    except Exception as e:
        print(f"JSON parsing error in analyze_initial_symptom: {e}")
        print(f"Response content: {content}")
        # Fallback if JSON parsing fails
        return {
            'category': 'other',
            'severity': 'medium',
            'questions': [
                'When did this problem start?',
                'Does it happen all the time or only in certain conditions?',
                'Have you noticed any other symptoms?'
            ],
            'initial_assessment': 'Need more information to diagnose properly.'
        }


def generate_diagnosis_with_parts(symptom: str, answers: Dict, vehicle_context: str = "") -> Dict:
    """
    Generate final diagnosis with parts recommendations
    
    Args:
        symptom: Initial symptom
        answers: Dict of question -> answer pairs
        vehicle_context: Vehicle information
    
    Returns:
        {
            'diagnosis': str,
            'causes': List[str],
            'fix_steps': List[str],
            'parts_needed': List[str],
            'cost_estimate': str,
            'safety_warning': str,
            'products': List[Dict]  # Scraped products with images
        }
    """
    groq_key = os.getenv("GROQ_API_KEY")
    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        temperature=0.3,
        groq_api_key=groq_key,
    )
    
    # Format answers
    answers_text = "\n".join([f"Q: {q}\nA: {a}" for q, a in answers.items()])
    
    prompt = f"""You are an automotive diagnostic expert for Kerala, India.

Vehicle: {vehicle_context or 'Not specified'}
Initial Symptom: {symptom}

Follow-up Information:
{answers_text}

Based on this information, provide a comprehensive diagnosis. Respond ONLY with valid JSON in this exact format:
{{
    "diagnosis": "Clear one-sentence summary of the problem",
    "causes": ["Most likely cause", "Second likely cause", "Third possible cause"],
    "fix_steps": ["First step to fix", "Second step", "Third step"],
    "parts_needed": ["Part name 1", "Part name 2"],
    "cost_estimate": "₹X,XXX - ₹X,XXX",
    "labor_hours": "X-X hours",
    "safety_warning": "Critical warning if needed, otherwise empty string",
    "urgency": "immediate"
}}

IMPORTANT: 
- Return ONLY valid JSON, no markdown, no code blocks, no extra text
- Be specific and practical for Kerala mechanics
- Use Indian Rupees (₹) for costs
- Keep diagnosis concise and clear"""

    response = llm.invoke(prompt)
    
    # Clean response - remove markdown code blocks if present
    content = response.content.strip()
    if content.startswith('```'):
        # Remove markdown code blocks
        content = content.split('```')[1]
        if content.startswith('json'):
            content = content[4:].strip()
    
    try:
        diagnosis_data = json.loads(content)
    except Exception as e:
        print(f"JSON parsing error: {e}")
        print(f"Response content: {content}")
        # Fallback with better error handling
        diagnosis_data = {
            'diagnosis': 'Unable to parse diagnosis. Please try again.',
            'causes': ['System error occurred'],
            'fix_steps': ['Please rephrase your question and try again'],
            'parts_needed': [],
            'cost_estimate': 'N/A',
            'labor_hours': 'N/A',
            'safety_warning': '',
            'urgency': 'routine'
        }
    
    # Scrape products for needed parts
    products = []
    if diagnosis_data.get('parts_needed'):
        for part in diagnosis_data['parts_needed'][:2]:  # Top 2 parts
            try:
                scraped = scrape_parts(part, "", "")
                products.extend(scraped[:3])  # Top 3 products per part
            except:
                pass
    
    diagnosis_data['products'] = products
    return diagnosis_data


def format_structured_response(data: Dict) -> str:
    """Format structured diagnosis into readable text"""
    output = f"""🔍 DIAGNOSIS
{data.get('diagnosis', 'No diagnosis available')}

📋 POSSIBLE CAUSES"""
    
    causes = data.get('causes', [])
    if causes:
        for i, cause in enumerate(causes, 1):
            output += f"\n{i}. {cause}"
    else:
        output += "\n• Information insufficient for detailed analysis"
    
    output += "\n\n🛠️ REPAIR STEPS"
    fix_steps = data.get('fix_steps', [])
    if fix_steps:
        for i, step in enumerate(fix_steps, 1):
            output += f"\n{i}. {step}"
    else:
        output += "\n• Consult a professional mechanic"
    
    parts_needed = data.get('parts_needed', [])
    if parts_needed:
        output += "\n\n🔧 PARTS NEEDED"
        for part in parts_needed:
            output += f"\n• {part}"
    
    output += f"\n\n💰 ESTIMATED COST\n{data.get('cost_estimate', 'Contact local mechanic for quote')}"
    output += f"\n\n⏱️ LABOR TIME\n{data.get('labor_hours', 'Varies based on issue')}"
    
    safety_warning = data.get('safety_warning', '')
    if safety_warning:
        output += f"\n\n⚠️ SAFETY WARNING\n{safety_warning}"
    
    urgency = data.get('urgency', 'routine')
    urgency_emoji = {
        'immediate': '🚨',
        'soon': '⚡',
        'routine': '📅'
    }
    urgency_text = {
        'immediate': 'IMMEDIATE ATTENTION REQUIRED',
        'soon': 'Address Soon',
        'routine': 'Routine Maintenance'
    }
    output += f"\n\n{urgency_emoji.get(urgency, '📅')} URGENCY\n{urgency_text.get(urgency, 'Routine')}"
    
    # Add products
    products = data.get('products', [])
    if products:
        output += "\n\n🛒 AVAILABLE PARTS ONLINE"
        for i, product in enumerate(products[:5], 1):
            output += f"\n\n{i}. {product['name']}"
            output += f"\n   💰 {product['price']} | 🏪 {product['seller']}"
            if product.get('link'):
                output += f"\n   🔗 {product['link']}"
    
    return output
