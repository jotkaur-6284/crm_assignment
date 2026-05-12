from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class InteractionBase(BaseModel):
    hcp_name: str
    interaction_type: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None
    topics: Optional[str] = None
    materials_shared: Optional[str] = None
    sample_distributed: Optional[str] = None
    sentiment: Optional[str] = None
    outcomes: Optional[str] = None


class InteractionCreate(InteractionBase):
    pass


class Interaction(InteractionBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ChatRequest(BaseModel):
    text: str


class AgentLogRequest(BaseModel):
    text: str


class AgentEditRequest(BaseModel):
    updates: dict


class AgentExecuteRequest(BaseModel):
    tool_name: str
    text: Optional[str] = None
    hcp_name: Optional[str] = None
    interaction_id: Optional[int] = None
    updates: Optional[dict] = None


class AIExtractResponse(InteractionBase):
    summary: Optional[str] = None
