# data-display — beginner-friendly presentation of stock and fund information

## Recommendation

Use a **snapshot → explanation → comparison** hierarchy. A beginner should be able to answer “What is this, what is it worth, how did it move, and when was that measured?” without opening a chart or decoding an API response. Do not expose raw tool-call JSON, field names, or unexplained provider codes in the product UI.

Treat market data as time-bounded education, not a recommendation. Include the app’s general-education disclaimer near investment comparisons, and avoid language such as “best,” “buy,” or “safe.”

## 1. Quote cards

Use one compact quote card for a searched security and the same component inside answers. Keep the first view to the fields most people need:

- **Name** and **ticker**: “Vanguard Total Stock Market ETF (VTI)”.
- **Plain-language type**: “ETF — a fund traded during the day,” “Mutual fund — a pooled fund priced once per business day,” or “Stock — a share of one company.” Keep the formal term in a secondary line.
- **Current price** (or **NAV** for a mutual fund) with currency.
- **Change today** shown both as a dollar amount and a percentage: “+$1.24 (+0.62%) today.” Label the period explicitly; do not make users infer whether it is intraday, since open, or one-year performance.
- A small **sparkline** with a visible range selector such as 1D / 1M / 1Y / 5Y. The selected range must be written in the heading or accessible name.
- **As of** timestamp, timezone, market status, and data state: “As of Jun 12, 2025, 4:00 PM ET · market closed · quote may be delayed.”
- **Source** link and, where relevant, “Prices can change; this is not a recommendation.”

For funds, add only a few high-value facts below the fold: **expense ratio** (“annual fund operating expenses”), assets, number of holdings, distribution yield (with its measurement period), and benchmark. For an ETF, distinguish **market price** from **NAV** rather than presenting them as interchangeable. A mutual-fund NAV and an exchange-traded market quote have different timing and meanings; label them accordingly.

Recommended card anatomy:

```text
Vanguard Total Stock Market ETF                  VTI
ETF · holds many U.S. companies
$286.41                                  As of Jun 12, 2025, 4:00 PM ET
+$1.24 (+0.62%) today                    Market closed · data may be delayed
[ sparkline ]                             1D  1M  1Y  5Y
Expense ratio  0.03% · Fund fee, charged from fund assets
[Compare] [Learn what these numbers mean]
```

Do not color the entire card or use green/red as the only status signal. The sign, words, and arrow provide the meaning even in monochrome or for color-vision deficiencies.

## 2. Comparison cards and tables

When a user asks “How does VOO compare with VTI?”, show two compact identity cards followed by a **small comparison table**. Keep the table to roughly 5–8 rows initially and allow “Show more,” rather than presenting every available fund field.

Suggested beginner rows:

| Comparison row | Example plain-language label | Why it matters |
|---|---|---|
| What it owns | “Large U.S. companies” / “Nearly the whole U.S. stock market” | Explains exposure before performance |
| Number of holdings | “About 500” / “About 3,700” | A quick diversification signal; not a safety score |
| Fund fee | “0.03% annual fund fee” | Makes expense ratio understandable |
| 1-year return | “+12.4% over the last year” | Time-bounded historical result |
| 5-year annualized return | “+14.1% per year, annualized” | Prevents confusing a total return with a yearly rate |
| Risk / volatility | “How much returns have varied” | Explains the metric rather than implying a forecast |
| Benchmark | “Index the fund aims to track” | Helps users understand what performance is being compared with |

Add a short **“What this means”** sentence under unusual rows. Example: “VTI owns more companies; that does not guarantee a higher return.” If a field is unavailable, say “Not available” rather than silently dropping the row. Display the same as-of date or measurement period for both columns; if periods differ, flag that prominently and do not imply a fair comparison.

Do not produce a winner badge from one metric. If a comparison is personalized by the chat context, phrase it as education: “The trade-off to explore is broader coverage versus exposure to large companies,” followed by a link to the relevant explanation.

Use semantic HTML for the table: a visible `<caption>`, `<th scope="col">` for column headers, and `<th scope="row">` for row labels. GOV.UK’s table guidance specifically recommends captions for finding and understanding a table, scope attributes for assistive technology, and right-aligning comparable numbers. Source: https://design-system.service.gov.uk/components/table/

On narrow screens, preserve the row/column relationship with horizontal scrolling and a sticky first column, or transform each security into a labeled card. Never turn the table into unlabeled number blocks. Ensure the comparison control itself has a visible focus state and a clear accessible name.

## 3. Sparklines

Sparklines are useful as a quiet orientation cue, not as a substitute for data:

- Put the range in the title: “VTI price trend — 1 year.”
- Give the start and end dates and values in adjacent text; show the latest value outside the line.
- Add a text summary, for example: “Ended higher than it started; largest dip was in March.” The summary should be generated from the actual series, not guessed from the line color.
- Use a line plus endpoint/hover details, not color alone. If the graphic conveys material information, provide the values or a data table in the DOM / an “View data” disclosure. W3C says complex charts need a short identification plus a textual representation of essential information, and recommends making the description available to everyone. Source: https://www.w3.org/WAI/tutorials/images/complex/
- Use an accessible SVG `<title>` and `<desc>` or an adjacent visible description; do not rely on an image `alt` such as “chart.”
- Avoid deceptive scaling: state whether the line is price, total return, or normalized performance, and whether dividends are included. A sparkline with no axis is acceptable only when it is clearly labeled as a qualitative trend.
- Respect `prefers-reduced-motion`; no automatic animated drawing, pulsing, or live updates that repeatedly move the user’s focus.

## 4. Plain-language labels

Prefer familiar labels with the technical term in parentheses only when it helps learning:

- “Price” rather than “last trade”; “Fund fee (expense ratio)” rather than “ER”; “Companies held” rather than “holdings count”; “How widely the fund is spread” rather than “diversification”; “Return over the last year” rather than “1Y performance”; “Fund price (NAV)” rather than “NAV” alone.
- Explain **return** as “how much the investment changed over a period,” and distinguish price change from total return (which may include distributions).
- Explain **annualized** as “the average yearly rate over this period; it is not what happened in each year.”
- Explain **yield** with its period and avoid presenting it as a guaranteed interest rate.
- Put definitions next to the number through short helper text or a “What does this mean?” disclosure. Do not hide essential meaning in a hover-only tooltip, which is poor for touch, keyboard, and screen-reader users.
- Use sentence-case labels, one concept per row, and examples for unfamiliar numbers. Keep explanatory copy brief and link to a glossary for depth.

For investor education, link to official SEC/Investor.gov explanations of mutual funds and ETFs, diversification, fees, and past performance. Useful entry points include:

- Investor.gov investment products: https://www.investor.gov/investing-basics/investment-products
- Investor.gov fees and expenses: https://www.investor.gov/introduction-investing/investing-basics/understanding-fees
- Investor.gov past performance glossary: https://www.investor.gov/introduction-investing/investing-basics/glossary/past-performance

The UI should repeat the practical warning associated with historical numbers: past performance is not a reliable promise of future results. Do not turn a historical return into a forecast.

## 5. Accessible gain/loss encoding

WCAG 2.2 SC 1.4.1 says color cannot be the only visual means of conveying information; W3C explicitly recommends adding text or shape. Source: https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html

Implement gain/loss as a redundant combination:

- **Text**: “Gain,” “Loss,” or “No change,” plus the signed amount and percentage.
- **Symbol**: `↑` / `↓` or a meaningful inline SVG with an accessible label; do not use an ambiguous decorative icon alone.
- **Color**: a restrained positive/negative accent as a third cue, never the only cue. Do not assume green means gain for every theme or culture.
- **Accessible name**: a screen reader should hear “Gain, one dollar and twenty-four cents, zero point six two percent today,” not “green text.”
- **Non-color contrast**: meaningful chart strokes, status icons, focus indicators, and controls should meet at least 3:1 against adjacent colors under WCAG 2.2 SC 1.4.11. Source: https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html

Use the same treatment for filters, legends, and chart series: label each series in text and provide a pattern, marker, or line style in addition to hue. Test with grayscale, common color-vision simulations, keyboard navigation, zoom, and a screen reader.

## 6. Number and typography conventions

Use locale-aware formatting in JavaScript (`Intl.NumberFormat`) and keep the underlying numeric value separate from its display string. Use a font with tabular numerals for aligned financial values:

```css
.financial-number {
  font-variant-numeric: tabular-nums;
  text-align: end;
}
```

Conventions for the initial beginner UI:

- **Currency / price:** show the currency symbol and two decimals for a share price or NAV, e.g. `$286.41`. Use the user’s locale/currency when known; never silently mix USD and another currency. If precision is not meaningful, do not suggest false accuracy.
- **Dollar change:** `$+1.24` or `+$1.24` consistently throughout the product. Put the sign before the number and pair it with “Gain” / “Loss.”
- **Percentages:** include `%` every time, include the sign for change and return, and use one decimal for performance in beginner summaries (`+6.2%`). Use two decimals only when the difference is meaningful. Do not display `6.2` without saying it is a percent.
- **Fees:** show the percent and plain-language unit: `0.03% annual fund fee`; do not convert it to dollars unless the principal and period are explicit. For example, “about $3 per year for each $10,000 invested, before other effects” is more understandable than a bare basis-point value.
- **Basis points:** hide “bps” in the beginner layer; write “0.05 percentage points (5 basis points)” only in expanded detail.
- **Large values:** show the exact value in the primary view (`$1,234,567,890`) or use a compact value only with an exact accessible/expanded value (`$1.23B` / `$1,230,000,000`). Avoid unexplained K/M/B abbreviations.
- **Zeros and negatives:** use `0.00%` or “No change,” never a blank or a color-only neutral state. Prefer a minus sign (`−2.4%`) over parentheses in beginner-facing values; reserve accounting parentheses for contexts where users expect them.
- **Alignment:** left-align names and explanatory text; right/end-align prices, percentages, counts, and dates in comparison columns. Use consistent decimal precision within a column.
- **Significant digits:** do not show more decimal places than the source supports. Use an em dash for unavailable data and a visible “estimated” or “not available” label where appropriate.

MDN documents `font-variant-numeric: tabular-nums` as selecting figures where all numerals occupy the same width, which supports column scanning: https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/font-variant-numeric
MDN’s `Intl.NumberFormat` reference covers locale-sensitive currency, percent, and unit formatting: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/NumberFormat

## 7. “As of” and data freshness

Every quote, chart, return, NAV, yield, and fund statistic must have a visible measurement date/time or period. Separate these concepts:

- **As of:** when the displayed market value or statistic was measured (`As of Jun 12, 2025, 4:00 PM ET`).
- **Last updated:** when the app fetched or rendered the value. This can be later than the market measurement.
- **Period:** the interval for a return (`1-year return: Jun 12, 2024–Jun 12, 2025`) and whether it is cumulative or annualized.

Display the timezone and an explicit state such as “Market open,” “Market closed,” “Delayed quote,” “Previous close,” or “Fund NAV dated Jun 11.” Never display “today” without the date/time behind it. For a stale or failed feed, retain the old value only if it is clearly marked with its original as-of time; otherwise show “Data unavailable” rather than silently presenting it as current. A refresh should update the timestamp and source state, not just the number.

Use one consistent timestamp format in the interface, for example `As of Jun 12, 2025, 4:00 PM ET` and, in expanded detail, the machine-readable ISO timestamp. Include a source/provider link so users can verify the value. Market-data providers may differ in close time, NAV publication time, adjustments, and delay; the card should expose those facts instead of implying every number is real-time.

## Minimal implementation checklist

- Build one reusable `QuoteCard`, one `Sparkline`, and one semantic `ComparisonTable`; do not hand-code a different format for every chat answer.
- Normalize backend data into explicit fields: `instrumentType`, `priceOrNav`, `currency`, `changeAmount`, `changePercent`, `period`, `asOf`, `timezone`, `marketState`, `isDelayed`, `source`, and `sourceUrl`.
- Render values as text first; add color and SVG only as redundant visual enhancement.
- Give every chart a visible title, period, endpoint values, and text summary; provide a data table or “View data” disclosure.
- Keep the first view calm and sparse; put methodology, methodology caveats, fees, and definitions in progressive disclosure.
- Test keyboard and screen-reader output, 200% zoom, narrow screens, dark mode, grayscale, and missing/stale data before launch.

## Sources

- W3C WCAG 2.2 — Use of Color (SC 1.4.1): https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html
- W3C WCAG 2.2 — Non-text Contrast (SC 1.4.11): https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html
- W3C WAI Images Tutorial — Complex Images (charts need textual alternatives): https://www.w3.org/WAI/tutorials/images/complex/
- GOV.UK Design System — Table (captions, header scope, comparison tables, right-aligned numbers): https://design-system.service.gov.uk/components/table/
- MDN — `font-variant-numeric`: https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/font-variant-numeric
- MDN — `Intl.NumberFormat`: https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Intl/NumberFormat
- Investor.gov — Investment products: https://www.investor.gov/investing-basics/investment-products
- Investor.gov — Understanding fees: https://www.investor.gov/introduction-investing/investing-basics/understanding-fees
- Investor.gov — Past performance glossary: https://www.investor.gov/introduction-investing/investing-basics/glossary/past-performance
