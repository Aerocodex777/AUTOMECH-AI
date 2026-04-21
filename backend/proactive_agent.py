"""
Proactive Agent Capabilities
Predictive maintenance, reminders, and proactive suggestions
"""
from typing import Dict, List, Optional
from datetime import datetime, timedelta
import json
from pathlib import Path


class ProactiveAgent:
    """Agent that proactively suggests maintenance and predicts issues"""
    
    def __init__(self):
        self.maintenance_schedules = self._load_maintenance_schedules()
        self.predictions_file = Path("backend/memory/predictions.json")
        self.predictions = self._load_predictions()
    
    def _load_maintenance_schedules(self) -> Dict:
        """Load standard maintenance schedules"""
        return {
            "oil_change": {
                "interval_km": 5000,
                "interval_months": 6,
                "description": "Engine oil and filter change",
                "cost_range": (1500, 3000)
            },
            "brake_pads": {
                "interval_km": 40000,
                "interval_months": 24,
                "description": "Brake pad inspection/replacement",
                "cost_range": (2000, 4000)
            },
            "timing_belt": {
                "interval_km": 60000,
                "interval_months": 48,
                "description": "Timing belt replacement",
                "cost_range": (3000, 6000)
            },
            "coolant_flush": {
                "interval_km": 40000,
                "interval_months": 24,
                "description": "Coolant system flush",
                "cost_range": (1000, 2000)
            },
            "air_filter": {
                "interval_km": 15000,
                "interval_months": 12,
                "description": "Air filter replacement",
                "cost_range": (300, 600)
            },
            "spark_plugs": {
                "interval_km": 30000,
                "interval_months": 24,
                "description": "Spark plug replacement",
                "cost_range": (1200, 2400)
            },
            "battery": {
                "interval_km": 0,
                "interval_months": 36,
                "description": "Battery replacement",
                "cost_range": (3500, 6000)
            },
            "tires": {
                "interval_km": 50000,
                "interval_months": 48,
                "description": "Tire replacement",
                "cost_range": (12000, 20000)
            }
        }
    
    def _load_predictions(self) -> Dict:
        """Load saved predictions"""
        if self.predictions_file.exists():
            with open(self.predictions_file, 'r') as f:
                return json.load(f)
        return {}
    
    def save_predictions(self):
        """Save predictions to disk"""
        self.predictions_file.parent.mkdir(exist_ok=True)
        with open(self.predictions_file, 'w') as f:
            json.dump(self.predictions, f, indent=2)
    
    def predict_maintenance(self, vehicle_info: Dict) -> List[Dict]:
        """
        Predict upcoming maintenance based on vehicle info
        
        Args:
            vehicle_info: {
                "mileage": 45000,
                "last_service_date": "2024-01-15",
                "last_service_mileage": 40000,
                "year": 2020
            }
        
        Returns:
            List of upcoming maintenance items
        """
        predictions = []
        current_mileage = vehicle_info.get("mileage", 0)
        last_service_mileage = vehicle_info.get("last_service_mileage", 0)
        vehicle_age_months = self._calculate_vehicle_age(vehicle_info.get("year", 2020))
        
        for service, schedule in self.maintenance_schedules.items():
            # Check mileage-based
            if schedule["interval_km"] > 0:
                km_since_service = current_mileage - last_service_mileage
                km_until_due = schedule["interval_km"] - km_since_service
                
                if km_until_due <= 5000 and km_until_due > 0:
                    urgency = "soon" if km_until_due <= 2000 else "upcoming"
                    predictions.append({
                        "service": service,
                        "description": schedule["description"],
                        "due_in_km": km_until_due,
                        "urgency": urgency,
                        "cost_range": schedule["cost_range"],
                        "reason": f"Due at {schedule['interval_km']:,} km"
                    })
                elif km_until_due <= 0:
                    predictions.append({
                        "service": service,
                        "description": schedule["description"],
                        "due_in_km": 0,
                        "urgency": "overdue",
                        "cost_range": schedule["cost_range"],
                        "reason": f"Overdue by {abs(km_until_due):,} km"
                    })
            
            # Check time-based (battery)
            if schedule["interval_months"] > 0 and schedule["interval_km"] == 0:
                if vehicle_age_months >= schedule["interval_months"]:
                    predictions.append({
                        "service": service,
                        "description": schedule["description"],
                        "due_in_km": 0,
                        "urgency": "due",
                        "cost_range": schedule["cost_range"],
                        "reason": f"Due after {schedule['interval_months']} months"
                    })
        
        # Sort by urgency
        urgency_order = {"overdue": 0, "due": 1, "soon": 2, "upcoming": 3}
        predictions.sort(key=lambda x: urgency_order.get(x["urgency"], 4))
        
        return predictions
    
    def _calculate_vehicle_age(self, year: int) -> int:
        """Calculate vehicle age in months"""
        current_year = datetime.now().year
        current_month = datetime.now().month
        return (current_year - year) * 12 + current_month
    
    def predict_issues_from_symptoms(self, symptoms: str, vehicle_info: Dict) -> List[Dict]:
        """
        Predict potential future issues based on current symptoms
        
        Args:
            symptoms: Current symptoms
            vehicle_info: Vehicle information
        
        Returns:
            List of potential future issues
        """
        predictions = []
        symptoms_lower = symptoms.lower()
        
        # Pattern matching for predictive analysis
        patterns = {
            "rough idle": {
                "future_issues": ["spark plug failure", "ignition coil failure"],
                "timeframe": "1-3 months",
                "prevention": "Replace spark plugs and check ignition system"
            },
            "squealing brakes": {
                "future_issues": ["brake disc damage", "complete brake failure"],
                "timeframe": "2-4 weeks",
                "prevention": "Replace brake pads immediately"
            },
            "overheating": {
                "future_issues": ["head gasket failure", "engine damage"],
                "timeframe": "immediate",
                "prevention": "Stop driving, check coolant, inspect radiator"
            },
            "oil leak": {
                "future_issues": ["engine seizure", "bearing damage"],
                "timeframe": "1-2 months",
                "prevention": "Fix leak, monitor oil level regularly"
            },
            "transmission slip": {
                "future_issues": ["complete transmission failure"],
                "timeframe": "2-6 weeks",
                "prevention": "Check transmission fluid, avoid heavy loads"
            },
            "battery warning": {
                "future_issues": ["alternator failure", "electrical system damage"],
                "timeframe": "1-2 weeks",
                "prevention": "Test battery and alternator immediately"
            }
        }
        
        for pattern, prediction in patterns.items():
            if pattern in symptoms_lower:
                predictions.append({
                    "current_symptom": pattern,
                    "future_issues": prediction["future_issues"],
                    "timeframe": prediction["timeframe"],
                    "prevention": prediction["prevention"],
                    "severity": "high" if prediction["timeframe"] == "immediate" else "medium"
                })
        
        return predictions
    
    def generate_proactive_message(self, vehicle_info: Dict) -> str:
        """
        Generate proactive maintenance message
        
        Args:
            vehicle_info: Vehicle information
        
        Returns:
            Proactive message string
        """
        maintenance = self.predict_maintenance(vehicle_info)
        
        if not maintenance:
            return "✅ Your vehicle is up to date with maintenance!"
        
        message = "🔔 **Proactive Maintenance Alerts**\n\n"
        
        # Group by urgency
        overdue = [m for m in maintenance if m["urgency"] == "overdue"]
        due = [m for m in maintenance if m["urgency"] == "due"]
        soon = [m for m in maintenance if m["urgency"] == "soon"]
        upcoming = [m for m in maintenance if m["urgency"] == "upcoming"]
        
        if overdue:
            message += "⚠️ **OVERDUE:**\n"
            for item in overdue:
                cost_min, cost_max = item["cost_range"]
                message += f"  • {item['description']} - {item['reason']}\n"
                message += f"    Cost: ₹{cost_min:,} - ₹{cost_max:,}\n"
            message += "\n"
        
        if due:
            message += "🔴 **DUE NOW:**\n"
            for item in due:
                cost_min, cost_max = item["cost_range"]
                message += f"  • {item['description']} - {item['reason']}\n"
                message += f"    Cost: ₹{cost_min:,} - ₹{cost_max:,}\n"
            message += "\n"
        
        if soon:
            message += "🟡 **DUE SOON:**\n"
            for item in soon:
                cost_min, cost_max = item["cost_range"]
                message += f"  • {item['description']} - In {item['due_in_km']:,} km\n"
                message += f"    Cost: ₹{cost_min:,} - ₹{cost_max:,}\n"
            message += "\n"
        
        if upcoming:
            message += "🟢 **UPCOMING:**\n"
            for item in upcoming:
                cost_min, cost_max = item["cost_range"]
                message += f"  • {item['description']} - In {item['due_in_km']:,} km\n"
                message += f"    Cost: ₹{cost_min:,} - ₹{cost_max:,}\n"
        
        return message


class SeasonalAdvisor:
    """Provides seasonal maintenance advice for Kerala climate"""
    
    def __init__(self):
        self.seasons = {
            "monsoon": {
                "months": [6, 7, 8, 9],  # June-September
                "advice": [
                    "Check wiper blades and replace if worn",
                    "Inspect tire tread depth (minimum 3mm for wet roads)",
                    "Test brake performance (wet braking distance increases)",
                    "Check all lights and indicators",
                    "Inspect door seals for water leaks",
                    "Apply anti-rust coating to undercarriage",
                    "Check battery terminals for corrosion"
                ],
                "common_issues": [
                    "Brake fade due to water",
                    "Electrical issues from moisture",
                    "Rust formation",
                    "Reduced visibility"
                ]
            },
            "summer": {
                "months": [3, 4, 5],  # March-May
                "advice": [
                    "Check coolant level and condition",
                    "Inspect AC system performance",
                    "Check tire pressure (increases in heat)",
                    "Test battery (heat reduces lifespan)",
                    "Inspect radiator for leaks",
                    "Check engine oil level more frequently"
                ],
                "common_issues": [
                    "Overheating",
                    "AC failure",
                    "Battery failure",
                    "Tire blowouts"
                ]
            },
            "winter": {
                "months": [12, 1, 2],  # December-February
                "advice": [
                    "Check battery charge (cold affects performance)",
                    "Inspect heating system",
                    "Check tire pressure (decreases in cold)",
                    "Test all lights (shorter days)"
                ],
                "common_issues": [
                    "Hard starting",
                    "Reduced battery performance"
                ]
            }
        }
    
    def get_seasonal_advice(self) -> Dict:
        """Get advice for current season"""
        current_month = datetime.now().month
        
        for season, data in self.seasons.items():
            if current_month in data["months"]:
                return {
                    "season": season,
                    "advice": data["advice"],
                    "common_issues": data["common_issues"]
                }
        
        return {
            "season": "general",
            "advice": ["Regular maintenance as per schedule"],
            "common_issues": []
        }
    
    def format_seasonal_message(self) -> str:
        """Format seasonal advice message"""
        advice = self.get_seasonal_advice()
        season = advice["season"].title()
        
        message = f"🌦️ **{season} Maintenance Tips for Kerala**\n\n"
        
        message += "**Recommended Checks:**\n"
        for tip in advice["advice"]:
            message += f"  • {tip}\n"
        
        if advice["common_issues"]:
            message += f"\n**Common {season} Issues:**\n"
            for issue in advice["common_issues"]:
                message += f"  • {issue}\n"
        
        return message
