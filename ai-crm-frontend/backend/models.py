from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime
from database import Base


class HCPInteraction(Base):
    __tablename__ = "hcp_interactions"

    id = Column(Integer, primary_key=True, index=True)
    hcp_name = Column(String(255), nullable=False)
    interaction_type = Column(String(100), nullable=True)
    date = Column(String(50), nullable=True)
    time = Column(String(50), nullable=True)
    topics = Column(Text, nullable=True)
    materials_shared = Column(String(255), nullable=True)
    sample_distributed = Column(String(255), nullable=True)
    sentiment = Column(String(50), nullable=True)
    outcomes = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class ChatLog(Base):
    __tablename__ = "chat_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_input = Column(Text, nullable=False)
    ai_response = Column(Text, nullable=True)
    extracted_hcp_name = Column(String(255), nullable=True)
    extracted_sentiment = Column(String(50), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
