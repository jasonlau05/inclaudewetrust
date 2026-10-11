# Alex · investing education (prototype)

An investing-education chat app built on Google Gemini. The person fills in a profile, and Gemini
answers using the team's knowledge base plus live market data from a small MCP server. Every
answer shows its work: the KB rule IDs it cites are clickable and resolve to the rule text, and
the evidence rail lists each market-data call with its source and timestamp.

```
browser (app/static) ──► FastAPI (app/main.py) ──► Gemini API (google-genai, chat + automatic function calling)
                                │                         │ tool calls
                                │                         ▼
                                └──── one long-lived MCP stdio session ──► market_mcp/server.py ──► yfinance (+ TTL cache)
```

## Run it

```bash
uv sync
cp .env.example .env        # then set GEMINI_API_KEY
uv run uvicorn app.main:app --port 8765
```

Open http://localhost:8765. Pick a persona and ask a question. Hover any rule ID in the answer to
see it in the evidence rail on the right, which also lists every MCP call and its raw result.

The UI's visual system ("Intaglio Note") is documented in `DESIGN.md`, and product context is in
`PRODUCT.md`. Both were made with [Impeccable](https://impeccable.style);
`npx impeccable detect app/static` checks the UI for design anti-patterns.

| Endpoint | Purpose |
|---|---|
| `GET /` | Single-page UI |
| `GET /healthz` | Liveness check, shows the model and how many MCP tools were found |
| `GET /api/status` | The model, thinking level, and MCP tool list |
| `GET /api/personas` | Test profiles from `profiles/` |
| `GET /api/kb` | KB ID → one-line summary (R-, PB-, GR-, PS-, RN-, MCP-), used to link citations |
| `POST /api/chat` | `{profile, messages:[{role,text}]}` returns `{reply, tool_calls, tokens, elapsed_ms}` |

## Pieces

**`market_mcp/server.py`** is an MCP server (Python SDK v2 `MCPServer`, stdio). It has four tools
and keeps responses compact:

| Tool | Returns | Cache |
|---|---|---|
| `get_quotes(symbols[≤10])` | Identity (name, exchange, type), price, prior close, market state, quote time, 52-week range, P/E, yield, beta | 60s |
| `get_performance(symbol)` | 1m/3m/YTD/1y total return, 3y/5y/10y annualized return, 1y volatility, max drawdown | 1h |
| `get_fund_info(symbol)` | Expense ratio, category, turnover, asset classes, top sectors, top 10 holdings | 24h |
| `get_news(query, limit)` | Recent headlines for a ticker or topic (Yahoo search) | 15m |

Every result names its provider and timestamp, which the KB's `MCP-PRESENT` and `GR-007` sections
ask for. Unknown tickers come back as `{"error": ...}` instead of failing the request. The server
also runs standalone, so it works with any MCP client (Claude Desktop, Gemini CLI, MCP Inspector):

```json
{ "command": "uv", "args": ["run", "--directory", "<repo path>", "python", "-m", "market_mcp.server"] }
```

**`app/advisor.py`** connects Gemini to MCP. The MCP `ClientSession` is passed straight into
`GenerateContentConfig(tools=[session])`, and google-genai's automatic function calling handles
the loop of listing tools, calling them, and feeding results back. The system instruction is
`knowledge/GEMINI_SYSTEM_PROMPT.md`, a short app addendum that maps "the stock lookup tool" to the
4 MCP tools, `knowledge/KNOWLEDGE_BASE.md`, and the profile, in that order. Putting the KB before
the profile keeps the prefix stable, so Gemini's implicit caching reuses it (~20k of ~23k prompt
tokens come back as cached).

**`knowledge/`** is a copy of the investing KB taken from `research/D-investing-kb` on 2026-10-10.
Only `GEMINI_SYSTEM_PROMPT.md` and `KNOWLEDGE_BASE.md` are loaded. `notes/` and `draft.md` are
source material. Both files are re-read on every request, so edits apply without a restart.

**`profiles/`** has test personas whose fields use the KB's `PROFILE-SCHEMA` keys (PS-xxx).

## Scripts

```bash
uv run python scripts/smoke_mcp.py                       # MCP server alone: calls every tool, prints timings
uv run python scripts/smoke_gemini.py 3-tech-rsus "Am I too concentrated in NVDA?"   # Gemini + MCP from the CLI
uv run ruff check . && uv run ruff format --check .
```

## Config (`.env`)

| Var | Default | Notes |
|---|---|---|
| `GEMINI_API_KEY` | (none) | Required |
| `GEMINI_MODEL` | `gemini-3.8-flash` | Any Gemini model that supports function calling |
| `GEMINI_THINKING_LEVEL` | `low` | `minimal`/`low`/`medium`/`high`. Lower is faster |
| `GEMINI_FALLBACK_MODELS` | (none) | Comma list tried in order when a model returns 429. A model that ran out of quota is skipped for an hour |

## Gotchas

- **mcp v2 + google-genai:** the SDK deep-copies the request config, and an mcp v2
  `ClientSession` can't be copied because it holds live asyncio tasks. `SharedSession` in
  `advisor.py` overrides `__deepcopy__` to return itself.
- **Tool trace with chats:** when you use `client.aio.chats`, the function calls and results are in
  `chat.get_history()`, not in `response.automatic_function_calling_history`.
- **Free-tier quota:** about 20 requests per day **per model**, and one answer with tool calls
  uses several. 429s are not retried (the SDK's backoff would hang the request for hours).
  Instead the advisor falls through `GEMINI_FALLBACK_MODELS`, and if every model is out of
  quota the UI shows a clear error. The first request after a model runs out can take up to
  75s before falling back.
- **yfinance is unofficial.** It can rate-limit or change shape. `Ticker.news` currently returns
  nothing, so news uses `yf.Search` instead.
- Latency is ~13–25s per answer, mostly Gemini writing a long templated response. Streaming would
  make it feel much faster.

## Not production-ready

There's no auth, no persistence, and no streaming. The KB README warns that personalized output
can count as investment advice under the Investment Advisers Act (see GR-001), so get securities
counsel before launch.
