"""
Multi-Agent System for AutoMech
Specialized agents for different tasks coordinated by master agent
"""
from langchain.agents import AgentExecutor, create_react_agent
from langchain_groq import ChatGroq
from langchain.prompts import PromptTemplate
from typing import Dict, List, Optional
import os
from dotenv import load_dotenv

from agentic_tools import create_agentic_tools

load_dotenv()


class SpecializedAgent:
    """Base class for specialized agents"""
    
    def __init__(self, name: str, role: str, tools: List, llm):
        self.name = name
        self.role = role
        self.tools = tools
        self.llm = llm
        self.agent = self._create_agent()
    
    def _create_agent(self):
        """Create the agent with ReAct framework"""
        prompt = PromptTemplate.from_template(
            """You are {role}.

You have access to the following tools:
{tools}

Tool Names: {tool_names}

Use this format:

Question: the input question you must answer
Thought: think about what to do
Action: the action to take, must be one of [{tool_names}]
Action Input: the input to the action
Observation: the result of the action
... (repeat Thought/Action/Action Input/Observation as needed)
Thought: I now know the final answer
Final Answer: the final answer to the original question

Begin!

Question: {input}
Thought: {agent_scratchpad}"""
        )
        
        agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt.partial(role=self.role)
        )
        
        return AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
            max_iterations=5,
            handle_parsing_errors=True
        )
    
    def run(self, task: str) -> str:
        """Execute the agent's task"""
        try:
            result = self.agent.invoke({"input": task})
            return result.get("output", "No output generated")
        except Exception as e:
            return f"Agent {self.name} error: {str(e)}"


class MultiAgentSystem:
    """Coordinates multiple specialized agents"""
    
    def __init__(self, groq_api_key: str):
        self.llm = ChatGroq(
            model="llama-3.3-70b-versatile",
            temperature=0.2,
            groq_api_key=groq_api_key
        )
        
        # Create all tools
        all_tools = create_agentic_tools()
        
        # Create specialized agents
        self.agents = self._create_specialized_agents(all_tools)
        
        # Master coordinator
        self.master_agent = self._create_master_agent()
    
    def _create_specialized_agents(self, all_tools: List) -> Dict[str, SpecializedAgent]:
        """Create all specialized agents"""
        
        # Filter tools for each agent
        diagnostic_tools = [t for t in all_tools if t.name in 
                          ["OBD_Code_Lookup", "Manual_Search", "Symptom_Validator"]]
        
        parts_tools = [t for t in all_tools if t.name in 
                      ["Parts_Search", "Cost_Calculator"]]
        
        vision_tools = [t for t in all_tools if t.name in 
                       ["Image_Analysis"]]
        
        teaching_tools = [t for t in all_tools if t.name in 
                         ["Video_Search", "Manual_Search"]]
        
        agents = {
            "diagnostic": SpecializedAgent(
                name="Diagnostic Agent",
                role="an expert automotive diagnostic specialist who identifies vehicle problems using OBD codes, symptoms, and technical manuals",
                tools=diagnostic_tools,
                llm=self.llm
            ),
            "parts": SpecializedAgent(
                name="Parts Agent",
                role="an automotive parts specialist who finds the best parts and calculates repair costs for Kerala market",
                tools=parts_tools,
                llm=self.llm
            ),
            "vision": SpecializedAgent(
                name="Vision Agent",
                role="a vehicle damage assessment expert who analyzes images to identify external damage and internal mechanical issues",
                tools=vision_tools,
                llm=self.llm
            ),
            "teaching": SpecializedAgent(
                name="Teaching Agent",
                role="a DIY repair instructor who provides step-by-step guidance and finds tutorial videos for vehicle repairs",
                tools=teaching_tools,
                llm=self.llm
            ),
        }
        
        return agents
    
    def _create_master_agent(self):
        """Create master coordinator agent"""
        # Master agent doesn't use tools directly, it delegates
        return None
    
    def route_task(self, user_input: str, context: Dict = None) -> Dict:
        """Route task to appropriate specialized agent(s)"""
        
        # Analyze user input to determine which agents to use
        user_lower = user_input.lower()
        
        results = {
            "agents_used": [],
            "outputs": {},
            "final_response": ""
        }
        
        # Determine which agents to activate
        agents_to_use = []
        
        # Check for OBD codes or diagnostic keywords
        if any(word in user_lower for word in ["p0", "code", "check engine", "diagnostic", "symptom", "problem", "issue"]):
            agents_to_use.append("diagnostic")
        
        # Check for parts/cost keywords
        if any(word in user_lower for word in ["part", "buy", "price", "cost", "how much", "estimate"]):
            agents_to_use.append("parts")
        
        # Check for image analysis
        if context and context.get("has_image"):
            agents_to_use.append("vision")
        
        # Check for DIY/tutorial requests
        if any(word in user_lower for word in ["how to", "diy", "tutorial", "video", "guide", "teach", "show me"]):
            agents_to_use.append("teaching")
        
        # Default to diagnostic if nothing specific
        if not agents_to_use:
            agents_to_use.append("diagnostic")
        
        # Execute agents in sequence
        for agent_name in agents_to_use:
            agent = self.agents.get(agent_name)
            if agent:
                print(f"\n🤖 Activating {agent.name}...")
                output = agent.run(user_input)
                results["agents_used"].append(agent_name)
                results["outputs"][agent_name] = output
        
        # Combine outputs
        results["final_response"] = self._combine_outputs(results["outputs"])
        
        return results
    
    def _combine_outputs(self, outputs: Dict[str, str]) -> str:
        """Combine outputs from multiple agents into coherent response"""
        if not outputs:
            return "No response generated."
        
        combined = "🔧 **AutoMech AI Analysis**\n\n"
        
        # Order of presentation
        order = ["diagnostic", "vision", "parts", "teaching"]
        
        for agent_name in order:
            if agent_name in outputs:
                output = outputs[agent_name]
                
                # Add section headers
                headers = {
                    "diagnostic": "📊 Diagnostic Analysis",
                    "vision": "📸 Image Analysis",
                    "parts": "🛒 Parts & Cost Information",
                    "teaching": "🎓 DIY Guidance"
                }
                
                combined += f"\n### {headers.get(agent_name, agent_name.title())}\n"
                combined += f"{output}\n\n"
                combined += "---\n"
        
        return combined.strip()
    
    def run(self, user_input: str, context: Dict = None) -> str:
        """Main entry point for multi-agent system"""
        results = self.route_task(user_input, context or {})
        return results["final_response"]
