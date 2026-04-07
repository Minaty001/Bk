from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Any
import os

from .groq_client import GroqClient

try:
    from serp_client import SerpClient
except Exception:
    SerpClient = None

app = FastAPI()


class PlanRequest(BaseModel):
    nl: str


class ActionResponse(BaseModel):
    actions: List[Any]


# Global planner client and optional web search client
groq_client = None
serp_client = None


@app.on_event("startup")
def startup_event():
    global groq_client
    global serp_client
    api_base = os.getenv("GROQ_API_BASE", "https://api.groq.com/openai/v1")
    chat_model = os.getenv("GROQ_CHAT_MODEL", "llama-3.1-8b-instant")
    chat_api_key = os.getenv("GROQ_CHAT_API_KEY", "")
    coding_model = os.getenv("GROQ_CODING_MODEL", "llama-3.3-70b-versatile")
    coding_api_key = os.getenv("GROQ_CODING_API_KEY", "")
    compound_model = os.getenv("GROQ_COMPOUND_MODEL", "compound-beta-mini")
    compound_api_key = os.getenv("GROQ_COMPOUND_API_KEY", "")

    groq_client = GroqClient(
        api_base,
        chat_model,
        chat_api_key,
        coding_model,
        coding_api_key,
        compound_model,
        compound_api_key,
    )
    # Optional: initialize SerpAPI client if API key provided
    serp_api_key = os.getenv("SERP_API_KEY", "")
    if serp_api_key and SerpClient is not None:
        global serp_client
        serp_client = SerpClient(serp_api_key)


@app.post("/plan", response_model=ActionResponse)
def plan(req: PlanRequest):
    if groq_client is None:
        raise HTTPException(status_code=500, detail="Planner not initialized")
    try:
        actions = groq_client.chat_to_actions(req.nl)
        return ActionResponse(actions=actions)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
