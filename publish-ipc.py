"""Publish the Implied Probability Calculator page to PropsBot.AI WordPress."""
import base64, json, urllib.request

# Read the calculator widget HTML
with open('C:/Users/david/Daily-Pick/propsbot-tools/implied-probability-calculator.html', 'r', encoding='utf-8') as f:
    calc_html = f.read()

# Build the full page content using WP block format.
# Pattern: SEO intro -> calculator widget (wrapped in Custom HTML block) -> deep explainer content + FAQ + related tools.
page_content = f"""<!-- wp:paragraph -->
<p>Convert American, decimal, and fractional sportsbook odds into <strong>implied probability</strong> with PropsBot's free calculator. Implied probability is the win-rate the bookmaker is pricing into a line — at <strong>-150</strong>, the implied probability is <strong>60%</strong>, meaning a bettor needs to win at a 60%+ true rate to break even after vig. Knowing this number is the foundation of every +EV bet.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Type any odds below to see the implied probability instantly. Toggle between American, decimal, and fractional formats — all three convert to the same percentage. Use the preset buttons for the most common sportsbook prices.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
{calc_html}
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

# Base64 encode the full page content
content_b64 = base64.b64encode(page_content.encode('utf-8')).decode('ascii')

# POST to the temp WPCode endpoint
payload = json.dumps({
    'title': 'Implied Probability Calculator — Convert Sportsbook Odds to Win Probability',
    'slug': 'tools/implied-probability-calculator',
    'content': content_b64,
}).encode('utf-8')

req = urllib.request.Request(
    'https://propsbot.ai/wp-json/custom/v1/publish-page',
    data=payload,
    headers={'Content-Type': 'application/json'},
    method='POST'
)
with urllib.request.urlopen(req, timeout=120) as resp:
    print(resp.read().decode())
