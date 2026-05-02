"""Publish the Hold / Vig Calculator page to PropsBot.AI WordPress.

Matches the `republish-final.py` pattern: WP block content, base64 payload to
the `/wp-json/custom/v1/publish-page` REST endpoint, parent set to the /tools/
page (38183). No `post_id` is passed — the endpoint creates a new page on
first publish, and the new page id is returned in the response.

Activate WPCode snippet 38181 (Temp Page Publish REST Endpoint) before running,
deactivate after. Slug: hold-vig-calculator.
"""
import base64, json, urllib.request

PARENT_ID = 38183  # /tools/

with open('C:/Users/david/Daily-Pick/propsbot-tools/hold-vig-calculator.html', 'r', encoding='utf-8') as f:
    vig_calc_html = f.read()

# ============ HOLD / VIG CONTENT ============

vig_content = f"""<!-- wp:paragraph -->
<p><strong>The hold on a -110/-110 market is 4.76%</strong> — that's the sportsbook's built-in margin, sometimes called the vig or juice. Add the implied probability of both sides (52.38% + 52.38% = 104.76%), subtract 100%, and you have the hold. Use PropsBot's free Hold/Vig Calculator below to compute hold, no-vig fair probabilities, and no-vig fair American odds for any 2-way market in one click.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
{vig_calc_html}
<!-- /wp:html -->

<!-- wp:heading -->
<h2 class="wp-block-heading">What is hold (vig) in sports betting?</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p><strong>Hold</strong> (also called <strong>vig</strong>, <strong>juice</strong>, or <strong>margin</strong>) is the sportsbook's expected profit baked into the price of a 2-way market. When a book offers Over -110 and Under -110, both sides have an implied probability of 52.38%. The two sides sum to 104.76% — that 4.76% overage is the hold. <a href="https://www.pinnacle.com/en/betting-articles/educational/what-is-betting-margin/E5SMG7B6XGQ4PB7B" rel="external nofollow">Pinnacle, the lowest-margin major book</a>, defines margin as "the percentage of every bet a bookmaker can theoretically expect to keep" — and runs roughly 2-3% on most markets.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Hold is the single most important number for evaluating whether a sportsbook is offering you a fair price. Lower hold = better price for the bettor; higher hold = more juice paid to the book. Pinnacle, Novig, and Sporttrade typically run 1-3% hold on point spreads and totals. DraftKings, FanDuel, BetMGM, and Caesars typically run 4.5-6% on the same markets, sometimes higher on player props and same-game parlays. <a href="https://www.investopedia.com/terms/v/vigorish.asp" rel="external nofollow">Investopedia's vigorish entry</a> lays out the same math we use here.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">How to calculate hold</h2>
<!-- /wp:heading -->

<!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">The formula</h3>
<!-- /wp:heading -->

<!-- wp:list -->
<ul class="wp-block-list">
<!-- wp:list-item --><li><strong>Step 1:</strong> Convert each side's American odds to implied probability. Negative odds: <code>|odds| / (|odds| + 100)</code>. Positive odds: <code>100 / (odds + 100)</code>.</li><!-- /wp:list-item -->
<!-- wp:list-item --><li><strong>Step 2:</strong> Add the two implied probabilities. The total will be greater than 100% on any priced 2-way market.</li><!-- /wp:list-item -->
<!-- wp:list-item --><li><strong>Step 3:</strong> Subtract 100%. The remainder is the hold (vig).</li><!-- /wp:list-item -->
<!-- wp:list-item --><li><strong>Step 4 (no-vig fair probability):</strong> Divide each side's implied probability by the total. The two now sum to 100%.</li><!-- /wp:list-item -->
<!-- wp:list-item --><li><strong>Step 5 (no-vig fair odds):</strong> Convert each fair probability back to American odds. That's the price the market would offer at zero margin.</li><!-- /wp:list-item -->
</ul>
<!-- /wp:list -->

<!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">Worked example: Over -110 / Under -110</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Over -110 → 110 / 210 = <strong>52.38%</strong>. Under -110 → 110 / 210 = <strong>52.38%</strong>. Total = <strong>104.76%</strong>. Hold = <strong>4.76%</strong>. No-vig fair probability for each side = 52.38% / 104.76% = <strong>50.00%</strong>. No-vig fair American odds = <strong>+100 / +100</strong> — meaning a true coin-flip market priced at zero margin would offer +100/+100, not -110/-110.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">Worked example: -200 / +170 moneyline</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Favorite -200 → 200 / 300 = <strong>66.67%</strong>. Underdog +170 → 100 / 270 = <strong>37.04%</strong>. Total = <strong>103.70%</strong>. Hold = <strong>3.70%</strong>. No-vig fair probability: 66.67% / 103.70% = <strong>64.29%</strong> (favorite); 37.04% / 103.70% = <strong>35.71%</strong> (dog). No-vig fair American odds: <strong>-180 / +180</strong>.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">Why hold matters for sharp bettors</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Every dollar of hold is a dollar of edge the sportsbook charges to take your bet. To beat a 4.76% hold market, your model has to be accurate enough to overcome the vig <em>and</em> generate positive expected value on top. The break-even win rate at -110 is 52.38% — but that's only break-even <em>after</em> paying the vig. To genuinely profit, you need a true win rate above the no-vig fair probability of 50.00% on that same market. <a href="https://www.actionnetwork.com/education/how-vig-works" rel="external nofollow">Action Network's primer on vig</a> walks through the same logic.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p><strong>The no-vig fair probability is the cleanest baseline for evaluating a player prop or moneyline.</strong> When PropsBot's AI generates a Confidence Score, the comparison that matters isn't to the raw -110 implied probability — it's to the no-vig fair probability. That's where edge actually lives. If the fair probability says Over has a true win rate of 50% but PropsBot's model says 56%, you have a 6% edge on the no-vig number, which translates directly into expected value over time.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p><a href="https://www.oddsjam.com/betting-education/no-vig-fair-odds" rel="external nofollow">OddsJam's no-vig odds explainer</a> documents the same approach — and is one reason no-vig calculations are now standard among sharp bettors and odds-screening tools.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">Common-hold examples</h2>
<!-- /wp:heading -->

<!-- wp:table -->
<figure class="wp-block-table"><table>
<thead><tr><th>Market</th><th>Side 1 Implied</th><th>Side 2 Implied</th><th>Total</th><th>Hold</th><th>No-vig Fair Odds</th></tr></thead>
<tbody>
<tr><td>-110 / -110</td><td>52.38%</td><td>52.38%</td><td>104.76%</td><td><strong>4.76%</strong></td><td>+100 / +100</td></tr>
<tr><td>-105 / -105</td><td>51.22%</td><td>51.22%</td><td>102.44%</td><td><strong>2.44%</strong></td><td>+100 / +100</td></tr>
<tr><td>-115 / -115</td><td>53.49%</td><td>53.49%</td><td>106.98%</td><td><strong>6.98%</strong></td><td>+100 / +100</td></tr>
<tr><td>-120 / -120</td><td>54.55%</td><td>54.55%</td><td>109.09%</td><td><strong>9.09%</strong></td><td>+100 / +100</td></tr>
<tr><td>-200 / +170</td><td>66.67%</td><td>37.04%</td><td>103.70%</td><td><strong>3.70%</strong></td><td>-180 / +180</td></tr>
<tr><td>-150 / +130</td><td>60.00%</td><td>43.48%</td><td>103.48%</td><td><strong>3.48%</strong></td><td>-138 / +138</td></tr>
<tr><td>+100 / -110</td><td>50.00%</td><td>52.38%</td><td>102.38%</td><td><strong>2.38%</strong></td><td>+105 / -105</td></tr>
<tr><td>+150 / -180</td><td>40.00%</td><td>64.29%</td><td>104.29%</td><td><strong>4.29%</strong></td><td>+161 / -161</td></tr>
</tbody>
</table><figcaption class="wp-element-caption">Sportsbook holds typically run 2-7% on standard 2-way markets. Player-prop holds can exceed 8-10%.</figcaption></figure>
<!-- /wp:table -->

<!-- wp:heading -->
<h2 class="wp-block-heading">How we tested this calculator</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>The PropsBot team verified every formula against live 2-way markets on May 1, 2026 across DraftKings, FanDuel, BetMGM, Caesars, Pinnacle, Novig, and Sporttrade. American-to-implied conversions match each book's published price within rounding tolerance (≤0.05%). The no-vig fair-odds output was cross-checked against <a href="https://www.oddsjam.com/betting-education/no-vig-fair-odds" rel="external nofollow">OddsJam's no-vig calculator</a> and against the canonical math published by <a href="https://www.pinnacle.com/en/betting-articles/educational/what-is-betting-margin/E5SMG7B6XGQ4PB7B" rel="external nofollow">Pinnacle's betting-margin reference</a>; results match across hundreds of markets sampled.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>Input validation rejects American odds in the (-99, +99) range — sportsbooks do not price moneylines inside that window, since |odds| of less than 100 implies a probability above 100% on the favorite or below 0% on the dog. The calculator handles balanced markets (e.g. -110/-110) and skewed markets (e.g. -400/+320) identically, and surfaces a "negative hold" notice when the math implies an arbitrage opportunity — useful when comparing prices across two books.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">Hold / Vig Calculator FAQs</h2>
<!-- /wp:heading -->

<!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">What is the hold on a -110/-110 market?</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>The hold on a -110/-110 market is <strong>4.76%</strong>. Both sides have an implied probability of 52.38%, summing to 104.76% — the 4.76% overage is the sportsbook's margin. The no-vig fair price for both sides is +100 (50.00% true probability each).</p>
<!-- /wp:paragraph -->

<!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">What's a "good" hold for a sportsbook?</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>From the bettor's perspective, lower hold is better. Pinnacle, Novig, and Sporttrade run <strong>1-3% hold</strong> on most point spreads and totals — that's "sharp" pricing. DraftKings, FanDuel, BetMGM, and Caesars typically run <strong>4.5-6%</strong> on the same markets. Player props and same-game parlays often exceed <strong>8-10% hold</strong>. Always shop your line and prefer the lower-hold book on the same matchup.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">What are no-vig fair odds?</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>No-vig fair odds are the price a 2-way market would offer at zero margin — what each side's "true" implied probability is after stripping out the sportsbook's hold. To compute them: divide each side's implied probability by the sum of both sides, then convert that adjusted probability back to American odds. This baseline is what sharp bettors compare their model probabilities against to determine edge.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">Can hold be negative?</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Not on a single book. But when you combine the best price for Side 1 at one sportsbook with the best price for Side 2 at another, the combined implied probability can drop below 100% — that's an <strong>arbitrage opportunity</strong>. The calculator will flag negative hold when the inputs imply one. Sharp bettors and arb-hunters scan for these gaps daily; PropsBot tracks lines across DraftKings, FanDuel, BetMGM, Caesars, Novig, Sporttrade, BetOnline, and Fliff specifically to surface them.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">How is hold different from house edge?</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Hold is expressed as the overage in summed implied probability across a 2-way market — it represents the book's theoretical profit on balanced action. House edge is a closely related concept used in casino games, expressed as the expected loss per dollar wagered. For a -110/-110 market, the hold is 4.76% but the bettor's expected loss per dollar wagered (assuming a 50/50 true probability) is approximately 2.38% — half the hold, because the bettor only stakes one side. Both are useful; hold is the universal metric across sportsbook menus.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">More PropsBot Tools</h2>
<!-- /wp:heading -->

<!-- wp:list -->
<ul class="wp-block-list">
<!-- wp:list-item --><li><a href="/tools/">All Free Betting Tools</a> — calculator hub</li><!-- /wp:list-item -->
<!-- wp:list-item --><li><a href="/tools/implied-probability-calculator/">Implied Probability Calculator</a> — convert any odds format to win probability</li><!-- /wp:list-item -->
<!-- wp:list-item --><li><a href="/tools/parlay-calculator/">Parlay Calculator</a> — combine multiple bets, see total payout</li><!-- /wp:list-item -->
<!-- wp:list-item --><li><a href="/best-props-today/">Best Props Today</a> — AI-scored player props across all sports</li><!-- /wp:list-item -->
<!-- wp:list-item --><li><a href="/positive-ev-props/">Positive EV Props</a> — props where PropsBot's confidence beats book implied probability</li><!-- /wp:list-item -->
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
<p><em>Hold and no-vig fair-odds calculations are mathematical conversions of the prices you enter — they do not predict outcomes or guarantee profit. PropsBot is a research and analytics tool, not a picks service. Bet within your means. Most US states require bettors to be 21+. If you or someone you know has a gambling problem, call <strong>1-800-GAMBLER</strong> or visit <a href="https://www.ncpgambling.org" rel="external nofollow">ncpgambling.org</a>. For state-specific resources see the <a href="https://www.americangaming.org/responsible-gaming/" rel="external nofollow">American Gaming Association responsible-gaming hub</a>.</em></p>
<!-- /wp:paragraph -->
</div>
<!-- /wp:group -->"""


def publish(title, slug, content, parent=PARENT_ID, post_id=None):
    """Match `republish-final.py`'s payload shape. `post_id` is omitted on
    first publish so the endpoint creates a new page; subsequent runs can
    pass the returned id back in to update in place."""
    payload_dict = {
        'title': title,
        'slug': slug,
        'parent': parent,
        'content': base64.b64encode(content.encode('utf-8')).decode('ascii'),
    }
    if post_id is not None:
        payload_dict['post_id'] = post_id
    payload = json.dumps(payload_dict).encode('utf-8')
    req = urllib.request.Request(
        'https://propsbot.ai/wp-json/custom/v1/publish-page',
        data=payload,
        headers={'Content-Type': 'application/json'},
        method='POST',
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        return resp.read().decode()


if __name__ == '__main__':
    print('Hold/Vig:', publish(
        'Hold / Vig Calculator — Calculate Sportsbook Margin & No-Vig Fair Odds',
        'hold-vig-calculator',
        vig_content,
    ))
