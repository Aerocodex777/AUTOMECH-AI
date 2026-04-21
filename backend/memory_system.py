"""
Memory System for Agentic AI
Handles conversation memory, user history, and learning
"""
from langchain.memory import ConversationBufferMemory, ConversationSummaryMemory
from langchain_groq import ChatGroq
from typing import Dict, List, Optional
import json
import os
from datetime import datetime
from pathlib import Path


class AgenticMemory:
    """Multi-layered memory system for the agent"""
    
    def __init__(self, user_id: Optional[str] = None, llm=None):
        self.user_id = user_id or "default"
        self.llm = llm
        
        # Short-term memory (current conversation)
        self.conversation_memory = ConversationBufferMemory(
            memory_key="chat_history",
            return_messages=True,
            output_key="output"
        )
        
        # Long-term memory storage
        self.memory_dir = Path("backend/memory")
        self.memory_dir.mkdir(exist_ok=True)
        self.user_memory_file = self.memory_dir / f"{self.user_id}_history.json"
        
        # Load user history
        self.user_history = self._load_user_history()
    
    def _load_user_history(self) -> Dict:
        """Load user's historical data"""
        if self.user_memory_file.exists():
            with open(self.user_memory_file, 'r') as f:
                return json.load(f)
        return {
            "vehicles": [],
            "past_issues": [],
            "preferences": {},
            "total_interactions": 0,
            "last_interaction": None
        }
    
    def save_user_history(self):
        """Save user history to disk"""
        with open(self.user_memory_file, 'w') as f:
            json.dump(self.user_history, f, indent=2)
    
    def add_vehicle(self, vehicle_info: Dict):
        """Remember user's vehicle"""
        if vehicle_info not in self.user_history["vehicles"]:
            self.user_history["vehicles"].append(vehicle_info)
            self.save_user_history()
    
    def add_issue(self, issue: Dict):
        """Remember past diagnostic issue"""
        issue["timestamp"] = datetime.now().isoformat()
        self.user_history["past_issues"].append(issue)
        self.user_history["total_interactions"] += 1
        self.user_history["last_interaction"] = datetime.now().isoformat()
        self.save_user_history()
    
    def get_context(self) -> str:
        """Get relevant context for the agent"""
        context = []
        
        # Vehicle context
        if self.user_history["vehicles"]:
            vehicles = ", ".join([f"{v.get('year', '')} {v.get('make', '')} {v.get('model', '')}" 
                                 for v in self.user_history["vehicles"]])
            context.append(f"User's vehicles: {vehicles}")
        
        # Recent issues
        if self.user_history["past_issues"]:
            recent = self.user_history["past_issues"][-3:]  # Last 3 issues
            issues_text = "\n".join([f"- {i.get('symptom', 'Unknown')}: {i.get('diagnosis', 'N/A')}" 
                                    for i in recent])
            context.append(f"Recent issues:\n{issues_text}")
        
        # Interaction count
        if self.user_history["total_interactions"] > 0:
            context.append(f"Total interactions: {self.user_history['total_interactions']}")
        
        return "\n\n".join(context) if context else "New user - no history"
    
    def get_conversation_history(self) -> str:
        """Get current conversation history"""
        return self.conversation_memory.load_memory_variables({}).get("chat_history", "")
    
    def clear_conversation(self):
        """Clear current conversation memory"""
        self.conversation_memory.clear()


class LearningSystem:
    """System for agent to learn from interactions"""
    
    def __init__(self):
        self.knowledge_file = Path("backend/memory/learned_knowledge.json")
        self.knowledge = self._load_knowledge()
    
    def _load_knowledge(self) -> Dict:
        """Load learned knowledge"""
        if self.knowledge_file.exists():
            with open(self.knowledge_file, 'r') as f:
                return json.load(f)
        return {
            "common_issues": {},
            "successful_diagnoses": [],
            "tool_effectiveness": {},
            "kerala_specific": {}
        }
    
    def save_knowledge(self):
        """Save learned knowledge"""
        self.knowledge_file.parent.mkdir(exist_ok=True)
        with open(self.knowledge_file, 'w') as f:
            json.dump(self.knowledge, f, indent=2)
    
    def record_diagnosis(self, symptom: str, diagnosis: str, tools_used: List[str], success: bool):
        """Record a diagnosis for learning"""
        if success:
            self.knowledge["successful_diagnoses"].append({
                "symptom": symptom,
                "diagnosis": diagnosis,
                "tools_used": tools_used,
                "timestamp": datetime.now().isoformat()
            })
        
        # Track tool effectiveness
        for tool in tools_used:
            if tool not in self.knowledge["tool_effectiveness"]:
                self.knowledge["tool_effectiveness"][tool] = {"uses": 0, "successes": 0}
            self.knowledge["tool_effectiveness"][tool]["uses"] += 1
            if success:
                self.knowledge["tool_effectiveness"][tool]["successes"] += 1
        
        self.save_knowledge()
    
    def get_similar_cases(self, symptom: str, limit: int = 3) -> List[Dict]:
        """Find similar past cases"""
        similar = []
        symptom_lower = symptom.lower()
        
        for case in self.knowledge["successful_diagnoses"]:
            case_symptom = case["symptom"].lower()
            # Simple similarity check (can be improved with embeddings)
            common_words = set(symptom_lower.split()) & set(case_symptom.split())
            if len(common_words) >= 2:
                similar.append(case)
        
        return similar[-limit:]  # Return most recent similar cases
    
    def get_tool_recommendations(self) -> List[str]:
        """Get most effective tools"""
        effectiveness = []
        for tool, stats in self.knowledge["tool_effectiveness"].items():
            if stats["uses"] > 0:
                success_rate = stats["successes"] / stats["uses"]
                effectiveness.append((tool, success_rate, stats["uses"]))
        
        # Sort by success rate and usage
        effectiveness.sort(key=lambda x: (x[1], x[2]), reverse=True)
        return [tool for tool, _, _ in effectiveness[:5]]
