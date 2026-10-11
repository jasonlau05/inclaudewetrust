"""End-to-end: Gemini + MCP for one persona, printed to the console.

uv run python scripts/smoke_gemini.py [profile-name] "question"
"""

import asyncio
import json
import sys
from pathlib import Path

from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
load_dotenv(ROOT / ".env")

from app.advisor import Advisor  # noqa: E402


async def main() -> None:
    name = sys.argv[1] if len(sys.argv) > 1 else "1-new-grad"
    default_q = "What should I do with an extra $500/month? Show current prices for anything you suggest."
    question = sys.argv[2] if len(sys.argv) > 2 else default_q
    profile = json.loads((ROOT / "profiles" / f"{name}.json").read_text())
    profile.pop("label", None)
    advisor = Advisor()
    await advisor.start()
    try:
        out = await advisor.chat(profile, [{"role": "user", "text": question}])
    finally:
        await advisor.stop()
    print(f"model={out['model']} elapsed={out['elapsed_ms']}ms tokens={out['tokens']} kb={out['knowledge_sources']}")
    for call in out["tool_calls"]:
        print(f"  tool {call['name']}({call['args']}) -> {call.get('result', '')[:160]}")
    print("\n" + out["reply"])


if __name__ == "__main__":
    asyncio.run(main())
