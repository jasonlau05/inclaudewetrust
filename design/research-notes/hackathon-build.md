# Fastest polished UI plan: FastAPI + vanilla HTML/CSS/JS, no build step

## Executive recommendation

For a 1–2 hour hackathon pass, use **semantic HTML plus a small, deliberate `style.css` token/component layer**. Do not introduce a full utility framework. Add only two optional CDNs if the current API requires them:

1. **Lucide** for a handful of consistent outline icons, or inline SVGs for the very small fixed icon set.
2. **Marked plus DOMPurify** only if Gemini returns Markdown that must be displayed as formatted answer content.

This gives the engineer complete control over the calm, trustworthy visual language and avoids spending the time learning framework conventions, debugging generated styles, or rewriting existing markup. FastAPI can continue to serve the files with `StaticFiles`; its official example mounts a static directory with `app.mount("/static", StaticFiles(directory="static"), name="static")` ([FastAPI Static Files](https://fastapi.tiangolo.com/tutorial/static-files/)).

Use a **single responsive application shell**, not an always-visible 340px developer sidebar:

- a compact header: product name, “Education, not financial advice” link/badge, theme control;
- a centered content column, approximately 680–760px wide;
- a short “About you” card with the few inputs needed to start and an expandable “More context” section;
- an empty-state welcome and three example-question chips;
- a message stream with user and assistant bubbles/cards;
- a composer fixed to the bottom of the content column on desktop and naturally placed on mobile;
- a small, persistent disclaimer below the composer.

This is enough structure to look intentional without building navigation, routing, accounts, charts, or a design system.

## Option comparison

| Approach | Speed in this codebase | What it gives | Main risk | Verdict |
|---|---:|---|---|---|
| **Plain CSS** | Fastest after the first 20 minutes | Exact layout, responsive behavior, tokens, states, no runtime dependency | Engineer must write a few components | **Recommended**. A small 150–250 line stylesheet is sufficient. |
| **Pico.css** | Initially very fast | Semantic HTML defaults, responsive elements, forms, buttons, and a CDN link ([Pico quick start](https://picocss.com/docs)) | Pico’s own documentation currently says it is “no longer maintained”; its defaults can also fight a bespoke chat layout | Useful for a throwaway spike, but do not make it the foundation of this demo. |
| **Open Props** | Fast for tokens, not components | A coherent set of CSS custom properties for sizes, colors, shadows, radii, easing, and optional normalize/buttons packs; it documents CDN imports and incremental adoption ([Open Props](https://open-props.style/)) | Still requires writing the actual app components; external `@import`/CDN availability and broad token surface add decisions | Optional. Copy a few ideas/tokens into `style.css`, or import only a small pinned pack if time permits. |
| **Tailwind Play CDN** | Fast for a green-field tiny page | Utility classes without a build step ([Play CDN](https://tailwindcss.com/docs/installation/play-cdn)) | Tailwind explicitly says Play CDN is for development only, not production. Long class strings make this existing markup harder to refactor and can produce inconsistent one-off styling | Fine for a disposable visual experiment; not recommended for this deliverable. |
| **Markdown renderer** | Fast if answers are already Markdown | Headings, lists, emphasis, code, tables in assistant answers | Markdown output is HTML; Marked explicitly does **not** sanitize output and recommends filtering with DOMPurify ([Marked security warning](https://marked.js.org/)) | Use Marked + DOMPurify only for assistant text. Never assign raw model text directly to `innerHTML`. |
| **Icon fonts / Font Awesome** | Familiar but more setup | Large catalog and CSS class usage | Font files/CSS, style choices, baseline alignment, and visual weight are more work than this UI needs. Font Awesome’s self-hosted setup requires both `/css` and `/webfonts` assets ([Font Awesome web fonts](https://fontawesome.com/docs/web/setup/host-yourself/webfonts)) | Skip unless the repo already has it. |
| **Lucide SVG icons** | Very fast for 5–8 controls | Lightweight framework-free SVG icons, CSS sizing/color, no icon font baseline problems; Lucide documents vanilla JS use and data attributes ([Lucide Vanilla JS](https://lucide.dev/guide/packages/lucide)) | A CDN is an additional runtime dependency; pin a version | Recommended icon option if inline SVGs are not already available. |
| **Inline SVG** | Fastest for a fixed set | No dependency, sharp at all sizes, accessible when labeled | A little repetitive markup | Best for send, plus, sun/moon, copy, external-link, and chevron if there are only a few. |

### Why not over-style with a CDN framework?

A CDN reduces installation but does not reduce product decisions. For this screen, most of the work is information hierarchy, state handling, and trustworthy copy—not generating a large collection of utility classes. Plain CSS also makes it easier to guarantee a visible focus ring, mobile layout, reduced-motion behavior, and a consistent color system. If Open Props is used, import only the needed token packs and keep local component rules in `style.css`; the project’s own site says it is non-prescriptive and incrementally adoptable ([Open Props](https://open-props.style/)).

## File-by-file implementation

### `index.html`: semantic shell and understandable content

Replace schema-heavy labels and raw dumps with an accessible, visually quiet structure. Keep the existing form controls in the DOM or preserve their values in state if the API requires them, but expose beginner language:

```html
<header class="topbar">
  <a class="brand" href="/" aria-label="Investing assistant home">
    <span class="brand-mark" aria-hidden="true">✦</span>
    <span>ClearPath</span>
  </a>
  <div class="topbar-actions">
    <button class="icon-button" id="theme-toggle" type="button"
            aria-label="Switch color theme" title="Switch color theme">…</button>
    <a class="text-link" href="#disclaimer">How this works</a>
  </div>
</header>

<main class="app-shell">
  <section class="intro" aria-labelledby="page-title">
    <p class="eyebrow">Your investing questions, made clearer</p>
    <h1 id="page-title">What would you like to understand?</h1>
    <p class="intro-copy">Share a little context, then ask anything. You’ll get general education—not a recommendation to buy or sell.</p>
  </section>

  <form id="profile-form" class="context-card">
    <div class="section-heading">
      <div><h2>Start with your context</h2><p>Optional, but it helps tailor the explanation.</p></div>
      <button class="button-quiet" type="button" aria-expanded="false" aria-controls="more-context">Add details</button>
    </div>
    <div class="field-grid">
      <label>What are you investing for?
        <select name="goal"><option value="">Choose one</option><option>Retirement</option><option>Short-term goal</option><option>Building wealth</option></select>
      </label>
      <label>How comfortable are you with ups and downs?
        <select name="risk_tolerance"><option value="">Choose one</option><option>Still learning</option><option>Some fluctuation is okay</option><option>I understand large fluctuations</option></select>
      </label>
    </div>
    <div id="more-context" hidden>
      <!-- Keep the existing API’s remaining fields here. Use human labels; do not show PS-011-style codes. -->
    </div>
  </form>

  <section id="empty-state" class="empty-state" aria-labelledby="empty-title">
    <div class="welcome-icon" aria-hidden="true">↗</div>
    <h2 id="empty-title">A good place to start</h2>
    <p>Try one of these, or ask in your own words.</p>
    <div class="prompt-list">
      <button class="prompt-chip" type="button">What should I do with an extra $500 a month?</button>
      <button class="prompt-chip" type="button">How are VOO and VTI different?</button>
      <button class="prompt-chip" type="button">Explain index funds like I’m new to investing.</button>
    </div>
  </section>

  <section id="conversation" class="conversation" aria-label="Conversation" aria-live="polite"></section>
  <p id="status" class="sr-only" role="status" aria-live="polite"></p>

  <form id="composer" class="composer">
    <label class="sr-only" for="question">Ask an investing question</label>
    <textarea id="question" name="question" rows="1" maxlength="2000"
      placeholder="Ask a question about investing…"></textarea>
    <button id="send-button" class="button-primary" type="submit">
      <span>Ask</span><span aria-hidden="true">↗</span>
    </button>
  </form>
  <p id="disclaimer" class="disclaimer">For educational purposes only. This is not personalized financial, tax, or legal advice. Consider your circumstances and verify important information.</p>
</main>
```

Implementation notes:

- Use real `button`, `label`, `textarea`, `select`, `details`, and headings rather than clickable `div`s.
- Keep a `noscript` message if the app cannot work without JavaScript.
- If the current API requires 18 fields, do not delete them from the payload. Show the two or three most useful fields first and place the rest in “Add details”; retain the existing schema keys in JavaScript.
- Put tool/source information in a collapsed `<details>` block titled “Sources and market data,” not in the primary answer stream. Keep raw JSON out of the default experience.

### `style.css`: tokens first, then six small components

Start with a restrained palette and a narrow set of reusable rules. Avoid a dashboard gradient, heavy shadows, and red/green color-coding as the main meaning. A sample starting point:

```css
:root {
  color-scheme: light;
  --bg: #f7f8f6;
  --surface: #ffffff;
  --surface-muted: #eef2ef;
  --ink: #17211d;
  --muted: #65736c;
  --line: #d9e2dc;
  --accent: #176b58;
  --accent-strong: #0f5647;
  --accent-soft: #dff1e9;
  --warning-soft: #fff7e3;
  --warning-ink: #624c16;
  --focus: #176b58;
  --radius-sm: 8px;
  --radius-md: 14px;
  --radius-lg: 22px;
  --shadow: 0 8px 28px rgb(23 33 29 / 7%);
  --content: 740px;
  font: 16px/1.55 system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--ink); }
button, textarea, select { font: inherit; }
button, select, textarea { min-height: 44px; }
:focus-visible { outline: 3px solid var(--focus); outline-offset: 3px; }
.sr-only { position: absolute; width: 1px; height: 1px; padding: 0; margin: -1px; overflow: hidden; clip: rect(0,0,0,0); white-space: nowrap; border: 0; }
.topbar { height: 64px; display: flex; align-items: center; justify-content: space-between; padding: 0 24px; border-bottom: 1px solid var(--line); background: rgb(255 255 255 / 82%); }
.app-shell { width: min(calc(100% - 32px), var(--content)); margin: 0 auto; padding: 48px 0 32px; }
.intro { margin-bottom: 28px; }
.eyebrow { margin: 0 0 8px; color: var(--accent); font-size: .78rem; font-weight: 700; letter-spacing: .09em; text-transform: uppercase; }
h1, h2, p { margin-top: 0; }
h1 { max-width: 620px; margin-bottom: 12px; font-size: clamp(2rem, 5vw, 3.25rem); line-height: 1.05; letter-spacing: -.035em; }
.intro-copy { max-width: 600px; color: var(--muted); }
.context-card, .assistant-message { background: var(--surface); border: 1px solid var(--line); border-radius: var(--radius-lg); box-shadow: var(--shadow); }
.context-card { padding: 20px; margin-bottom: 36px; }
.section-heading { display: flex; gap: 16px; align-items: flex-start; justify-content: space-between; }
.section-heading h2 { margin-bottom: 3px; font-size: 1rem; }
.section-heading p, .field-grid label { color: var(--muted); font-size: .9rem; }
.field-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin-top: 18px; }
label { display: grid; gap: 7px; }
select, textarea { width: 100%; border: 1px solid var(--line); border-radius: var(--radius-sm); background: var(--surface); color: var(--ink); padding: 10px 12px; }
.empty-state { text-align: center; padding: 24px 0 36px; }
.empty-state h2 { margin-bottom: 4px; }
.empty-state p { color: var(--muted); }
.prompt-list { display: flex; flex-wrap: wrap; justify-content: center; gap: 9px; }
.prompt-chip, .button-quiet { border: 1px solid var(--line); border-radius: 999px; background: var(--surface); color: var(--ink); padding: 9px 14px; cursor: pointer; }
.prompt-chip:hover, .button-quiet:hover { border-color: var(--accent); background: var(--accent-soft); }
.conversation { display: grid; gap: 18px; margin-bottom: 20px; }
.message { max-width: 92%; }
.message.user { justify-self: end; color: white; background: var(--accent); border-radius: 18px 18px 4px 18px; padding: 12px 16px; }
.assistant-message { max-width: 100%; padding: 20px; border-radius: 18px 18px 18px 4px; }
.assistant-message :first-child { margin-top: 0; }
.assistant-message :last-child { margin-bottom: 0; }
.composer { position: sticky; bottom: 12px; display: flex; gap: 10px; align-items: flex-end; padding: 10px; background: color-mix(in srgb, var(--bg) 88%, transparent); backdrop-filter: blur(10px); border: 1px solid var(--line); border-radius: 18px; }
.composer textarea { min-height: 44px; max-height: 140px; resize: none; border: 0; background: transparent; }
.button-primary { display: inline-flex; align-items: center; gap: 8px; border: 0; border-radius: 11px; padding: 11px 16px; background: var(--accent); color: white; font-weight: 700; cursor: pointer; white-space: nowrap; }
.button-primary:hover { background: var(--accent-strong); }
.button-primary:disabled { cursor: wait; opacity: .65; }
.disclaimer { margin: 13px auto 0; max-width: 680px; color: var(--muted); font-size: .76rem; text-align: center; }
@media (max-width: 600px) { .topbar { padding: 0 16px; } .app-shell { width: min(calc(100% - 24px), var(--content)); padding-top: 32px; } .field-grid { grid-template-columns: 1fr; } .context-card { padding: 16px; } .composer { bottom: 6px; } .composer .button-primary span:first-child { display: none; } }
@media (prefers-reduced-motion: reduce) { *, *::before, *::after { scroll-behavior: auto !important; transition-duration: .01ms !important; animation-duration: .01ms !important; animation-iteration-count: 1 !important; } }
```

The final values should be checked in a browser, especially text and control contrast. WCAG’s guidance explains the purpose of visible focus and requires a keyboard-operable interface to have a mode with a visible focus indicator ([WCAG 2.4.7 Focus Visible](https://www.w3.org/WAI/WCAG22/Understanding/focus-visible.html)). Also check normal-text contrast against WCAG’s contrast guidance ([WCAG 1.4.3 Contrast Minimum](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html)). The `prefers-reduced-motion` media query is the appropriate browser mechanism for respecting a user’s motion preference ([MDN `prefers-reduced-motion`](https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion)).

### `app.js`: preserve the API contract, improve state and rendering

Do not rewrite the server contract during the visual pass. First copy the existing endpoint, request builder, and response extraction into named functions. Preserve every existing schema key even if a field is now hidden in “More context.” A minimal structure is:

```js
const state = {
  messages: [],
  busy: false,
  profile: loadProfile(), // same keys/shape the current API expects
};

const els = {
  form: document.querySelector('#composer'),
  input: document.querySelector('#question'),
  send: document.querySelector('#send-button'),
  stream: document.querySelector('#conversation'),
  empty: document.querySelector('#empty-state'),
  status: document.querySelector('#status'),
};

function addMessage(role, text, meta = {}) {
  state.messages.push({ role, text, ...meta });
  renderMessages();
}

function renderMessages() {
  els.empty.hidden = state.messages.length > 0;
  els.stream.replaceChildren();
  for (const message of state.messages) {
    const node = document.createElement('article');
    node.className = `message ${message.role === 'user' ? 'user' : 'assistant-message'}`;
    node.setAttribute('aria-label', message.role === 'user' ? 'You' : 'Assistant');
    // Use textContent for user text. For assistant Markdown, use the safe renderer below.
    node.innerHTML = message.role === 'assistant'
      ? safeMarkdown(message.text)
      : escapeHtml(message.text);
    els.stream.append(node);
  }
  els.stream.lastElementChild?.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
}

async function ask(question) {
  state.busy = true;
  els.send.disabled = true;
  els.input.disabled = true;
  els.status.textContent = 'Thinking…';
  addMessage('user', question);
  addMessage('assistant', '<p class="loading-message">Thinking through that…</p>', { temporary: true });

  try {
    // Keep the exact endpoint, headers, payload keys, and auth behavior from the existing app.js.
    const response = await fetch(EXISTING_CHAT_ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(buildExistingPayload(state.profile, state.messages)),
    });
    if (!response.ok) throw new Error(`Request failed (${response.status})`);
    const data = await response.json();
    state.messages = state.messages.filter(m => !m.temporary);
    addMessage('assistant', extractExistingAnswer(data), { sources: extractExistingSources(data) });
    els.status.textContent = 'Answer ready.';
  } catch (error) {
    state.messages = state.messages.filter(m => !m.temporary);
    addMessage('assistant', 'I couldn’t reach the assistant. Please check the connection and try again.', { error: true });
    els.status.textContent = 'There was a problem getting an answer.';
  } finally {
    state.busy = false;
    els.send.disabled = false;
    els.input.disabled = false;
    els.input.focus();
  }
}

els.form.addEventListener('submit', event => {
  event.preventDefault();
  const question = els.input.value.trim();
  if (!question || state.busy) return;
  els.input.value = '';
  ask(question);
});
```

Adapt the names in the example to the actual prototype rather than guessing a new endpoint. The important separation is:

- `buildExistingPayload(...)`: old request shape, old persona/profile keys, no UI labels in the payload;
- `extractExistingAnswer(data)`: one place translating the existing response shape to display text;
- `extractExistingSources(data)`: one place translating live-market/MCP metadata to compact source rows;
- `renderMessages()`: presentation only;
- event handlers: submission, prompt chips, expandable context, theme, copy, retry.

Add these small behaviors for a finished demo:

1. **Prompt chips** populate the composer and focus it; they should submit exactly like typed questions.
2. **Enter to send, Shift+Enter for a newline** on desktop; do not prevent normal mobile textarea behavior.
3. **Autosize** the composer from one to approximately four lines.
4. **Disable the send button while waiting**, show “Thinking…” in a polite live status, and restore focus after completion.
5. **Handle failures visibly** with a friendly retry action; never leave a disabled spinner with no explanation.
6. **Persist only harmless UI state** such as theme, expanded context, and the draft; do not persist sensitive financial details unless the product explicitly requires it.
7. **Render source freshness** (for example, “Market data retrieved 2 min ago”) when the API provides it. Do not invent a timestamp.
8. **Render tool calls as disclosure**, e.g. `<details><summary>Sources and market data</summary>…</details>`, and show human-readable tool names, not JSON or token counts.
9. **Add copy-answer and retry controls only after the core submit flow works.** They are high-value polish, but not worth delaying the first working path.

#### Markdown safety

If the current Gemini answer is Markdown, the quickest safe browser pipeline is:

```html
<script src="https://cdn.jsdelivr.net/npm/marked/lib/marked.umd.js"></script>
<script src="https://cdn.jsdelivr.net/npm/dompurify/dist/purify.min.js"></script>
```

```js
function safeMarkdown(markdown) {
  const html = marked.parse(String(markdown).replace(/^[\u200B\u200C\u200D\u200E\u200F\uFEFF]/, ''));
  return DOMPurify.sanitize(html, {
    USE_PROFILES: { html: true },
    FORBID_TAGS: ['style', 'form'],
  });
}
```

Pin exact versions for the demo’s deployed HTML instead of `latest`, and include Subresource Integrity if the chosen CDN provides a stable integrity hash. The Marked documentation explicitly warns that it does not sanitize HTML and recommends DOMPurify or another sanitizer ([Marked](https://marked.js.org/)). If no Markdown is needed, do not add either dependency: create paragraphs/list text with DOM APIs and `textContent`.

#### Icons

Use `aria-hidden="true"` for decorative icons and an accessible name for icon-only controls. The quickest no-dependency choice is a few inline SVGs with `viewBox="0 0 24 24"`, `fill="none"`, `stroke="currentColor"`, and `stroke-width="2"`. If using Lucide, use its vanilla package/CDN and call its documented icon replacement after rendering; do not mix emoji, Font Awesome classes, and unrelated icon sets. An icon should reinforce a visible label, not be the only explanation for a consequential action.

## Visual/content decisions that make a two-hour demo feel finished

- **One confident first screen:** “What would you like to understand?” is more inviting than an exposed schema form.
- **Progressive disclosure:** two useful context questions first; all other profile fields behind “Add details.”
- **Human labels:** “How comfortable are you with ups and downs?” instead of `risk_tolerance (PS-011)`; keep the machine key internal.
- **Example prompts:** make the empty state useful and demonstrate the intended product in one click.
- **Answer hierarchy:** short lead answer, headings, bullets, caveats, then “Sources and market data.” Avoid a wall of model text.
- **Trust language:** show “general education,” the data freshness/source area, and a concise disclaimer without making the interface feel alarmist.
- **No fake certainty:** use “may,” “depends,” and “consider” where the model does; do not add green “good investment” badges or red “bad investment” badges in the UI.
- **Responsive behavior:** on narrow screens hide secondary header links, use a one-column context form, keep the composer full width, and ensure no horizontal scroll.
- **Empty/loading/error states:** intentionally style all three. A skeleton or “Thinking through that…” line is better than a blank gap; an error includes a retry path.
- **Small details:** consistent 8/14/22px radii, one accent, one shadow, matching icon stroke widths, button hover/focus/disabled states, current message scroll, and a visible date/freshness label where the API provides one.
- **Accessibility:** keyboard-operable controls, labels for every field, heading order, visible `:focus-visible`, adequate contrast, status announcements, and no information conveyed only by color. WCAG’s status-message guidance explains how updates that do not move focus should be exposed to assistive technology ([WCAG 4.1.3 Status Messages](https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html)).

## 1–2 hour execution plan

**0–10 minutes — inventory and contract lock**

- Open the current `index.html`, `style.css`, and `app.js`.
- Record the existing chat endpoint, request body, response answer field, persona/profile keys, and MCP/source fields.
- Make a small `EXISTING_*` adapter in `app.js`; do not change the server.

**10–35 minutes — HTML and base CSS**

- Replace the sidebar with the shell/context/empty-state/composer structure.
- Add tokens, typography, spacing, cards, messages, responsive rules, focus styles, and disclaimer.
- Keep the existing fields available inside the expandable context section.

**35–65 minutes — JS integration**

- Wire profile collection, prompt chips, submit, loading, response, error, and auto-scroll.
- Remove raw JSON/token-count output from the default stream.
- Add safe Markdown rendering only if the response needs it.

**65–90 minutes — demo polish and accessibility pass**

- Add theme toggle or omit it if it introduces risk; light theme alone is acceptable.
- Add source disclosure, copy/retry, textarea autosize, and local draft if time remains.
- Test keyboard-only navigation, mobile width, empty/loading/error states, long answer, Markdown links/code, and a failed API request.

**90–120 minutes — rehearsal and cleanup**

- Pin CDN versions and verify the page with network access disabled as far as the demo permits.
- Remove console logs, schema labels, raw tool payloads, placeholder lorem ipsum, token counters, and unused controls.
- Run the exact two or three demo prompts from a clean refresh.

## Do-not list

- **Do not use Tailwind Play CDN as if it were a production build.** Tailwind says Play CDN is intended for development only ([Tailwind Play CDN](https://tailwindcss.com/docs/installation/play-cdn)).
- **Do not make Pico.css the core dependency without noticing its current maintenance warning.** If used, pin it and override it locally; plain CSS is safer for this quick surface ([Pico docs](https://picocss.com/docs)).
- **Do not rewrite or silently rename the existing API payload keys.** Hide/relabel fields in the UI, but preserve the server contract.
- **Do not expose PS codes, raw JSON, MCP request/response dumps, token counts, stack traces, or model internals in the primary user experience.** Put only useful source/freshness information behind disclosure.
- **Do not put raw Gemini/Markdown output into `innerHTML` without sanitization.** Marked’s own documentation warns about XSS; use DOMPurify or text-only rendering ([Marked](https://marked.js.org/)).
- **Do not use color alone for gain/loss, risk, warnings, loading, or errors.** Pair color with text and/or an icon.
- **Do not remove native focus outlines without replacing them.** WCAG requires a visible focus mode ([WCAG Focus Visible](https://www.w3.org/WAI/WCAG22/Understanding/focus-visible.html)).
- **Do not make every field required before a user can ask a basic educational question.** Use optional context and sensible server-compatible defaults.
- **Do not build charts, authentication, streaming, multi-page navigation, a custom modal system, or a full theme engine in this pass.** They are scope traps unless already supplied by the prototype.
- **Do not imply personalized investment advice or guaranteed returns.** Keep the educational disclaimer in the initial screen and near the composer.
- **Do not add a dozen CDN libraries.** Every external script is another failure mode; plain CSS, inline SVG, and text rendering are enough for the first demo.

## Source index

- FastAPI, Static Files: https://fastapi.tiangolo.com/tutorial/static-files/
- Pico CSS documentation and CDN quick start: https://picocss.com/docs
- Open Props documentation and CDN imports: https://open-props.style/
- Tailwind Play CDN and its development-only warning: https://tailwindcss.com/docs/installation/play-cdn
- Marked documentation and sanitization warning: https://marked.js.org/
- Lucide for vanilla JavaScript: https://lucide.dev/guide/packages/lucide
- Font Awesome self-hosted web fonts: https://fontawesome.com/docs/web/setup/host-yourself/webfonts
- WCAG 2.2 Focus Visible: https://www.w3.org/WAI/WCAG22/Understanding/focus-visible.html
- WCAG 2.2 Contrast Minimum: https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html
- WCAG 2.2 Target Size Minimum: https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html
- WCAG 2.2 Status Messages: https://www.w3.org/WAI/WCAG22/Understanding/status-messages.html
- MDN `prefers-reduced-motion`: https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion
