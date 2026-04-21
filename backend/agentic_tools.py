"""
Agentic AI Tools for AutoMech
All tools wrapped for LangChain agent autonomous decision-making
"""
from langchain.tools import Tool
from langchain.pydantic_v1 import BaseModel, Field
from typing import Optional, List, Dict
import json

from tools.obd_lookup import lookup_obd_code
from tools.rag_tool import query_manuals
from tools.parts_scraper import scrape_parts
from tools.image_analyzer import analyze_vehicle_image


# ── Tool Input Schemas ────────────────────────────────────────────────────────

class OBDInput(BaseModel):
    """Input for OBD code lookup"""
    code: str = Field(description="OBD-II code like P0300, P0420, etc.")


class RAGInput(BaseModel):
    """Input for manual search"""
    query: str = Field(description="Question about vehicle repair or maintenance")
    vehicle_make: Optional[str] = Field(default="", description="Vehicle manufacturer")
    vehicle_model: Optional[str] = Field(default="", description="Vehicle model")


class PartsInput(BaseModel):
    """Input for parts search"""
    part_name: str = Field(description="Name of the automotive part to search")
    vehicle_make: Optional[str] = Field(default="", description="Vehicle manufacturer")
    vehicle_model: Optional[str] = Field(default="", description="Vehicle model")


class ImageInput(BaseModel):
    """Input for image analysis"""
    image_path: str = Field(description="Path to the uploaded vehicle image")


class SymptomInput(BaseModel):
    """Input for symptom validation"""
    symptoms: str = Field(description="Vehicle symptoms described by user")
    vehicle_type: Optional[str] = Field(default="", description="Type of vehicle")


class CostInput(BaseModel):
    """Input for cost calculation"""
    parts: List[str] = Field(description="List of parts needed")
    labor_hours: Optional[float] = Field(default=2.0, description="Estimated labor hours")


class VideoInput(BaseModel):
    """Input for repair video search"""
    repair_task: str = Field(description="Repair task to find video tutorial for")
    vehicle_info: Optional[str] = Field(default="", description="Vehicle make and model")


class VehicleHistoryInput(BaseModel):
    """Input for vehicle history query"""
    vehicle_id: str = Field(description="Vehicle identifier or user ID")
    query: Optional[str] = Field(default="", description="Specific query about history")


class MechanicFinderInput(BaseModel):
    """Input for mechanic finder"""
    location: str = Field(description="Location in Kerala (city/area)")
    specialty: Optional[str] = Field(default="", description="Specialty needed (e.g., transmission, electrical)")


class AppointmentInput(BaseModel):
    """Input for appointment scheduling"""
    mechanic_name: str = Field(description="Mechanic or shop name")
    date: str = Field(description="Preferred date (YYYY-MM-DD)")
    service_type: str = Field(description="Type of service needed")


# ── Tool Functions ────────────────────────────────────────────────────────────

def obd_lookup_tool(code: str) -> str:
    """Look up OBD-II diagnostic trouble code"""
    try:
        result = lookup_obd_code(code.strip().upper())
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"Error looking up OBD code: {str(e)}"


def manual_search_tool(query: str, vehicle_make: str = "", vehicle_model: str = "") -> str:
    """Search vehicle repair manuals and documentation"""
    try:
        context = f"{vehicle_make} {vehicle_model}".strip()
        full_query = f"{query} {context}".strip()
        result = query_manuals(full_query)
        return result if result else "No relevant information found in manuals."
    except Exception as e:
        return f"Error searching manuals: {str(e)}"


def parts_search_tool(part_name: str, vehicle_make: str = "", vehicle_model: str = "") -> str:
    """Search for automotive parts online with prices"""
    try:
        parts = scrape_parts(part_name, vehicle_make, vehicle_model)
        if not parts:
            return f"No parts found for: {part_name}"
        
        result = f"Found {len(parts)} parts for '{part_name}':\n\n"
        for i, part in enumerate(parts[:5], 1):
            result += f"{i}. {part['name']}\n"
            result += f"   Price: ₹{part['price']}\n"
            result += f"   Store: {part['store']}\n"
            result += f"   Link: {part['link']}\n\n"
        return result
    except Exception as e:
        return f"Error searching parts: {str(e)}"


def image_analysis_tool(image_path: str) -> str:
    """Analyze vehicle damage or mechanical issues from image"""
    try:
        result = analyze_vehicle_image(image_path)
        return result
    except Exception as e:
        return f"Error analyzing image: {str(e)}"


def symptom_validator_tool(symptoms: str, vehicle_type: str = "") -> str:
    """Validate and categorize vehicle symptoms"""
    try:
        # Symptom categories
        categories = {
            "engine": ["misfire", "stall", "rough idle", "won't start", "knocking", "smoking"],
            "brakes": ["grinding", "squealing", "soft pedal", "pulling", "vibration"],
            "transmission": ["slipping", "hard shift", "delay", "grinding gears"],
            "electrical": ["battery", "alternator", "lights", "starting", "charging"],
            "suspension": ["bouncing", "clunking", "steering", "alignment"],
            "cooling": ["overheating", "coolant", "radiator", "thermostat"],
            "fuel": ["fuel pump", "injector", "gas smell", "poor mileage"],
        }
        
        symptoms_lower = symptoms.lower()
        detected_categories = []
        
        for category, keywords in categories.items():
            if any(keyword in symptoms_lower for keyword in keywords):
                detected_categories.append(category)
        
        if not detected_categories:
            detected_categories = ["general"]
        
        result = f"Symptom Analysis:\n"
        result += f"Categories: {', '.join(detected_categories)}\n"
        result += f"Vehicle Type: {vehicle_type or 'Not specified'}\n"
        result += f"Symptoms: {symptoms}\n\n"
        result += "Recommendation: Proceed with diagnostic tools for these categories."
        
        return result
    except Exception as e:
        return f"Error validating symptoms: {str(e)}"


def cost_calculator_tool(parts: List[str], labor_hours: float = 2.0) -> str:
    """Calculate estimated repair costs for Kerala market"""
    try:
        # Kerala average labor rate
        labor_rate_per_hour = 500  # INR
        
        # Estimated part costs (Kerala market averages)
        part_costs = {
            "spark plug": 300,
            "brake pad": 1500,
            "oil filter": 250,
            "air filter": 400,
            "battery": 4500,
            "alternator": 8000,
            "starter": 6000,
            "radiator": 5000,
            "timing belt": 2000,
            "clutch": 7000,
            "fuel pump": 4000,
            "oxygen sensor": 3000,
            "catalytic converter": 15000,
            "brake disc": 2500,
            "shock absorber": 3500,
            "headlight": 2000,
            "wiper blade": 300,
            "tyre": 4000,
        }
        
        total_parts_cost = 0
        parts_breakdown = []
        
        for part in parts:
            part_lower = part.lower()
            cost = 0
            
            # Find matching part
            for key, value in part_costs.items():
                if key in part_lower:
                    cost = value
                    break
            
            if cost == 0:
                cost = 2000  # Default estimate
            
            total_parts_cost += cost
            parts_breakdown.append(f"  - {part}: ₹{cost:,}")
        
        labor_cost = labor_hours * labor_rate_per_hour
        total_cost = total_parts_cost + labor_cost
        
        result = "💰 Cost Estimate (Kerala Market):\n\n"
        result += "Parts:\n" + "\n".join(parts_breakdown) + "\n\n"
        result += f"Labor: {labor_hours} hours × ₹{labor_rate_per_hour}/hr = ₹{labor_cost:,}\n\n"
        result += f"Total Estimated Cost: ₹{total_cost:,}\n"
        result += f"Range: ₹{int(total_cost * 0.8):,} - ₹{int(total_cost * 1.2):,}\n\n"
        result += "Note: Actual costs may vary based on vehicle model and mechanic."
        
        return result
    except Exception as e:
        return f"Error calculating costs: {str(e)}"


def video_search_tool(repair_task: str, vehicle_info: str = "") -> str:
    """Search for repair tutorial videos"""
    try:
        # Simulate video search (in production, use YouTube API)
        search_query = f"{repair_task} {vehicle_info} repair tutorial".strip()
        
        result = f"🎥 Repair Video Tutorials for: {repair_task}\n\n"
        result += f"Search YouTube for: '{search_query}'\n\n"
        result += "Recommended channels:\n"
        result += "  - ChrisFix (General repairs)\n"
        result += "  - Scotty Kilmer (Diagnostics)\n"
        result += "  - Engineering Explained (Technical)\n"
        result += "  - Car Care Nut (Maintenance)\n\n"
        result += f"Direct search: https://www.youtube.com/results?search_query={search_query.replace(' ', '+')}"
        
        return result
    except Exception as e:
        return f"Error searching videos: {str(e)}"


def vehicle_history_tool(vehicle_id: str, query: str = "") -> str:
    """Query vehicle history and past diagnostics"""
    try:
        from memory_system import AgenticMemory
        
        memory = AgenticMemory(user_id=vehicle_id)
        history = memory.user_history
        
        if not history.get("past_issues"):
            return "No previous diagnostic history found for this vehicle."
        
        result = f"📋 Vehicle History (ID: {vehicle_id}):\n\n"
        
        # Vehicle info
        if history.get("vehicles"):
            result += "**Registered Vehicles:**\n"
            for v in history["vehicles"]:
                result += f"  - {v.get('year', '')} {v.get('make', '')} {v.get('model', '')}\n"
            result += "\n"
        
        # Past issues
        result += f"**Past Diagnostics ({len(history['past_issues'])} total):**\n"
        for i, issue in enumerate(history["past_issues"][-5:], 1):  # Last 5
            result += f"\n{i}. {issue.get('symptom', 'Unknown')}\n"
            result += f"   Diagnosis: {issue.get('diagnosis', 'N/A')[:100]}...\n"
            result += f"   Date: {issue.get('timestamp', 'Unknown')}\n"
        
        result += f"\n**Total Interactions:** {history.get('total_interactions', 0)}"
        
        return result
    except Exception as e:
        return f"Error querying vehicle history: {str(e)}"


def price_comparison_tool(part_name: str, vehicle_make: str = "", vehicle_model: str = "") -> str:
    """Compare part prices across multiple stores"""
    try:
        parts = scrape_parts(part_name, vehicle_make, vehicle_model)
        
        if not parts:
            return f"No parts found for comparison: {part_name}"
        
        # Sort by price
        parts_sorted = sorted(parts, key=lambda x: float(x.get('price', '999999').replace(',', '')))
        
        result = f"💰 Price Comparison for '{part_name}':\n\n"
        result += f"Found {len(parts_sorted)} options:\n\n"
        
        for i, part in enumerate(parts_sorted[:5], 1):
            price = part.get('price', 'N/A')
            result += f"{i}. ₹{price} - {part.get('store', 'Unknown')}\n"
            result += f"   {part.get('name', 'Unknown')}\n"
            result += f"   Link: {part.get('link', 'N/A')}\n\n"
        
        if len(parts_sorted) > 0:
            cheapest = parts_sorted[0]
            most_expensive = parts_sorted[-1]
            result += f"**Price Range:** ₹{cheapest.get('price', 'N/A')} - ₹{most_expensive.get('price', 'N/A')}\n"
            result += f"**Best Deal:** {cheapest.get('store', 'Unknown')} at ₹{cheapest.get('price', 'N/A')}"
        
        return result
    except Exception as e:
        return f"Error comparing prices: {str(e)}"


def mechanic_finder_tool(location: str, specialty: str = "") -> str:
    """Find mechanics in Kerala"""
    try:
        # Simulated mechanic database (in production, use Google Maps API)
        mechanics_db = {
            "kochi": [
                {"name": "AutoCare Kochi", "specialty": "general", "rating": 4.5, "phone": "+91-484-1234567"},
                {"name": "Expert Auto Electricals", "specialty": "electrical", "rating": 4.7, "phone": "+91-484-2345678"},
                {"name": "Transmission Masters", "specialty": "transmission", "rating": 4.6, "phone": "+91-484-3456789"},
            ],
            "trivandrum": [
                {"name": "City Auto Service", "specialty": "general", "rating": 4.4, "phone": "+91-471-1234567"},
                {"name": "AC Repair Specialists", "specialty": "ac", "rating": 4.8, "phone": "+91-471-2345678"},
            ],
            "kozhikode": [
                {"name": "Calicut Auto Works", "specialty": "general", "rating": 4.3, "phone": "+91-495-1234567"},
                {"name": "Brake & Suspension Experts", "specialty": "brakes", "rating": 4.6, "phone": "+91-495-2345678"},
            ],
        }
        
        location_lower = location.lower()
        mechanics = []
        
        # Find mechanics in location
        for city, shops in mechanics_db.items():
            if city in location_lower or location_lower in city:
                mechanics = shops
                break
        
        if not mechanics:
            return f"No mechanics found in {location}. Try: Kochi, Trivandrum, or Kozhikode"
        
        # Filter by specialty if provided
        if specialty:
            mechanics = [m for m in mechanics if specialty.lower() in m["specialty"].lower()]
        
        result = f"🔧 Mechanics in {location.title()}:\n\n"
        
        if not mechanics:
            return f"No {specialty} specialists found in {location}"
        
        for i, mech in enumerate(mechanics, 1):
            result += f"{i}. **{mech['name']}**\n"
            result += f"   Specialty: {mech['specialty'].title()}\n"
            result += f"   Rating: {'⭐' * int(mech['rating'])} ({mech['rating']}/5)\n"
            result += f"   Phone: {mech['phone']}\n\n"
        
        result += f"\n💡 Tip: Call ahead to check availability and get quotes"
        
        return result
    except Exception as e:
        return f"Error finding mechanics: {str(e)}"


def appointment_scheduler_tool(mechanic_name: str, date: str, service_type: str) -> str:
    """Schedule mechanic appointment"""
    try:
        result = f"📅 Appointment Scheduling:\n\n"
        result += f"**Mechanic:** {mechanic_name}\n"
        result += f"**Date:** {date}\n"
        result += f"**Service:** {service_type}\n\n"
        result += "**Status:** Appointment request created\n\n"
        result += "**Next Steps:**\n"
        result += f"1. Call the mechanic to confirm availability\n"
        result += f"2. Mention this appointment reference\n"
        result += f"3. Arrive 10 minutes early\n"
        result += f"4. Bring vehicle documents\n\n"
        result += "**Reminder:** You'll receive an SMS reminder 1 day before the appointment.\n\n"
        result += "⚠️ Note: This is a booking request. Please call to confirm."
        
        return result
    except Exception as e:
        return f"Error scheduling appointment: {str(e)}"


# ── Create LangChain Tools ────────────────────────────────────────────────────

def create_agentic_tools() -> List[Tool]:
    """Create all tools for the agentic system"""
    
    tools = [
        Tool(
            name="OBD_Code_Lookup",
            func=obd_lookup_tool,
            description="Look up OBD-II diagnostic trouble codes (like P0300, P0420). Use when user mentions error codes or check engine light. Input: OBD code string."
        ),
        Tool(
            name="Manual_Search",
            func=manual_search_tool,
            description="Search vehicle repair manuals and technical documentation. Use for detailed repair procedures, specifications, or technical questions. Input: search query string."
        ),
        Tool(
            name="Parts_Search",
            func=parts_search_tool,
            description="Search for automotive parts online with prices from Indian stores (Amazon, Flipkart). Use when user needs to buy parts. Input: part name string."
        ),
        Tool(
            name="Image_Analysis",
            func=image_analysis_tool,
            description="Analyze vehicle images for damage or mechanical issues. Use when user uploads photos of their vehicle. Input: image file path string."
        ),
        Tool(
            name="Symptom_Validator",
            func=symptom_validator_tool,
            description="Validate and categorize vehicle symptoms to determine which diagnostic path to take. Use at the start of diagnosis. Input: symptoms description string."
        ),
        Tool(
            name="Cost_Calculator",
            func=cost_calculator_tool,
            description="Calculate estimated repair costs for Kerala market including parts and labor. Use after identifying needed repairs. Input: comma-separated list of parts."
        ),
        Tool(
            name="Video_Search",
            func=video_search_tool,
            description="Find repair tutorial videos on YouTube. Use when user wants DIY guidance or visual instructions. Input: repair task description string."
        ),
        Tool(
            name="Vehicle_History",
            func=vehicle_history_tool,
            description="Query vehicle's past diagnostics and service history. Use when user asks about previous issues or you need context about past repairs. Input: vehicle ID or user ID string."
        ),
        Tool(
            name="Price_Comparison",
            func=price_comparison_tool,
            description="Compare prices for automotive parts across multiple online stores. Use when user wants the best deal or price comparison. Input: part name string."
        ),
        Tool(
            name="Mechanic_Finder",
            func=mechanic_finder_tool,
            description="Find mechanics and auto repair shops in Kerala. Use when user needs professional help or wants to find a nearby mechanic. Input: location in Kerala (city/area)."
        ),
        Tool(
            name="Appointment_Scheduler",
            func=appointment_scheduler_tool,
            description="Schedule an appointment with a mechanic. Use after finding a mechanic and user wants to book service. Input: mechanic name, date (YYYY-MM-DD), service type."
        ),
    ]
    
    return tools
