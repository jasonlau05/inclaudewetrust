"""Spawn the market MCP server over stdio and call every tool once (no Gemini involved).

uv run python scripts/smoke_mcp.py
"""

import asyncio
import json
import sys
import time
from pathlib import Path

from mcp import ClientSession, StdioServerParameters, stdio_client

ROOT = Path(__file__).resolve().parent.parent

CALLS = [
    ("get_quotes", {"symbols": ["VOO", "AAPL", "BND", "NOTAREALTICKER"]}),
    ("get_quotes", {"symbols": ["VOO", "AAPL", "BND", "NOTAREALTICKER"]}),  # cache hit
    ("get_performance", {"symbol": "VTI"}),
    ("get_fund_info", {"symbol": "VOO"}),
    ("get_news", {"query": "NVDA", "limit": 3}),
]


async def main() -> int:
    params = StdioServerParameters(command=sys.executable, args=["-m", "market_mcp.server"], cwd=str(ROOT))
    async with stdio_client(params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()
        tools = await session.list_tools()
        print("tools:", [t.name for t in tools.tools])
        failures = 0
        for name, args in CALLS:
            t0 = time.perf_counter()
            result = await session.call_tool(name, args)
            ms = (time.perf_counter() - t0) * 1000
            payload = result.structured_content or [c.text for c in result.content if hasattr(c, "text")]
            text = json.dumps(payload, default=str)
            print(f"\n== {name}({args}) {ms:.0f} ms  error={result.is_error}\n{text[:700]}")
            failures += bool(result.is_error)
    return failures


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
