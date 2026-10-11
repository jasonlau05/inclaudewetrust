# fintech-references

## Synthesis

The admired products make complex financial or technical systems feel simple through **strong defaults, progressive disclosure, clear status, and visible control**—not by hiding important information. Their interfaces generally share:

1. **One obvious next action.**
2. **A calm overview before detailed data.**
3. **Plain-language explanations next to expert terminology.**
4. **Automation presented as reversible and inspectable.**
5. **Context, timestamps, sources, and limitations close to the claim.**
6. **Advanced features available without making beginners confront them immediately.**

For this investing-education assistant, copy the structure and transparency—not the engagement mechanics of trading apps.

## Patterns worth copying

### 1. Goal-first orientation instead of product-first navigation

Wealthfront and Betterment frame investing around outcomes such as retirement, education, or building wealth, then use a short set of questions to construct a portfolio. Wealthfront explicitly describes a flow in which users answer “a few questions” and receive a diversified portfolio based on their situation and goals. It also emphasizes automatic rebalancing and dividend reinvestment.

- **Copy:** Start with “What are you trying to accomplish?” rather than asking users to understand asset classes first.
- **Copy:** Keep the user’s goal visible as context in the chat.
- **Copy:** Explain automation in terms of what it does and what it does not do.
- **Avoid:** Implying that an automated result is guaranteed or individually suitable investment advice.

Sources:  
[Wealthfront Automated Investing](https://www.wealthfront.com/investing)  
[Betterment Investing](https://www.betterment.com/investing)

### 2. Progressive disclosure with a simple default and an inspectable explanation

Financial products reduce cognitive load by showing a high-level state first, then allowing users to inspect allocation, fees, methodology, and risks. Wealthfront’s product page follows this pattern: a simple benefit statement is followed by portfolio construction, customization, tax-loss harvesting, fees, insurance, and disclosures.

- **Copy:** Show a concise answer first: “For your situation, the main trade-off is…”
- **Copy:** Put “How I got this” or “See assumptions” in a collapsible section.
- **Copy:** Keep technical tool calls behind friendly summaries such as “Looked up VOO’s latest price and expense ratio.”
- **Avoid:** Hiding material caveats behind a disclosure that users cannot reasonably find.

This aligns with NN/g’s findings that trust depends on design quality, upfront disclosure, current content, and clear connections to credible external information. NN/g specifically warns that users dislike lengthy forms and that asking for information before providing value can damage trust.

Source: [NN/g — Trustworthiness in Web Design](https://www.nngroup.com/articles/trustworthy-design/)

### 3. A dashboard that answers “How am I doing?” before “What can I configure?”

Copilot Money and Monarch organize multiple accounts and financial concepts into a coherent overview: spending, budgets, investments, net worth, and goals. Their value proposition is aggregation and interpretation, not forcing the user to navigate each underlying account separately.

- **Copy:** Use a small number of overview cards: goal, available context, latest answer, and relevant market data.
- **Copy:** Present a “snapshot” before detailed tables.
- **Copy:** Use consistent labels and units across cards.
- **Copy:** Let users open a profile drawer to review or edit context without leaving chat.
- **Avoid:** Turning the profile into a permanent 300-pixel form sidebar full of schema codes.

Sources:  
[Copilot Money](https://www.copilot.money/)  
[Monarch features](https://www.monarchmoney.com/features)

### 4. Search and universal actions reduce navigation burden

Mercury highlights universal search for transactions, vendors, cards, and actions. Linear’s product philosophy also favors focused workflows, keyboard efficiency, and reducing operational friction. These are useful models for a chat product even though the domains differ.

- **Copy:** Make the chat composer the primary universal action: users can ask about a fund, a goal, or a concept without choosing a mode first.
- **Copy:** Add a few suggested prompts for common beginner tasks.
- **Copy:** Support keyboard submission and clear focus states.
- **Copy:** Use direct labels such as “Compare funds” or “Review my profile,” not clever category names.
- **Avoid:** Requiring users to understand the difference between “quote,” “fund info,” “performance,” and “news” before asking a question.

Sources:  
[Mercury](https://mercury.com/)  
[Linear Method](https://linear.app/method)

### 5. Educational context is part of the product, not a separate help center

Public combines investing products with a substantial learning area covering stocks, ETFs, retirement, bonds, options, and risk. This is a useful pattern for a beginner audience: education should appear at the point of confusion, not only in a separate navigation section.

- **Copy:** Add short “In plain English” explanations beside terms such as expense ratio, diversification, volatility, and tax efficiency.
- **Copy:** Offer follow-up chips such as “Explain expense ratio,” “Show the risks,” and “Compare with VTI.”
- **Copy:** Link to authoritative sources when a response depends on a rule, current figure, or fund document.
- **Avoid:** Using educational content as a disguised sales prompt or presenting an article link without explaining why it matters.

Source: [Public Learn](https://public.com/learn)

### 6. AI interfaces build trust through context and traceability

ChatGPT Search documents a particularly useful interaction pattern: responses may include inline citations, a Sources panel, and a warning that citations can be incomplete, outdated, or incorrect. Users are encouraged to open the source and verify important information.

Claude’s Projects provide another useful model: a bounded workspace with its own conversations, uploaded knowledge, and instructions. For this app, the financial profile functions as a lightweight, user-visible context layer.

- **Copy:** Show source names and links near factual claims.
- **Copy:** Include “As of [date/time]” for market data and “Source: [provider]” for fund facts.
- **Copy:** Distinguish retrieved facts from model interpretation.
- **Copy:** Let users inspect or edit the profile context used for an answer.
- **Copy:** Make tool activity understandable: “Checked VOO quote,” “Retrieved fund profile,” “Reviewed recent news.”
- **Avoid:** Raw JSON, token counts, internal function names, or a theatrical “thinking” transcript.
- **Avoid:** A citation icon that opens nothing, cites a search result rather than the underlying source, or gives the impression that every conclusion is verified.

Sources:  
[OpenAI — Searching the web with ChatGPT](https://help.openai.com/en/articles/9237897-chatgpt-search)  
[Claude — What are projects?](https://support.claude.com/en/articles/9517075-what-are-projects)

### 7. Calm visual hierarchy and restrained branding

Linear, Claude, Mercury, and Copilot demonstrate that a minimal product can still feel distinctive through typography, spacing, surfaces, and carefully chosen accent colors rather than dense decoration. Claude’s help center uses warm off-white surfaces, dark readable text, restrained borders, and moderate corner radii. Stripe’s dashboard design system similarly uses systematic color, spacing, typography, and states rather than arbitrary decoration.

- **Copy:** Use a neutral background, one calm accent, and semantic colors for success, warning, and error.
- **Copy:** Reserve strong color for actions, status, and important warnings.
- **Copy:** Use cards sparingly and group related content with spacing before adding borders.
- **Copy:** Use tabular numerals for prices, percentages, and performance figures.
- **Avoid:** Neon gradients, excessive glass effects, a card for every sentence, or making a finance product look like a casino or crypto-trading terminal.

Sources:  
[Linear Method](https://linear.app/method)  
[Claude Help Center](https://support.claude.com/en/)  
[Stripe Dashboard documentation](https://docs.stripe.com/dashboard/basics)

### 8. Make risk and uncertainty visually normal

The best finance products do not rely only on a reassuring visual tone. They disclose fees, account protections, investment risk, performance limitations, and the difference between historical and future results. Wealthfront, Betterment, and Public all place material disclosures near product claims.

- **Copy:** Put a short disclaimer below the composer or at the end of an answer, with a link or expandable longer version.
- **Copy:** Label data as “delayed,” “latest available,” or “as of [timestamp].”
- **Copy:** Use “may,” “could,” and scenario language where uncertainty is material.
- **Copy:** State when the assistant lacks information that could change the answer.
- **Avoid:** “Best stock,” “safe investment,” “you should buy,” or a single precise recommendation based on incomplete profile data.
- **Avoid:** Using green performance numbers as a persuasive success signal without showing period, benchmark, and risk.

Sources:  
[Wealthfront disclosures and investing information](https://www.wealthfront.com/investing)  
[Betterment investing information](https://www.betterment.com/investing)  
[Public disclosures](https://public.com/learn)  
[FINRA Rule 2210](https://www.finra.org/rules-guidance/rulebooks/finra-rules/2210)

## Product-specific lessons

| Product | Useful pattern | Do not copy blindly |
|---|---|---|
| Wealthfront | Short intake, goal-based portfolio, automation, visible fees and protections | Presenting automation or historical performance as certainty |
| Betterment | Goal planning and managed-investing framing for beginners | Overloading a simple goal with product upsells |
| Robinhood | Fast recurring-investment interaction and clear transaction-oriented flows | Engagement-first trading, urgency, frequent action prompts, or making investing feel like a game |
| Public | Investing education, plain-language resources, transparent product disclosures | Blurring education, product promotion, AI-generated analysis, and personalized advice |
| Copilot Money | Unified view of spending, investments, and net worth; clean categorization | Hiding the underlying assumptions behind automated categorization |
| Monarch | A comprehensive financial “home” organized around planning and overview | Exposing every advanced planning control at first run |
| Mercury | Fast task completion, clear money overview, universal search, strong operational feedback | Treating a broad feature catalog as the primary navigation |
| Stripe | Consistent dashboard primitives, status, tables, and systematized UI | Developer-oriented density and jargon in a beginner-facing app |
| Linear | Focus, speed, keyboard support, purposeful hierarchy, polished details | Assuming every user wants command palettes or keyboard shortcuts |
| ChatGPT | Conversational entry point, sources, citations, and flexible follow-up | Unqualified confidence or citations that users do not inspect |
| Claude | Bounded projects, persistent context, uploaded knowledge, focused workspaces | Letting invisible persistent context surprise users |
| Perplexity | Answer-first search with cited sources and source review | Treating a generated synthesis as equivalent to an authoritative source |
| Gemini | Familiar conversational interface and Google ecosystem context | Presenting “double-check” or search grounding as a guarantee of correctness |

## Recommended interaction model for this app

### Main screen

Use a three-part desktop layout:

- **Header:** product name, “Profile” button, status/data freshness indicator.
- **Conversation center:** welcome state, user messages, assistant answers, data cards, sources, follow-up chips.
- **Optional compact context rail:** only show the active goal and a few profile chips; hide the full intake.

On mobile, collapse the context rail into a profile drawer. Keep the composer fixed near the bottom, accounting for the on-screen keyboard.

### Empty state

The first screen should demonstrate value without requiring a full financial profile. Include three or four starter prompts:

- “What should I do with an extra $500 a month?”
- “How does VOO compare with VTI?”
- “Explain index funds like I’m new to investing.”
- “What information would help you answer my question?”

A small note should say that users can answer a few optional questions for more relevant education.

### Answer structure

Use this consistent anatomy:

1. **Short answer or takeaway**
2. **Why it may fit the stated goal**
3. **Trade-offs and risks**
4. **Relevant quote/comparison card**
5. **Assumptions and profile context**
6. **Sources and timestamps**
7. **Suggested follow-up chips**
8. **Short educational disclaimer**

Use “I don’t know” or “I need one more detail” when the available context is insufficient.

## Pitfalls to avoid

- **Raw developer UI:** schema IDs, tool-call JSON, token counts, API names, and debug logs.
- **False precision:** exact allocations or return forecasts when the user gave only rough information.
- **Hidden data freshness:** showing a quote without an as-of timestamp or delay label.
- **Color-only meaning:** green/red gain-loss states without text, icons, or signed values. WCAG requires that color not be the sole way to convey information.
- **Low-contrast minimalism:** gray text that looks elegant but is difficult to read. WCAG 2.2 AA requires at least 4.5:1 contrast for normal text and 3:1 for large text.
- **Over-onboarding:** collecting sensitive information before users receive any value.
- **Irreversible profile assumptions:** silently using an old income, goal, or risk preference.
- **Overconfident AI voice:** presenting generated explanations as professional advice or verified fact.
- **Engagement loops:** streaks, confetti, price alerts, “trending” pressure, or language designed to increase trading frequency.
- **Disclosure dumping:** a long legal block that obscures the answer. Use a short, readable warning plus expandable detail.
- **Decorative complexity:** excessive gradients, animations, charts, and cards that compete with the answer.

Sources:  
[W3C WCAG 2.2 — Use of Color](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html)  
[W3C WCAG 2.2 — Contrast Minimum](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)  
[FINRA Rule 2210](https://www.finra.org/rules-guidance/rulebooks/finra-rules/2210)