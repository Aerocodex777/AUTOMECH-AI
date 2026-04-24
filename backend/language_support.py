"""
Multi-language support for AutoMech AI
Supports English and Malayalam for Kerala users
"""
import re
from typing import Dict, Tuple

# Malayalam translations for common automotive terms
MALAYALAM_TRANSLATIONS = {
    # Common issues
    "engine": "എഞ്ചിൻ",
    "brake": "ബ്രേക്ക്",
    "battery": "ബാറ്ററി",
    "oil": "ഓയിൽ",
    "tire": "ടയർ",
    "wheel": "ചക്രം",
    "clutch": "ക്ലച്ച്",
    "gear": "ഗിയർ",
    "steering": "സ്റ്റിയറിംഗ്",
    "headlight": "ഹെഡ്‌ലൈറ്റ്",
    "taillight": "ടെയിൽലൈറ്റ്",
    "windshield": "വിൻഡ്‌ഷീൽഡ്",
    "radiator": "റേഡിയേറ്റർ",
    "alternator": "ആൾട്ടർനേറ്റർ",
    "starter": "സ്റ്റാർട്ടർ",
    "spark plug": "സ്പാർക്ക് പ്ലഗ്",
    "air filter": "എയർ ഫിൽട്ടർ",
    "fuel pump": "ഫ്യൂവൽ പമ്പ്",
    
    # Symptoms
    "noise": "ശബ്ദം",
    "sound": "ശബ്ദം",
    "leak": "ചോർച്ച",
    "smoke": "പുക",
    "vibration": "വൈബ്രേഷൻ",
    "problem": "പ്രശ്നം",
    "issue": "പ്രശ്നം",
    "damage": "കേടുപാട്",
    "broken": "തകർന്നു",
    "not working": "പ്രവർത്തിക്കുന്നില്ല",
    
    # Actions
    "repair": "അറ്റകുറ്റപ്പണി",
    "replace": "മാറ്റിസ്ഥാപിക്കുക",
    "fix": "ശരിയാക്കുക",
    "check": "പരിശോധിക്കുക",
    "service": "സർവീസ്",
    "maintenance": "മെയിന്റനൻസ്",
    
    # Common phrases
    "car won't start": "കാർ സ്റ്റാർട്ട് ആകുന്നില്ല",
    "check engine light": "ചെക്ക് എഞ്ചിൻ ലൈറ്റ്",
    "how much": "എത്ര വില",
    "cost": "വില",
    "price": "വില",
}

# Malayalam UI text
MALAYALAM_UI = {
    "welcome": "സ്വാഗതം! ഞാൻ AutoMech AI ആണ്.",
    "describe_problem": "നിങ്ങളുടെ വാഹനത്തിന്റെ പ്രശ്നം വിവരിക്കുക",
    "analyzing": "വിശകലനം ചെയ്യുന്നു...",
    "diagnosis": "രോഗനിർണയം",
    "recommendations": "ശുപാർശകൾ",
    "parts_needed": "ആവശ്യമായ ഭാഗങ്ങൾ",
    "estimated_cost": "കണക്കാക്കിയ വില",
    "upload_image": "ചിത്രം അപ്‌ലോഡ് ചെയ്യുക",
    "send": "അയയ്ക്കുക",
}


def detect_language(text: str) -> str:
    """
    Detect if text is in Malayalam or English
    
    Args:
        text: Input text
    
    Returns:
        'ml' for Malayalam, 'en' for English
    """
    # Check for Malayalam Unicode range (0D00-0D7F)
    malayalam_chars = re.findall(r'[\u0D00-\u0D7F]', text)
    
    if len(malayalam_chars) > len(text) * 0.3:  # If >30% Malayalam characters
        return 'ml'
    return 'en'


def enhance_prompt_for_malayalam(prompt: str, detected_lang: str) -> str:
    """
    Enhance the AI prompt to respond in Malayalam if input is Malayalam
    
    Args:
        prompt: Original prompt
        detected_lang: Detected language ('ml' or 'en')
    
    Returns:
        Enhanced prompt with language instruction
    """
    if detected_lang == 'ml':
        language_instruction = """
**IMPORTANT: The user is asking in Malayalam. Please respond in Malayalam (മലയാളം) language.**

Use Malayalam script for your entire response. Include:
- Diagnosis in Malayalam
- Part names in Malayalam (with English in brackets if needed)
- Cost estimates in Indian Rupees (₹)
- Kerala-specific context and recommendations

Example format:
പ്രശ്നം: [issue in Malayalam]
കാരണം: [cause in Malayalam]
ആവശ്യമായ ഭാഗങ്ങൾ: [parts in Malayalam]
വില: ₹[amount]

"""
        return language_instruction + prompt
    
    return prompt


def translate_response_to_malayalam(english_text: str) -> str:
    """
    Translate key automotive terms in response to Malayalam
    (Basic word replacement, not full translation)
    
    Args:
        english_text: Response in English
    
    Returns:
        Text with key terms translated
    """
    result = english_text
    
    # Replace common terms
    for eng, mal in MALAYALAM_TRANSLATIONS.items():
        # Case-insensitive replacement
        pattern = re.compile(re.escape(eng), re.IGNORECASE)
        result = pattern.sub(f"{mal} ({eng})", result)
    
    return result


def get_malayalam_greeting() -> str:
    """Get a friendly Malayalam greeting"""
    return """👋 സ്വാഗതം! ഞാൻ AutoMech AI ആണ്.

നിങ്ങളുടെ വാഹനത്തിന്റെ പ്രശ്നം മലയാളത്തിലോ ഇംഗ്ലീഷിലോ വിവരിക്കാം.

ഉദാഹരണങ്ങൾ:
🔧 "എന്റെ കാർ സ്റ്റാർട്ട് ആകുന്നില്ല"
🔧 "ബ്രേക്ക് അമർത്തുമ്പോൾ ശബ്ദം വരുന്നു"
🔧 "എഞ്ചിൻ ലൈറ്റ് കത്തിയിരിക്കുന്നു"

I can help you in Malayalam or English!"""


def format_cost_for_kerala(cost_min: int, cost_max: int, lang: str = 'en') -> str:
    """
    Format cost estimate for Kerala market
    
    Args:
        cost_min: Minimum cost
        cost_max: Maximum cost
        lang: Language ('en' or 'ml')
    
    Returns:
        Formatted cost string
    """
    if lang == 'ml':
        return f"വില: ₹{cost_min:,} - ₹{cost_max:,} (കേരള വിപണി)"
    else:
        return f"Cost: ₹{cost_min:,} - ₹{cost_max:,} (Kerala market)"


def get_example_queries(lang: str = 'en') -> Dict[str, str]:
    """
    Get example queries in specified language
    
    Args:
        lang: Language ('en' or 'ml')
    
    Returns:
        Dictionary of example queries
    """
    if lang == 'ml':
        return {
            "start_issue": "എന്റെ കാർ സ്റ്റാർട്ട് ആകുന്നില്ല. ക്ലിക്ക് ശബ്ദം വരുന്നു",
            "brake_noise": "ബ്രേക്ക് അമർത്തുമ്പോൾ ഗ്രൈൻഡിംഗ് ശബ്ദം",
            "engine_light": "ചെക്ക് എഞ്ചിൻ ലൈറ്റ് കത്തിയിരിക്കുന്നു",
            "oil_leak": "എഞ്ചിനിൽ നിന്ന് ഓയിൽ ചോർന്നു പോകുന്നു",
            "maintenance": "45,000 കിലോമീറ്റർ ആയി. എന്ത് മെയിന്റനൻസ് വേണം?",
        }
    else:
        return {
            "start_issue": "My car won't start. It makes a clicking sound",
            "brake_noise": "Grinding noise when I press the brake",
            "engine_light": "Check engine light is on",
            "oil_leak": "Oil is leaking from the engine",
            "maintenance": "My car has 45,000 km. What maintenance is needed?",
        }


# Test function
if __name__ == "__main__":
    # Test language detection
    print("Testing language detection:")
    test_text = "My car won't start"
    print(f"English: {detect_language(test_text)}")
    print(f"Malayalam: {detect_language('എന്റെ കാർ സ്റ്റാർട്ട് ആകുന്നില്ല')}")
    test_mixed = "My കാർ won't start"
    print(f"Mixed: {detect_language(test_mixed)}")
    
    print("\nMalayalam greeting:")
    print(get_malayalam_greeting())
    
    print("\nExample queries (Malayalam):")
    for key, query in get_example_queries('ml').items():
        print(f"  {key}: {query}")
