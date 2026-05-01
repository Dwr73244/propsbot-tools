# PropsBot Tools

Free betting calculators built for [PropsBot.AI](https://propsbot.ai) — dark glass theme, JetBrains Mono data type, scoped CSS, no proprietary AI data exposed.

## Live URLs
- [/tools/](https://propsbot.ai/tools/) — landing page
- [/tools/implied-probability-calculator/](https://propsbot.ai/tools/implied-probability-calculator/)
- [/tools/parlay-calculator/](https://propsbot.ai/tools/parlay-calculator/)

## Architecture

Each calculator widget is a self-contained HTML+CSS file (no inline JS — see note below). The HTML is embedded inside a WordPress `wp:html` block on the published page. The CSS is scoped under `.pb-ipc` (implied probability) or `.pb-parlay` (parlay) to avoid theme conflicts.

### JavaScript

WordPress's content filter HTML-escapes inline `<script>` content inside `wp:html` blocks (turns `>` into `&gt;`, `&&` into `&amp;&amp;`, etc.), breaking script execution. To work around this, the calculator JS lives in **WPCode snippet 38188 (`PropsBot Tools Calculator JS`)** which loads site-wide in the footer. It auto-detects whether the IPC or parlay calculator is on the page and initializes accordingly. Inputs are created programmatically (also stripped by WP's filter when present in post content as static HTML).

### Nav injection

WPCode snippet 38191 (`PropsBot Nav: Inject Tools Calculator Links`) injects the three new tool links into the existing accordion menu (`#pb-nav-overlay`) under the existing "Props Tools" section. Works for both desktop and mobile because the site uses a single hamburger overlay.

## Files
- `implied-probability-calculator.html` — IPC widget (DOM + CSS)
- `parlay-calculator.html` — Parlay widget (DOM + CSS)
- `publish-tools-parent.py` — creates the `/tools/` parent page + republishes IPC as child
- `publish-parlay.py` — publishes parlay calculator as child of /tools/
- `republish-both.py` — republishes both pages from current widget files (used for updates)

## Deployment

1. Activate WPCode snippet 38181 (`Temp Page Publish REST Endpoint`)
2. Run `python republish-both.py` (or one of the individual publish scripts)
3. Deactivate snippet 38181

## Brand reference

Tokens come from PropsBot.AI's design system:
- Teal `#15ffc2` (primary accent), Red `#ff1552`, Gold `#f0c040`, Blue `#22a9ec`
- Dark glass surfaces over `#070e1a` base
- JetBrains Mono for numeric data, Inter for UI
- 12px card radius, brand gradient `linear-gradient(135deg, #09d5a0, #22a9ec)` on top accent line
