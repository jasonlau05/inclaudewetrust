# Investing knowledge base for Gemini

Made 2026-10-10 by ONA (job `f85478c9`, intern `quick_research`): 8 research agents ran in
parallel, Claude Opus 4.8 wrote the knowledge base, and Claude Code completed the last sections.
Cost: $1.16. Time: about 14 minutes.

| File | What it is |
|---|---|
| `KNOWLEDGE_BASE.md` | The knowledge base (~9k words, ~12k tokens), with stable IDs for retrieval |
| `GEMINI_SYSTEM_PROMPT.md` | A system instruction that tells Gemini how to use it |
| `notes/` | The 8 sourced research notes it was built from |
| `draft.md` | The writer's original output, which stopped at its output limit (kept for reference) |

## What's in the knowledge base

- **PROFILE-SCHEMA** `PS-001…032`: every parameter that changes strategy, with its type,
  allowed values, why it matters, and the question to ask when it's missing.
- **DECISION-RULES** `R-001…052`: sourced if/then rules covering foundations and debt, goals and
  horizon, accounts and taxes, occupation, portfolio construction, and special situations.
- **PROFILE-PLAYBOOKS** `PB-001…011`: college student, new grad, resident doctor, attending
  physician, teacher with a pension, nurse single parent, tech worker with RSUs, gig worker,
  military, pre-retiree behind on savings, and retiree. Each has priorities, an allocation
  range, the account order, and pitfalls.
- **MCP-LOOKUP-GUIDE**: when to call the stock tool, which fields to fetch, how to interpret
  them, red flags, and how to present results.
- **GUARDRAILS** `GR-001…007`, **RESPONSE-TEMPLATE**, **REFERENCE-NUMBERS** (2026 IRS figures),
  **GLOSSARY**, and **SOURCES**.

## Using it with the Gemini API

- At this size, put the whole knowledge base in the `system_instruction` along with
  `GEMINI_SYSTEM_PROMPT.md` and use Gemini's **context caching**, so you don't pay for the same
  ~12k tokens on every request. Retrieval or chunking only becomes worth it if the knowledge base
  grows a lot. If you do chunk it, split on the `<a id>` anchors so each chunk keeps its ID.
- Register your stock MCP as a function tool. GR-007 assumes the app, not the model, validates
  tickers and attaches timestamps.
- Refresh `REFERENCE-NUMBERS` every January from the IRS sources listed.

## Before you ship

- This is **general education**. Depending on your features and how you make money (subscriptions,
  ads, referrals), personalized output can count as investment advice under the Investment
  Advisers Act. Read GR-001 and get securities counsel before launch.
- Spot-check the playbook allocation ranges and the rules against the cited sources. They were
  researched quickly, in one ~14-minute pass.
