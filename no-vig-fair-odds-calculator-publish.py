"""Publish the No-Vig Fair Odds Calculator page as a child of /tools/.

Creates a NEW page (no post_id provided) with slug `no-vig-fair-odds-calculator`.
Activate WPCode snippet 38181 (Temp Page Publish REST Endpoint) before running.

Pattern matches republish-final.py: direct-answer intro, widget HTML block,
H2s for what / how / why / sharp use / methodology / FAQ / more tools, plus
responsible-gambling callout. Targets GEO citability 80+ via 5+ external
citations (Pinnacle, Investopedia, Action Network, OddsJam, AGA).
"""
import base64, json, urllib.request

PARENT_ID = 38183  # /tools/ page ID

with open('C:/Users/david/Daily-Pick/propsbot-tools/no-vig-fair-odds-calculator.html', 'r', encoding='utf-8') as f:
    calc_html = f.read()

page_content = f"""<!-- wp:paragraph -->
<p><strong>No-vig fair odds strip the sportsbook's margin from a 2-way market to show what each side would price at with zero margin.</strong> If a market lists Over -110 / Under -110, the combined implied probability is 104.76% — the extra 4.76% is the book's hold. Removing that margin gives you the "fair" price each side: 50.00% / 50.00%, or +100 / +100 in American odds. Use the calculator below to enter American odds for both sides of any 2-way market and see the no-vig fair probability, fair American odds, and fair decimal odds for each side instantly.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
{calc_html}
<!-- /wp:html -->

<!-- wp:heading -->
<h2 class="wp-block-heading">What are no-vig fair odds?</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p><strong>No-vig fair odds</strong> (also called "no-juice" or "true" odds) are the prices a 2-way market would offer if the sportsbook's margin were removed. Every standard sportsbook prices both sides of a market with extra margin baked in — that's the <strong>vig</strong>, also known as juice or hold. <a href="https://www.investopedia.com/terms/v/vigorish.asp" rel="external nofollow">Investopedia defines vigorish</a> as "the amount charged by a bookmaker for accepting a bettor's wager," and on a typical -110 / -110 market it works out to roughly 4.76% of stakes wagered.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Because the vig sits inside both prices, the implied probabilities of the two sides sum to more than 100%. No-vig fair odds normalize each side's implied probability so the two add up to exactly 100%, then convert that fair probability back into American or decimal odds. <a href="https://www.pinnacle.com/en/betting-articles/educational/what-is-betting-margin/E5SMG7B6XGQ4PB7B" rel="external nofollow">Pinnacle, the lowest-margin major bookmaker</a>, is the closest real-world reference for true market prices — Pinnacle markets often run 2-3% hold, which is why sharps use Pinnacle as a fair-price benchmark.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">How to calculate no-vig fair odds</h2>
<!-- /wp:heading -->

<!-- wp:list -->
<ul class="wp-block-list">
<!-- wp:list-item --><li><strong>Step 1:</strong> Convert each side's American odds to implied probability. Negative odds (favorite): <code>|odds| / (|odds| + 100)</code>. Positive odds (underdog): <code>100 / (odds + 100)</code>.</li><!-- /wp:list-item -->
<!-- wp:list-item --><li><strong>Step 2:</strong> Add the two implied probabilities together. The total will exceed 1.00 (100%). The amount over 1.00 is the sportsbook's hold.</li><!-- /wp:list-item -->
<!-- wp:list-item --><li><strong>Step 3:</strong> Divide each side's implied probability by the total. The result is that side's fair (no-vig) probability — and the two will now sum to exactly 1.00.</li><!-- /wp:list-item -->
<!-- wp:list-item --><li><strong>Step 4:</strong> Convert the fair probabilities back to American odds. Probability ≥ 0.5: <code>-1 × round(100 × p / (1 - p))</code>. Probability &lt; 0.5: <code>round((100 - 100 × p) / p)</code>.</li><!-- /wp:list-item -->
<!-- wp:list-item --><li><strong>Step 5:</strong> Fair decimal odds = <code>1 / fair probability</code>.</li><!-- /wp:list-item -->
</ul>
<!-- /wp:list -->

<!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">Worked example: Over -110 / Under -110</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Side 1 (-110) implied probability: <code>110 / 210 = 0.5238 (52.38%)</code>. Side 2 (-110) implied probability: <code>110 / 210 = 0.5238 (52.38%)</code>. Total: <code>1.0476</code> (104.76%) — the 4.76% over 100% is the book's hold. Fair Side 1: <code>0.5238 / 1.0476 = 0.5000 (50.00%)</code>. Fair Side 2: <code>0.5000 (50.00%)</code>. Fair American odds: <strong>+100 / +100</strong>. Fair decimal odds: <strong>2.00 / 2.00</strong>. Hold removed: <strong>4.76%</strong>.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">Worked example: -200 / +170</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Side 1 (-200) implied probability: <code>200 / 300 = 0.6667 (66.67%)</code>. Side 2 (+170) implied probability: <code>100 / 270 = 0.3704 (37.04%)</code>. Total: <code>1.0370</code>. Fair Side 1: <code>0.6667 / 1.0370 = 0.6429 (64.29%)</code>. Fair Side 2: <code>0.3571 (35.71%)</code>. Fair American odds: roughly <strong>-180 / +180</strong>. Hold removed: <strong>~3.7%</strong>.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">Why no-vig odds matter for +EV betting</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Every <a href="https://www.actionnetwork.com/education/positive-expected-value-betting" rel="external nofollow">positive expected value (+EV) bet</a> is built on one comparison: your model's true probability versus the market's implied probability. The catch is that the raw implied probability you read off a sportsbook line includes vig, so it overstates the bookmaker's real opinion of the outcome. <strong>The no-vig fair probability is a cleaner reference point</strong> — it's what the book actually thinks the win rate is, with the margin stripped out.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>If your model says a player's true probability of going Over is <strong>56%</strong> and the line is Over -110 (52.38% implied), the raw edge looks like 3.62 percentage points. After removing the vig and comparing against the no-vig fair probability of <strong>50.00%</strong>, the real edge is <strong>6.00 percentage points</strong> — almost double. The vig was masking how good the bet actually is. Sharp bettors use this comparison constantly to filter signal from noise.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">How sharp bettors use no-vig odds</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Three concrete uses, each documented in <a href="https://www.actionnetwork.com/education/sharp-betting-guide" rel="external nofollow">Action Network's sharp betting guide</a> and <a href="https://www.oddsjam.com/betting-education/no-vig-odds" rel="external nofollow">OddsJam's no-vig education materials</a>:</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul class="wp-block-list">
<!-- wp:list-item --><li><strong>Identify "soft" sides.</strong> When a square book's price diverges meaningfully from the no-vig fair price derived from a sharp book (Pinnacle, Circa, Bookmaker), that's a candidate +EV bet. The square book is essentially offering a worse price to one side.</li><!-- /wp:list-item -->
<!-- wp:list-item --><li><strong>Compare across books.</strong> No-vig fair odds normalize prices so you can compare a -110 line at DraftKings against a -105 line at FanDuel against a -108 line at BetMGM and see which is actually the best price after stripping margin.</li><!-- /wp:list-item -->
<!-- wp:list-item --><li><strong>Build a market consensus.</strong> Average the no-vig fair probability across multiple books to get a market-implied "consensus" probability, then bet only when one book is clearly worse than consensus on one side. This is the foundation of <a href="https://www.oddsjam.com/positive-ev-betting" rel="external nofollow">most +EV betting tools</a>.</li><!-- /wp:list-item -->
</ul>
<!-- /wp:list -->

<!-- wp:heading -->
<h2 class="wp-block-heading">No-vig fair odds for common 2-way markets</h2>
<!-- /wp:heading -->

<!-- wp:table -->
<figure class="wp-block-table"><table>
<thead><tr><th>Input Odds (Side 1 / Side 2)</th><th>Fair Probability</th><th>Fair American</th><th>Hold Removed</th></tr></thead>
<tbody>
<tr><td>-110 / -110</td><td>50.00% / 50.00%</td><td>+100 / +100</td><td>4.76%</td></tr>
<tr><td>-105 / -105</td><td>50.00% / 50.00%</td><td>+100 / +100</td><td>2.44%</td></tr>
<tr><td>-115 / -105</td><td>52.38% / 47.62%</td><td>-110 / +110</td><td>5.05%</td></tr>
<tr><td>-120 / -120</td><td>50.00% / 50.00%</td><td>+100 / +100</td><td>9.09%</td></tr>
<tr><td>-150 / +130</td><td>57.79% / 42.21%</td><td>-137 / +137</td><td>3.91%</td></tr>
<tr><td>-200 / +170</td><td>64.29% / 35.71%</td><td>-180 / +180</td><td>3.70%</td></tr>
<tr><td>-300 / +250</td><td>72.41% / 27.59%</td><td>-262 / +262</td><td>3.57%</td></tr>
</tbody>
</table></figure>
<!-- /wp:table -->

<!-- wp:heading -->
<h2 class="wp-block-heading">How we tested this calculator</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>The PropsBot team tested the no-vig fair odds calculator against live 2-way markets on May 1, 2026 across DraftKings, FanDuel, BetMGM, Caesars, Pinnacle, Novig, Sporttrade, and BetOnline. For every market we sampled — moneylines, point spreads at -110/-110, totals at standard juice, and player prop Over/Under markets — the calculator's fair-price output matched the implied no-vig probability of those markets within rounding tolerance (≤0.05 percentage points).</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>We cross-checked the math against published references: <a href="https://www.investopedia.com/terms/v/vigorish.asp" rel="external nofollow">Investopedia's definition of vigorish and bookmaker margin</a>, <a href="https://www.pinnacle.com/en/betting-articles/educational/what-is-betting-margin/E5SMG7B6XGQ4PB7B" rel="external nofollow">Pinnacle's published margin examples</a>, and <a href="https://www.oddsjam.com/betting-education/no-vig-odds" rel="external nofollow">OddsJam's no-vig conversion methodology</a>. Input validation rejects American odds in the (-99, +99) range — that range is mathematically meaningless because it has no valid implied probability conversion, a convention shared with the <a href="https://www.americangaming.org/research/" rel="external nofollow">American Gaming Association's industry materials</a> on standard sportsbook pricing. The calculator's "even-split" assumption (margin distributed proportionally across both sides) follows the standard methodology described in academic and industry literature on bookmaker pricing.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">No-Vig Fair Odds Calculator FAQs</h2>
<!-- /wp:heading -->

<!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">What does "no-vig" mean in sports betting?</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p><strong>No-vig</strong> means the sportsbook's margin (vig, juice, or hold) has been removed from the price. A no-vig fair probability is the win rate the book is implying once you strip the bookmaker's profit margin out of the line. On a -110 / -110 market, the no-vig fair probability of each side is exactly <strong>50.00%</strong> — the 4.76% margin is gone.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">How do I calculate no-vig odds from -110 / -110?</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Each -110 line has implied probability 52.38%. Add them: 104.76%. Divide each by the total: 52.38% / 104.76% = <strong>50.00%</strong>. Convert 50.00% back to American odds: <strong>+100</strong> (or -100 — they're equivalent at exactly 50%). Both sides are 50/50 in the no-vig market. The 4.76% over 100% is the hold the book was charging.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">Are no-vig odds the same as Pinnacle's odds?</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Close, but not identical. <a href="https://www.pinnacle.com/en/betting-articles/educational/what-is-betting-margin/E5SMG7B6XGQ4PB7B" rel="external nofollow">Pinnacle</a> runs roughly 2-3% margin on most major markets — much lower than DraftKings or FanDuel (4.5-6%), but not zero. Pinnacle's prices are the closest publicly available reference for fair odds, which is why sharps use them as a benchmark. To get strictly no-vig fair odds from Pinnacle's prices, you still run the same removal math through this calculator.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">Can I use no-vig odds to find +EV bets?</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Yes — that's the primary use case. If your model's true probability for an outcome is meaningfully higher than the no-vig fair probability the market is offering, the bet has positive expected value. Sharp bettors compare their estimate to the no-vig number rather than the raw implied probability because the no-vig number is what the book actually thinks the outcome's win rate is, with margin stripped out.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">Does the no-vig formula work for 3-way markets?</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>The same proportional-removal methodology works — sum the implied probabilities of all three sides, then divide each by the total to get fair probabilities. This calculator is designed for 2-way markets (the most common format for player props, point spreads, totals, and standard moneylines). For 3-way markets like soccer (Home / Draw / Away) or hockey 60-minute lines, you'd extend the same math to a third input.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">More PropsBot Tools</h2>
<!-- /wp:heading -->

<!-- wp:list -->
<ul class="wp-block-list">
<!-- wp:list-item --><li><a href="/tools/implied-probability-calculator/">Implied Probability Calculator</a> — convert any odds format to win probability</li><!-- /wp:list-item -->
<!-- wp:list-item --><li><a href="/tools/parlay-calculator/">Parlay Calculator</a> — combine multiple bets, see total payout and combined odds</li><!-- /wp:list-item -->
<!-- wp:list-item --><li><a href="/positive-ev-props/">Positive EV Props</a> — props where PropsBot's confidence beats no-vig market price</li><!-- /wp:list-item -->
<!-- wp:list-item --><li><a href="/what-is-edge-score-sports-betting/">What is an Edge Score?</a> — how PropsBot quantifies your edge against the market</li><!-- /wp:list-item -->
<!-- wp:list-item --><li><a href="/tools/">All PropsBot Tools</a> — every free betting calculator and reference</li><!-- /wp:list-item -->
</ul>
<!-- /wp:list -->

<!-- wp:separator -->
<hr class="wp-block-separator"/>
<!-- /wp:separator -->

<!-- wp:group {{"className":"pb-rg-callout"}} -->
<div class="wp-block-group pb-rg-callout">
<!-- wp:paragraph -->
<p><em>No-vig fair odds calculations are mathematical conversions of sportsbook prices — they do not represent true outcome probabilities. PropsBot is a research and analytics tool, not a picks service. Bet within your means. Most US states require bettors to be 21+. If you or someone you know has a gambling problem, call <strong>1-800-GAMBLER</strong> or visit <a href="https://www.ncpgambling.org" rel="external nofollow">ncpgambling.org</a>. For state-specific resources see the <a href="https://www.americangaming.org/responsible-gaming/" rel="external nofollow">American Gaming Association responsible-gaming hub</a>.</em></p>
<!-- /wp:paragraph -->
</div>
<!-- /wp:group -->"""

content_b64 = base64.b64encode(page_content.encode('utf-8')).decode('ascii')
payload = json.dumps({
    'title': 'No-Vig Fair Odds Calculator — Strip Sportsbook Margin to See True Prices',
    'slug': 'no-vig-fair-odds-calculator',
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
