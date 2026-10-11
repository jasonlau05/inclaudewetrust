"""Gemini <-> MCP bridge.

One long-lived stdio MCP session is opened at startup. Each chat request hands that
session to google-genai as a tool; the SDK's automatic function calling lists the
MCP tools, lets Gemini call them, and feeds results back until it has an answer.
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
from contextlib import AsyncExitStack
from pathlib import Path
from typing import Any

from google import genai
from google.genai import errors, types
from mcp import ClientSession, StdioServerParameters, stdio_client

ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE_DIR = ROOT / "knowledge"
SYSTEM_PROMPT_FILE = KNOWLEDGE_DIR / "GEMINI_SYSTEM_PROMPT.md"
KNOWLEDGE_FILE = KNOWLEDGE_DIR / "KNOWLEDGE_BASE.md"

# App-specific glue on top of the KB team's GEMINI_SYSTEM_PROMPT.md: maps "the stock
# lookup tool" onto our MCP tools and explains where the profile comes from.
APP_ADDENDUM = """\
## This app
- "The stock lookup tool" in the knowledge base means these MCP tools:
  get_quotes (prices, valuation, identity; batch up to 10 symbols in one call),
  get_performance (historical total returns, volatility, drawdown),
  get_fund_info (ETF/mutual fund expense ratio, category, holdings, sectors),
  get_news (recent headlines for a ticker or topic).
  Only call what the answer needs. Data comes from Yahoo Finance and is delayed, not
  real-time. Each result has an as-of time; cite it.
- News is context only (see R- rules on behavior). Never present a headline as a reason to trade.
- The user's profile below comes from a form. Fields left blank are unknown; ask for them
  per PROFILE-SCHEMA when they would change the answer.
- When you apply a rule, playbook or guardrail, cite its ID in parentheses, e.g. (R-012, PB-002).
"""


def load_knowledge() -> tuple[str, str, list[str]]:
    """Return (system prompt, knowledge base, source file names). Re-read per request,
    so edits to knowledge/ apply without a restart."""
    prompt = SYSTEM_PROMPT_FILE.read_text(encoding="utf-8").strip()
    kb = KNOWLEDGE_FILE.read_text(encoding="utf-8").strip()
    return prompt, kb, [SYSTEM_PROMPT_FILE.name, KNOWLEDGE_FILE.name]


_KB_PATTERNS = [
    # - **R-001:** If investing would cause ...
    (re.compile(r"^- \*\*(R-\d{3}):\*\*\s*(.+)$"), lambda m: m[2]),
    # ## GR-001 — Stay on the education side of the line   (also PB-xxx, MCP-xxx)
    (re.compile(r"^#{2,3} ((?:GR|PB|MCP)-[A-Z0-9]+) — (.+)$"), lambda m: m[2]),
    # | PS-001 | `age`: integer | ...
    (re.compile(r"^\| (PS-\d{3}) \| `([^`]+)`"), lambda m: m[2].replace("_", " ")),
    # | RN-001 | 401(k) ... deferral | $24,500 (...) | source |
    (re.compile(r"^\| (RN-\d{3}) \| ([^|]+)\| ([^|]+)\|"), lambda m: f"{m[2].strip()}: {m[3].strip()}"),
]


def _clip(text: str, limit: int = 140) -> str:
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"", text).replace("**", "").strip()
    return text if len(text) <= limit else text[: limit - 1].rsplit(" ", 1)[0] + "…"


def kb_index() -> dict[str, str]:
    """ID -> one-line summary for every rule, playbook, guardrail, schema field and reference number."""
    index: dict[str, str] = {}
    for line in KNOWLEDGE_FILE.read_text(encoding="utf-8").splitlines():
        for pattern, summary in _KB_PATTERNS:
            if m := pattern.match(line):
                index.setdefault(m[1], _clip(summary(m)))
                break
    return index


def build_system_prompt(profile: dict[str, Any]) -> tuple[str, list[str]]:
    prompt, kb, sources = load_knowledge()
    profile_json = json.dumps({k: v for k, v in profile.items() if v not in ("", None)}, indent=2)
    # Stable prefix (prompt + KB) first so Gemini's implicit context caching can reuse it;
    # the per-user profile goes last.
    text = (
        f"{prompt}\n\n{APP_ADDENDUM}\n"
        f'<knowledge_base file="KNOWLEDGE_BASE.md">\n{kb}\n</knowledge_base>\n\n'
        f"<user_profile>\n{profile_json}\n</user_profile>"
    )
    return text, sources


def _result_payload(response: dict[str, Any]) -> str:
    """AFC stores {'result'|'error': CallToolResult}; show its JSON payload, not the repr."""
    key = "error" if "error" in response else "result"
    value = response.get(key)
    payload = (
        getattr(value, "structured_content", None)
        or [getattr(c, "text", str(c)) for c in getattr(value, "content", None) or []]
        or value
    )
    text = json.dumps(payload, default=str)
    return f"ERROR: {text}" if key == "error" else text


def _tool_trace(contents: list[types.Content]) -> list[dict[str, Any]]:
    """Pair each function_call in a turn's history with its function_response."""
    calls: list[dict[str, Any]] = []
    for content in contents:
        for part in content.parts or []:
            if part.function_call:
                calls.append({"name": part.function_call.name, "args": dict(part.function_call.args or {})})
            elif part.function_response:
                match = next((c for c in calls if c["name"] == part.function_response.name and "result" not in c), None)
                if match is not None:
                    match["result"] = _result_payload(part.function_response.response or {})[:2000]
    return calls


class SharedSession(ClientSession):
    """google-genai deep-copies the request config, tools included. An mcp>=2 session
    holds live asyncio tasks and can't be copied, and a copy would be a different
    connection anyway, so share the one session."""

    def __deepcopy__(self, memo: dict) -> SharedSession:
        return self


QUOTA_COOLDOWN_S = 3600


class QuotaExhaustedError(RuntimeError):
    pass


class Advisor:
    def __init__(self) -> None:
        self.model = os.environ.get("GEMINI_MODEL", "gemini-3.8-flash")
        fallbacks = os.environ.get("GEMINI_FALLBACK_MODELS", "")
        self.models = [self.model, *(m.strip() for m in fallbacks.split(",") if m.strip())]
        self.thinking = os.environ.get("GEMINI_THINKING_LEVEL", "low")
        # Never retry 429s: the SDK's backoff would hang the request for the whole quota window.
        self.client = genai.Client(  # reads GEMINI_API_KEY
            http_options=types.HttpOptions(
                timeout=75_000,
                retry_options=types.HttpRetryOptions(attempts=2, http_status_codes=[500, 502, 503, 504]),
            )
        )
        self._exhausted: dict[str, float] = {}  # model -> monotonic time its quota hit
        self._stack = AsyncExitStack()
        self.session: SharedSession | None = None
        self.tools: list[dict[str, str]] = []

    async def start(self) -> None:
        env = os.environ.copy()
        paths = [str(ROOT), *(path for path in sys.path if path)]
        if env.get("PYTHONPATH"):
            paths.append(env["PYTHONPATH"])
        env["PYTHONPATH"] = os.pathsep.join(dict.fromkeys(paths))

        params = StdioServerParameters(
            command=sys.executable,
            args=["-m", "market_mcp.server"],
            cwd=str(ROOT),
            env=env,
        )
        read, write = await self._stack.enter_async_context(stdio_client(params))
        self.session = await self._stack.enter_async_context(SharedSession(read, write))
        await self.session.initialize()
        listed = await self.session.list_tools()
        self.tools = [
            {"name": t.name, "description": t.description or ""}
            for t in listed.tools
    ]

    async def stop(self) -> None:
        await self._stack.aclose()

    async def chat(self, profile: dict[str, Any], messages: list[dict[str, str]]) -> dict[str, Any]:
        """`messages` is the full visible conversation, ending with the new user message."""
        assert self.session is not None, "advisor not started"
        system_prompt, sources = build_system_prompt(profile)
        history = [
            types.Content(role="model" if m["role"] == "assistant" else "user", parts=[types.Part(text=m["text"])])
            for m in messages[:-1]
        ]
        config = types.GenerateContentConfig(
            system_instruction=system_prompt,
            tools=[self.session],
            automatic_function_calling=types.AutomaticFunctionCallingConfig(maximum_remote_calls=8),
            thinking_config=types.ThinkingConfig(thinking_level=self.thinking),
            temperature=0.4,
        )
        t0 = time.perf_counter()
        model, chat, response = await self._send(config, history, messages[-1]["text"])
        elapsed_ms = round((time.perf_counter() - t0) * 1000)

        usage = response.usage_metadata
        return {
            "reply": response.text or "(no text returned)",
            # Chat keeps the tool round-trips in its history rather than on the response.
            "tool_calls": _tool_trace(chat.get_history()[len(history) :]),
            "model": model,
            "elapsed_ms": elapsed_ms,
            "knowledge_sources": sources,
            "tokens": {
                "prompt": getattr(usage, "prompt_token_count", None),
                "cached": getattr(usage, "cached_content_token_count", None),
                "output": getattr(usage, "candidates_token_count", None),
            },
        }

    async def _send(self, config: types.GenerateContentConfig, history: list[types.Content], text: str):
        """Try the primary model, then each fallback, skipping models whose quota recently ran out."""
        now = time.monotonic()
        available = [m for m in self.models if now - self._exhausted.get(m, -QUOTA_COOLDOWN_S) >= QUOTA_COOLDOWN_S]
        for model in available:
            chat = self.client.aio.chats.create(model=model, config=config, history=history)
            try:
                return model, chat, await chat.send_message(text)
            except errors.ClientError as exc:
                if exc.code != 429:
                    raise
                self._exhausted[model] = time.monotonic()
        raise QuotaExhaustedError(
            f"Gemini quota is used up for {', '.join(self.models)}. "
            "Wait for the quota to reset, add GEMINI_FALLBACK_MODELS, or use a paid API key."
        )
