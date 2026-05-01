# PropsBot Tools

Free betting calculators built for [PropsBot.AI](https://propsbot.ai) — dark glass theme matching the app's design system, JetBrains Mono for numeric data, scoped CSS, no proprietary AI data exposed.

## Live URLs
- **[/tools/](https://propsbot.ai/tools/)** — landing page (page 38183)
- **[/tools/implied-probability-calculator/](https://propsbot.ai/tools/implied-probability-calculator/)** — IPC (page 38182)
- **[/tools/parlay-calculator/](https://propsbot.ai/tools/parlay-calculator/)** — Parlay (page 38185)

## Architecture (post-audit)

The calculators are **split across four WordPress assets** because WordPress's content filters mangle inline `<style>` and `<script>` tags inside `wp:html` blocks (wptexturize converts `--` to en-dashes; HTML escaper turns `>` to `&gt;`; sanitizer strips `<input>`). Each asset addresses one of those filters.

| Layer | Where it lives | Why |
|---|---|---|
| Widget DOM (HTML structure) | Inline `wp:html` block on each page | Static markup survives WP content filters as long as it doesn't contain `<style>`, `<script>`, or `<input>` |
| Calculator CSS | **WPCode snippet 38192** (`PropsBot Tools Calculator CSS`) — site-wide head | Inline `<style>` in post content gets `--` corrupted to en-dashes by wptexturize, breaking every CSS variable |
| Calculator JS | **WPCode snippet 38188** (`PropsBot Tools Calculator JS`) — site-wide footer | Inline `<script>` content gets HTML-encoded (`>` → `&gt;`), breaking JS parsing. Also creates `<input>` elements programmatically since WP strips them from post content. |
| Nav links injection | **WPCode snippet 38191** (`PropsBot Nav: Inject Tools Calculator Links`) — site-wide footer | Adds three Tools links into the existing accordion menu (`#pb-nav-overlay`) under "Props Tools" section. Works for both desktop and mobile (single hamburger UI). |
| Schema + author byline | **WPCode snippet 38195** (`PropsBot Tools: Schema + Author Byline Injection`) | Outputs `WebApplication`, `FAQPage`, `Article`, `Person`, `Organization`, `CollectionPage` JSON-LD on the relevant pages, plus a visible "By David Reilich, Founder of PropsBot.AI · Last updated [date]" byline above the calculator. Addresses E-E-A-T audit findings. |

## Files in this repo

- `implied-probability-calculator.html` — IPC widget DOM (CSS + JS removed; loaded via snippets)
- `parlay-calculator.html` — Parlay widget DOM
- `calculators.css` — Canonical CSS for both calculators (paste into snippet 38192 if rebuilding)
- `publish-tools-parent.py` — Creates `/tools/` parent + republishes IPC as child
- `publish-parlay.py` — Publishes parlay as child of /tools/
- `republish-both.py` — Re-publishes both pages from current widget files

## Deployment / update workflow

**Changing copy or page structure:**
1. Activate WPCode snippet 38181 (`Temp Page Publish REST Endpoint`)
2. `python republish-both.py`
3. Deactivate snippet 38181

**Changing CSS:** Edit `calculators.css` here, paste into WPCode snippet 38192. Auto-loads site-wide; `.pb-ipc` / `.pb-parlay` class scoping prevents bleed.

**Changing JS:** Update WPCode snippet 38188. Site-wide footer load, gated on whether `.pb-ipc` or `.pb-parlay` exists in the DOM.

**Changing schema or byline:** Update WPCode snippet 38195. Hooks into `wp_head` (schema) and `the_content` filter (byline) only on the three calculator pages.

## Audit findings + fixes applied

Four audit agents ran on the initial deployment (2026-05-01). Findings + responses:

### Critical (fixed)
- **wptexturize corrupted CSS variables** (49 occurrences IPC / 57 parlay). `--pb-*` → `–pb-*` (en-dash) inside post content. **Fix:** CSS moved to WPCode snippet 38192.
- **Title tag duplicate `| PropsBot.AI | PropsBot.AI`** on `/tools/` and `/parlay-calculator/`. **Fix:** updated page titles to remove manual brand suffix.
- **`<input>` elements stripped from post content.** **Fix:** widgets render mount divs; JS creates inputs programmatically.
- **Schema was BreadcrumbList only.** **Fix:** snippet 38195 outputs WebApplication + FAQPage + Article + Person + CollectionPage JSON-LD.
- **No author byline / Person schema / datePublished** (E-E-A-T gap). **Fix:** snippet 38195 injects visible byline + Person schema.

### Important (fixed)
- **`--pb-gold` referenced but undefined in parlay** — added.
- **`--pb-text-3` alpha 0.5 not 0.3** — fixed to match design system Muted token.
- **Outer card radius 16px instead of canonical 12px** — fixed.
- **`:focus-visible` missing on all custom buttons** (WCAG 2.4.7) — added.
- **Active-pill border alpha 0.45 vs canonical 0.6** — fixed.
- **`--pb-purple` (off-brand color) referenced** — removed.

### Polish (deferred)
- Tab role/aria-controls/tabpanel pattern incomplete. Either complete ARIA APG or downgrade to plain `<button>`s. Not blocking ranking.
- Parlay decimal display rounds to 6.97 but payout uses unrounded 6.9577. Cosmetic reconciliation gap.
- Tab keyboard navigation (Left/Right arrows) not implemented.

### GEO citability scores (post-fix)
- **IPC: 72/100** — strong content, math correct, 5 citation-ready FAQ Q&As. Now has author byline + Person schema + Article schema.
- **Parlay: 68/100** — strong topical authority (vig, hold, SGP correlation). Same byline + schema added.

Both should improve toward 80-85 once external citations (sportsbook house rules, OddsJam/Action Network references) are added to the prose.

## Brand reference

Tokens from PropsBot.AI's design system:
- **Teal** `#15ffc2` (primary), **Red** `#ff1552`, **Gold** `#f0c040`, **Blue** `#22a9ec`
- Base `#070e1a` with dark glass surfaces
- **JetBrains Mono** for numeric data, **Inter** for UI
- 12px card radius, brand gradient `linear-gradient(135deg, #09d5a0, #22a9ec)` top accent line
- IPC probability bar: confidence-high gradient (teal cascade) when ≥40%, low gradient (red cascade) below
