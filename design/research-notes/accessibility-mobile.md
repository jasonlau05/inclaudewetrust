# accessibility-mobile

## Baseline

Target **WCAG 2.2 Level AA** for the full investing chat flow, including onboarding, profile editing, chat, streaming responses, data cards, comparison tables, errors, drawers, and responsive states. WCAG applies across desktop and mobile devices: [WCAG 2.2](https://www.w3.org/TR/WCAG22/).

## 1. Semantic structure

Use native HTML before ARIA:

- Provide a skip link to `<main>`.
- Use one descriptive `<h1>` per screen, followed by logical `<h2>`/`<h3>` headings. Do not use font size or visual styling alone to communicate hierarchy.
- Use landmarks:
  - `<header>` for product/header actions
  - `<nav aria-label="Primary">` where navigation exists
  - `<main id="main-content">` for chat or onboarding
  - `<aside>` for a persistent desktop profile panel
  - `<form>` for intake and message submission
  - `<footer>` only where useful
- Mark each chat message as an `<article>` or list item with a meaningful accessible label such as “You” and “Assistant.” Do not use generic clickable `<div>` elements.
- Use real `<button>`, `<a>`, `<input>`, `<textarea>`, `<select>`, radio, and checkbox controls. Native controls provide keyboard behavior and accessible names.
- Associate every input with a visible `<label for="...">`; use `<fieldset>` and `<legend>` for related choices such as risk tolerance or goals. Use `aria-describedby` for hints and errors, not as a replacement for visible labels.
- Use `<table>`, `<caption>`, `<thead>`, `<th scope="col">`, and `<th scope="row">` for fund comparisons. Do not create tables from visually aligned `<div>` elements.
- Use text in addition to color, icons, or visual emphasis: “Up 2.4%,” “Down 1.1%,” “Higher risk,” and “Data delayed” should remain understandable without color.

Relevant requirements: [1.3.1 Info and Relationships](https://www.w3.org/WAI/WCAG22/Understanding/info-and-relationships.html), [3.3.2 Labels or Instructions](https://www.w3.org/WAI/WCAG22/Understanding/labels-or-instructions.html), and W3C’s [Labeling Controls tutorial](https://www.w3.org/WAI/tutorials/forms/labels/).

## 2. Contrast and visual states

- Normal text must have at least **4.5:1** contrast against its background.
- Large text must have at least **3:1** contrast. WCAG defines large text as approximately 18pt regular or 14pt bold.
- Meaningful icons, chart lines, input borders, button boundaries, selected states, and focus indicators must have at least **3:1** contrast against adjacent colors.
- Do not use pale gray body text, low-contrast placeholder text, or light gray borders as the only indication of an input boundary.
- Do not communicate gains/losses, risk, validation, or selection using color alone. Pair color with words, symbols, patterns, labels, or an accessible text alternative.
- Ensure links are distinguishable from surrounding text by more than color alone, such as an underline.
- Provide a clearly visible focus style in both light and dark modes. A two-color outline or an outline plus offset is robust against varied backgrounds.
- Avoid relying on disabled styling to communicate availability; disabled controls often have poor contrast. Prefer explanatory text or keep the control enabled with a clear validation message where appropriate.

Requirements: [1.4.3 Contrast (Minimum)](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html), [1.4.11 Non-text Contrast](https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html), and [1.4.1 Use of Color](https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html).

## 3. Keyboard navigation

All functionality must work with a keyboard, without requiring a mouse gesture or timing-dependent key sequence: [2.1.1 Keyboard](https://www.w3.org/WAI/WCAG22/Understanding/keyboard.html).

Implementation rules:

- Keep DOM order aligned with the intended reading and interaction order. Do not use positive `tabindex` values.
- Use native buttons so Enter and Space work naturally.
- The sequence should generally be: skip link → header controls → profile control → chat history → message input → send button → secondary actions.
- Provide a keyboard-operable send button. `Enter` may submit a single-line input, but multiline textareas should support a documented alternative such as `Ctrl+Enter`/`Cmd+Enter`; never make keyboard users depend on an undiscoverable shortcut.
- Ensure the profile drawer, “How I got this” disclosure, sources, follow-up chips, retry controls, and table controls are all reachable and operable.
- Do not trap focus in ordinary inline disclosures. A modal profile drawer must trap focus until closed.
- `Escape` should close an open profile drawer or modal and return focus to its invoking button.
- Never remove focus after a click or rerender.
- Keep a “Jump to latest” button available when the user is reading older messages. Do not automatically scroll the chat while the user is navigating or selecting text.
- Ensure focus is not hidden behind the sticky message composer, mobile browser UI, profile drawer, or notification banner. Use adequate bottom scroll padding and scroll focused controls into view.

Requirements: [2.4.3 Focus Order](https://www.w3.org/WAI/WCAG22/Understanding/focus-order.html), [2.4.7 Focus Visible](https://www.w3.org/WAI/WCAG22/Understanding/focus-visible.html), and [2.4.11 Focus Not Obscured (Minimum)](https://www.w3.org/WAI/WCAG22/Understanding/focus-not-obscured-minimum.html).

## 4. Focus management

### Profile drawer

Desktop may show the profile as a persistent `<aside>`. On mobile, use a responsive drawer:

- If the drawer blocks the underlying chat, implement it as a true modal using native `<dialog>` where practical, or a correctly implemented `role="dialog" aria-modal="true"`.
- Give it a visible title and connect it with `aria-labelledby`.
- Move focus into the drawer when it opens.
- Keep Tab and Shift+Tab within the drawer.
- Include a visible “Close profile” button; support Escape.
- Restore focus to the profile trigger when it closes.
- Make the background inert while modal.
- Do not use `aria-modal="true"` unless the background is actually visually and interactively blocked.

W3C APG: [Dialog (Modal) Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/).

### Dynamic content

When a user submits a question:

1. Keep focus in the message field unless there is a strong reason to move it.
2. Add the user message and a stable assistant placeholder to the chat.
3. Announce a concise status such as “Assistant is thinking.”
4. Let the user continue to navigate or cancel where possible.
5. Announce completion without forcibly moving focus.
6. Provide a stable “Read latest answer” or “Jump to latest response” action for users who want to navigate directly.

Avoid moving focus to every new response or every stream update; unexpected focus movement is disorienting.

## 5. Chat and streaming responses

### Recommended structure

Use a labeled chat region, for example:

```html
<section aria-labelledby="conversation-heading">
  <h2 id="conversation-heading">Conversation</h2>

  <ol id="message-log" role="log" aria-live="polite" aria-relevant="additions">
    <li>
      <article aria-labelledby="assistant-message-1-label">
        <h3 id="assistant-message-1-label">Assistant</h3>
        ...
      </article>
    </li>
  </ol>
</section>
```

WAI-ARIA defines live-region semantics in [WAI-ARIA 1.2](https://www.w3.org/TR/wai-aria-1.2/). Use ARIA only where native semantics do not already provide the behavior.

### Live-region behavior

- A chat log should generally use **polite** announcements. Do not interrupt the user with assertive speech for ordinary responses.
- Insert the live region before adding messages; dynamically adding `aria-live` after content changes can prevent announcements in some assistive technologies.
- Do not put `aria-live` on the entire page or on a container that changes continuously.
- Do not announce every streamed token. Token-by-token announcements can cause a screen reader to repeatedly interrupt or produce unusable output.
- During streaming:
  - Render visible text normally for sighted users.
  - Mark the response as busy where appropriate.
  - Keep a visually hidden status such as “Assistant is writing a response.”
  - Announce a concise completion message such as “Assistant response complete.”
  - Make the final response available as one stable, navigable article.
- Avoid an animated three-dot indicator as the only feedback. Use text such as “Assistant is thinking” and optionally a static progress indicator.
- Do not use `role="alert"` for normal chat responses. Alerts are for brief, important messages that should be announced without moving focus; frequent alerts create excessive interruption. See [WAI-ARIA Alert Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/alert/).
- For a long response, use real headings, lists, paragraphs, tables, and disclosures so screen-reader users can navigate by structure. Do not place the entire answer in one unstructured text node.
- If new content is loaded into a feed-like structure, W3C APG recommends semantic articles and careful busy-state handling: [Feed Pattern](https://www.w3.org/WAI/ARIA/apg/patterns/feed/). A normal finite chat history does not need to be forced into the feed pattern.

## 6. Errors and status messages

### Intake and profile validation

For automatically detected errors:

- Identify the exact field in text.
- Explain what went wrong.
- Suggest how to fix it where known.
- Set `aria-invalid="true"` on the invalid control.
- Associate the error with the control using `aria-describedby`.
- Preserve the user’s entered values.
- On submit, show an error summary at the top with links to invalid fields and move focus to the summary or first invalid field.
- Do not rely on a red border or icon alone.
- Use a hidden “Error:” prefix if needed so screen readers receive clear context.

Example:

```html
<label for="monthly-saving">Monthly amount you could save</label>
<input id="monthly-saving"
       aria-invalid="true"
       aria-describedby="monthly-saving-error">
<p id="monthly-saving-error">Error: Enter an amount from $0 to $100,000.</p>
```

Use [3.3.1 Error Identification](https://www.w3.org/WAI/WCAG22/Understanding/error-identification.html), [3.3.3 Error Suggestion](https://www.w3.org/WAI/WCAG22/Understanding/error-suggestion.html), and W3C’s [User Notifications tutorial](https://www.w3.org/WAI/tutorials/forms/notifications/). GOV.UK’s [Error message guidance](https://design-system.service.gov.uk/components/error-message/) is a useful implementation reference.

### Chat/API errors

Distinguish user-correctable validation errors from service failures:

- Keep the unsent question in the composer.
- Show a concise inline message near the failed response: “We couldn’t get a response. Check your connection and try again.”
- Provide a keyboard-accessible “Try again” button.
- Use a polite status region for ordinary failures; reserve `role="alert"` for urgent errors requiring immediate attention.
- Do not erase the conversation or silently retry forever.
- Explain data limitations separately, for example: “Market data may be delayed.”

## 7. Touch targets and mobile input

WCAG 2.2 AA requires pointer targets to be at least **24 × 24 CSS pixels**, unless an exception applies: [2.5.8 Target Size (Minimum)](https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html).

For usability, target **44–48 px** for primary buttons, chips, close buttons, send, profile, and menu controls:

- Give icon-only buttons an accessible name, e.g. `aria-label="Open profile"`.
- Make the entire visual button area clickable, not only a small icon.
- Leave spacing between adjacent icon buttons and chips.
- Do not place tiny close, edit, or source controls next to one another.
- Ensure controls remain usable at increased text size and browser zoom.
- Use appropriate input types and `inputmode` values to provide mobile keyboards, while retaining visible labels.
- Avoid disabling pinch zoom with viewport configuration.

W3C’s form guidance recommends visible labels and appropriate HTML5 form fields for mobile: [Labeling Controls](https://www.w3.org/WAI/tutorials/forms/labels/).

## 8. Responsive chat/profile layouts

### Mobile-first behavior

Design first for a 320–390 CSS pixel viewport:

- Use one vertical column: header → disclaimer/status → conversation → composer.
- Keep the composer sticky at the bottom only if it does not obscure focused controls or content.
- Account for safe-area insets on devices with home indicators.
- Make long assistant responses wrap naturally with `overflow-wrap:anywhere`.
- Avoid fixed-width chat bubbles, sidebars, and cards.
- Keep the message content width readable; bubbles may use roughly 90% of the mobile width and a narrower maximum width on desktop.
- Do not rely on horizontal scrolling for normal prose or controls.
- A comparison table may scroll horizontally within its own labeled container because tabular comparison is a valid two-dimensional layout; provide an accessible caption and consider a stacked/card alternative on small screens.
- Move the profile panel into a full-screen or near-full-width drawer on mobile. On desktop, use a persistent aside or a non-modal panel.
- Keep all profile fields available in the drawer; do not hide essential functionality on mobile.

WCAG requires content to reflow without loss of information or functionality at a width equivalent to **320 CSS pixels** and at 400% zoom, except for content whose two-dimensional layout is essential: [1.4.10 Reflow](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html). Also test [1.4.4 Resize Text](https://www.w3.org/WAI/WCAG22/Understanding/resize-text.html) and [1.4.12 Text Spacing](https://www.w3.org/WAI/WCAG22/Understanding/text-spacing.html).

### Desktop behavior

At a sufficiently wide breakpoint:

```text
┌──────────────────────────────────────────────────────────────┐
│ Header: product                         Profile   Help        │
├────────────────┬─────────────────────────────────────────────┤
│ Profile aside  │ Conversation                              │
│ review/edit    │ Assistant and user messages                │
│                │                                             │
│                │                                             │
│                ├─────────────────────────────────────────────┤
│                │ Message input                         Send  │
└────────────────┴─────────────────────────────────────────────┘
```

At narrow widths:

```text
┌──────────────────────────────┐
│ Product             Profile  │
├──────────────────────────────┤
│ Conversation                │
│                             │
│ Assistant response          │
│                             │
│ User question               │
│                             │
├──────────────────────────────┤
│ Ask a question…       Send  │
└──────────────────────────────┘
```

Use CSS layout rather than duplicated markup so the semantic order remains logical at every breakpoint.

## 9. Reduced motion

Reduced motion is especially relevant to streaming indicators, drawer transitions, auto-scroll, skeletons, chart animation, and message insertion.

- Respect `prefers-reduced-motion`.
- Remove nonessential slide, bounce, parallax, zoom, and typing animations.
- Replace animated dots with static text such as “Assistant is thinking.”
- Do not animate the page to the latest response when the user did not request it.
- Keep essential state changes understandable without animation.
- Provide an in-app motion setting only if useful; the operating-system preference should work automatically.

Example:

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
    scroll-behavior: auto !important;
  }
}
```

WCAG 2.2’s specific “Animation from Interactions” criterion is **Level AAA**, not AA, but supporting it is a strong practice for this app: [2.3.3 Animation from Interactions](https://www.w3.org/WAI/WCAG22/Understanding/animation-from-interactions.html). Also consider [2.2.2 Pause, Stop, Hide](https://www.w3.org/WAI/WCAG22/Understanding/pause-stop-hide.html) for any automatically moving or updating content.

## 10. Minimum acceptance test

Before shipping, test:

- Keyboard-only navigation through onboarding, chat, profile drawer, disclosures, tables, retry, and send.
- Visible focus at every breakpoint and in dark mode.
- Screen reader announcements for submission, thinking, completion, errors, and new messages.
- No token-by-token streaming announcements.
- Profile drawer focus entry, Tab containment, Escape, and focus restoration.
- 320px viewport, 400% zoom, and text-only reflow.
- Contrast ratios for body text, muted text, links, borders, icons, selected states, errors, and focus.
- Touch targets of at least 24×24 CSS px; primary controls preferably 44–48 px.
- `prefers-reduced-motion: reduce`.
- Voice control or switch-style keyboard emulation for buttons and form controls.
- Chat behavior while the user is reading older messages: no forced scroll, focus movement, or disappearing content.