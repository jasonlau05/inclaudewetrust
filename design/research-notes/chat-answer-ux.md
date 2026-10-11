# AI chat UX patterns for advice-like investing education

## Recommendation in one sentence
Use a calm, answer-first conversation: give a short plain-language takeaway, show only the most relevant supporting detail, make uncertainty and assumptions visible, and put technical evidence/tool activity behind clearly labeled progressive disclosure. The assistant should teach users how to think about a decision—not present a confident buy/sell command.

## 1. Answer anatomy

A beginner should be able to understand the first screenful without reading a long essay. A useful default response is **150–350 words**, with a compact answer around **60–100 words** for simple definition questions and up to **500–700 words** only for comparisons or planning questions. Avoid an arbitrary character cutoff if a table, quote card, or source list is needed; keep the prose short and let the user request more detail.

Recommended order:

1. **One-sentence takeaway** in a visually distinct summary block. Use conditional language: “For your stated goal, a broad, low-cost fund may be a reasonable place to learn more; the right choice depends on time horizon, risk, fees, and account type.” Do not headline a ticker or imply certainty.
2. **Why this may fit** — 2–4 bullets tied to the user’s stated goal, horizon, risk comfort, and constraints. Label profile-derived assumptions explicitly, for example “Based on what you shared: 10+ year horizon; emergency savings not confirmed.”
3. **Trade-offs / risks** — 2–4 bullets, including what could go wrong, liquidity/tax/fee considerations where relevant, and what information is missing. Never make color or a positive tone the only indication of risk.
4. **A small next-step checklist** — usually 2–3 actions the learner can take, such as “compare expense ratios,” “check whether this is an emergency-fund dollar,” or “read the fund prospectus.” For high-stakes decisions, suggest consulting a qualified professional rather than escalating confidence.
5. **Optional data card(s)** — only when the question calls for live data or comparison. Show the metric, units, period, and “as of” timestamp; distinguish historical data from a forecast.
6. **How I got this** disclosure — collapsed by default, with a friendly summary of searches/tools and the key assumptions. Never expose raw tool-call JSON, internal schemas, token counts, chain-of-thought, or implementation IDs.
7. **Sources** — a small, readable list of authoritative links with source name, page title, URL, and publication/updated date when available. For live market values, show the data timestamp and provider.
8. **Suggested follow-ups** — 2–4 chips at the bottom, tailored to the answer.
9. **Short disclaimer** — persistent but quiet below the answer or in the composer area; use a longer version in the first-run education screen and in high-risk responses.

Use headings that sound like a teacher, not a terminal: “The short version,” “Why,” “What to watch,” and “Next steps.” Define jargon at first use (“expense ratio = the fund’s annual operating cost”) and make a longer explanation available through “Explain this” or an accordion. This follows progressive disclosure: show the few important options first and reveal specialized detail on request. NN/G reports that this reduces novice complexity and errors while retaining power for advanced users: https://www.nngroup.com/articles/progressive-disclosure/ . Its chatbot research also found that users value both selectable options and free text, and that systems should be transparent that the user is talking to a bot: https://www.nngroup.com/articles/chatbots/ .

For investing education, the response should reflect the SEC’s basic framing: products differ by goals, time horizon, risk tolerance, fees, diversification, and liquidity; all investments involve risk and can lose money. Source: https://www.investor.gov/investor-tools/investing-basics/investment-products (the page is also available at https://www.investor.gov/introduction-investing/investing-basics/investment-products ).

## 2. Conversation behavior and answer length

- **Answer the question before asking for more profile data.** If a missing fact materially changes the answer, provide a useful general explanation first, then ask one focused question: “The key missing detail is when you’ll need the money—under 3 years, 3–10 years, or 10+ years?”
- **Ask at most one or two clarifying questions per turn.** Offer “Not sure” and “Skip for now.” Do not block a learner behind an exhaustive financial form.
- **Separate education from recommendation-like language.** Prefer “Here are the factors to compare” and “One way to think about it” over “You should buy.” If the user asks for a definitive allocation, explain the limits of the product and provide a framework/checklist.
- **Use calibrated uncertainty.** Say “I don’t have enough information,” “this data may be delayed,” or “historical performance does not predict future results” when applicable. Mark estimates and scenarios as such.
- **Keep each message scannable.** One idea per paragraph; bullets for trade-offs; a table only for genuinely comparable fields. Offer “Show more detail” rather than placing an encyclopedia in the initial response.
- **Do not repeat the entire profile in every turn.** Show only the profile facts used for this answer in a small “Using your context” line, with an “Edit profile” action.

These choices support NN/G’s heuristic of visibility of system status and match between system language and the real world: https://www.nngroup.com/articles/ten-usability-heuristics/ . Clear, plain-language supplemental summaries are also consistent with WCAG’s guidance to make complex text easier to understand: https://www.w3.org/WAI/WCAG22/Understanding/reading-level.html .

## 3. Streaming and loading for 5–20-second answers

### Preferred behavior
Use progressive response rendering if the backend/API supports it safely:

1. **0–200 ms:** add the user message immediately, disable duplicate submit, preserve the composer text until the request is accepted, and insert an assistant placeholder.
2. **200 ms–2 s:** show a compact status row: “Thinking about your question…” with a subtle nonessential animation. Keep the input available for cancellation if feasible.
3. **During tool work:** replace generic status with truthful, high-level stages, e.g. “Checking current fund information…” then “Putting the comparison together…”. Do not reveal search queries, private profile fields, hidden prompts, or raw tool payloads. Do not claim a source was consulted until it was actually returned.
4. **As text arrives:** stream coherent chunks, not one character at a time. Prefer sentence/paragraph boundaries so the answer does not constantly reflow. Keep the summary near the top; if the model cannot know the summary until completion, show a skeleton summary then reveal the final answer when complete.
5. **At completion:** announce “Answer ready,” restore the send button, focus only when it will not disrupt reading (normally do not steal focus), and scroll to the new answer only if the user was already at the bottom. Add sources and follow-up chips after the main prose.
6. **At 8–10 seconds:** if still running, provide a reassuring but honest update: “This is taking a little longer while I check live data. You can wait or try again without losing your question.” Add a visible **Stop** action. At 20 seconds, offer retry/cancel; never leave an indefinite spinner.

### If streaming is not available
Use a stable assistant skeleton with the eventual height approximate enough to avoid layout jumps, a determinate-looking stage list (not fake percentage progress), and rotating messages only when each describes a real stage. Keep the user’s question visible. Provide “Cancel” and, after a timeout, “Try again.” Preserve prior messages and avoid replacing the whole transcript with a blank loading page.

Material distinguishes progress indicator patterns and gives guidance for determinate/indeterminate progress: https://m3.material.io/components/progress-indicators/overview . NN/G’s response-time guidance recommends immediate feedback and communicating progress during waits: https://www.nngroup.com/articles/response-time-3-important-limits/ . W3C treats waiting, progress, completion, and errors as status messages that should be programmatically conveyed without unnecessarily moving focus: https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html . Implement the status node with `role="status"` or an appropriately polite live region; do not put every streamed token in an assertive live region, which would make a screen reader unusably chatty.

### Loading copy
Use human, specific, non-anthropomorphic copy:

- “Thinking about the trade-offs…”
- “Checking current fund information…”
- “Comparing fees and diversification…”
- “Writing a plain-language explanation…”
- “Still working—live-data questions can take a little longer.”
- “I couldn’t finish that lookup. Your question is still here—try again.”

Avoid “guaranteed,” fake progress percentages, “just a second,” or an animated stream that implies the model has reached a conclusion when it has not.

## 4. Empty state and starter prompts

The empty state should explain what the assistant does, set the education-only boundary without sounding punitive, and demonstrate the kinds of questions beginners can ask. A useful layout is a short welcome plus 4–6 large starter cards, then a smaller “or type your own question” composer.

Suggested heading: **“Learn investing by asking questions.”**

Suggested subcopy: **“I can explain investing concepts, compare information, and help you build a checklist. I’m an educational tool—not a financial adviser, and I can be wrong.”**

Starter prompts should be concrete and represent different intents:

- “I’m new to investing. What should I learn first?”
- “How much emergency savings should I keep before investing?”
- “What’s the difference between an ETF and a mutual fund?”
- “How do VOO and VTI differ in plain English?”
- “What should I compare before choosing a fund?”
- “I have $500 a month. What questions should I ask before investing it?”

For a demo, add clearly labeled persona quick-starts such as **“New graduate,” “Teacher building retirement savings,”** and **“Pre-retiree comparing options.”** Selecting one should populate demo context, not silently claim that it is the user’s real profile; show a “Demo context” badge and a reset action.

Do not present starter prompts as recommendations or prefill a high-risk trade. Keep free text available: NN/G’s chatbot study found that people appreciate predefined options but also need flexibility to deviate: https://www.nngroup.com/articles/chatbots/ .

## 5. Suggested follow-up chips

Show 2–4 chips after an answer, generated from the answer’s unresolved decisions. They should be short, tappable questions, not generic marketing CTAs:

- “Explain that term”
- “Show a simple example”
- “Compare fees”
- “What are the main risks?”
- “What if I need the money in 3 years?”
- “Use my profile” / “Change my time horizon”
- “Show the sources”
- “Ask a different question”

For a fund comparison: **“Compare diversification,” “Compare expense ratios,” “What does ‘index’ mean?”** For a monthly-savings question: **“Start with emergency savings,” “Show conservative/middle/aggressive scenarios,” “What information is missing?”**

Chips should submit the represented text as a normal user message, remain visible in transcript history, support keyboard focus, and have clear pressed/disabled/loading states. Avoid more than one horizontal row on mobile; wrap or use a horizontally scrollable region with an accessible label.

## 6. Profile context without creepy personalization

Profile context is useful only when the user can see and control it. Provide:

- A compact header control such as **“Using your context”** with 2–3 relevant tags: “Goal: retirement · Horizon: 10+ years · Risk comfort: moderate.”
- A tooltip or popover saying: “These details help tailor explanations. You can edit or remove them.”
- An **Edit profile** action opening a labeled drawer/dialog; never make the user hunt through raw schema fields.
- A per-message disclosure when context materially affects the answer: “I used your long-term goal and moderate risk comfort. I did not use income because you skipped it.”
- A one-tap **“Answer generally”** control for sensitive questions.
- A clear distinction between user-provided information, inferred assumptions, and live data.
- Masking or omission of sensitive dollar amounts in the visible chat summary unless the user explicitly chose to show them.

Do not imply that profile context makes the output personalized financial advice or that it is stored securely unless the product actually implements and can explain that protection. For a profile drawer using a modal dialog, move focus into it, trap focus while open, close on Escape, and return focus to the invoking button; W3C APG guidance: https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/ .

## 7. Sources and citations

Treat sources as part of the answer, not as a developer console. Use two layers:

- **Inline citations or superscript source markers** immediately after claims that depend on external material or live data. The marker should be a normal keyboard-focusable link or button with an accessible name, e.g. “SEC, Investment Products.”
- A **Sources** section at the end with 2–5 high-value links. Each row includes source name, page title, direct URL, date published/updated if known, and “accessed” or “data as of” time for live values. Prefer SEC/Investor.gov, FINRA, fund issuer prospectuses, exchange/provider data, and original research over SEO summaries.

For a quote or price card, show **“$X.XX · as of 3:42 PM ET · data may be delayed”** and a source link. For historical performance, show the period and whether the figure is total return or price return; do not let a sparkline stand in for an explanation.

A collapsed disclosure can say:

> **How I got this**  
> I used your stated goal and time horizon, looked up current fund information, and compared fees and holdings. Market data is from [provider], as of [time]. I did not use information you skipped.

Then expand to list tool categories and results, not implementation details:

- “Looked up VOO price and fund details.”
- “Checked VTI holdings and expense ratio.”
- “Used SEC education material about risk and diversification.”

If a lookup fails, say **“I couldn’t verify the current price, so I left it out”** rather than filling the gap from memory. OpenAI’s current ChatGPT search documentation is a useful example of source presentation: responses may include citations, users can select them to open the source, and the product warns that citations can be incomplete/outdated/incorrect and should be checked: https://help.openai.com/en/articles/9237897-chatgpt-search .

## 8. Errors, uncertainty, and safety copy

Keep errors in the affected assistant turn, preserve the user’s message, and offer a specific recovery action:

- **Temporary/API error:** “I couldn’t complete that answer right now. Your question is saved. Try again.” `[Try again]`
- **Live data unavailable:** “I can explain the comparison, but current market data is unavailable. I won’t guess at today’s price.” `[Answer without live data]`
- **Ambiguous ticker:** “I found more than one match for ‘ABC.’ Which company or fund did you mean?”
- **Insufficient context:** “I can give general education now. To compare the options more meaningfully, what is your time horizon?” `[Under 3 years] [3–10 years] [10+ years] [Skip]`
- **Potentially urgent financial distress:** “If this involves overdue bills, housing, or immediate access to cash, investing may not be the first step. Consider a qualified nonprofit counselor or trusted professional; I can help make a questions-to-ask list.” Avoid judgment and do not suggest a speculative product.

A disclaimer should be visible but not repeated as a wall of text in every message:

- **Short:** “Educational information only—not financial, tax, or legal advice. Investing involves risk, including possible loss. Check current sources and consider a qualified professional for decisions about your situation.”
- **Long / first run:** “This assistant provides general investing education, not financial, tax, or legal advice. It may make mistakes and market data may be delayed. It does not know everything about your circumstances. Verify important facts with authoritative sources, review a fund’s official documents, and consider a qualified professional before acting. Never invest money you may need soon, and remember that past performance does not guarantee future results.”

The SEC’s investor education material supports explicitly discussing risk, fees, diversification, liquidity, and the fact that products should be evaluated against goals, horizon, and risk tolerance: https://www.investor.gov/investor-tools/investing-basics/investment-products .

## 9. Minimum implementation checklist

- Render user and assistant messages as semantic sections with headings, lists, tables, links, and code-free friendly tool summaries.
- Keep a `pending` assistant message in the transcript so 5–20-second waits are visible and recoverable.
- Use one polite live status region for stages and completion; do not stream every token to assistive technology.
- Disable duplicate sends while pending, but provide Stop/Cancel and preserve the typed question.
- Auto-scroll only when the user is near the bottom; show a “New answer” jump control otherwise.
- Add a source list model that stores URL, title, publisher, timestamp, and citation relationship; never render untrusted URLs as unsanitized HTML.
- Label profile-derived statements and expose “Answer generally” and “Edit profile.”
- Make all chips, source links, accordions, Stop, Retry, and “How I got this” controls keyboard accessible; ensure visible focus and touch targets. WCAG status messages: https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html ; focus visibility: https://www.w3.org/WAI/WCAG22/Understanding/focus-visible.html ; target size minimum: https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html .
- Respect `prefers-reduced-motion` for typing indicators and transitions: https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html .
- Test with long answers, no sources, stale data, tool failure, ambiguous tickers, skipped profile fields, mobile width, keyboard-only navigation, zoom, and a screen reader.

### Avoid

Raw JSON/tool traces; token counts; fake progress bars; an unexplained “AI is thinking” black box; forced onboarding before a useful answer; a profile recap on every turn; confident buy/sell imperatives; unsupported current prices; source dumps with no relationship to claims; infinite spinners; automatic focus jumps; and color-only risk or gain/loss cues.