"""
Voice Chatbot Service for natural conversations
"""
import logging
from typing import Dict, List, Optional
from datetime import datetime

from src.config.settings import settings
from src.services.agents.tool_registry import ToolRegistry
from src.services.agents.knowledge_base import KnowledgeBase
from src.services.llm_factory import get_llm

logger = logging.getLogger(__name__)


class VoiceChatbot:
    """Conversational agent for voice interactions"""
    
    def __init__(
        self,
        tools: ToolRegistry,
        knowledge_base: KnowledgeBase
    ):
        """
        Initialize voice chatbot
        
        Args:
            tools: Tool registry
            knowledge_base: Knowledge base
        """
        self.tools = tools
        self.knowledge_base = knowledge_base
        self.llm = get_llm()  # Use LLM factory
        self.sessions: Dict[str, Dict] = {}  # Session storage
        
        logger.info("Voice chatbot initialized")
    
    def create_session(
        self,
        farmer_id: str,
        language: str = "en",
        context: Optional[Dict] = None
    ) -> str:
        """
        Create new conversation session
        
        Args:
            farmer_id: Farmer ID
            language: Conversation language
            context: Initial context
        
        Returns:
            Session ID
        """
        session_id = f"session_{farmer_id}_{datetime.utcnow().timestamp()}"
        
        self.sessions[session_id] = {
            "farmer_id": farmer_id,
            "language": language,
            "context": context or {},
            "conversation_history": [],
            "created_at": datetime.utcnow().isoformat(),
            "turn_count": 0
        }
        
        logger.info(f"Created session {session_id} for farmer {farmer_id}")
        return session_id
    
    async def process_turn(
        self,
        session_id: str,
        user_input: str
    ) -> Dict:
        """
        Process conversation turn
        
        Args:
            session_id: Session ID
            user_input: User's speech input (transcribed)
        
        Returns:
            Response with text and metadata
        """
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")
        
        session = self.sessions[session_id]
        session["turn_count"] += 1
        
        # Add user input to history
        session["conversation_history"].append({
            "role": "user",
            "content": user_input,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        # Detect intent
        intent = await self._detect_intent(user_input, session)
        
        # Retrieve relevant context
        if intent["needs_knowledge"]:
            knowledge_context = await self.knowledge_base.get_context_for_query(
                user_input,
                n_results=2
            )
        else:
            knowledge_context = ""
        
        # Get farmer context if needed
        if intent["needs_farmer_data"]:
            farmer_data = self.tools.get_tool("get_farm_data")(
                farmer_id=session["farmer_id"]
            )
        else:
            farmer_data = {}
        
        # Generate response
        response_text = await self._generate_response(
            user_input,
            session,
            intent,
            knowledge_context,
            farmer_data
        )
        
        # Add response to history
        session["conversation_history"].append({
            "role": "assistant",
            "content": response_text,
            "timestamp": datetime.utcnow().isoformat()
        })
        
        # Check if conversation should end
        should_end = self._should_end_conversation(response_text, session)
        
        result = {
            "session_id": session_id,
            "response_text": response_text,
            "intent": intent["type"],
            "confidence": intent["confidence"],
            "should_end": should_end,
            "turn_count": session["turn_count"]
        }
        
        logger.info(
            f"Processed turn {session['turn_count']} for session {session_id}, "
            f"intent={intent['type']}"
        )
        
        return result
    
    async def _detect_intent(
        self,
        user_input: str,
        session: Dict
    ) -> Dict:
        """
        Detect user intent
        
        Args:
            user_input: User input text
            session: Session data
        
        Returns:
            Intent information
        """
        # Simple intent detection using keywords
        # In production, use a proper NLU model
        
        user_input_lower = user_input.lower()
        
        # Greeting intents
        if any(word in user_input_lower for word in ["hello", "hi", "namaste", "vanakkam"]):
            return {
                "type": "greeting",
                "confidence": 0.9,
                "needs_knowledge": False,
                "needs_farmer_data": False
            }
        
        # Query about crop health
        if any(word in user_input_lower for word in ["crop", "health", "ndvi", "problem"]):
            return {
                "type": "crop_health_query",
                "confidence": 0.85,
                "needs_knowledge": True,
                "needs_farmer_data": True
            }
        
        # Query about weather
        if any(word in user_input_lower for word in ["weather", "rain", "temperature"]):
            return {
                "type": "weather_query",
                "confidence": 0.85,
                "needs_knowledge": False,
                "needs_farmer_data": True
            }
        
        # Query about pest/disease
        if any(word in user_input_lower for word in ["pest", "disease", "insect", "bug"]):
            return {
                "type": "pest_disease_query",
                "confidence": 0.85,
                "needs_knowledge": True,
                "needs_farmer_data": False
            }
        
        # Query about advisory
        if any(word in user_input_lower for word in ["advisory", "recommendation", "what should"]):
            return {
                "type": "advisory_query",
                "confidence": 0.8,
                "needs_knowledge": True,
                "needs_farmer_data": True
            }
        
        # Goodbye intent
        if any(word in user_input_lower for word in ["bye", "goodbye", "thank you", "thanks"]):
            return {
                "type": "goodbye",
                "confidence": 0.9,
                "needs_knowledge": False,
                "needs_farmer_data": False
            }
        
        # Default: general query
        return {
            "type": "general_query",
            "confidence": 0.6,
            "needs_knowledge": True,
            "needs_farmer_data": False
        }
    
    async def _generate_response(
        self,
        user_input: str,
        session: Dict,
        intent: Dict,
        knowledge_context: str,
        farmer_data: Dict
    ) -> str:
        """
        Generate response using LLM
        
        Args:
            user_input: User input
            session: Session data
            intent: Detected intent
            knowledge_context: Retrieved knowledge
            farmer_data: Farmer data
        
        Returns:
            Response text
        """
        # Build system prompt
        system_prompt = f"""You are KrishiMitra, a helpful agricultural assistant speaking to a farmer in {session['language']}.

Your role:
- Provide clear, actionable agricultural advice
- Be concise and speak naturally (this is a voice conversation)
- Use simple language appropriate for farmers
- Be empathetic and supportive

Context:
{knowledge_context}

Farmer information:
{farmer_data}

Guidelines:
- Keep responses under 100 words for voice delivery
- Use the farmer's language naturally
- Provide specific, actionable advice
- Ask clarifying questions if needed
"""
        
        # Build messages
        messages = [{"role": "system", "content": system_prompt}]
        
        # Add recent conversation history (last 5 turns)
        recent_history = session["conversation_history"][-10:]
        for turn in recent_history:
            messages.append({
                "role": turn["role"],
                "content": turn["content"]
            })
        
        # Add current input
        messages.append({"role": "user", "content": user_input})
        
        # Generate response using LLM factory
        try:
            response = await self.llm.generate_completion(
                messages=messages,
                temperature=0.7,
                max_tokens=200  # Keep responses concise for voice
            )
            
            return response
            
        except Exception as e:
            logger.error(f"Response generation failed: {e}")
            return "I'm sorry, I'm having trouble understanding. Could you please repeat that?"
    
    def _should_end_conversation(
        self,
        response_text: str,
        session: Dict
    ) -> bool:
        """Check if conversation should end"""
        
        # End if goodbye detected
        goodbye_phrases = ["goodbye", "bye", "thank you for calling", "have a good day"]
        if any(phrase in response_text.lower() for phrase in goodbye_phrases):
            return True
        
        # End if too many turns (prevent infinite conversations)
        if session["turn_count"] >= 20:
            return True
        
        return False
    
    def get_session(self, session_id: str) -> Optional[Dict]:
        """Get session data"""
        return self.sessions.get(session_id)
    
    def end_session(self, session_id: str):
        """End and cleanup session"""
        if session_id in self.sessions:
            session = self.sessions[session_id]
            
            # Log session summary
            logger.info(
                f"Ended session {session_id}: "
                f"{session['turn_count']} turns, "
                f"farmer={session['farmer_id']}"
            )
            
            # In production, save to database before deleting
            del self.sessions[session_id]
    
    def get_conversation_summary(self, session_id: str) -> Dict:
        """Get conversation summary"""
        if session_id not in self.sessions:
            return {}
        
        session = self.sessions[session_id]
        
        return {
            "session_id": session_id,
            "farmer_id": session["farmer_id"],
            "language": session["language"],
            "turn_count": session["turn_count"],
            "duration_seconds": (
                datetime.utcnow() - 
                datetime.fromisoformat(session["created_at"])
            ).total_seconds(),
            "conversation_history": session["conversation_history"]
        }
