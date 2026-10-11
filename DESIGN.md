# Design · Alex

Visual world: **Intaglio Note**, from US banknote engraving and security printing. Each answer is
"issued" like a note: engraved, serial-numbered and backed by visible evidence. The world gives
the product its type, palette, density and one signature move. Layout, navigation and controls
stay standard web components.

Source of truth: `app/static/style.css` (tokens on `:root`) and `app/static/app.js`
(the guilloché generators).

## Palette

| Token | Value | Job |
|---|---|---|
| `--paper` | `#ecede4` | Page ground (currency paper) |
| `--paper-hi` | `#f6f7f1` | Issued answer sheet, inputs |
| `--paper-lo` | `#e2e4d8` | Evidence rail |
| `--rule` | `#c3c7b6` | Every hairline. Division comes from 1px rules, not boxes |
| `--ink` / `--ink-soft` | `#15181a` / `#4a5048` | Text / secondary text |
| `--face` | `#1f3a2e` | Intaglio face green: the header band, primary buttons, questions, focus ring |
| `--back` | `#3f6b52` | Labels, PS codes, table headers |
| `--evidence` | `#7f5300` | **Reserved** for citations and tool calls. Nothing else uses it |
| `--evidence-tint` | `#f1e6cf` | Highlight for a focused citation and its source |
| `--fibre-red` | `#a8231b` | Serial numbers and failure state only |
| `--fibre-blue` | `#2b4c9a` | Links only |

It's light only. The use scene is a projected demo, so it isn't based on the OS theme.

## Type

| Role | Face | Size |
|---|---|---|
| Wordmark | Cinzel 600, tracked .14em | 30px (24px on phone). Used for the wordmark only |
| Answer prose | Source Serif 4 | 17px/1.6, measure ≤72ch. Headings 20–23px, balanced |
| Welcome heading | Source Serif 4 600 | 30px |
| UI | Public Sans | 15px body, 13–14px controls |
| Labels | Public Sans 600, uppercase, tracked .16em | 12px minimum |
| Citations / evidence rows | Public Sans 600 / 400 | 13.5px / 14.5px, sized for a projector |

Every number uses `font-variant-numeric: tabular-nums`. Nothing is under 12px except the raw
JSON in tool results.

## Layout

- A 72px band, then a 3-column grid: profile `clamp(280px,22vw,340px)` | conversation
  `minmax(0,1fr)` | evidence `clamp(300px,25vw,390px)`.
- The band uses the same column template, so the wordmark, source status and session serial line
  up with the work areas below.
- **At 1180px and below**, the evidence rail is hidden and each answer carries its evidence in an
  inline `<details>`.
- **At 760px and below** it's a single column: the profile fields collapse behind "Show fields",
  the composer is sticky, and the fine print is hidden (every answer and the header still carry
  the disclosure).

## Components

- **Persona buttons:** rectangular with a 2px radius. Selected is solid face green with
  `aria-pressed`.
- **Profile rows:** a hairline above each row. The PS code sits in the left gutter, with the
  label and an inline borderless input to its right. Blank fields read "unknown" in italic.
- **Question:** a solid face-green block, right-aligned.
- **Note (answer):**
  - It sits on a paper-hi sheet with a hairline border and a soft offset shadow.
  - The head row has the red serial (`A 0001 · DATA OCT 9, 4:00 PM ET`), the call, rule and
    time counts, and the provenance mark as a button.
  - A note that couldn't be issued gets a red border, "NOT ISSUED" and a Try again button.
- **Citation:** every KB ID in an answer becomes a `<button class="cite">`. It's set in evidence
  ink with an underline, and its title shows the rule summary from `/api/kb`.
- **Evidence rail:** provenance mark and caption, then market-data calls (name, arguments,
  provider and timestamp, raw JSON in a `<details>`), then the KB IDs cited with their summaries,
  then model, time and tokens.
- **Composer:** a textarea with a 1.5px face-green border, "Ask Alex" as the primary button and
  "New conversation" as the secondary. Enter sends and Shift+Enter adds a newline.

## Signature: the provenance mark

`rosette(petals, rings)` in `app.js` draws a guilloché rosette:
- The outer petal frequency equals the number of rules cited, between 3 and 24, drawn in face
  green.
- There is one inner wavy ring per market-data call (up to 8), drawn in evidence ink.
- Clicking a note's mark brings up its evidence: the rail scrolls to the top and replays the settle animation, or, when the rail is hidden, the note's inline evidence opens.

The band's background is generated wave line work at 20% opacity.

## Motion

There is one authored moment. While Alex is working, the pending rosette engraves itself:
`stroke-dashoffset` on `pathLength=1` paths, 2.4s ease-out, alternating. When the note is
issued, its mark settles in one 1.1s draw. Focusing a citation fades the other evidence items to
38% and highlights its source. `prefers-reduced-motion` turns off all the drawing.

## Browser surfaces

- Selection is a 22% back-green tint (never the evidence tint, which only marks provenance), and the caret is face green.
- The focus ring is 2px face green with a 2px offset.
- Scrollbars use rule-colored thumbs, and link underlines are offset 3px.

## Rules

- Evidence ink only marks provenance. Never use it for emphasis or decoration.
- Use no money motifs beyond the guilloché and the serial: no seals, portraits or dollar signs as
  ornament. They would imply endorsement or a guarantee, which guardrails GR-001 and GR-003 rule
  out.
- Never present data as live. Every timestamp names "delayed" and its time zone.
