"""Publish the Parlay Calculator page as a child of /tools/."""
import base64, json, urllib.request

PARENT_ID = 38183  # /tools/ page ID

with open('C:/Users/david/Daily-Pick/propsbot-tools/parlay-calculator.html', 'r', encoding='utf-8') as f:
    calc_html = f.read()

page_content = f"""<!-- wp:paragraph -->
<p>Calculate parlay payouts with PropsBot's free <strong>parlay calculator</strong>. Add up to 12 legs of American odds, set your bet amount, and see total payout, profit, combined American and decimal odds, and implied probability — instantly. Built for sports bettors who want to evaluate multi-leg tickets before placing them.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Each leg's decimal conversion is shown next to the input so you can spot a typo at a glance. Add or remove legs with one click. The calculator works for same-game parlays, cross-sport parlays, and any combination of moneylines, spreads, totals, or player props.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
{calc_html}
<!-- /wp:html -->

<!-- wp:heading -->
<h2 class="wp-block-heading">How does a parlay calculator work?</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>A parlay calculator multiplies the decimal odds of every leg together to get the combined parlay odds. Multiplied by your bet amount, that gives total payout. The math is simple — but doing it by hand for 4+ legs is tedious and error-prone, especially when mixing American odds (which need converting first).</p>
<!-- /wp:paragraph -->

<!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">The formula</h3>
<!-- /wp:heading -->

<!-- wp:list -->
<ul class="wp-block-list">
<!-- wp:list-item --><li><strong>Step 1:</strong> Convert each American leg to decimal. Negative odds (favorite): <code>(100 / |odds|) + 1</code>. Positive odds (underdog): <code>(odds / 100) + 1</code>.</li><!-- /wp:list-item -->
<!-- wp:list-item --><li><strong>Step 2:</strong> Multiply all decimal odds together to get combined decimal.</li><!-- /wp:list-item -->
<!-- wp:list-item --><li><strong>Step 3:</strong> Multiply combined decimal by bet amount → total payout.</li><!-- /wp:list-item -->
<!-- wp:list-item --><li><strong>Step 4:</strong> Subtract bet from payout → profit.</li><!-- /wp:list-item -->
<!-- wp:list-item --><li><strong>Step 5 (optional):</strong> Implied probability of the full parlay = <code>1 / combined decimal × 100</code>.</li><!-- /wp:list-item -->
</ul>
<!-- /wp:list -->

<!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">Example: 3-leg parlay at -110 each</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Three legs at -110 each. Each converts to decimal odds of <strong>1.91</strong>. Combined: <code>1.91 × 1.91 × 1.91 = 6.97</code>. On a $10 bet, payout is <strong>$69.65</strong> and profit is <strong>$59.65</strong>. Combined American odds: <strong>+597</strong>. Implied probability: <strong>14.35%</strong>.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">Why parlays are tougher to win than they look</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Each additional leg compounds risk. A 3-leg parlay at -110 each requires you to win a 14.35% probability outcome — that's roughly 1 in 7. A 5-leg version requires winning a 6.86% outcome. The payout looks attractive, but the implied probability tells the real story.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Sportsbooks promote parlays heavily because the combined hold (vig) compounds too. A single -110 leg has a 4.76% vig. A 5-leg parlay of -110 legs has an effective hold over <strong>20%</strong> — which is why sharp bettors are selective with parlays and use the implied probability number to evaluate whether the combined edge is worth it.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">Same-game parlays vs traditional parlays</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>A <strong>same-game parlay (SGP)</strong> combines multiple bets from the same game (e.g., Patrick Mahomes Over 250 passing yards + Travis Kelce anytime TD + Chiefs -3.5). Sportsbooks adjust SGP odds for correlation — legs in the same game are not independent, and books model that. The calculator above works for SGPs but the result is approximate; the book's actual SGP price will differ from straight multiplication because of correlation adjustments.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p><strong>Traditional parlays</strong> combine bets across separate games, which are statistically independent. Straight multiplication gives the exact combined odds — what this calculator computes.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">Parlay Calculator FAQs</h2>
<!-- /wp:heading -->

<!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">How do you calculate a parlay payout?</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Convert each leg to decimal odds, multiply all decimal odds together, then multiply by your bet amount. The result is your total payout (including your original stake). Subtract your bet to get profit.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">What is a 3-leg parlay payout at -110?</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>A 3-leg parlay where each leg is at -110 has combined decimal odds of <strong>6.97</strong> and combined American odds of <strong>+597</strong>. A $10 bet returns $69.65 ($59.65 profit). A $100 bet returns $696.46.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">Is the parlay calculator accurate for same-game parlays?</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Approximate, not exact. Sportsbooks adjust SGP odds for correlation between legs in the same game. The calculator gives you the "uncorrelated" benchmark — useful for comparing what the book is offering against straight-multiplication value. If the book's SGP price is significantly worse than the calculator's number, the book is pricing in negative correlation and you're paying extra for it.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">How many legs can a parlay have?</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Most US sportsbooks allow up to 12-25 legs. PropsBot's calculator supports up to <strong>12 legs</strong>. Beyond that, the math gets unstable and the implied probability is so low (often under 1%) that the bet is effectively a lottery ticket.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">Can I use this for prop parlays on PrizePicks or Underdog?</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Sort of. PrizePicks and Underdog Fantasy use fixed payout multipliers (e.g., 3x for 3-leg, 6x for 4-leg) rather than American odds, so the calculator above isn't directly applicable. But you can convert their multipliers to decimal odds (just use the multiplier directly) and use the implied probability output to compare against your actual win probability — same +EV logic.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">More PropsBot Tools</h2>
<!-- /wp:heading -->

<!-- wp:list -->
<ul class="wp-block-list">
<!-- wp:list-item --><li><a href="/tools/implied-probability-calculator/">Implied Probability Calculator</a> — convert any odds format to win probability</li><!-- /wp:list-item -->
<!-- wp:list-item --><li><a href="/best-props-today/">Best Props Today</a> — AI-scored player props across all sports</li><!-- /wp:list-item -->
<!-- wp:list-item --><li><a href="/positive-ev-props/">Positive EV Props</a> — find spots where the market price beats your model</li><!-- /wp:list-item -->
<!-- wp:list-item --><li><a href="/prizepicks-picks-today/">PrizePicks Picks Today</a></li><!-- /wp:list-item -->
<!-- wp:list-item --><li><a href="/underdog-fantasy-picks-today/">Underdog Fantasy Picks Today</a></li><!-- /wp:list-item -->
<!-- wp:list-item --><li><a href="/what-is-confidence-score-sports-betting/">What is a Confidence Score?</a></li><!-- /wp:list-item -->
<!-- wp:list-item --><li><a href="/what-is-edge-score-sports-betting/">What is an Edge Score?</a></li><!-- /wp:list-item -->
</ul>
<!-- /wp:list -->

<!-- wp:separator -->
<hr class="wp-block-separator"/>
<!-- /wp:separator -->

<!-- wp:group {{"className":"pb-rg-callout"}} -->
<div class="wp-block-group pb-rg-callout">
<!-- wp:paragraph -->
<p><em>Parlay payout calculations are mathematical projections based on the odds you enter — they do not guarantee or predict outcomes. PropsBot is a research and analytics tool, not a picks service. Bet within your means. Most US states require bettors to be 21+. If you or someone you know has a gambling problem, call <strong>1-800-GAMBLER</strong> or visit <a href="https://www.ncpgambling.org">ncpgambling.org</a>.</em></p>
<!-- /wp:paragraph -->
</div>
<!-- /wp:group -->"""

content_b64 = base64.b64encode(page_content.encode('utf-8')).decode('ascii')
payload = json.dumps({
    'title': 'Parlay Calculator — Calculate Parlay Payouts & Combined Odds | PropsBot.AI',
    'slug': 'parlay-calculator',
    'content': content_b64,
    'parent': PARENT_ID,
}).encode('utf-8')

req = urllib.request.Request(
    'https://propsbot.ai/wp-json/custom/v1/publish-page',
    data=payload,
    headers={'Content-Type': 'application/json'},
    method='POST'
)
with urllib.request.urlopen(req, timeout=120) as resp:
    print(resp.read().decode())
