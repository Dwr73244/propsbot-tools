"""Re-publish both calculator pages with the JS-rendered input fix."""
import base64, json, urllib.request

PARENT_ID = 38183
IPC_ID = 38182
PARLAY_ID = 38185

# === IPC ===
with open('C:/Users/david/Daily-Pick/propsbot-tools/implied-probability-calculator.html', 'r', encoding='utf-8') as f:
    ipc_calc_html = f.read()

ipc_content = f"""<!-- wp:paragraph -->
<p>Convert American, decimal, and fractional sportsbook odds into <strong>implied probability</strong> with PropsBot's free calculator. Implied probability is the win-rate the bookmaker is pricing into a line — at <strong>-150</strong>, the implied probability is <strong>60%</strong>, meaning a bettor needs to win at a 60%+ true rate to break even after vig. Knowing this number is the foundation of every +EV bet.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Type any odds below to see the implied probability instantly. Toggle between American, decimal, and fractional formats — all three convert to the same percentage. Use the preset buttons for the most common sportsbook prices.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
{ipc_calc_html}
<!-- /wp:html -->

<!-- wp:heading -->
<h2 class="wp-block-heading">What is implied probability in sports betting?</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p><strong>Implied probability</strong> is the win-rate baked into a sportsbook's price for a bet. Every set of odds — whether <strong>-110</strong>, <strong>+200</strong>, or <strong>2.50</strong> — translates to a percentage representing how often that outcome must occur for the bet to be a long-term break-even. Sportsbooks build margin (the "vig" or "juice") into their lines, so summed implied probabilities of both sides of a market typically exceed 100% — that overage is the book's hold.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>For sharp bettors and prop research, implied probability is the single most important number on the screen. It tells you what the market believes — and gives you a baseline to compare against your own model, projections, or AI confidence score. If you believe a player's true probability of going Over is <strong>62%</strong> and the book's implied probability is only <strong>56%</strong>, you have a <strong>6% edge</strong> — that's the foundation of positive expected value (+EV) betting.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">How to calculate implied probability by hand</h2>
<!-- /wp:heading -->

<!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">From American odds</h3>
<!-- /wp:heading -->

<!-- wp:list -->
<ul class="wp-block-list">
<!-- wp:list-item --><li><strong>Negative odds</strong> (favorites, e.g. <code>-150</code>): <code>|odds| / (|odds| + 100) × 100</code> → 150 / 250 × 100 = <strong>60.00%</strong></li><!-- /wp:list-item -->
<!-- wp:list-item --><li><strong>Positive odds</strong> (underdogs, e.g. <code>+200</code>): <code>100 / (odds + 100) × 100</code> → 100 / 300 × 100 = <strong>33.33%</strong></li><!-- /wp:list-item -->
</ul>
<!-- /wp:list -->

<!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">From decimal odds</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p><code>1 / decimal × 100</code> → 1 / 2.50 × 100 = <strong>40.00%</strong></p>
<!-- /wp:paragraph -->

<!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">From fractional odds</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p><code>denominator / (numerator + denominator) × 100</code> → for <code>5/2</code>: 2 / 7 × 100 = <strong>28.57%</strong></p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">Why implied probability matters for prop betting</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Player props live or die on small edges. The difference between a -110 line and a -120 line is roughly <strong>2.4 percentage points</strong> of implied probability — meaning your model needs to be accurate to within fractions of a percentage point to know whether a bet is profitable. Implied probability is how you compare prices across sportsbooks, identify the best line for your bet, and quantify your edge.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>PropsBot's AI generates a <a href="/what-is-confidence-score-sports-betting/">Confidence Score</a> for every player prop — a model-derived probability that the prop will hit. Subtracting the book's implied probability from PropsBot's confidence gives you the <a href="/what-is-edge-score-sports-betting/">Edge Score</a>, the cleanest one-number summary of whether a bet is worth placing. Both numbers start with implied probability as their reference point.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">Implied probability examples for common odds</h2>
<!-- /wp:heading -->

<!-- wp:table -->
<figure class="wp-block-table"><table>
<thead><tr><th>American Odds</th><th>Decimal Odds</th><th>Implied Probability</th><th>Break-even Win Rate</th></tr></thead>
<tbody>
<tr><td>-300</td><td>1.33</td><td>75.00%</td><td>75.00%</td></tr>
<tr><td>-200</td><td>1.50</td><td>66.67%</td><td>66.67%</td></tr>
<tr><td>-150</td><td>1.67</td><td>60.00%</td><td>60.00%</td></tr>
<tr><td>-110</td><td>1.91</td><td>52.38%</td><td>52.38%</td></tr>
<tr><td>+100</td><td>2.00</td><td>50.00%</td><td>50.00%</td></tr>
<tr><td>+110</td><td>2.10</td><td>47.62%</td><td>47.62%</td></tr>
<tr><td>+150</td><td>2.50</td><td>40.00%</td><td>40.00%</td></tr>
<tr><td>+200</td><td>3.00</td><td>33.33%</td><td>33.33%</td></tr>
<tr><td>+300</td><td>4.00</td><td>25.00%</td><td>25.00%</td></tr>
<tr><td>+500</td><td>6.00</td><td>16.67%</td><td>16.67%</td></tr>
</tbody>
</table></figure>
<!-- /wp:table -->

<!-- wp:heading -->
<h2 class="wp-block-heading">Implied Probability FAQs</h2>
<!-- /wp:heading -->

<!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">What is the implied probability of -110 odds?</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>The implied probability of <strong>-110</strong> is <strong>52.38%</strong>. That's why -110 is the standard "even" pricing on most point spreads and totals — both sides have to win 52.38% of the time to break even, and the 4.76% extra (combined 104.76%) is the sportsbook's vig.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">How do I calculate vig from implied probabilities?</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Add the implied probability of both sides of a market. The amount over 100% is the sportsbook's hold (vig). For example, if Over is -110 (52.38%) and Under is -110 (52.38%), the combined implied probability is 104.76%, so the vig is roughly <strong>4.76%</strong>. Lower vig books like Novig, Sporttrade, and Pinnacle typically have hold in the 1–3% range.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">What's the difference between implied probability and true probability?</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p><strong>Implied probability</strong> is what the sportsbook's price implies. <strong>True probability</strong> is what you (or a model) believe the actual likelihood is. The gap between the two is your <strong>edge</strong>. Sharp bettors look for situations where their estimated true probability is higher than the implied probability priced into the line.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">Are decimal odds the same as implied probability?</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>No, but they're directly related. Decimal odds represent the total payout per $1 staked, while implied probability is the percentage chance the bet wins. Convert decimal to implied with <code>1 / decimal × 100</code>. Decimal odds of <strong>2.00</strong> equal an implied probability of <strong>50.00%</strong>.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">How do I find the best implied probability across sportsbooks?</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>For a bet you want to make, the <strong>lowest</strong> implied probability across books gives you the best price. Lower implied probability means you're getting more payout per dollar relative to the book's view of likelihood. PropsBot tracks lines across DraftKings, FanDuel, BetMGM, Caesars, Novig, Sporttrade, BetOnline, and Fliff — see the best line for every prop in our <a href="https://app.propsbot.ai/">app</a>.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">More PropsBot Tools</h2>
<!-- /wp:heading -->

<!-- wp:list -->
<ul class="wp-block-list">
<!-- wp:list-item --><li><a href="/tools/parlay-calculator/">Parlay Calculator</a> — combine multiple bets, see total payout</li><!-- /wp:list-item -->
<!-- wp:list-item --><li><a href="/best-props-today/">Best Props Today</a> — AI-scored player props across all sports</li><!-- /wp:list-item -->
<!-- wp:list-item --><li><a href="/positive-ev-props/">Positive EV Props</a> — props where PropsBot's confidence beats book implied probability</li><!-- /wp:list-item -->
<!-- wp:list-item --><li><a href="/prop-bet-analyzer/">Prop Bet Analyzer</a> — break down any player prop with PropsBot AI</li><!-- /wp:list-item -->
<!-- wp:list-item --><li><a href="/what-is-confidence-score-sports-betting/">What is a Confidence Score?</a> — how PropsBot's AI ranks every prop</li><!-- /wp:list-item -->
<!-- wp:list-item --><li><a href="/what-is-edge-score-sports-betting/">What is an Edge Score?</a> — how to find +EV bets</li><!-- /wp:list-item -->
</ul>
<!-- /wp:list -->

<!-- wp:separator -->
<hr class="wp-block-separator"/>
<!-- /wp:separator -->

<!-- wp:group {{"className":"pb-rg-callout"}} -->
<div class="wp-block-group pb-rg-callout">
<!-- wp:paragraph -->
<p><em>Implied probability calculations are mathematical conversions of sportsbook odds — they do not represent true win probability. PropsBot is a research and analytics tool, not a picks service. Bet within your means. Most US states require bettors to be 21+. If you or someone you know has a gambling problem, call <strong>1-800-GAMBLER</strong> or visit <a href="https://www.ncpgambling.org">ncpgambling.org</a>.</em></p>
<!-- /wp:paragraph -->
</div>
<!-- /wp:group -->"""

# === Parlay ===
with open('C:/Users/david/Daily-Pick/propsbot-tools/parlay-calculator.html', 'r', encoding='utf-8') as f:
    parlay_calc_html = f.read()

parlay_content = f"""<!-- wp:paragraph -->
<p>Calculate parlay payouts with PropsBot's free <strong>parlay calculator</strong>. Add up to 12 legs of American odds, set your bet amount, and see total payout, profit, combined American and decimal odds, and implied probability — instantly. Built for sports bettors who want to evaluate multi-leg tickets before placing them.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Each leg's decimal conversion is shown next to the input so you can spot a typo at a glance. Add or remove legs with one click. The calculator works for same-game parlays, cross-sport parlays, and any combination of moneylines, spreads, totals, or player props.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
{parlay_calc_html}
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

def publish(post_id, title, slug, content):
    content_b64 = base64.b64encode(content.encode('utf-8')).decode('ascii')
    payload = json.dumps({
        'post_id': post_id,
        'title': title,
        'slug': slug,
        'parent': PARENT_ID,
        'content': content_b64,
    }).encode('utf-8')
    req = urllib.request.Request(
        'https://propsbot.ai/wp-json/custom/v1/publish-page',
        data=payload, headers={'Content-Type': 'application/json'}, method='POST'
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        return resp.read().decode()

print('IPC:', publish(IPC_ID, 'Implied Probability Calculator — Convert Sportsbook Odds to Win Probability', 'implied-probability-calculator', ipc_content))
print('Parlay:', publish(PARLAY_ID, 'Parlay Calculator — Calculate Parlay Payouts & Combined Odds | PropsBot.AI', 'parlay-calculator', parlay_content))
