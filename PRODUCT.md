# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users
Primary audience right now: hackathon judges watching a live demo on a projector or shared
screen. They need to grasp what the product does in seconds and see that it's grounded in real
rules and live data rather than generic chatbot output. Behind them is the eventual end user: a
US individual thinking through how their age, income, debts, accounts and goals should shape
their investing.

## Product Purpose
Alex is an investing-education assistant. The user describes their financial situation (a
profile) and asks questions. Gemini answers with general educational guidance that's tailored to
the profile, follows a curated knowledge base, and uses live market data fetched through an MCP
server. Success in the demo means a judge sees, in one exchange, the profile going in, the rules
applied, the market data fetched, and a clear, cautious answer coming out.

## Positioning
Every answer is traceable. It cites the knowledge base's rule, playbook and guardrail IDs
(R-xxx, PB-xxx, GR-xxx) and shows the exact market-data tool calls and their results, each with
its source and timestamp. A generic chatbot can't truthfully copy that.

## Operating Context
- The demo flow is: pick a persona (or type a profile), ask a question, then read the answer and
  the tool calls behind it.
- Answers take about 13–25 seconds, and the wait has to read as work happening.
- Answers are long, structured markdown with headings, bullets, tables and a required
  disclosure paragraph.
- Market data comes from Yahoo Finance (via yfinance), is delayed rather than real-time, and
  carries a timestamp.

## Capabilities and Constraints
- Profile fields follow the KB's PROFILE-SCHEMA (PS-001…PS-032), and a blank field means
  `unknown`. There are four sample personas in `profiles/`.
- There are four MCP tools: `get_quotes`, `get_performance`, `get_fund_info` and `get_news`.
- The model is Gemini (`gemini-3.8-flash`), and multi-turn chat is stateless on the server.
- The stack is FastAPI serving one static page with plain HTML/CSS/JS and no build step.
  marked and DOMPurify load from a CDN.
- Desktop/projector comes first. On a phone it only has to be usable.
- Not built yet: auth, persistence, streaming.

## Brand Commitments
- The name is **Alex**. There is no logo, palette or other brand assets.
- The voice is cautious and educational. The UI must never imply "buy/sell this",
  guaranteed returns, or that this is personalized advice (KB guardrails GR-001, GR-003, GR-004).

## Evidence on Hand
- `knowledge/KNOWLEDGE_BASE.md` holds the rules, playbooks, guardrails and 2026 reference numbers.
- `profiles/*.json` holds four synthetic personas, which are clearly samples and not real people.
- There are no testimonials, users, metrics or partner logos, and none may be invented.

## Product Principles
1. Show the work: the rules applied and the data fetched are part of the answer, not hidden.
2. Education, not instruction. Trade-offs over directives, and the disclosure is always visible.
3. Profile first: the answer is only as good as the situation it's given, so make missing facts obvious.
4. Honest data: always show the source and timestamp, and never present delayed data as live.

## Accessibility & Inclusion
WCAG AA contrast, and it has to stay legible on a projector (larger type, strong contrast, no
meaning carried by color alone).
