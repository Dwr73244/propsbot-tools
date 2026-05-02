"""Update /tools/ landing page to list all 5 calculators (IPC, Parlay, Hold/Vig, EV, No-Vig)."""
import base64, json, urllib.request

PARENT_ID = 38183

content = """<!-- wp:paragraph -->
<p><strong>Free betting calculators from PropsBot.AI.</strong> Convert odds to implied probability, calculate parlay payouts, find vig and hold, compute expected value, strip the vig to find fair odds — every tool below is free, no signup required, mobile-friendly, and built for sharp prop bettors who want to evaluate lines before placing them.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">Available Tools</h2>
<!-- /wp:heading -->

<!-- wp:list -->
<ul class="wp-block-list">
<!-- wp:list-item --><li><strong><a href="/tools/implied-probability-calculator/">Implied Probability Calculator</a></strong> — convert American, decimal, or fractional odds to win probability</li><!-- /wp:list-item -->
<!-- wp:list-item --><li><strong><a href="/tools/parlay-calculator/">Parlay Calculator</a></strong> — combine multiple bets, see total payout, profit, and combined odds</li><!-- /wp:list-item -->
<!-- wp:list-item --><li><strong><a href="/tools/hold-vig-calculator/">Hold &amp; Vig Calculator</a></strong> — compute the sportsbook's margin from a 2-way market</li><!-- /wp:list-item -->
<!-- wp:list-item --><li><strong><a href="/tools/ev-calculator/">Expected Value (EV) Calculator</a></strong> — find +EV bets by comparing your true probability to the book's price</li><!-- /wp:list-item -->
<!-- wp:list-item --><li><strong><a href="/tools/no-vig-fair-odds-calculator/">No-Vig Fair Odds Calculator</a></strong> — strip the vig to see what each side would price at with zero margin</li><!-- /wp:list-item -->
</ul>
<!-- /wp:list -->

<!-- wp:heading -->
<h2 class="wp-block-heading">Why use PropsBot's tools?</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Every tool on this page is built for sports prop bettors who want to evaluate lines, build parlays, and identify edges. They're free, fast, mobile-friendly, and built with the same data PropsBot's AI uses to score props every day. When you're ready to see <strong>AI Confidence Scores</strong> on every player prop, head to the <a href="https://app.propsbot.ai/">PropsBot app</a>.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">How sharp bettors use these tools together</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>The five calculators above form a complete pre-bet evaluation workflow:</p>
<!-- /wp:paragraph -->

<!-- wp:list {"ordered":true} -->
<ol class="wp-block-list">
<!-- wp:list-item --><li><strong>Convert</strong> the line you're considering into implied probability with the <a href="/tools/implied-probability-calculator/">Implied Probability Calculator</a>.</li><!-- /wp:list-item -->
<!-- wp:list-item --><li><strong>Strip</strong> the sportsbook's vig with the <a href="/tools/no-vig-fair-odds-calculator/">No-Vig Fair Odds Calculator</a> to see the "true" probability the book is implying for each side.</li><!-- /wp:list-item -->
<!-- wp:list-item --><li><strong>Compare</strong> the no-vig probability to your own model's estimate. If yours is higher, you've found a +EV opportunity.</li><!-- /wp:list-item -->
<!-- wp:list-item --><li><strong>Quantify</strong> the edge with the <a href="/tools/ev-calculator/">EV Calculator</a> to see expected dollar profit per bet.</li><!-- /wp:list-item -->
<!-- wp:list-item --><li><strong>Check the book's hold</strong> with the <a href="/tools/hold-vig-calculator/">Hold/Vig Calculator</a> to confirm you're not paying excessive margin.</li><!-- /wp:list-item -->
<!-- wp:list-item --><li><strong>Build a parlay</strong> if combining multiple +EV bets, using the <a href="/tools/parlay-calculator/">Parlay Calculator</a> to verify combined payout.</li><!-- /wp:list-item -->
</ol>
<!-- /wp:list -->

<!-- wp:heading -->
<h2 class="wp-block-heading">More from PropsBot</h2>
<!-- /wp:heading -->

<!-- wp:list -->
<ul class="wp-block-list">
<!-- wp:list-item --><li><a href="/best-props-today/">Best Props Today</a> — AI-scored player props across all sports</li><!-- /wp:list-item -->
<!-- wp:list-item --><li><a href="/positive-ev-props/">Positive EV Props</a> — props where PropsBot's confidence beats book implied probability</li><!-- /wp:list-item -->
<!-- wp:list-item --><li><a href="/ai-sports-picks/">AI Sports Picks — How It Works</a></li><!-- /wp:list-item -->
<!-- wp:list-item --><li><a href="/what-is-confidence-score-sports-betting/">What is a Confidence Score?</a></li><!-- /wp:list-item -->
<!-- wp:list-item --><li><a href="/what-is-edge-score-sports-betting/">What is an Edge Score?</a></li><!-- /wp:list-item -->
</ul>
<!-- /wp:list -->"""

content_b64 = base64.b64encode(content.encode('utf-8')).decode('ascii')
payload = json.dumps({
    'post_id': PARENT_ID,
    'title': 'Free Betting Tools — Calculators for Prop Bettors',
    'slug': 'tools',
    'content': content_b64,
}).encode('utf-8')
req = urllib.request.Request('https://propsbot.ai/wp-json/custom/v1/publish-page',
    data=payload, headers={'Content-Type': 'application/json'}, method='POST')
with urllib.request.urlopen(req, timeout=60) as resp:
    print(resp.read().decode())
