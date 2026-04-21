"""
Main Agentic AI Agent with ReAct Framework
Autonomous decision-making, planning, and self-correction
"""
from langchain.agents import AgentExecutor, create_react_agent
from langchain_groq import ChatGroq
from langchain_community.chat_models import ChatOllama
from langchain.prompts import PromptTemplate
from typing import Dict, Optional, List
import os
import time
from dotenv import load_dotenv

from agentic_tools import create_agentic_tools
from memory_system import AgenticMemory, LearningSystem
from multi_agent_system import MultiAgentSystem

load_dotenv()


def check_ollama_available(timeout: int = 2) -> bool:
    """Check if Ollama is available"""
    try:
        import requests
        response = requests.get("http://localhost:11434/api/tags", timeout=timeout)
        return response.status_code == 200
    except:
        return False


class AgenticAutoMech:
    """
    Main Agentic AI Agent for AutoMech
    Features:
    - ReAct (Reasoning + Acting) framework
    - Autonomous tool selection
    - Multi-agent coordination
    - Memory and learning
    - Self-correction
    - Planning and reasoning
    """
    
    def __init__(self, user_id: Optional[str] = None, use_multi_agent: bool = True):
        self.user_id = user_id
        self.use_multi_agent = use_multi_agent
        
        # Initialize LLM with fallback
        self.llm = self._initialize_llm()
        
        # Initialize memory system
        self.memory = AgenticMemory(user_id=user_id, llm=self.llm)
        
        # Initialize learning system
        self.learning = LearningSystem()
        
        # Create tools
        self.tools = create_agentic_tools()
        
        # Initialize multi-agent system if enabled
        self.multi_agent = None
        if use_multi_agent:
            try:
                groq_key = os.getenv("GROQ_API_KEY")
                if groq_key and groq_key != "your_groq_api_key_here":
                    self.multi_agent = MultiAgentSystem(groq_key)
                    print("✅ Multi-agent system initialized")
            except Exception as e:
                print(f"⚠️ Multi-agent system disabled: {e}")
        
        # Create main agent
        self.agent = self._create_agent()
        
        print(f"✅ Agentic AI initialized with {len(self.tools)} tools")
    
    def _initialize_llm(self):
        """Initialize LLM with Ollama → Groq fallback (production-ready)"""
        
        # Check if we should prefer cloud (useful for hosting)
        prefer_cloud = os.getenv("PREFER_CLOUD_LLM", "false").lower() == "true"
        
        if prefer_cloud:
            print("☁️ Cloud LLM preferred (PREFER_CLOUD_LLM=true)")
            return self._initialize_groq()
        
        # Try Ollama first (for local development)
        if check_ollama_available():
            try:
                llm = ChatOllama(
                    model="llama3",
                    temperature=0.2,
                    base_url="http://localhost:11434"
                )
                # Test the connection
                llm.invoke("test")
                print("🏠 Using local Ollama (llama3)")
                return llm
            except Exception as e:
                print(f"⚠️ Ollama connection failed: {e}")
                print("⚠️ Falling back to Groq API...")
        else:
            print("ℹ️ Ollama not available, using cloud API")
        
        # Fallback to Groq (always works when hosted)
        return self._initialize_groq()
    
    def _initialize_groq(self):
        """Initialize Groq API (cloud fallback)"""
        groq_key = os.getenv("GROQ_API_KEY")
        
        if not groq_key or groq_key == "your_groq_api_key_here":
            raise ValueError(
                "❌ GROQ_API_KEY not configured!\n"
                "Please set GROQ_API_KEY in backend/.env\n"
                "Get your free API key from: https://console.groq.com/keys"
            )
        
        try:
            llm = ChatGroq(
                model="llama-3.3-70b-versatile",
                temperature=0.2,
                groq_api_key=groq_key,
                max_retries=3
            )
            print("🌐 Using Groq API (llama-3.3-70b-versatile)")
            return llm
        except Exception as e:
            raise ValueError(
                f"❌ Failed to initialize Groq API: {e}\n"
                "Please check your GROQ_API_KEY in backend/.env"
            )
    
    def _create_agent(self) -> AgentExecutor:
        """Create ReAct agent with enhanced reasoning"""
        
        prompt = PromptTemplate.from_template(
            """You are AutoMech AI, an expert automotive diagnostic agent for Kerala, India.

You are autonomous and intelligent. You can:
- Reason about vehicle problems
- Decide which tools to use
- Execute tools in the right sequence
- Validate your findings
- Provide comprehensive solutions

AVAILABLE TOOLS:
{tools}

TOOL NAMES: {tool_names}

USER CONTEXT:
{user_context}

SIMILAR PAST CASES:
{similar_cases}

INSTRUCTIONS:
1. Analyze the user's question carefully
2. Break down complex problems into steps
3. Use tools strategically (don't use all tools unnecessarily)
4. Validate your findings before concluding
5. Provide practical solutions for Kerala mechanics
6. Include cost estimates in INR
7. Suggest both DIY and professional repair options

FORMAT:
Question: the input question
Thought: analyze what information you need
Action: choose the best tool to use
Action Input: provide the input for the tool
Observation: see the tool's result
... (repeat Thought/Action/Action Input/Observation as needed)
Thought: validate findings and check if more information is needed
Final Answer: provide comprehensive answer with diagnosis, parts, costs, and recommendations

IMPORTANT:
- For OBD codes: Use OBD_Code_Lookup first
- For symptoms: Use Symptom_Validator to categorize, then appropriate diagnostic tools
- For parts: Use Parts_Search and Cost_Calculator
- For images: Use Image_Analysis
- For DIY help: Use Video_Search
- Always provide Kerala market pricing
- Be specific and actionable

Begin!

Question: {input}
{agent_scratchpad}"""
        )
        
        # Get user context
        user_context = self.memory.get_context()
        
        # Get similar cases for learning
        similar_cases = "None yet"
        
        agent = create_react_agent(
            llm=self.llm,
            tools=self.tools,
            prompt=prompt.partial(
                user_context=user_context,
                similar_cases=similar_cases
            )
        )
        
        return AgentExecutor(
            agent=agent,
            tools=self.tools,
            verbose=True,
            max_iterations=10,
            handle_parsing_errors=True,
            return_intermediate_steps=True
        )
    
    def diagnose(self, user_input: str, context: Dict = None) -> Dict:
        """
        Main diagnostic function with agentic reasoning
        
        Args:
            user_input: User's question or symptom description
            context: Additional context (vehicle info, images, chat_history, etc.)
        
        Returns:
            Dict with diagnosis, reasoning steps, and recommendations
        """
        start_time = time.time()
        context = context or {}
        
        print(f"\n{'='*60}")
        print(f"🤖 AGENTIC AI PROCESSING")
        print(f"{'='*60}")
        print(f"Input: {user_input}")
        print(f"Context: {context}")
        print(f"{'='*60}\n")
        
        # Format chat history if available
        chat_history_text = ""
        if context.get("chat_history"):
            chat_history_text = "\n\nPrevious conversation:\n"
            for msg in context["chat_history"]:
                role = "User" if msg["role"] == "user" else "Assistant"
                chat_history_text += f"{role}: {msg['content']}\n"
            print(f"💬 Using {len(context['chat_history'])} previous messages for context")
        
        # Check for Malayalam language
        detected_lang = context.get("language", "en")
        language_instruction = ""
        if detected_lang == "ml":
            language_instruction = """
**IMPORTANT: User is asking in Malayalam. Respond in Malayalam (മലയാളം) language.**

Guidelines:
- Write your entire response in Malayalam script
- Use Malayalam for diagnosis, recommendations, and explanations
- Include part names in Malayalam with English in brackets: ബാറ്ററി (Battery)
- Use Indian Rupees (₹) for all costs
- Provide Kerala-specific context and recommendations
- Be conversational and friendly in Malayalam

"""
            print("🇮🇳 Responding in Malayalam")
        
        # Check if multi-agent system should handle this
        if self.multi_agent and self._should_use_multi_agent(user_input, context):
            print("🔀 Routing to multi-agent system...")
            response = self.multi_agent.run(user_input, context)
            tools_used = ["multi_agent_system"]
        else:
            # Use main ReAct agent
            print("🧠 Using main ReAct agent...")
            
            # Get similar cases for context
            similar = self.learning.get_similar_cases(user_input)
            if similar:
                similar_text = "\n".join([f"- {c['symptom']}: {c['diagnosis']}" for c in similar])
                print(f"\n📚 Found {len(similar)} similar past cases")
            else:
                similar_text = "No similar cases found"
            
            # Build enhanced input with chat history and language instruction
            enhanced_input = user_input
            if language_instruction:
                enhanced_input = language_instruction + enhanced_input
            if chat_history_text:
                enhanced_input = f"{chat_history_text}\n\nCurrent question: {enhanced_input}"
            
            # Run agent
            try:
                result = self.agent.invoke({
                    "input": enhanced_input,
                    "similar_cases": similar_text
                })
                
                response = result.get("output", "No diagnosis generated")
                intermediate_steps = result.get("intermediate_steps", [])
                
                # Extract tools used
                tools_used = [step[0].tool for step in intermediate_steps if hasattr(step[0], 'tool')]
                
            except Exception as e:
                response = f"⚠️ Agent error: {str(e)}\n\nFalling back to basic diagnosis..."
                tools_used = []
                # Fallback to simple response
                response += f"\n\nBased on your input: {user_input}\n"
                response += "Please provide more details or try rephrasing your question."
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Record in memory
        self.memory.add_issue({
            "symptom": user_input,
            "diagnosis": response,
            "tools_used": tools_used,
            "processing_time": processing_time
        })
        
        # Record in learning system
        self.learning.record_diagnosis(
            symptom=user_input,
            diagnosis=response,
            tools_used=tools_used,
            success=True  # Can be improved with user feedback
        )
        
        print(f"\n{'='*60}")
        print(f"✅ DIAGNOSIS COMPLETE")
        print(f"⏱️  Processing time: {processing_time:.2f}s")
        print(f"🔧 Tools used: {', '.join(tools_used) if tools_used else 'None'}")
        print(f"{'='*60}\n")
        
        return {
            "diagnosis": response,
            "tools_used": tools_used,
            "processing_time": processing_time,
            "reasoning_steps": len(tools_used),
            "user_context": self.memory.get_context()
        }
    
    def _should_use_multi_agent(self, user_input: str, context: Dict) -> bool:
        """Determine if multi-agent system should be used"""
        # Use multi-agent for complex queries or when multiple capabilities needed
        user_lower = user_input.lower()
        
        complexity_indicators = [
            "and", "also", "plus", "additionally",
            "both", "multiple", "several"
        ]
        
        has_image = context.get("has_image", False)
        has_document = context.get("has_document", False)
        
        # Use multi-agent if:
        # 1. Multiple complexity indicators
        # 2. Has image or document
        # 3. Asks for multiple things
        
        complexity_count = sum(1 for indicator in complexity_indicators if indicator in user_lower)
        
        return complexity_count >= 2 or has_image or has_document
    
    def get_explanation(self) -> str:
        """Get explanation of agent's reasoning process"""
        return """
🤖 **How Agentic AI Works:**

1. **Reasoning**: Analyzes your question and breaks it down
2. **Planning**: Decides which tools to use and in what order
3. **Acting**: Executes tools autonomously
4. **Validation**: Checks if findings make sense
5. **Learning**: Remembers successful diagnoses
6. **Response**: Provides comprehensive solution

**Available Capabilities:**
- OBD code lookup
- Symptom analysis
- Parts search with pricing
- Image analysis (damage/mechanical)
- Document analysis
- Cost calculation
- Video tutorials
- Multi-agent coordination

**Memory System:**
- Remembers your vehicles
- Tracks past issues
- Learns from successful diagnoses
- Provides context-aware responses
"""


# ── Convenience Functions ─────────────────────────────────────────────────────

def create_agentic_automech(user_id: Optional[str] = None) -> AgenticAutoMech:
    """Create and return agentic agent instance"""
    return AgenticAutoMech(user_id=user_id, use_multi_agent=True)


def run_agentic_diagnostic(user_input: str, context: Dict = None, user_id: Optional[str] = None) -> str:
    """Quick function to run diagnostic with agentic AI"""
    agent = create_agentic_automech(user_id=user_id)
    result = agent.diagnose(user_input, context)
    return result["diagnosis"]
