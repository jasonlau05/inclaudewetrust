# trust-compliance-ux

## Design position

Make the boundary visible at the moments when a user could mistake an explanation for a recommendation, but keep the default chrome quiet. A short persistent status (“General investing education · not personalized advice”) plus contextual disclosures is more usable than a large disclaimer on every screen. Disclosures do not, by themselves, cure advice-like behavior: the product should also avoid buy/sell/hold directives, certainty, urgency, or an implied ability to determine what is suitable for this individual.

This is a product/UI recommendation, not a legal conclusion. FINRA rules directly govern FINRA members and associated persons; the team should obtain securities-law/privacy review before launch, especially if the app is connected to a broker, receives compensation, or recommends particular securities.

## Minimal UI pattern

### 1. Persistent but low-noise boundary

* Put “General education—not personalized financial advice” in the app header or immediately above the composer, with an adjacent “How this works” link. Keep it readable on mobile and do not hide it solely in a footer.
* The one-time explainer can say: “This assistant explains investing concepts and compares information. It does not know your complete financial situation, cannot determine what is suitable for you, and does not place trades. AI can be wrong. Verify important information with primary sources or a qualified professional.” Allow the user to reopen it from Help/About.
* At onboarding, explain why profile questions are optional and how they affect wording/context. Do not require an acknowledgment on every message; use a stronger confirmation only before any external action (if actions are ever added).
* When the user supplies personal facts or asks “What should I do?”, place a compact contextual line directly above the answer: “Using the information you shared for context only—this is general education, not a recommendation for you.” The answer should then present considerations, alternatives, assumptions, and questions to discuss with a professional—not a personalized conclusion.
* Avoid labels such as “your plan,” “best investment for you,” “recommended allocation,” or “AI financial advisor.” Prefer “education,” “illustration,” “comparison,” and “questions to consider.”

### 2. Risk disclosure where the risk is encountered

Use progressive disclosure, but never make material risk depend on a buried modal or a hover state.

* For every security/fund/product card, show a visible “Risks” row next to the product name or key claim. Include the relevant risks in plain language: loss of principal, volatility, concentration, liquidity, fees/expenses, tax consequences, leverage/options/crypto complexity, or tracking error as applicable.
* Put the principal-risk sentence beside performance, return projections, rankings, and comparisons—not several screens away. Example: “Past performance is not a guarantee. Prices can fall, and you could lose money.” Link “More about risks” to a concise detail drawer with sources and assumptions.
* Make favorable and unfavorable information equally findable and visually comparable. Do not use green “opportunity” styling for one side and muted microcopy for the risk side. Do not imply a product is safe because it is diversified or because the answer sounds confident.
* For a high-risk or complex topic, show a short interruptive callout before the explanation: “Options can lose the entire premium and may create obligations beyond the amount paid. This is an overview, not trading instruction.” Keep the full risk detail one tap away.
* For calculators or hypothetical illustrations, show inputs, time horizon, fees, inflation/tax treatment, and a range or uncertainty statement. Never present an estimate as a forecast or likely outcome without support.

FINRA Rule 2210 is a useful minimum design standard even when it is not technically applicable to this prototype: communications must be fair and balanced, not misleading, and risks cannot be minimized or obscured. See [FINRA Rule 2210](https://www.finra.org/rules-guidance/rulebooks/finra-rules/2210). FINRA Rule 2111 also distinguishes general financial/investment information from recommendations, but says a member cannot disclaim its suitability responsibilities with a disclaimer. The implication for this product is behavioral: keep the experience educational rather than trying to disclaimer its way out of advice-like outputs. See [FINRA Rule 2111](https://www.finra.org/rules-guidance/rulebooks/finra-rules/2111), especially Supplementary Material .02 and .03.

### 3. AI limitations without a repetitive warning

Give each assistant response a small “AI-generated” label or icon with accessible text, and make “Why this answer?” expandable. That panel should expose:

* which user-provided facts were used;
* the assumptions and unanswered questions;
* source links (prefer SEC, FINRA, fund prospectuses, issuer filings, and the market-data provider);
* whether market data was used and its timestamp; and
* a “Report an error”/“Ask for sources” control.

Use plain, specific limitations instead of a generic “may make mistakes”: “This answer may omit facts, misread your question, or contain an outdated/wrong statement. It cannot assess your full finances, tax situation, legal situation, or suitability.” If the model lacks a source, data, or confidence sufficient for a factual answer, say so and ask the user to verify; do not invent a number or citation. Do not display fake confidence percentages.

Prompt and UI guardrails should make the assistant:

* explain concepts and trade-offs rather than issue commands;
* decline to select a security or allocation for a particular person, while offering a neutral comparison framework;
* avoid guaranteed returns, “act now” language, price predictions, and personalized tax/legal conclusions;
* distinguish “example,” “historical result,” and “current fact”; and
* recommend an appropriately qualified professional when the question is consequential or facts are missing.

FINRA says its rules are technology-neutral: use of generative AI does not remove existing securities-law, supervision, communications, recordkeeping, or fair-dealing obligations for member firms. Its AI overview is a useful explanation of that principle: [FINRA Artificial Intelligence](https://www.finra.org/rules-guidance/key-topics/artificial-intelligence). FINRA’s [Regulatory Notice 24-09](https://www.finra.org/rules-guidance/notices/24-09) addresses member obligations when using GenAI/LLMs. The SEC has also brought “AI washing” cases against advisers that overstated their AI use or capabilities; do not imply that the product is more intelligent, accurate, or autonomous than it is. See the SEC’s [March 18, 2024 AI-washing enforcement release](https://www.sec.gov/news/press-release/2024-36).

### 4. Live versus delayed data labels

Treat data provenance as part of the number, not as a footnote:

* Every quote or market-sensitive figure should show `LIVE`, `DELAYED`, or `HISTORICAL`, followed by `as of [date, time, time zone]` and the source. Use text and an icon/color together; never color alone.
* “Live” should be used only when the MCP/provider actually supplies real-time data under the relevant entitlement. Otherwise say, for example, “Delayed quote — as of 10:42:15 AM ET” or “Market closed — last price as of …”.
* Distinguish the quote timestamp from the answer timestamp. A response generated now may rely on a quote from minutes ago; display both when material.
* Add “Not for trade execution” near market-data cards and explain that prices can change before a user acts. A stale, missing, or failed feed should produce “Data unavailable” rather than a silently reused price.
* Historical returns must identify the period, distribution/dividend treatment where relevant, and whether values are nominal or inflation-adjusted. A news item should show its publication time and not be presented as current merely because the chat is current.

This is primarily a transparency/control requirement rather than a claim that SEC or FINRA prescribe one exact label for this educational app. It is consistent with the fair/non-misleading communications principle in [FINRA Rule 2210](https://www.finra.org/rules-guidance/rulebooks/finra-rules/2210). If the product later becomes a broker/dealer or displays exchange data, review the applicable market-data agreements and rules before calling data live.

### 5. Trust signals that do not create false authority

High-value signals are inspectable, not decorative:

* show source title, publisher, link, and “last checked” date;
* identify the assistant as AI and identify the data provider; disclose material affiliations, compensation, sponsorship, or product-placement logic;
* make assumptions and profile inputs editable, show when a fact is missing, and let users clear/delete the profile;
* provide a visible correction/report control and preserve a readable answer history for the user;
* use calm typography and neutral language, not badges that look like SEC/FINRA approval or a “safe” rating;
* tell users not to enter brokerage passwords, account numbers, Social Security numbers, or secrets into chat; and
* avoid testimonials, “top pick” rankings, unsupported win rates, or performance claims. If the business later advertises adviser-like services or performance, review the SEC [Investment Adviser Marketing Rule (Release IA-5653)](https://www.sec.gov/files/rules/final/2020/ia-5653.pdf), including its requirements around misleading claims, hypothetical performance, and balanced presentation.

A source link is not enough: the response must accurately represent what the source says, and product UX must not place a government source logo next to an answer in a way that suggests endorsement.

## Handling financial distress safely

Do not infer crisis from a low income, debt, age, or risk-tolerance field. Respond to the user’s words and offer a dismissible, nonjudgmental support path.

### Ordinary financial hardship

If a user says they cannot pay bills, are facing eviction/utility shutoff, have overwhelming debt, or are considering investing borrowed/essential money:

1. Acknowledge the stress: “That sounds difficult. Let’s focus on protecting essentials first.”
2. Pause investing recommendations and do not suggest leverage, speculative assets, or a way to “make it back.” Say that investing can lose money and may not be appropriate for money needed for near-term essentials.
3. Offer general, prioritized options: list urgent bills, contact creditors early about hardship options, protect a modest cash buffer where possible, and seek a nonprofit/qualified debt counselor or financial professional. Do not tell the user to stop paying a specific debt or give a personalized legal/tax instruction.
4. Provide independent resources in a compact “Support for money stress” card: [CFPB: Behind on bills](https://www.consumerfinance.gov/consumer-tools/behind-on-bills/), [CFPB: credit counseling](https://www.consumerfinance.gov/consumer-tools/credit-counseling/), [SEC Investor.gov](https://www.investor.gov/), and relevant local housing/food/emergency assistance links. Explain that the app is not a debt counselor.
5. Add a fraud/urgency reminder if the user is looking for a fast rescue: no guaranteed returns, no pressure to transfer money, and verify any person or firm independently. Link to [SEC Investor.gov: Protect Your Investments](https://www.investor.gov/protect-your-investments) and FINRA’s [Avoid Fraud](https://www.finra.org/investors/protect-your-money/avoid-fraud).

### Possible self-harm or immediate danger

If the user expresses hopelessness, wanting to die, self-harm, or an immediate safety threat, stop the investing flow. Use empathetic, direct language; encourage contacting a trusted person and emergency services if there is immediate danger. In the U.S., offer call/text `988` or chat at [988 Lifeline](https://988lifeline.org/). Do not diagnose, promise confidentiality, or bury the support under investing content. Keep the response localized and do not claim that 988 is available everywhere.

## Suggested copy and acceptance checks

Header: **“Investing education, not personalized advice.”**

Context line: **“This uses what you shared to explain general considerations—not to recommend an investment or tell you what to do.”**

AI disclosure: **“AI-generated. It can be wrong or incomplete; check the sources and the data timestamp.”**

Data label: **“DELAYED · as of 10:42 AM ET · Source: [provider] · Not for trade execution.”**

Risk line: **“Past performance is not guaranteed. Investments can lose value, including principal.”**

For an MVP, test that a beginner can answer: (a) Is this a recommendation? (b) Is the quote live, delayed, or historical? (c) What could go wrong? (d) What facts and sources did the answer use? (e) Where can I get help if money stress is the real problem? If any answer requires opening a long legal disclaimer, the disclosure is too hidden; if every response is dominated by warnings, move stable material to the explainer and retain only the relevant contextual warning.

## Sources

* FINRA, [Rule 2210 — Communications with the Public](https://www.finra.org/rules-guidance/rulebooks/finra-rules/2210)
* FINRA, [Rule 2111 — Suitability](https://www.finra.org/rules-guidance/rulebooks/finra-rules/2111)
* FINRA, [Artificial Intelligence overview](https://www.finra.org/rules-guidance/key-topics/artificial-intelligence)
* FINRA, [Regulatory Notice 24-09 — Generative AI and LLM obligations](https://www.finra.org/rules-guidance/notices/24-09)
* SEC, [AI-washing enforcement release, March 18, 2024](https://www.sec.gov/news/press-release/2024-36)
* SEC, [Investment Adviser Marketing Rule, Release IA-5653](https://www.sec.gov/files/rules/final/2020/ia-5653.pdf)
* SEC Investor.gov, [Protect Your Investments](https://www.investor.gov/protect-your-investments)
* CFPB, [Behind on bills](https://www.consumerfinance.gov/consumer-tools/behind-on-bills/)
* CFPB, [Credit counseling](https://www.consumerfinance.gov/consumer-tools/credit-counseling/)
* 988 Lifeline, [Call/text/chat crisis support](https://988lifeline.org/)
