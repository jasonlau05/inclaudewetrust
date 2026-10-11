"""FastAPI front door: serves the single-page UI and a small JSON API.

uv run uvicorn app.main:app --reload --port 8765
"""

from __future__ import annotations

import json
import logging
from contextlib import asynccontextmanager
from typing import Any, Literal

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from app.advisor import ROOT, Advisor, QuotaExhaustedError, kb_index

load_dotenv(ROOT / ".env")
log = logging.getLogger("app")
STATIC = ROOT / "app" / "static"
PROFILES = ROOT / "profiles"


@asynccontextmanager
async def lifespan(app: FastAPI):
    advisor = Advisor()
    await advisor.start()
    app.state.advisor = advisor
    try:
        yield
    finally:
        await advisor.stop()


app = FastAPI(title="Investing assistant prototype", lifespan=lifespan)
app.mount("/static", StaticFiles(directory=STATIC), name="static")


class Message(BaseModel):
    role: Literal["user", "assistant"]
    text: str = Field(min_length=1, max_length=8000)


class ChatRequest(BaseModel):
    profile: dict[str, Any] = {}
    messages: list[Message] = Field(min_length=1, max_length=40)


@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC / "index.html")


@app.get("/healthz")
def healthz() -> dict[str, Any]:
    advisor: Advisor = app.state.advisor
    return {"ok": True, "model": advisor.model, "mcp_tools": len(advisor.tools)}


@app.get("/api/status")
def status() -> dict[str, Any]:
    advisor: Advisor = app.state.advisor
    return {
        "model": advisor.model,
        "fallback_models": advisor.models[1:],
        "thinking_level": advisor.thinking,
        "tools": advisor.tools,
    }


@app.get("/api/kb")
def kb() -> dict[str, str]:
    return kb_index()


@app.get("/api/personas")
def personas() -> list[dict[str, Any]]:
    return [{"id": p.stem, **json.loads(p.read_text(encoding="utf-8"))} for p in sorted(PROFILES.glob("*.json"))]


@app.post("/api/chat")
async def chat(req: ChatRequest) -> dict[str, Any]:
    if req.messages[-1].role != "user":
        raise HTTPException(400, "last message must be from the user")
    try:
        return await app.state.advisor.chat(req.profile, [m.model_dump() for m in req.messages])
    except QuotaExhaustedError as exc:
        raise HTTPException(429, str(exc)) from exc
    except Exception as exc:
        log.exception("chat failed")
        raise HTTPException(502, "The model or market-data service failed.") from exc
