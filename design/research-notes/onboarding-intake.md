# onboarding-intake — research node

## Recommendation

Use a **short, guided stepper with conversational copy**, not a free-form chat intake and not one dense form. Collect only the minimum context needed to make the first educational answer more relevant, then let the assistant ask for one additional detail only when a later question genuinely requires it.

This is the best compromise for beginners:

- A pure chat intake is friendly, but users may not know what information is relevant, may answer inconsistently, and may not realize how many questions remain.
- A single form makes the data model visible to the product team, but 18 fields creates a “financial application” feel and increases abandonment and error risk.
- A stepper gives a clear start, end, back/edit controls, and progress, while conversational labels and chips preserve warmth and reduce jargon.

Use **5–7 questions for the first pass** (six is a good default). Questions should be answerable in under two minutes, mostly with one tap. Treat all answers as optional for an educational chat: a user can skip the whole intake and start asking questions immediately.

This recommendation follows the principle of progressive disclosure: show the few options needed initially and defer specialized information until requested. NN/g says this helps novice users avoid mistakes and improves learnability, efficiency, and error rate: https://www.nngroup.com/articles/progressive-disclosure/ . GOV.UK similarly recommends knowing why every question is asked, using branching so users see only relevant questions, and starting with one thing per page: https://www.gov.uk/service-manual/design/form-structure .

## Proposed first-pass questions

Use plain-language labels and store normalized values behind the scenes. Do not expose schema IDs such as `PS-011`.

| # | User-facing question | Suggested controls and answer choices | Why it matters |
|---|---|---|---|
| 1 | **What best describes your investing experience?** | Chips: `Just getting started`, `Some experience`, `I invest regularly`, `Not sure` | Sets explanation depth and vocabulary; avoids inferring competence from age or income. |
| 2 | **What are you hoping to learn or work toward?** | Multi-select chips: `Build an emergency fund`, `Start investing`, `Retirement`, `A major purchase`, `Understand funds/stocks`, `Pay down debt first`, `Something else`, `Not sure` | Provides intent without asking for a precise portfolio or account balance. Allow up to 2–3 selections. |
| 3 | **When might you need this money?** | Chips: `Within 1 year`, `1–3 years`, `3–10 years`, `10+ years`, `No specific timeline`, `Not sure` | Time horizon is more useful than a date for basic educational context and supports plain-language explanations of volatility. |
| 4 | **About how much could you set aside each month?** | Ranges: `$0`, `$1–$50`, `$51–$250`, `$251–$500`, `$500+`, `It varies`, `Prefer not to say` | Use an approximate range, not an exact income or contribution amount. Make currency/locale configurable. |
| 5 | **How much cash would you feel comfortable keeping available for surprises?** | Ranges: `Less than 1 month of expenses`, `1–3 months`, `3–6 months`, `6+ months`, `Not sure`, `Prefer not to say` | Elicits a useful liquidity signal without asking for an exact savings balance. Explain “emergency fund” in a hint if needed. |
| 6 | **If an investment temporarily lost value, which sounds most like you?** | Chips with short descriptions: `I’d want to avoid losses`, `I could accept a small drop`, `I could accept a larger drop for potential long-term growth`, `Not sure` | A beginner-friendly risk-attitude prompt. Do not label someone “conservative” or “aggressive” as a definitive score from one answer. |
| 7 (optional) | **Is there anything else that would help me explain things?** | Optional short text: “For example: student loans, variable income, workplace plan, or a question you already have.” | Capture relevant context only when the user volunteers it; never require a debt amount, employer, account number, or other sensitive identifier. |

The first six questions are the default. Question 7 should be a clearly optional “Add context” step or be deferred until the first user question. Age and job should not be required in the initial profile: they rarely justify the friction or sensitivity for general education, and the assistant can ask later if they change the explanation materially.

### Ranges, chips, and uncertainty

- Prefer **semantic ranges** over exact figures: monthly amount, liquid savings, debt, and income should not require a dollar-perfect answer. Include `It varies`, `Not sure`, `Prefer not to say`, and where appropriate `None`.
- Never preselect a chip. GOV.UK warns that preselected radios/checkboxes can cause users to miss a question or submit the wrong answer, and recommends “I do not know” where it is a valid response: https://design-system.service.gov.uk/components/radios/ .
- Use radio-like chips for one choice and checkbox-like chips for “select all that apply”; make the selection rule explicit in text, not only through styling. GOV.UK’s checkbox guidance: https://design-system.service.gov.uk/components/checkboxes/ . Material Design’s chip guidance can inform the visual treatment, but chips must remain real, labeled form controls: https://m3.material.io/components/chips/overview .
- Avoid false precision. The backend can store an ordinal range (`monthly_surplus: 251_500`) and a confidence state (`known`, `varies`, `not_sure`, `prefer_not_to_say`) rather than inventing a midpoint.
- If a range does not fit, offer `Skip for now`; do not force a “best guess.” “Not sure” is meaningful profile data, not a validation error.

## Interaction flow

1. **Welcome / value exchange.** “I can explain investing in a way that fits your situation. This takes about 2 minutes; you can skip it and change answers later.” Include the education-only disclaimer in nearby, calm text: “This is general education, not personalized financial advice.”
2. **Offer persona quick-starts.** Present 3–4 non-exclusive examples such as `Student or new grad`, `Early-career saver`, `Family / variable expenses`, and `Pre-retirement`. Label them as **starting points**, not classifications. Selecting one fills suggested ranges and goals, but every field remains editable and visibly marked as “Suggested.” Include `Start from scratch` and `Skip setup`.
3. **Stepper.** Show “Question 2 of 6” (or a simple progress bar with an accessible text label), one question per view on mobile and a centered narrow column on desktop. Use `Back`, `Skip`, and `Continue`; never hide the ability to revise an earlier answer. GOV.UK’s question-page pattern calls for a back link, page heading, continue button, and—when useful—a progress indicator: https://design-system.service.gov.uk/patterns/question-pages/ .
4. **Adaptive branching.** Ask only relevant follow-ups. For example, if the user selects `Pay down debt first`, ask later whether the debt is `high-interest`, `lower-interest`, or `not sure`; do not immediately ask lender, account, or exact balance. If the user chooses `I invest regularly`, optionally ask which account types they want explained. Keep this second layer out of first-run onboarding.
5. **Finish with a compact review.** Show “Your starting profile” as human labels: “Learning: just getting started,” “Goal: retirement,” “Timeline: 10+ years.” Show `Edit` beside each row and `Clear profile` / `Delete profile` in the settings area. Do not show internal JSON or codes.
6. **Return to chat immediately.** The primary completion CTA should be `Start learning`, not `Submit financial profile`. Seed the chat with useful starter prompts based on selected goals, e.g. “What should I understand before investing for retirement?”
7. **Ask later, in context.** When an answer would materially improve from more context, ask one focused follow-up with `Why I’m asking` and `Skip`. Do not reopen the entire onboarding form.

### Conversational layer without chat-only intake

The stepper can sound conversational: “Let’s start simple—what are you hoping to learn?” and “A rough range is perfect.” A user may also type a natural-language answer; map it to a chip/range and show the interpretation for confirmation (“I heard ‘about $300 a month’—use the $251–$500 range?”). This preserves the naturalness of chat while retaining visible state, recoverability, and structured data. Never silently infer a sensitive value from free text.

## Trust and sensitive financial data

Trust must be established **before** asking for money information, not retrofitted after submission. At the top of the intake, include a concise “Why we ask” link or disclosure:

- “These answers help tailor explanations and examples.”
- “Approximate ranges are enough.”
- “You can skip any question and edit or delete your profile later.”
- “We do not need bank logins, account numbers, Social Security numbers, or exact holdings for this educational experience.”
- “Here is where the profile is stored, who can access it, whether it is sent to the AI model, how long it is retained, and how to delete it.”

Do not claim “secure,” “private,” encryption, or deletion unless the implementation actually provides it. For a hackathon prototype, be explicit if data is held only in the browser, is sent to a server/model, or is not retained. Provide links to a plain-language privacy notice and terms; make them available without interrupting the flow.

Use these concrete cues:

- A lock/privacy icon only as a supplement to words; never rely on an icon or color alone.
- “Optional” beside genuinely optional questions; avoid collecting optional data by default.
- No bank-linking prompt in onboarding. If a future release supports account aggregation, introduce it separately with the provider, data categories, permissions, revocation, and security details before consent.
- A persistent `Profile` or `Your context` entry in the chat header so users know when profile context is being used. Let them turn it off for a conversation.
- A visible `Edit profile` and `Delete profile` action. Confirm destructive deletion and explain what will disappear.
- A brief reminder near free text: “Please don’t enter passwords, account numbers, Social Security numbers, or other identifying details.”
- If profile answers are transmitted to an external AI provider, say so plainly and link to the relevant policy. Do not imply the model is a fiduciary or that profile completion creates a recommendation relationship.

The data-minimization rationale is consistent with GOV.UK’s “question protocol”: only add a question when the service needs it, knows why it needs it, knows what it will do with it, and knows how it will keep it up to date and secure: https://www.gov.uk/service-manual/design/form-structure . FTC business guidance likewise recommends designing security around the personal information a business collects and retaining only what it needs: https://www.ftc.gov/business-guidance/resources/protecting-personal-information-guide-business .

## Error handling and accessibility

- Since most answers are controlled choices, validate only impossible states. Do not mark skipped answers as errors.
- When free text is used, explain the problem next to the field in text, preserve the user’s entry, and move focus to the error. WCAG 2.2 requires that detected input errors identify the field and describe the error in text: https://www.w3.org/WAI/WCAG22/Understanding/error-identification.html .
- Use native `fieldset`/`legend` for each question, associated labels, keyboard-operable chips, visible focus, and a logical tab order. A chip should not be a `<div>` with a click handler.
- Ensure the progress indicator has a text equivalent, and announce step changes to assistive technology without repeatedly reading the whole page.
- Keep touch targets comfortably tappable, maintain a single-column mobile layout, and support browser back without losing answers.

## What to measure in the prototype

Instrument only aggregate, non-sensitive events where possible: intake started, question-level skip rate, completion rate, time to first useful chat question, back/edit use, and abandonment by step. Avoid logging raw financial answers or free-text profile content. Test at least three novice personas and one user who declines all money questions. Success means users can reach a useful educational answer quickly, understand what was collected and why, and can correct or remove it without assistance.

## Sources

- Nielsen Norman Group, “Progressive Disclosure”: https://www.nngroup.com/articles/progressive-disclosure/
- Nielsen Norman Group, “Website Forms Usability: Top 10 Recommendations”: https://www.nngroup.com/articles/web-form-design/
- GOV.UK Service Manual, “Structuring forms”: https://www.gov.uk/service-manual/design/form-structure
- GOV.UK Design System, “Question pages”: https://design-system.service.gov.uk/patterns/question-pages/
- GOV.UK Design System, “Radios”: https://design-system.service.gov.uk/components/radios/
- GOV.UK Design System, “Checkboxes”: https://design-system.service.gov.uk/components/checkboxes/
- Material Design 3, “Chips”: https://m3.material.io/components/chips/overview
- W3C WAI, WCAG 2.2 Understanding SC 3.3.1, “Error Identification”: https://www.w3.org/WAI/WCAG22/Understanding/error-identification.html
- Federal Trade Commission, “Protecting Personal Information: A Guide for Business”: https://www.ftc.gov/business-guidance/resources/protecting-personal-information-guide-business
