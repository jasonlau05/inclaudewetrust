# Minimal UI Specification for an AI Investing Assistant

**Working product name:** **ClearPath**  
**Positioning:** Calm, beginner-friendly investing education with transparent market data and sources.  
**Implementation constraint:** FastAPI + static vanilla HTML/CSS/JS, no build step, existing API unchanged.


> **For the engineer building this:** read section 0 first. It maps this spec onto the existing `app/` code (profile keys, prompt tweak for answer structure and follow-ups, tool-result fields for cards). Sections 1–8 are the researched design; section 0 wins on conflicts.

---

## 0. Read first: notes for this codebase

The research agents didn't see the backend, so this section pins the spec to what `app/` actually
does. Where it conflicts with sections 1–8, **this section wins**.

### 0.1 What the backend gives you (unchanged API)

- `GET /api/personas` → `[{id, label, ...profile keys}]`. There are 4 personas: "New grad (PB-002)",
  "Mid-career family", "Tech worker with RSUs (PB-007)", "Pre-retiree (PB-010)". Strip the
  `(PB-xxx)` codes from labels in the UI (`label.replace(/\s*\(PB-\d+\)/, "")`). Use these 4 as
  the demo quick-starts, not the 3 example personas in section 2.1.
- `GET /api/status` → `{model, thinking_level, tools:[{name}]}`. Treat `tools.length > 0` as
  "market data available". Never show the model name or tool names to users.
- `POST /api/chat` → `{reply, tool_calls:[{name, args, result}], tokens, elapsed_ms}`. It isn't
  streamed and takes 5–20 s. `reply` is Markdown (keep the already-loaded marked@12.0.2 +
  DOMPurify@3.1.6). Don't show `tokens` or `elapsed_ms` (optionally behind `?debug=1`).
- The profile is a free-form object. `app/advisor.py` JSON-dumps whatever keys you send and drops
  empty values, so **new keys are fine**.

### 0.2 Intake answers → profile keys

| Intake question (section 6) | Send as | Value |
|---|---|---|
| 1. Investing experience | `investing_experience` (new key) | the chip text, e.g. "Just getting started" |
| 2. Goal (up to 3) | `goals` | chips joined with "; " |
| 3. When you need the money | `time_horizon` (new key) | chip text, e.g. "3–10 years" |
| 4. Monthly amount | `contribution_capacity` | e.g. "$251–$500 per month" |
| 5. Cash for surprises | `cash_reserves` | e.g. "1–3 months of expenses" |
| 6. Reaction to a temporary loss | `risk_tolerance` + `loss_reaction` | avoid → `low`, small drop → `moderate`, larger drop → `high`, not sure → omit; also send the full chip text as `loss_reaction` |

"Not sure", "Prefer not to say" and Skip mean the key is **omitted** (blank = unknown; Gemini
asks for it when it matters). The profile drawer's **Optional details** holds the other existing
keys as plain inputs with friendly labels and no PS codes:

- **Work and income:** `age`, `life_stage`, `occupation`, `income`, `income_stability`
- **Savings and debts:** `essential_expenses`, `debts`, `employer_match`
- **Accounts:** `available_accounts`, `current_assets`, `tax_profile`, `retirement_plan`
- **Household:** `household_status`, `dependents`

Choosing a persona fills every key; the drawer shows them and the context strip summarizes
`goals`, `time_horizon` (or `age`) and `risk_tolerance`. Keep the profile in memory (and
optionally `sessionStorage`); don't claim it's private or deleted beyond that.

### 0.3 Answer structure and follow-up chips: a small prompt change, not an API change

The "answer anatomy" (section 3) comes from Gemini, so set it in the prompt. In `app/advisor.py`,
append to `APP_ADDENDUM`:

```text
- Format every answer for the app's UI:
  start with "**The short version**" (1–2 sentences), then "**Why**", "**What to watch**" and
  "**Next steps**" as short bullet lists (skip a section if it doesn't apply). Keep it to
  150–350 words unless a comparison needs more. Use a Markdown table for comparisons.
- The app always shows the short educational disclaimer under the input box, so don't repeat
  the full GR-004 disclosure. Do add a one-line warning when the answer covers performance,
  single stocks, leverage, options, crypto, or financial distress.
- End with exactly one line: "Follow-ups: <question> | <question> | <question>"
  (2–3 short questions the user might ask next, written in the user's voice).
```

On the frontend, before rendering the Markdown:

```js
// Split off the follow-up line and the knowledge-base IDs Gemini cites, e.g. "(R-012, PB-002)".
function splitReply(md) {
  const lines = md.trimEnd().split("\n");
  let followups = [];
  const last = lines[lines.length - 1] || "";
  if (/^follow-?ups:/i.test(last)) {
    followups = last.replace(/^follow-?ups:\s*/i, "").split("|").map(s => s.trim()).filter(Boolean).slice(0, 4);
    lines.pop();
  }
  const ids = new Set();
  const ID = /\s*\(((?:R|PB|GR|PS|MCP|RN)-[\w-]+(?:\s*,\s*(?:R|PB|GR|PS|MCP|RN)-[\w-]+)*)\)/g;
  const body = lines.join("\n").replace(ID, (_, list) => { list.split(/\s*,\s*/).forEach(i => ids.add(i)); return ""; });
  return { body, followups, ids: [...ids] };
}
```

Show the extracted IDs inside **How I got this** as "Guidance used: R-012, PB-002". That keeps
them out of the prose but still visible for transparency, which judges like. Follow-up chips send
their text as a new user message.

### 0.4 Tool calls → friendly summaries, cards and sources

`tool_calls[i].result` is a JSON string, an `"ERROR: …"` string, or JSON containing `"error"`.
`advisor.py` cuts it at **2,000 characters**, so a multi-symbol `get_quotes` can arrive cut off.
Always `JSON.parse` inside `try/catch`, and fall back to the summary line alone. (Optional
one-line backend change: raise `[:2000]` to `[:8000]` in `_tool_trace`.)

| Tool | Summary line in "How I got this" | Card / source to render | Result fields |
|---|---|---|---|
| `get_quotes` `{symbols}` | "Looked up prices for VOO, VTI" | One quote card per item in `quotes[]` | `symbol, name, type, exchange, currency, price, previous_close, change_pct_today, market_state, quote_time, data_delay_min, trailing_pe, forward_pe, dividend_yield_pct, beta, market_cap, sector, provider, retrieved_at` |
| `get_performance` `{symbol}` | "Checked VOO's past returns" | Returns row in the card or comparison table | `return_pct{1m,3m,ytd,1y}, annualized_return_pct{3y,5y,10y}, max_drawdown_pct, as_of, note` |
| `get_fund_info` `{symbol}` | "Checked VTI's fees and holdings" | Fee and top-holdings rows | `category, family, expense_ratio_pct, turnover_pct, top_holdings[{symbol,name,weight_pct}], top_sectors_pct, asset_classes_pct, provider, retrieved_at` |
| `get_news` `{query}` | "Read recent headlines about NVDA" | **Sources** list | `articles[{title, publisher, published, link}]` |
| any `error` / `ERROR:` | "Couldn't get data for XYZ, so I left it out" | none | `error` |

- **Data status label:** every quote is from Yahoo Finance and delayed. Show **DELAYED** when
  `data_delay_min > 0` or is missing, and never **LIVE**. Use `quote_time` (UTC ISO) formatted
  in the user's timezone: "As of 3:59 PM CT · Yahoo Finance".
- **Change:** compute from `price` and `previous_close` (or `change_pct_today`). Show sign,
  arrow and the word "Gain"/"Loss", as section 5 requires.
- **Sources:** news links, plus one "Market data: Yahoo Finance, retrieved <time>" row when
  any market tool ran. Knowledge-base citations come from the IDs in 0.3.
- If two or more symbols have quotes, render a comparison table (section 5) instead of
  separate cards.

### 0.5 Smaller fixes to sections 1–8

- **Dark mode:** the token block only switches on `[data-theme="dark"]`. On load, set it from
  `localStorage.theme`, else from `matchMedia("(prefers-color-scheme: dark)")`, and keep the
  header toggle. Keep the `@media (prefers-color-scheme: dark)` behavior the current
  `style.css` has.
- **Fonts:** load Inter from Google Fonts (`wght@400;500;600`) or use the system stack, as the
  token block says.
- **Product name:** "ClearPath" is a placeholder the spec invented, not a checked name. Swap in
  the team's name.
- **Stop button:** `/api/chat` isn't streamed. `AbortController` only stops waiting on the
  client; the server still finishes the call.
- **Keep:** `Enter` sends and `Shift+Enter` adds a new line (already in `app.js`); "New chat"
  resets the messages.

---

## 1. Design principles

1. **Give value before requesting detail.**  
   Let users ask a general question immediately. Offer the profile as an optional way to improve explanations, not as a gate. Progressive disclosure reduces novice complexity and preserves advanced options.  
   Source: [Nielsen Norman Group — Progressive Disclosure](https://www.nngroup.com/articles/progressive-disclosure/)

2. **Ask one understandable question at a time.**  
   Use a six-step intake with plain-language choices, ranges, Back, and Skip. Never expose schema codes or recreate the 18-field sidebar.  
   Source: [GOV.UK — Structuring forms](https://www.gov.uk/service-manual/design/form-structure)

3. **Teach rather than direct.**  
   Explain factors, alternatives, risks, and next steps. Avoid “buy,” “best for you,” precise allocations, urgency, and certainty. Favorable and unfavorable information must be balanced.  
   Source: [FINRA Rule 2210 — Communications with the Public](https://www.finra.org/rules-guidance/rulebooks/finra-rules/2210)

4. **Make context and automation inspectable.**  
   Show which profile facts, sources, and market lookups informed an answer. Keep raw tool calls, hidden prompts, token counts, and chain-of-thought out of the UI.  
   Source: [OpenAI — Searching the web with ChatGPT](https://help.openai.com/en/articles/9237897-chatgpt-search)

5. **Treat freshness and uncertainty as part of the data.**  
   Every market-sensitive value needs a source, period, timezone, and `LIVE`, `DELAYED`, `HISTORICAL`, or `UNAVAILABLE` label. Never fill failed lookups from memory.  
   Source: [Investor.gov — Investment Products](https://www.investor.gov/investing-basics/investment-products)

6. **Use calm hierarchy, not trading-app excitement.**  
   Prefer whitespace, readable typography, one restrained accent, and stable numbers. Avoid neon gradients, winner badges, confetti, streaks, and ticker-like motion.  
   Source: [Material Design 3 — Color System](https://m3.material.io/styles/color/system/overview)

7. **Accessibility is a release requirement.**  
   Use semantic HTML, keyboard support, visible focus, sufficient contrast, non-color status cues, screen-reader-safe updates, and 320px reflow.  
   Source: [W3C — WCAG 2.2](https://www.w3.org/TR/WCAG22/)

---

## 2. Screens and flow

### 2.1 First-run onboarding

Show onboarding on first visit, but keep **Skip setup and ask a question** visible from the start.

#### Welcome

- Heading: “Learn investing by asking questions.”
- Explain the value exchange and two-minute estimate.
- State that answers are optional, approximate ranges are enough, and profile details can be changed or cleared.
- Warn users not to enter passwords, account numbers, Social Security numbers, or brokerage credentials.
- Load demo personas from `GET /api/personas`.

#### Demo quick-starts

Show the four personas from `GET /api/personas` as cards (see 0.1): New grad, Mid-career family, Tech worker with RSUs, Pre-retiree.

Selecting one:

- Loads its data into the same editable profile model.
- Shows a persistent **Demo context** badge.
- Does not imply those details belong to the user.
- Provides **Reset demo context**.

Also show:

- **Set up my context**
- **Skip setup and ask a question**

#### Six-question stepper

Display one question per screen. Show `Question 2 of 6`, Back, Skip for now, and Continue. Never preselect an answer.

1. Investing experience
2. Goal
3. Time horizon
4. Approximate monthly amount
5. Emergency-savings position
6. Comfort with temporary losses

After question six, show a compact review with an Edit action per row. Primary CTA: **Start learning**.

Store normalized values behind existing API field names. If the current backend expects additional fields, keep them in the profile drawer under **Optional details** rather than first-run onboarding.

### 2.2 Main chat

Header:

- ClearPath wordmark
- Quiet label: “General investing education”
- **Profile** button
- **How this works** link
- Optional theme button

Conversation:

- Maximum reading width: `44rem`.
- Empty state contains four starter prompts and the composer.
- User messages are compact right-aligned bubbles.
- Assistant answers are document-like articles, not narrow speech bubbles.
- Show a small context strip only when context exists:
  - `Goal: retirement · Horizon: 10+ years · Risk comfort: moderate`
  - **Edit**
  - **Answer generally**

Composer:

- Sticky near the bottom without covering content.
- Multiline textarea and visible Send button.
- Enter sends; Shift+Enter adds a line break. Include this hint on desktop.
- Under it: short disclaimer and link to the full explanation.
- Do not force-scroll if the user is reading earlier content. Show **Jump to latest** instead.

Status from `GET /api/status`:

- Healthy: omit or show “Market data available” in quiet text.
- Unavailable: “Live market data is unavailable. General explanations still work.”
- Never expose server names, stack traces, MCP details, or provider credentials.

### 2.3 Profile drawer

Open from the header or context strip.

Contents:

1. “Your context” heading and explanation.
2. Human-readable profile summary.
3. Six editable intake sections.
4. **Optional details** disclosure containing any remaining existing API fields, grouped as:
   - Work and income
   - Savings and debts
   - Accounts and investing experience
   - Other goals
5. Toggle/action: **Answer without profile context**
6. **Save changes**
7. **Clear profile** with confirmation

Desktop: a 360px right-side drawer over the chat; do not restore a permanent sidebar.  
Mobile: a full-screen native `<dialog>` where practical.

### Desktop wireframes

```text
FIRST RUN
┌────────────────────────────────────────────────────────────────────┐
│ ClearPath                    General investing education   How it works
├────────────────────────────────────────────────────────────────────┤
│                                                                    │
│                 Learn investing by asking questions                │
│          Optional context helps tailor the explanation.            │
│                                                                    │
│  Demo quick-starts                                                 │
│  [New graduate] [Teacher saving] [Pre-retiree]                     │
│                                                                    │
│              ┌──────────────────────────────────────┐              │
│              │ Question 2 of 6                     │              │
│              │ What are you hoping to work toward? │              │
│              │ [Start investing] [Retirement]      │              │
│              │ [Emergency fund]  [Pay down debt]   │              │
│              │ [Not sure]                          │              │
│              │ Back     Skip for now      Continue │              │
│              └──────────────────────────────────────┘              │
│                   Skip setup and ask a question                    │
└────────────────────────────────────────────────────────────────────┘
```

```text
MAIN CHAT WITH PROFILE OPEN
┌─────────────────────────────────────────────────────────────────────────┐
│ ClearPath       General investing education       Profile  How it works │
├───────────────────────────────────────────────┬─────────────────────────┤
│ Goal: retirement · Horizon: 10+ years  Edit   │ Your context        [×]│
│                                               │                         │
│ Assistant                                     │ Goal                    │
│ ┌───────────────────────────────────────────┐ │ [Retirement        ▾]  │
│ │ The short version                         │ │ Timeline                │
│ │ ...                                       │ │ [10+ years         ▾]  │
│ │                                           │ │ Risk comfort            │
│ │ VOO / VTI comparison                      │ │ [Moderate          ▾]  │
│ │ [semantic comparison table]               │ │                         │
│ │                                           │ │ ▸ Optional details      │
│ │ ▸ How I got this                          │ │                         │
│ │ Sources                                   │ │ [Save changes]          │
│ │ [Compare fees] [Explain diversification]  │ │ Answer without context  │
│ └───────────────────────────────────────────┘ │ Clear profile           │
│                                               │                         │
│ ┌───────────────────────────────────────────┐ │                         │
│ │ Ask an investing question…          Send │ │                         │
│ └───────────────────────────────────────────┘ │                         │
│ Educational information only · How this works│                         │
└───────────────────────────────────────────────┴─────────────────────────┘
```

### Mobile wireframes

```text
┌──────────────────────────────┐
│ ClearPath            Profile │
├──────────────────────────────┤
│ Question 2 of 6              │
│                              │
│ What are you hoping to       │
│ learn or work toward?        │
│                              │
│ [Start investing]            │
│ [Retirement]                 │
│ [Build an emergency fund]    │
│ [Pay down debt first]        │
│ [Not sure]                   │
│                              │
│ [Continue]                   │
│ Back        Skip for now     │
│                              │
│ Skip setup and ask           │
└──────────────────────────────┘
```

```text
┌──────────────────────────────┐
│ ClearPath            Profile │
│ General investing education │
├──────────────────────────────┤
│ Goal: retirement · Edit      │
│                              │
│ Assistant · AI-generated     │
│ The short version            │
│ ...                          │
│                              │
│ [Quote/data card]            │
│                              │
│ ▸ How I got this             │
│ Sources                      │
│                              │
│ [Compare fees]               │
│ [What are the risks?]        │
│                              │
│                     You      │
│        How do VOO and VTI…   │
├──────────────────────────────┤
│ Ask a question…       [Send] │
│ Education only · Details     │
└──────────────────────────────┘
```

---

## 3. Assistant answer anatomy

Default length: **150–350 words**. Simple definitions may be 60–100 words; planning or comparison answers may reach 500–700 words when necessary.

Render each answer as an `<article>` in this order:

1. **Metadata**
   - “Assistant · AI-generated”
   - When applicable: “Using your stated retirement goal and 10+ year horizon for context.”
   - Include **Answer generally** and **Edit profile**.

2. **The short version**
   - One or two sentences answering the question.
   - Use conditional wording and avoid a buy/sell command.

3. **Why**
   - Two to four bullets tied to the user’s question and relevant stated context.

4. **What to watch**
   - Risks, fees, liquidity, taxes, missing facts, or uncertainty.
   - Put principal-risk language beside performance or product claims.

5. **Next steps**
   - Two or three educational actions, such as comparing expense ratios or checking when the money may be needed.

6. **Data cards or comparison table**
   - Only when live or historical data improves the answer.
   - Distinguish fact, historical result, estimate, and example.

7. **How I got this**
   - Native `<details>`, collapsed by default.
   - Show facts used, missing facts, assumptions, tool summaries, and lookup failures.
   - Examples:
     - “Looked up VOO’s latest available price.”
     - “Checked VTI’s expense ratio and holdings.”
     - “Compared historical five-year returns.”
     - “Reviewed recent fund news.”
     - “I couldn’t verify the current price, so I left it out.”
   - Never display raw JSON, internal function names, schema IDs, prompts, chain-of-thought, or token counts.

8. **Sources**
   - Two to five high-value links.
   - Show publisher, title, published/updated date when known, and accessed/data timestamp.
   - Prefer Investor.gov, FINRA, issuer prospectuses, filings, and the actual data provider.

9. **Follow-up chips**
   - Two to four context-specific prompts, such as:
     - “Compare fees”
     - “What are the main risks?”
     - “Explain diversification”
     - “What if I need the money in 3 years?”

10. **Disclosure**
    - Keep the persistent short disclaimer below the composer.
    - Add a contextual warning inside the answer when performance, leverage, options, crypto, financial distress, or recommendation-like questions make it material.

---

## 4. Design tokens

Ready to paste into `style.css`:

```css
:root {
  color-scheme: light;

  --font-sans: Inter, ui-sans-serif, system-ui, -apple-system,
    BlinkMacSystemFont, "Segoe UI", sans-serif;
  --font-mono: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;

  --text-xs: .75rem;
  --text-sm: .875rem;
  --text-md: 1rem;
  --text-lg: 1.125rem;
  --text-xl: 1.375rem;
  --text-2xl: 1.75rem;
  --text-3xl: 2.25rem;

  --leading-tight: 1.2;
  --leading-body: 1.5;

  --space-1: .25rem;
  --space-2: .5rem;
  --space-3: .75rem;
  --space-4: 1rem;
  --space-5: 1.25rem;
  --space-6: 1.5rem;
  --space-8: 2rem;
  --space-10: 2.5rem;
  --space-12: 3rem;
  --space-16: 4rem;

  --content-max: 44rem;
  --drawer-width: 22.5rem;
  --header-height: 4rem;
  --control-height: 2.75rem;

  --radius-sm: .375rem;
  --radius-md: .625rem;
  --radius-lg: .875rem;
  --radius-xl: 1.25rem;
  --radius-pill: 999px;

  --color-bg: #f7f8fa;
  --color-surface: #ffffff;
  --color-surface-subtle: #f1f4f2;
  --color-surface-selected: #e7f2ed;
  --color-overlay: rgb(23 33 29 / 48%);

  --color-text: #17211d;
  --color-text-muted: #52605a;
  --color-text-subtle: #68766f;
  --color-on-primary: #ffffff;

  --color-border: #d7dfda;
  --color-border-strong: #aebbb3;
  --color-primary: #176b52;
  --color-primary-hover: #0f513d;
  --color-primary-soft: #e7f2ed;
  --color-link: #245a73;

  --color-positive: #176b52;
  --color-positive-soft: #e7f2ed;
  --color-negative: #a33a35;
  --color-negative-soft: #fbeceb;
  --color-warning: #7a4d00;
  --color-warning-soft: #fff3d6;
  --color-info: #245a73;
  --color-info-soft: #e8f3f8;

  --color-focus: #245a73;
  --color-focus-soft: #b9dcea;
  --focus-ring: 0 0 0 3px var(--color-focus-soft);

  --shadow-sm: 0 1px 2px rgb(23 33 29 / 6%);
  --shadow-md: 0 6px 18px rgb(23 33 29 / 8%);
  --shadow-lg: 0 16px 40px rgb(23 33 29 / 14%);

  --duration-fast: 120ms;
  --duration-standard: 180ms;
  --duration-slow: 260ms;
  --ease-standard: cubic-bezier(.2, 0, 0, 1);
}

[data-theme="dark"] {
  color-scheme: dark;

  --color-bg: #101513;
  --color-surface: #17201c;
  --color-surface-subtle: #1d2823;
  --color-surface-selected: #203a30;
  --color-overlay: rgb(0 0 0 / 62%);

  --color-text: #f3f7f4;
  --color-text-muted: #b6c4bc;
  --color-text-subtle: #92a199;
  --color-on-primary: #0e2a20;

  --color-border: #3a4941;
  --color-border-strong: #617168;
  --color-primary: #83d2b1;
  --color-primary-hover: #a0e2c6;
  --color-primary-soft: #203a30;
  --color-link: #8dd6f0;

  --color-positive: #83d2b1;
  --color-positive-soft: #203a30;
  --color-negative: #ffb4ab;
  --color-negative-soft: #492321;
  --color-warning: #f3c56c;
  --color-warning-soft: #443414;
  --color-info: #8dd6f0;
  --color-info-soft: #17333d;

  --color-focus: #8dd6f0;
  --color-focus-soft: #315668;

  --shadow-sm: 0 1px 2px rgb(0 0 0 / 28%);
  --shadow-md: 0 8px 20px rgb(0 0 0 / 32%);
  --shadow-lg: 0 18px 44px rgb(0 0 0 / 44%);
}

* { box-sizing: border-box; }

html {
  font: 16px/var(--leading-body) var(--font-sans);
  background: var(--color-bg);
  color: var(--color-text);
}

body { margin: 0; }

button, input, textarea, select { font: inherit; }

:focus-visible {
  outline: 2px solid var(--color-focus);
  outline-offset: 2px;
  box-shadow: var(--focus-ring);
}

.numeric {
  font-variant-numeric: tabular-nums;
}

@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 1ms !important;
    animation-iteration-count: 1 !important;
    scroll-behavior: auto !important;
    transition-duration: 1ms !important;
  }
}
```

Use Inter via Google Fonts if desired; the system fallback is acceptable and faster.

---

## 5. Component specifications

### Buttons

- Minimum height: 44px; icon-only hit area: 44×44px.
- Primary: solid primary color.
- Secondary: surface with strong border.
- Tertiary: text plus hover surface; never an unlabeled icon.
- States: default, hover, pressed, focus-visible, loading, disabled.
- Loading keeps the label visible: “Sending…” rather than spinner-only.
- Disabled state remains readable and includes an explanation when needed.

### Chips

- Height: 36–44px; 12–14px horizontal padding; pill radius.
- Use real radio/checkbox inputs with visually styled labels for intake.
- Selected state combines fill, border, and checkmark—not color alone.
- Prompt chips submit their visible text as a normal message.
- States: default, hover, focus, selected, disabled, pending.
- On mobile, wrap intake choices; follow-up chips may horizontally scroll in a labeled region.

### Inputs

- Visible label above the control; placeholder is supplementary.
- Height: 44–48px; 12px padding; strong border.
- Provide helper text before errors.
- Error state uses `aria-invalid`, text beginning with “Error:”, and `aria-describedby`.
- Preserve entered values after validation or API failure.

### Intake step

- Centered width: 36rem maximum.
- Native `<fieldset>` and `<legend>`.
- Progress shown visually and as text.
- Back, Skip, and Continue remain in predictable locations.
- Changing steps updates the heading and announces “Question N of 6.”
- Skipping is never treated as an error.

### Message bubbles

- User: right-aligned, primary-soft background, maximum 80% desktop/90% mobile.
- Assistant: full reading column with normal document structure.
- Label each article “You” or “Assistant.”
- Use headings, lists, links, tables, and `<details>` inside assistant answers.
- Do not put long answers in oversized rounded bubbles.

### Quote/data card

Show:

- Name, ticker, and plain-language instrument type.
- Price or NAV with currency.
- Change as signed dollars, percentage, arrow, and “Gain,” “Loss,” or “No change.”
- Period, market state, data status, timestamp, timezone, and provider.
- Visible risk line and “Not for trade execution.”
- Optional sparkline only with a period label, endpoint values, and text summary.

Example:

```text
Vanguard Total Stock Market ETF · VTI
ETF — holds many U.S. companies
$286.41
Gain ↑ +$1.24 (+0.62%) today
DELAYED · As of Jun 12, 2025, 4:00 PM ET · Source: [provider]
Past performance is not guaranteed. Investments can lose value.
```

Format values with `Intl.NumberFormat` and tabular numerals.

### Comparison table

- Initially show five to eight rows: what it owns, holdings, fund fee, return period, volatility explanation, and benchmark.
- Use `<table>`, visible `<caption>`, `<thead>`, and scoped row/column headers.
- Right-align numeric cells and use consistent precision.
- Show “Not available” rather than dropping a field.
- No winner badge.
- On mobile, place horizontal scrolling around the table with a visible label; keep the first column sticky if practical.

### Loading/thinking indicator

- Immediately append the user message and a stable assistant placeholder.
- Visible text: “Thinking about the trade-offs…”
- At 8–10 seconds: “Still working—live-data questions can take a little longer.”
- Use a polite status region; do not announce animation or every streamed token.
- If supported, provide Stop using `AbortController`.
- Do not show fake percentages or claim a lookup is happening unless the API reports it.

### Error

- Render within the affected assistant turn.
- Preserve the question and prior conversation.
- Show a specific recovery action:
  - **Try again**
  - **Answer without live data**
  - **Choose the correct ticker**
- Do not display stack traces, response JSON, or endless automatic retries.

### Disclaimer banner

- Quiet text below the composer; not a large blocking banner.
- `How this works` opens the long explanation.
- Use a stronger inline warning next to complex products, historical performance, estimates, or distress-related content.
- Never rely on a disclaimer to correct recommendation-like behavior.

### Financial-distress support card

If the user explicitly describes inability to pay essentials, eviction, utility shutoff, overwhelming debt, or investing borrowed money:

- Pause investing suggestions.
- Acknowledge the difficulty without judgment.
- Prioritize essentials and general support options.
- Link to [CFPB Behind on Bills](https://www.consumerfinance.gov/consumer-tools/behind-on-bills/) and [CFPB Credit Counseling](https://www.consumerfinance.gov/consumer-tools/credit-counseling/).
- Do not infer distress from profile values alone.
- If the user expresses self-harm or immediate danger, stop the investing flow and present localized crisis support; in the US include [988 Lifeline](https://988lifeline.org/).

---

## 6. Copy deck

### Product and headings

- Product: **ClearPath** or `[Product name]`
- Tagline: **Investing questions, made clearer.**
- First-run heading: **Learn investing by asking questions.**
- Main empty-state heading: **What would you like to understand?**
- Profile heading: **Your context**
- Answer headings:
  - **The short version**
  - **Why**
  - **What to watch**
  - **Next steps**
  - **How I got this**
  - **Sources**

### Intake introduction

> Answer a few optional questions so explanations can use examples closer to your situation. This takes about two minutes. Rough ranges are enough, and you can skip or change anything later.

> Please don’t enter passwords, account numbers, Social Security numbers, or brokerage credentials.

### Intake questions and choices

1. **What best describes your investing experience?**  
   `Just getting started` · `Some experience` · `I invest regularly` · `Not sure`

2. **What are you hoping to learn or work toward?**  
   `Build an emergency fund` · `Start investing` · `Retirement` · `A major purchase` · `Understand funds or stocks` · `Pay down debt first` · `Not sure`  
   Allow up to three choices.

3. **When might you need this money?**  
   `Within 1 year` · `1–3 years` · `3–10 years` · `10+ years` · `No specific timeline` · `Not sure`

4. **About how much could you set aside each month?**  
   `$0` · `$1–$50` · `$51–$250` · `$251–$500` · `$500+` · `It varies` · `Prefer not to say`

5. **How much cash do you currently have available for surprises?**  
   `Less than 1 month of expenses` · `1–3 months` · `3–6 months` · `6+ months` · `Not sure` · `Prefer not to say`

6. **If an investment temporarily lost value, which sounds most like you?**  
   `I’d want to avoid losses` · `I could accept a small drop` · `I could accept a larger drop for possible long-term growth` · `Not sure`

### Empty-state prompts

- “I’m new to investing. What should I learn first?”
- “What should I consider before investing an extra $500 a month?”
- “How do VOO and VTI differ in plain English?”
- “How much emergency savings should I consider before investing?”
- “What’s the difference between an ETF and a mutual fund?”
- “What information would help you answer my question?”

### Loading copy

- “Thinking about the trade-offs…”
- “Putting together a plain-language explanation…”
- “Still working—live-data questions can take a little longer.”
- “Answer ready.”

### Error copy

- General: **“We couldn’t get a response. Your question is still here—check your connection and try again.”**
- Live data: **“Current market data is unavailable. I can explain the comparison without guessing at today’s price.”**
- Ambiguous ticker: **“I found more than one match for ‘ABC.’ Which company or fund did you mean?”**
- Status endpoint: **“Live market data is unavailable. General explanations still work.”**
- Timeout: **“This is taking longer than expected. You can keep waiting or try again without losing your question.”**

### Disclaimers

**Short**

> Educational information only—not personalized financial, tax, or legal advice. Investing involves risk, including possible loss. Verify important information before acting.

**Long**

> This AI assistant provides general investing education, not individualized financial, tax, or legal advice. It may misunderstand your question, omit important facts, or provide outdated or incorrect information. Market data may be delayed and is not for trade execution. The assistant cannot determine what is suitable for you or account for your complete circumstances. Verify important facts with authoritative sources, review official fund documents, and consider a qualified professional before making consequential decisions. Past performance does not guarantee future results.

---

## 7. Accessibility checklist

Target **WCAG 2.2 AA**.

- Add a skip link to `<main>`.
- Use semantic header, main, forms, headings, articles, lists, details, dialog, and tables.
- Use one descriptive `<h1>` per visible screen and logical nested headings.
- Every control has a visible label; icon-only controls have accessible names.
- Intake choices use native radio/checkbox inputs inside fieldsets.
- Normal text contrast is at least 4.5:1; large text and meaningful UI boundaries at least 3:1.
- Gains, losses, risk, errors, data status, and selected states are not conveyed by color alone.
- All controls work by keyboard, with no positive `tabindex`.
- Visible focus appears in light and dark themes and is not hidden by the composer.
- Primary touch targets are 44×44px or larger; never below WCAG’s 24×24px minimum without an allowed exception.
- Chat uses a pre-existing polite live region. Announce “Assistant is thinking” and completion, not every token.
- Keep focus in the composer after submit; do not move it to each new answer.
- Provide **Jump to latest** instead of forced scrolling when the user is reading older content.
- Mobile profile uses a proper modal dialog: focus enters it, Tab stays inside, Escape closes it, and focus returns to the trigger.
- Errors identify the field/problem in text, use `aria-invalid`, and preserve values.
- Comparison tables use captions and scoped headers.
- Charts include a visible summary and textual data alternative.
- Content reflows at 320px and 400% zoom except the contained comparison table.
- Do not disable pinch zoom.
- Respect `prefers-reduced-motion`; remove animated chart drawing, sliding, and pulsing.
- Test keyboard-only use, VoiceOver/NVDA, dark mode, grayscale, 320px width, 200–400% zoom, API failure, long answers, stale data, and skipped profile fields.

---

## 8. Build plan

### 0–10 minutes: inventory the current API

In `app.js`, record the existing:

- `POST /api/chat` request shape and required profile keys
- Answer field
- Tool-call/source fields
- Error behavior
- Persona and status response shapes

Create adapters rather than changing the backend:

```js
normalizePersonas(data)
normalizeStatus(data)
buildChatPayload(state)
normalizeChatResponse(data)
summarizeToolCall(tool)
```

### 10–30 minutes: rebuild `index.html`

- Add skip link and semantic header/main.
- Add onboarding welcome, persona area, and one reusable step container.
- Add empty state, context strip, message log, composer, polite status region, and disclaimer.
- Add a native `<dialog>` for the profile.
- Keep existing backend field names in `name` or `data-field` attributes.
- Remove schema codes, debug panels, JSON dumps, and token counts.

### 30–50 minutes: implement `style.css`

- Paste the token block.
- Build mobile-first layouts for onboarding, chat, drawer, cards, tables, and composer.
- Add desktop breakpoint around 800px.
- Add focus, selected, loading, disabled, error, and dark-theme states.
- Keep the conversation centered and the drawer hidden until invoked.

### 50–80 minutes: implement state and API wiring in `app.js`

Use one state object:

```js
const state = {
  view: "onboarding",
  step: 0,
  profile: {},
  demoPersona: null,
  messages: [],
  pending: false,
  status: null
};
```

On startup:

```js
await Promise.all([
  fetch("/api/personas"),
  fetch("/api/status")
]);
```

- Render personas through `normalizePersonas`.
- Map friendly intake values to existing backend keys.
- Send the unchanged required payload to `POST /api/chat`.
- Add pending assistant placeholders, timeout copy, retry, and optional abort.
- Keep profile in session memory by default unless existing retention is explicitly disclosed.
- Never place unsanitized API text into `innerHTML`.

### 80–100 minutes: answer and data rendering

- Render assistant Markdown with pinned versions of **Marked + DOMPurify** only if Markdown is already returned.
- Otherwise use safe DOM creation and `textContent`.
- Convert tool metadata into friendly summaries.
- Render reusable quote cards, source rows, disclosures, and semantic comparison tables.
- Format numbers with `Intl.NumberFormat`.
- Only show freshness fields actually supplied by the backend.

### 100–120 minutes: polish and rehearsal

- Test all persona quick-starts and demo prompts.
- Test profile Skip, Back, Edit, Clear, and Answer generally.
- Test `/api/status` and chat failures.
- Test long answers, missing sources, failed lookups, narrow screens, dark mode, keyboard-only navigation, and focus restoration.
- Remove console logs, placeholders, dead controls, and developer terminology.
- Pin any CDN dependency versions.

### Do not

- Do not change endpoint paths or request/response contracts.
- Do not require profile completion before chat.
- Do not expose all 18 fields on first run.
- Do not show schema IDs, raw tool JSON, MCP payloads, token counts, prompts, or stack traces.
- Do not render unsanitized model output.
- Do not call delayed data “live.”
- Do not invent timestamps, sources, confidence percentages, or progress percentages.
- Do not show a winner badge, “best for you,” “safe investment,” or a buy/sell command.
- Do not use green/red alone for gains and losses.
- Do not add a charting library, authentication, routing, or a CSS framework during this pass.
- Do not use Tailwind Play CDN for the final demo.
- Do not add confetti, streaks, alerts designed to encourage trading, or animated prices.
- Do not claim profile data is private, encrypted, secure, or deleted unless the implementation proves it.
- Do not let a disclaimer substitute for fair, balanced, educational output.