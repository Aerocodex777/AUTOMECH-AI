"""
Image analysis for vehicle damage detection using Vision AI
"""
import base64
import os
from pathlib import Path
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from dotenv import load_dotenv

load_dotenv()

def analyze_vehicle_image(image_path: str) -> str:
    """
    Analyze vehicle damage from image using Vision API
    
    Args:
        image_path: Path to the image file
    
    Returns:
        Analysis of the damage with recommendations
    """
    try:
        # Read and encode image
        with open(image_path, 'rb') as image_file:
            image_data = base64.b64encode(image_file.read()).decode('utf-8')
        
        groq_key = os.getenv("GROQ_API_KEY")
        if not groq_key or groq_key == "your_groq_api_key_here":
            return "⚠️ Groq API key not configured. Please set GROQ_API_KEY in backend/.env"
        
        # Try Groq vision models first (they keep changing, so try multiple)
        groq_vision_models = [
            "llama-3.2-90b-vision-preview",
            "llama-3.2-11b-vision-preview",
            "llava-v1.5-7b-4096-preview"
        ]
        
        analysis_result = None
        
        # Try Groq models
        for model_name in groq_vision_models:
            try:
                print(f"🔍 Trying Groq vision model: {model_name}")
                
                llm = ChatGroq(
                    model=model_name,
                    temperature=0.2,
                    groq_api_key=groq_key,
                )
                
                message = HumanMessage(
                    content=[
                        {
                            "type": "text",
                            "text": _get_vision_prompt()
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{image_data}"
                            }
                        }
                    ]
                )
                
                response = llm.invoke([message])
                analysis_result = response.content
                print(f"✅ Successfully analyzed with {model_name}")
                break
                
            except Exception as e:
                error_msg = str(e)
                print(f"⚠️ Groq model {model_name} failed: {error_msg}")
                if "decommissioned" not in error_msg.lower():
                    # If it's not a decommissioned error, might be worth reporting
                    break
        
        # If Groq failed, try OpenAI (if available)
        if not analysis_result:
            try:
                from openai import OpenAI
                openai_key = os.getenv("OPENAI_API_KEY")
                
                if openai_key and openai_key != "your_openai_api_key_here":
                    print("🔍 Trying OpenAI vision model...")
                    client = OpenAI(api_key=openai_key)
                    
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",  # Cheaper vision model
                        messages=[
                            {
                                "role": "user",
                                "content": [
                                    {"type": "text", "text": _get_vision_prompt()},
                                    {
                                        "type": "image_url",
                                        "image_url": {
                                            "url": f"data:image/jpeg;base64,{image_data}"
                                        }
                                    }
                                ]
                            }
                        ],
                        max_tokens=1000
                    )
                    
                    analysis_result = response.choices[0].message.content
                    print("✅ Successfully analyzed with OpenAI")
                    
            except ImportError:
                print("⚠️ OpenAI library not installed")
            except Exception as e:
                print(f"⚠️ OpenAI vision failed: {e}")
        
        if analysis_result:
            return f"📸 **Image Analysis Results:**\n\n{analysis_result}"
        else:
            # All vision models failed, use text-based fallback
            return _fallback_text_analysis(image_path)
        
    except Exception as e:
        return f"⚠️ **Image Analysis Error**: {str(e)}\n\nPlease ensure the image is clear and in JPG/PNG format."


def _get_vision_prompt() -> str:
    """Get the vision analysis prompt"""
    return """You are an expert automotive mechanic specializing in both external damage and internal mechanical issues. Analyze this vehicle image thoroughly:

**EXTERNAL DAMAGE ANALYSIS:**
1. Body damage (dents, scratches, cracks, broken lights)
2. Tire condition (wear, punctures, pressure)
3. Glass damage (windshield, windows)

**ENGINE BAY / MECHANICAL ANALYSIS (if visible):**
1. **Fluid Leaks:**
   - Oil leaks (dark stains, wet spots on engine block)
   - Coolant leaks (green/orange fluid, radiator issues)
   - Brake fluid leaks (clear/brown fluid near brake components)
   - Power steering fluid leaks

2. **Component Condition:**
   - Battery terminals (corrosion, rust)
   - Belts (serpentine, timing) - cracks, fraying, wear
   - Hoses - cracks, bulges, deterioration
   - Air filter condition
   - Spark plug wires condition

3. **Corrosion & Rust:**
   - Engine block rust
   - Battery tray corrosion
   - Metal component oxidation

4. **Visible Wear:**
   - Worn gaskets
   - Loose connections
   - Missing components
   - Damaged wiring

**DIAGNOSIS:**
- Primary issue identified
- Severity: Minor/Moderate/Severe/Critical
- Immediate safety concerns
- Can vehicle be driven?

**REPAIR RECOMMENDATIONS:**
- Parts to replace (specific names)
- Estimated complexity (DIY/Professional)
- Kerala market cost estimate (INR)
- Urgency level

Be specific and practical for Kerala mechanics. If image shows engine bay, focus on mechanical issues. If external, focus on body damage."""


def _fallback_text_analysis(image_path: str) -> str:
    """
    Fallback analysis when vision models are unavailable
    Uses text-based model with generic automotive guidance
    """
    try:
        groq_key = os.getenv("GROQ_API_KEY")
        llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.2,
            groq_api_key=groq_key,
        )
        
        prompt = f"""An image of a vehicle has been uploaded for analysis (filename: {Path(image_path).name}).

Since I cannot directly view the image, I'll provide general guidance for common vehicle issues that can be identified visually:

**COMMON VISUAL INSPECTION POINTS:**

**External Damage:**
- Body dents, scratches, or paint damage
- Broken or cracked lights (headlights, taillights)
- Tire wear patterns or damage
- Windshield cracks or chips
- Rust or corrosion on body panels

**Engine Bay Issues (if visible):**
- Oil leaks (dark stains under engine)
- Coolant leaks (green/orange fluid)
- Worn or cracked belts
- Corroded battery terminals
- Damaged or loose hoses
- Dirty air filter
- Rust on metal components

**What to look for:**
1. Any fluid puddles or stains (indicates leaks)
2. Unusual wear patterns on tires
3. Visible cracks in rubber components
4. Corrosion or rust on metal parts
5. Loose or disconnected wires/hoses

**Recommended Actions:**
- Take the vehicle to a mechanic for proper inspection
- If you see fluid leaks, identify the color (oil=black, coolant=green/orange, brake fluid=clear)
- For body damage, get quotes from local Kerala body shops
- For mechanical issues, visit authorized service centers

**Kerala Service Centers:**
- Authorized dealers for warranty work
- Local trusted mechanics for routine repairs
- Body shops for cosmetic damage

For a detailed analysis, please describe what you see in the image, and I can provide specific guidance.

**Note:** Vision analysis is temporarily unavailable. For best results, describe the visible issues in your next message."""

        response = llm.invoke(prompt)
        return f"📸 **Image Analysis (Text-Based Fallback):**\n\n{response.content}\n\n💡 **Tip:** Describe what you see in the image for more specific guidance."
        
    except Exception as e:
        return f"⚠️ Image analysis unavailable. Please describe the visible issues in text for assistance."


def save_uploaded_image(file_data: bytes, filename: str) -> str:
    """
    Save uploaded image to disk
    
    Args:
        file_data: Binary image data
        filename: Original filename
    
    Returns:
        Path to saved file
    """
    # Create uploads directory
    upload_dir = Path("backend/uploads/images")
    upload_dir.mkdir(parents=True, exist_ok=True)
    
    # Generate unique filename
    import time
    timestamp = int(time.time())
    file_ext = Path(filename).suffix
    new_filename = f"vehicle_{timestamp}{file_ext}"
    
    file_path = upload_dir / new_filename
    
    # Save file
    with open(file_path, 'wb') as f:
        f.write(file_data)
    
    return str(file_path)
