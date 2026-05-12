from typing import List

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

import models
import schemas
from database import Base, engine, get_db
from langgraph_agent import HCPInteractionAgent
from services.ai_service import extract_interaction_from_text

Base.metadata.create_all(bind=engine)
agent = HCPInteractionAgent()

app = FastAPI(
    title="AI-First CRM Backend",
    description="FastAPI backend for HCP interaction logging and AI extraction",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/parse-chat", response_model=schemas.AIExtractResponse)
def parse_chat(request: schemas.ChatRequest):
    return extract_interaction_from_text(request.text)


@app.post("/api/log-interaction", response_model=schemas.Interaction)
def log_interaction(interaction: schemas.InteractionCreate, db: Session = Depends(get_db)):
    db_item = models.HCPInteraction(**interaction.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@app.get("/api/agent/tools")
def get_agent_tools():
    return {
        "role": agent.describe_role(),
        "tools": agent.list_tools(),
    }


@app.post("/api/agent/execute")
def execute_agent_tool(request: schemas.AgentExecuteRequest):
    return agent.run_tool(
        request.tool_name,
        text=request.text,
        hcp_name=request.hcp_name,
        interaction_id=request.interaction_id,
        updates=request.updates,
    )


@app.post("/api/agent/log-interaction", response_model=schemas.Interaction)
def agent_log_interaction(request: schemas.AgentLogRequest, db: Session = Depends(get_db)):
    parsed = agent.log_interaction_tool(request.text)["data"]
    filtered = {k: v for k, v in parsed.items() if k in {
        "hcp_name",
        "interaction_type",
        "date",
        "time",
        "topics",
        "materials_shared",
        "sample_distributed",
        "sentiment",
        "outcomes",
    }}
    db_item = models.HCPInteraction(**filtered)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


@app.put("/api/agent/edit-interaction/{interaction_id}", response_model=schemas.Interaction)
def agent_edit_interaction(interaction_id: int, request: schemas.AgentEditRequest, db: Session = Depends(get_db)):
    item = db.query(models.HCPInteraction).filter(models.HCPInteraction.id == interaction_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Interaction not found")
    for field, value in request.updates.items():
        if hasattr(item, field):
            setattr(item, field, value)
    db.commit()
    db.refresh(item)
    return item


@app.get("/api/interactions", response_model=List[schemas.Interaction])
def list_interactions(db: Session = Depends(get_db)):
    return db.query(models.HCPInteraction).order_by(models.HCPInteraction.created_at.desc()).all()


@app.post("/api/ai-suggest")
def ai_suggest(request: schemas.ChatRequest):
    extracted = extract_interaction_from_text(request.text)
    return {
        "suggestion": "Review the follow-up action for the HCP and confirm next steps.",
        "extracted_interaction": extracted,
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
