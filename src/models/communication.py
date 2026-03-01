"""
Communication models (Calls, Chatbot, Feedback)
"""
from sqlalchemy import Column, String, DateTime, ForeignKey, Integer, Boolean, Text, Enum as SQLEnum
from sqlalchemy.types import DECIMAL
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime
import enum
from src.config.database import Base
from src.config.db_types import UUID, ARRAY, JSONB


class CallStatus(enum.Enum):
    """Call status types"""
    SCHEDULED = "scheduled"
    INITIATED = "initiated"
    RINGING = "ringing"
    ANSWERED = "answered"
    COMPLETED = "completed"
    MISSED = "missed"
    FAILED = "failed"
    SMS_FALLBACK = "sms_fallback"


class ChatbotSessionStatus(enum.Enum):
    """Chatbot session status types"""
    ACTIVE = "active"
    COMPLETED = "completed"
    TRANSFERRED_TO_HUMAN = "transferred"
    ERROR = "error"
    FARMER_DISCONNECTED = "disconnected"


class CallRecord(Base):
    """Call Record model"""
    __tablename__ = "call_records"
    
    call_id = Column(UUID(), primary_key=True, default=uuid.uuid4)
    farmer_id = Column(UUID(), ForeignKey("farmers.farmer_id", ondelete="CASCADE"), nullable=False, index=True)
    advisory_id = Column(UUID(), ForeignKey("advisories.advisory_id"), index=True)
    
    # Call details
    initiated_at = Column(DateTime, nullable=False, index=True)
    answered_at = Column(DateTime)
    ended_at = Column(DateTime)
    duration_seconds = Column(Integer)
    
    # Call status
    status = Column(SQLEnum(CallStatus), nullable=False, index=True)
    attempt_number = Column(Integer, nullable=False)  # 1, 2, or 3
    
    # Language and interaction
    language_used = Column(String(10), nullable=False, index=True)
    replay_count = Column(Integer, default=0)
    farmer_acknowledged = Column(Boolean)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    farmer = relationship("Farmer", back_populates="call_records")
    advisory = relationship("Advisory", back_populates="call_records")
    feedback = relationship("FarmerFeedback", back_populates="call_record", uselist=False)
    
    def __repr__(self):
        return f"<CallRecord(id={self.call_id}, farmer_id={self.farmer_id}, status={self.status.value})>"


class FarmerFeedback(Base):
    """Farmer Feedback model"""
    __tablename__ = "farmer_feedback"
    
    feedback_id = Column(UUID(), primary_key=True, default=uuid.uuid4)
    call_id = Column(UUID(), ForeignKey("call_records.call_id", ondelete="CASCADE"), nullable=False, index=True)
    
    # Ratings
    usefulness_rating = Column(Integer)  # 1 to 5
    clarity_rating = Column(Integer)  # 1 to 5
    
    # Action and comments
    action_taken = Column(Boolean)
    comments = Column(Text)
    
    # Metadata
    submitted_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    call_record = relationship("CallRecord", back_populates="feedback")
    
    def __repr__(self):
        return f"<FarmerFeedback(call_id={self.call_id}, usefulness={self.usefulness_rating})>"


class ChatbotSession(Base):
    """Chatbot Session model"""
    __tablename__ = "chatbot_sessions"
    
    session_id = Column(UUID(), primary_key=True, default=uuid.uuid4)
    farmer_id = Column(UUID(), ForeignKey("farmers.farmer_id", ondelete="CASCADE"), nullable=False, index=True)
    phone_number = Column(String(20), nullable=False)
    
    # Session details
    language = Column(String(10), nullable=False, index=True)
    call_type = Column(String(30), nullable=False)  # "inbound" or "outbound_interactive"
    
    # Timing
    started_at = Column(DateTime, nullable=False, index=True)
    ended_at = Column(DateTime)
    duration_seconds = Column(Integer)
    
    # Status and metrics
    status = Column(SQLEnum(ChatbotSessionStatus), nullable=False, index=True)
    conversation_turns = Column(Integer, default=0)
    resolution_status = Column(String(20))  # "resolved", "escalated", "incomplete"
    farmer_satisfaction = Column(Integer)  # 1 to 5
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    farmer = relationship("Farmer", back_populates="chatbot_sessions")
    conversation_turns = relationship("ConversationTurn", back_populates="session", cascade="all, delete-orphan")
    
    def __repr__(self):
        return f"<ChatbotSession(id={self.session_id}, farmer_id={self.farmer_id}, status={self.status.value})>"


class ConversationTurn(Base):
    """Conversation Turn model"""
    __tablename__ = "conversation_turns"
    
    turn_id = Column(UUID(), primary_key=True, default=uuid.uuid4)
    session_id = Column(UUID(), ForeignKey("chatbot_sessions.session_id", ondelete="CASCADE"), nullable=False, index=True)
    turn_number = Column(Integer, nullable=False)
    
    # User input
    user_speech_audio_url = Column(Text)  # S3 URL
    user_speech_text = Column(Text, nullable=False)
    user_speech_confidence = Column(DECIMAL(3, 2))  # 0 to 1
    
    # Agent response
    agent_response_text = Column(Text, nullable=False)
    agent_response_audio_url = Column(Text)  # S3 URL
    
    # Tools and performance
    tools_used = Column(ARRAY(String))
    response_time_ms = Column(Integer)
    
    # Metadata
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    
    # Relationships
    session = relationship("ChatbotSession", back_populates="conversation_turns")
    
    def __repr__(self):
        return f"<ConversationTurn(session_id={self.session_id}, turn={self.turn_number})>"


class ChatbotMetrics(Base):
    """Chatbot Metrics model (daily aggregated metrics)"""
    __tablename__ = "chatbot_metrics"
    
    metric_id = Column(UUID(), primary_key=True, default=uuid.uuid4)
    date = Column(DateTime, nullable=False, unique=True, index=True)
    
    # Session metrics
    total_sessions = Column(Integer, nullable=False)
    inbound_calls = Column(Integer, nullable=False)
    outbound_interactive = Column(Integer, nullable=False)
    
    # Performance metrics
    avg_duration_seconds = Column(DECIMAL(8, 2))
    avg_turns_per_session = Column(DECIMAL(5, 2))
    resolution_rate = Column(DECIMAL(5, 4))  # 0 to 1
    escalation_rate = Column(DECIMAL(5, 4))  # 0 to 1
    farmer_satisfaction_avg = Column(DECIMAL(3, 2))  # 1 to 5
    
    # Language and topic distribution
    languages_used = Column(JSONB)  # {"hi": 100, "bn": 50, ...}
    common_topics = Column(ARRAY(String))
    
    # Response time
    avg_response_time_ms = Column(Integer)
    
    # Metadata
    created_at = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<ChatbotMetrics(date={self.date}, sessions={self.total_sessions})>"
