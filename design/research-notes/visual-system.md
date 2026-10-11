# Visual system: calm, trustworthy finance UI

## 1. Design direction

Use a quiet, editorial interface rather than a trading terminal:

- Warm off-white background, white surfaces, deep forest text, and restrained teal accents.
- One primary action color; avoid neon green, saturated gradients, ticker-like motion, and excessive card borders.
- Use color to support meaning, never as the only indicator of gain/loss, risk, selection, or errors.
- Prefer hierarchy, whitespace, and typography over decoration.
- Keep financial numbers visually stable: use tabular numerals and do not animate changing values.
- Use a 4 px spacing base and moderate radii. Cards should feel soft but not playful.
- Use borders and elevation sparingly; a surface should generally be distinguished by either a border or a shadow, not both.

This combines Material 3’s semantic color/elevation approach with WCAG 2.2 contrast and focus requirements.

## 2. Typography

### Font

Use **Inter** from Google Fonts, with a system fallback:

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
```

```css
font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont,
  "Segoe UI", sans-serif;
```

Inter is appropriate for this interface because it is neutral, highly legible at small sizes, and has clear distinctions between similar characters. If loading an external font is undesirable, use the system stack alone.

Use:

```css
font-variant-numeric: tabular-nums;
```

for prices, percentages, balances, dates, and comparison-table values so columns do not shift as numbers change.

### Type scale

| Token | Size / line height | Weight | Use |
|---|---:|---:|---|
| `--text-xs` | 12 / 16 px | 500 | Metadata, timestamps, source labels |
| `--text-sm` | 14 / 20 px | 400–500 | Secondary text, labels, helper copy |
| `--text-md` | 16 / 24 px | 400 | Default body and chat text |
| `--text-lg` | 18 / 26 px | 500–600 | Intro copy, emphasized answer text |
| `--text-xl` | 22 / 28 px | 600 | Section headings |
| `--text-2xl` | 28 / 34 px | 600 | Page heading, empty-state heading |
| `--text-3xl` | 36 / 42 px | 600 | Large balance or hero value; use sparingly |

Rules:

- Body text is always at least 16 px.
- Use sentence case, not all caps, except for very short metadata labels.
- Keep body measure between approximately 55–75 characters on desktop.
- Use 600 rather than 700 for most headings; this keeps the interface calm.
- Do not use light or thin font weights for essential text.

## 3. Ready-to-use CSS tokens

```css
:root {
  color-scheme: light;

  /* Typography */
  --font-sans: Inter, ui-sans-serif, system-ui, -apple-system,
    BlinkMacSystemFont, "Segoe UI", sans-serif;
  --font-mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas,
    "Liberation Mono", monospace;

  --text-xs: 0.75rem;    /* 12px */
  --text-sm: 0.875rem;   /* 14px */
  --text-md: 1rem;       /* 16px */
  --text-lg: 1.125rem;   /* 18px */
  --text-xl: 1.375rem;   /* 22px */
  --text-2xl: 1.75rem;   /* 28px */
  --text-3xl: 2.25rem;   /* 36px */

  --leading-xs: 1.333;
  --leading-sm: 1.429;
  --leading-md: 1.5;
  --leading-lg: 1.444;
  --leading-xl: 1.273;
  --leading-2xl: 1.214;
  --leading-3xl: 1.167;

  /* Spacing: 4px base unit */
  --space-1: 0.25rem;  /* 4px */
  --space-2: 0.5rem;   /* 8px */
  --space-3: 0.75rem;  /* 12px */
  --space-4: 1rem;     /* 16px */
  --space-5: 1.25rem;  /* 20px */
  --space-6: 1.5rem;   /* 24px */
  --space-8: 2rem;     /* 32px */
  --space-10: 2.5rem;  /* 40px */
  --space-12: 3rem;    /* 48px */
  --space-16: 4rem;    /* 64px */

  /* Layout */
  --content-max: 44rem;
  --page-gutter: 1.25rem;
  --header-height: 4rem;

  /* Radius */
  --radius-sm: 0.375rem;  /* 6px */
  --radius-md: 0.625rem;  /* 10px */
  --radius-lg: 0.875rem;  /* 14px */
  --radius-xl: 1.25rem;   /* 20px */
  --radius-pill: 999px;

  /* Light surfaces */
  --color-bg: #f7f8fa;
  --color-surface: #ffffff;
  --color-surface-subtle: #f1f4f2;
  --color-surface-selected: #e7f2ed;
  --color-overlay: rgba(23, 33, 29, 0.48);

  /* Light text */
  --color-text: #17211d;
  --color-text-muted: #52605a;
  --color-text-subtle: #68766f;
  --color-text-on-primary: #ffffff;
  --color-text-on-danger: #ffffff;

  /* Light borders and focus */
  --color-border: #d7dfda;
  --color-border-strong: #aebbb3;
  --color-focus: #245a73;
  --color-focus-soft: #b9dcea;

  /* Brand/action */
  --color-primary: #176b52;
  --color-primary-hover: #0f513d;
  --color-primary-soft: #e7f2ed;
  --color-link: #245a73;

  /* Semantic colors */
  --color-positive: #176b52;
  --color-positive-soft: #e7f2ed;
  --color-negative: #a33a35;
  --color-negative-soft: #fbeceb;
  --color-warning: #7a4d00;
  --color-warning-soft: #fff3d6;
  --color-info: #245a73;
  --color-info-soft: #e8f3f8;

  /* Elevation */
  --shadow-sm: 0 1px 2px rgba(23, 33, 29, 0.06);
  --shadow-md: 0 6px 18px rgba(23, 33, 29, 0.08),
                0 2px 5px rgba(23, 33, 29, 0.05);
  --shadow-lg: 0 16px 40px rgba(23, 33, 29, 0.14),
                0 4px 12px rgba(23, 33, 29, 0.07);

  /* Motion */
  --duration-fast: 120ms;
  --duration-standard: 180ms;
  --duration-slow: 260ms;
  --ease-standard: cubic-bezier(0.2, 0, 0, 1);
  --ease-emphasized: cubic-bezier(0.2, 0, 0, 1);

  /* Focus ring */
  --focus-ring: 0 0 0 3px var(--color-focus-soft);
}

[data-theme="dark"] {
  color-scheme: dark;

  --color-bg: #101513;
  --color-surface: #17201c;
  --color-surface-subtle: #1d2823;
  --color-surface-selected: #203a30;
  --color-overlay: rgba(0, 0, 0, 0.62);

  --color-text: #f3f7f4;
  --color-text-muted: #b6c4bc;
  --color-text-subtle: #92a199;
  --color-text-on-primary: #0e2a20;
  --color-text-on-danger: #26100e;

  --color-border: #3a4941;
  --color-border-strong: #617168;
  --color-focus: #8dd6f0;
  --color-focus-soft: #315668;

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

  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.28);
  --shadow-md: 0 8px 20px rgba(0, 0, 0, 0.32);
  --shadow-lg: 0 18px 44px rgba(0, 0, 0, 0.44);
}

/* Respect an OS-level dark preference unless the app explicitly chooses light. */
@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    color-scheme: dark;

    --color-bg: #101513;
    --color-surface: #17201c;
    --color-surface-subtle: #1d2823;
    --color-surface-selected: #203a30;
    --color-overlay: rgba(0, 0, 0, 0.62);

    --color-text: #f3f7f4;
    --color-text-muted: #b6c4bc;
    --color-text-subtle: #92a199;
    --color-text-on-primary: #0e2a20;
    --color-text-on-danger: #26100e;

    --color-border: #3a4941;
    --color-border-strong: #617168;
    --color-focus: #8dd6f0;
    --color-focus-soft: #315668;

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

    --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.28);
    --shadow-md: 0 8px 20px rgba(0, 0, 0, 0.32);
    --shadow-lg: 0 18px 44px rgba(0, 0, 0, 0.44);
  }
}

/* Global defaults */
html {
  font-family: var(--font-sans);
  font-size: 16px;
  background: var(--color-bg);
  color: var(--color-text);
}

body {
  margin: 0;
  background: var(--color-bg);
  color: var(--color-text);
  font-size: var(--text-md);
  line-height: var(--leading-md);
  font-synthesis: none;
  text-rendering: optimizeLegibility;
}

button,
input,
textarea,
select {
  font: inherit;
}

button,
a,
input,
textarea,
select {
  -webkit-tap-highlight-color: transparent;
}

:focus-visible {
  outline: 2px solid var(--color-focus);
  outline-offset: 2px;
  box-shadow: var(--focus-ring);
}

.numeric,
[data-numeric="true"] {
  font-variant-numeric: tabular-nums;
}
```

## 4. Color and contrast rules

### Required pairings

Use these combinations as the default accessible pairings:

| Context | Foreground | Background |
|---|---|---|
| Primary body text, light | `#17211D` | `#F7F8FA` or `#FFFFFF` |
| Secondary text, light | `#52605A` | `#F7F8FA` or `#FFFFFF` |
| Primary button, light | `#FFFFFF` | `#176B52` |
| Link, light | `#245A73` | `#F7F8FA` or `#FFFFFF` |
| Error text, light | `#A33A35` | `#FFFFFF` |
| Primary body text, dark | `#F3F7F4` | `#101513` or `#17201C` |
| Secondary text, dark | `#B6C4BC` | `#101513` or `#17201C` |
| Primary button, dark | `#0E2A20` | `#83D2B1` |
| Link, dark | `#8DD6F0` | `#101513` or `#17201C` |
| Error text, dark | `#FFB4AB` | `#101513` or `#17201C` |

WCAG 2.2 requires:

- At least **4.5:1** for normal text.
- At least **3:1** for large text.
- At least **3:1** for meaningful icons, chart lines, control boundaries, and state indicators.

Do not use `--color-text-subtle` for required instructions, input labels, error messages, or body text without checking the final background. It is intended for nonessential metadata.

### Financial meaning

- Positive: use `--color-positive` plus a `+` sign, “up,” or an upward icon.
- Negative: use `--color-negative` plus a `−` sign, “down,” or a downward icon.
- Neutral: use the standard text color and an em dash or “unchanged.”
- Never communicate gain/loss with green/red alone.
- Avoid red/green chart pairs. Use teal and blue for separate series, with labels or patterns.
- Warnings should include an icon and an explicit label such as “Important” or “Risk.”

### Surfaces

- Page background: `--color-bg`.
- Main content and message cards: `--color-surface`.
- Intake sections, selected controls, and subtle grouping: `--color-surface-subtle`.
- Selected chip or active navigation state: `--color-surface-selected`.
- Use a 1 px border for inputs and dense tables.
- Use a shadow for floating drawers, menus, and dialogs.
- Do not place a heavy shadow on every card.

## 5. Component geometry

### Buttons

- Minimum visual height: 44 px.
- Horizontal padding: 16 px.
- Primary radius: `--radius-md`.
- Primary button: solid `--color-primary` with `--color-text-on-primary`.
- Secondary button: transparent or `--color-surface`, 1 px `--color-border-strong`.
- Tertiary button: no border; use a visible text label and hover background.
- Disabled controls must remain readable; reduce opacity only slightly and use a distinct disabled background.
- Icon-only buttons must have an accessible name and a 44 × 44 px hit area.

### Chips

- Height: 36–40 px.
- Horizontal padding: 12–14 px.
- Radius: `--radius-pill`.
- Use chips for answer choices and follow-up prompts, not for dense navigation.
- Selected state should use fill, border, check icon, and/or text—not color alone.

### Inputs

- Height: 44–48 px.
- Padding: 12 px.
- Radius: `--radius-md`.
- Background: `--color-surface`.
- Border: 1 px `--color-border-strong`.
- Label sits above the field; do not rely on placeholder text as the label.
- Focus state uses the global visible focus ring.
- Error state adds an error icon and text below the field; do not rely only on a red border.

### Cards

- Default padding: 16 px.
- Larger data card padding: 20–24 px.
- Radius: `--radius-lg`.
- Border: 1 px `--color-border` when the card needs separation.
- Use `--shadow-sm` only for elevated or interactive cards.
- Keep card titles short and put the primary value first.

### Chat bubbles

- User message: `--color-primary-soft`, aligned to the right where space permits.
- Assistant message: transparent or `--color-surface`, aligned to the main reading column.
- Avoid large rounded “pill” bubbles for long answers. Use a modest 14 px radius.
- Assistant text should be readable as normal document content, not compressed into a narrow bubble.
- Keep the assistant content column around 44 rem maximum.

### Quote and comparison cards

- Instrument name and ticker at the top.
- Primary price or value in 22–28 px semibold.
- Change shown with sign, percentage, and text label.
- Include “As of [time]” in 12–14 px text.
- Show delayed-data status where applicable.
- Use `font-variant-numeric: tabular-nums`.
- Do not make a sparkline the only representation of performance; include a text value and period.

## 6. Motion

Motion should communicate state, hierarchy, and continuity—not add excitement to investing.

Recommended values:

```css
.transition-standard {
  transition:
    background-color var(--duration-standard) var(--ease-standard),
    border-color var(--duration-standard) var(--ease-standard),
    color var(--duration-standard) var(--ease-standard),
    box-shadow var(--duration-standard) var(--ease-standard),
    transform var(--duration-standard) var(--ease-standard);
}
```

Guidelines:

- Hover and pressed feedback: 120–180 ms.
- Drawer, modal, and disclosure transitions: 180–260 ms.
- Use small opacity/translate transitions for messages entering the chat.
- Do not animate balances, prices, percentages, or chart values as a flourish.
- Do not use flashing, bouncing, parallax, or continuous decorative movement.
- Loading indicators may use a subtle three-dot pulse, but must also have accessible status text such as “Thinking.”
- Never make progress or important information depend on animation.
- Preserve the user’s scroll position when streaming an answer unless the user is already at the bottom.

Respect reduced motion:

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 1ms !important;
    animation-iteration-count: 1 !important;
    scroll-behavior: auto !important;
    transition-duration: 1ms !important;
  }
}
```

For reduced-motion users, replace animated loading dots with a static “Thinking…” label and avoid sliding drawers; use an immediate state change instead.

## 7. Responsive application

### Desktop

- Main content max width: 44 rem.
- Page gutter: 20–32 px.
- Profile drawer: 320–380 px wide.
- Header height: 64 px.
- Keep the conversation visually central; do not recreate the existing developer-tool sidebar.
- Use a two-column layout only when the profile drawer is explicitly opened.

### Mobile

- Page gutter: 16 px.
- Full-width chat content.
- Composer fixed to the bottom with safe-area padding.
- Keep controls at least 44 × 44 px; WCAG 2.2’s AA minimum target size is 24 × 24 CSS px, but 44 px is a more comfortable mobile target.
- Chips can horizontally scroll rather than wrap into an overly tall block.
- Use a bottom sheet or full-screen profile view instead of a narrow desktop-style drawer.
- Ensure the keyboard does not obscure the composer.

## 8. Source basis

- W3C, WCAG 2.2 — Contrast Minimum:  
  https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html
- W3C, WCAG 2.2 — Non-text Contrast:  
  https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html
- W3C, WCAG 2.2 — Target Size Minimum:  
  https://www.w3.org/WAI/WCAG22/Understanding/target-size-minimum.html
- W3C, WCAG 2.2 overview and normative success criteria:  
  https://www.w3.org/TR/WCAG22/
- Material Design 3 — Color system:  
  https://m3.material.io/styles/color/system/overview
- Material Design 3 — Typography and type-scale tokens:  
  https://m3.material.io/styles/typography/type-scale-tokens
- Material Design 3 — Elevation:  
  https://m3.material.io/styles/elevation/overview
- Material Design 3 — Motion:  
  https://m3.material.io/styles/motion/overview
- Google Fonts — Inter:  
  https://fonts.google.com/specimen/Inter
- MDN — `prefers-reduced-motion`:  
  https://developer.mozilla.org/en-US/docs/Web/CSS/@media/prefers-reduced-motion
- GOV.UK Design System — spacing:  
  https://design-system.service.gov.uk/styles/spacing/
- GOV.UK Design System — typography:  
  https://design-system.service.gov.uk/styles/typography/