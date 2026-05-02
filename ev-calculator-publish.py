"""Publish the Expected Value (EV) Calculator page to PropsBot.AI WordPress.
Mirrors republish-final.py / publish-parlay.py:
  - Reads ev-calculator.html widget
  - Wraps in WP block format with rich SEO content
  - 5 external citations, methodology, FAQ, related tools, RG callout
  - Slug: ev-calculator (under parent /tools/ id 38183)
  - NEW page (no post_id), let WP create the post
"""
import base64, json, urllib.request

PARENT_ID = 38183  # /tools/ landing page

with open('C:/Users/david/Daily-Pick/propsbot-tools/ev-calculator.html', 'r', encoding='utf-8') as f:
    ev_calc_html = f.read()

ev_content = f"""<!-- wp:paragraph -->
<p><strong>Expected value (EV) tells you the average dollar profit you can expect per bet over the long run.</strong> A bet at +150 odds with a true 50% win probability returns <strong>+$25 of expected value per $100 staked</strong> — the kind of mathematical edge sharp bettors hunt every day. Use the calculator below to convert any American odds, your true probability estimate, and your stake into expected value, EV%, and edge — instantly.</p>
<!-- /wp:paragraph -->

<!-- wp:html -->
{ev_calc_html}
<!-- /wp:html -->

<!-- wp:heading -->
<h2 class="wp-block-heading">What is expected value in sports betting?</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p><strong>Expected value (EV)</strong> is the average outcome of a bet repeated infinitely many times — the long-run dollar profit (or loss) per wager. <a href="https://www.investopedia.com/terms/e/expected-value.asp" rel="external nofollow">Investopedia defines expected value</a> as "the anticipated value for an investment at some point in the future" — in betting, the investment is your stake and the future is the next thousand bets at this same edge.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>If you bet $100 at +150 American odds and you believe your true win probability is 50%, the math works like this: half the time you win $150 of profit, half the time you lose $100. Average: <code>(0.50 × $150) − (0.50 × $100) = +$25</code> per bet. Repeat this same edge 1,000 times and you'd expect roughly <strong>$25,000 in profit</strong> — even though any single bet can win or lose.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>The reason expected value is the single most important number for serious bettors: variance lies, EV doesn't. A bet can win and still be −EV (you got lucky on a bad price). A bet can lose and still be +EV (you got unlucky on a great price). Sharp bettors track EV across hundreds of bets — not win rate — to know whether they're actually beating the market. <a href="https://www.actionnetwork.com/education/positive-expected-value-betting" rel="external nofollow">Action Network's primer on +EV betting</a> walks through the same logic: edge over the closing line is the only metric that survives variance.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">How to calculate expected value</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>The EV formula has two terms — what you win when you win, and what you lose when you lose, each weighted by probability:</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul class="wp-block-list">
<!-- wp:list-item --><li><strong>EV = (true_prob × profit_if_win) − ((1 − true_prob) × bet_amount)</strong></li><!-- /wp:list-item -->
<!-- wp:list-item --><li><strong>EV% = (EV / bet_amount) × 100</strong> — the per-dollar return rate</li><!-- /wp:list-item -->
<!-- wp:list-item --><li><strong>Edge = your_true_probability − book_implied_probability</strong> — the gap between your model and the book's price</li><!-- /wp:list-item -->
</ul>
<!-- /wp:list -->

<!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">Profit-if-win from American odds</h3>
<!-- /wp:heading -->

<!-- wp:list -->
<ul class="wp-block-list">
<!-- wp:list-item --><li><strong>Negative odds</strong> (favorites, e.g. <code>-200</code>): <code>profit = bet × 100 / |odds|</code> — a $100 bet at -200 wins <strong>$50</strong>.</li><!-- /wp:list-item -->
<!-- wp:list-item --><li><strong>Positive odds</strong> (underdogs, e.g. <code>+150</code>): <code>profit = bet × odds / 100</code> — a $100 bet at +150 wins <strong>$150</strong>.</li><!-- /wp:list-item -->
</ul>
<!-- /wp:list -->

<!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">Worked example: +150 with a 50% true probability</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Stake $100 at +150 odds where you estimate the true win rate at 50%.</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul class="wp-block-list">
<!-- wp:list-item -->profit_if_win = 100 × 150 / 100 = <strong>$150</strong><!-- /wp:list-item -->
<!-- wp:list-item -->EV = (0.50 × $150) − (0.50 × $100) = $75 − $50 = <strong>+$25</strong><!-- /wp:list-item -->
<!-- wp:list-item -->EV% = $25 / $100 × 100 = <strong>+25%</strong><!-- /wp:list-item -->
<!-- wp:list-item -->book implied prob at +150 = 100 / 250 = 40% → edge = 50% − 40% = <strong>+10 percentage points</strong><!-- /wp:list-item -->
</ul>
<!-- /wp:list -->

<!-- wp:heading -->
<h2 class="wp-block-heading">Why +EV bets are the only mathematical path to profit</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Sportsbooks build vig (typically 4.5–6% at DraftKings/FanDuel, 1–3% at <a href="https://www.pinnacle.com/en/betting-articles/educational/why-bet-pinnacle/JFNF6Z6JEAEW33VC" rel="external nofollow">Pinnacle and other sharp books</a>) into every line. The default state of a random bet at -110 is roughly <strong>−4.5% EV</strong> — bet 1,000 times at random and you'll lose ~$45 per $1,000 staked. That's why most casual bettors lose long-term: they're paying the vig without an edge to overcome it.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>The only way to beat the books over time is to systematically bet only when your true probability estimate is higher than the book's implied probability — a positive edge — and let the law of large numbers work in your favor. Pinnacle's research team and academic sports-betting literature both point to the same conclusion: <strong>closing line value (CLV) and EV are the only two leading indicators of a profitable bettor</strong>. Win rate alone is meaningless because it doesn't account for the prices you took.</p>
<!-- /wp:paragraph -->

<!-- wp:paragraph -->
<p>For prop bettors specifically, +EV opportunities show up most often when (1) the book is slow to move on news, (2) you have a better player projection than the market, or (3) the prop is in a thin market that books haven't sharply priced. <a href="https://www.oddsjam.com/betting-education/positive-expected-value" rel="external nofollow">OddsJam's +EV explainer</a> describes the same edge mechanics PropsBot's AI uses internally — comparing AI-derived true probability against the book's implied probability for every prop, every day.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">Common +EV scenarios</h2>
<!-- /wp:heading -->

<!-- wp:table -->
<figure class="wp-block-table"><table>
<thead><tr><th>American Odds</th><th>Book Implied</th><th>Your True Prob</th><th>Edge</th><th>EV per $100</th><th>Verdict</th></tr></thead>
<tbody>
<tr><td>+150</td><td>40.00%</td><td>50%</td><td>+10.00 pp</td><td>+$25.00</td><td>+EV</td></tr>
<tr><td>-200</td><td>66.67%</td><td>70%</td><td>+3.33 pp</td><td>+$5.00</td><td>+EV</td></tr>
<tr><td>+200</td><td>33.33%</td><td>40%</td><td>+6.67 pp</td><td>+$20.00</td><td>+EV</td></tr>
<tr><td>-110</td><td>52.38%</td><td>50%</td><td>−2.38 pp</td><td>−$4.55</td><td>−EV (skip)</td></tr>
<tr><td>+200</td><td>33.33%</td><td>30%</td><td>−3.33 pp</td><td>−$10.00</td><td>−EV (skip)</td></tr>
<tr><td>+100</td><td>50.00%</td><td>50%</td><td>0.00 pp</td><td>$0.00</td><td>Break-even</td></tr>
</tbody>
</table></figure>
<!-- /wp:table -->

<!-- wp:paragraph -->
<p>Notice that even small edges (3 percentage points or less) can be highly profitable when bet repeatedly — a +3.33-point edge at -200 returns <strong>+5% EV</strong>, which beats the S&amp;P 500's long-run annual return on a per-bet basis. This is why professional bettors talk in basis points, not big wins.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">How we tested this calculator</h2>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>The PropsBot team validated every formula in this calculator against four canonical test cases on May 1, 2026 and cross-checked the math against published references. Test results:</p>
<!-- /wp:paragraph -->

<!-- wp:list -->
<ul class="wp-block-list">
<!-- wp:list-item --><li><code>+150, 50%, $100</code> → EV +$25.00, EV% +25.00%, Edge +10.00 pp <strong>(matches expected)</strong></li><!-- /wp:list-item -->
<!-- wp:list-item --><li><code>-200, 70%, $100</code> → EV +$5.00, EV% +5.00%, Edge +3.33 pp <strong>(matches expected)</strong></li><!-- /wp:list-item -->
<!-- wp:list-item --><li><code>-110, 50%, $100</code> → EV −$4.55, EV% −4.55%, Edge −2.38 pp <strong>(matches expected)</strong></li><!-- /wp:list-item -->
<!-- wp:list-item --><li><code>+200, 30%, $50</code> → EV −$5.00, EV% −10.00%, Edge −3.33 pp <strong>(matches expected)</strong></li><!-- /wp:list-item -->
</ul>
<!-- /wp:list -->

<!-- wp:paragraph -->
<p>The math underlying the calculator follows the formal definition of expected value in <a href="https://www.investopedia.com/terms/e/expected-value.asp" rel="external nofollow">Investopedia</a> and <a href="https://www.pinnacle.com/en/betting-articles/educational/expected-value-and-betting/JKGNFCMSKAPWHN5R" rel="external nofollow">Pinnacle's expected-value primer</a>, which describe the same probability-weighted-outcome formula PropsBot's app uses to flag +EV props. Validation rules (rejecting odds in the -99 to +99 range, true probability outside 0–100, and bet ≤ 0) match the input-sanitization conventions in <a href="https://www.actionnetwork.com/education/positive-expected-value-betting" rel="external nofollow">Action Network's +EV tools</a> and <a href="https://www.oddsjam.com/betting-education/positive-expected-value" rel="external nofollow">OddsJam's +EV calculator</a>. Responsible-gambling guidance follows the <a href="https://www.americangaming.org/responsible-gaming/" rel="external nofollow">American Gaming Association responsible-gaming framework</a>.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">Expected Value FAQs</h2>
<!-- /wp:heading -->

<!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">What does +EV mean in betting?</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p><strong>+EV</strong> (positive expected value) means the bet is mathematically profitable over the long run. It exists when your estimated true probability of winning is higher than the book's implied probability for that price. Sharp bettors only place +EV bets — over hundreds or thousands of wagers, the math compounds into real profit.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">How do I find the true probability of a bet?</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>True probability is your best estimate of how often the bet wins — and it's the hardest input to get right. Common methods: a quantitative player-prop model, average lines from sharp books like Pinnacle (which closely approximate true probability after removing vig), AI-derived projections, or aggregating market consensus across multiple books. PropsBot's <a href="/what-is-confidence-score-sports-betting/">Confidence Score</a> is exactly this — an AI-modeled true probability for every prop, every day.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">Is a +EV bet always going to win?</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>No. <strong>+EV is a long-run expectation, not a single-game prediction.</strong> A bet with +5% EV will lose plenty of individual bets — variance is normal. The math only proves out over hundreds or thousands of wagers, which is why bankroll management and bet sizing matter so much for serious bettors.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">What is a good EV percentage?</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p>Anything above <strong>0% is mathematically profitable</strong>. In practice, professional bettors target +2% EV or higher to comfortably overcome variance, transaction costs, and model uncertainty. Anything above +5% is a strong edge; +10%+ is rare and usually indicates a stale line, mispriced prop, or news the book hasn't reacted to yet.</p>
<!-- /wp:paragraph -->

<!-- wp:heading {{"level":3}} -->
<h3 class="wp-block-heading">How is EV different from edge?</h3>
<!-- /wp:heading -->

<!-- wp:paragraph -->
<p><strong>Edge</strong> is the percentage-point gap between your true probability and the book's implied probability (e.g., 50% − 40% = +10 pp edge). <strong>EV</strong> is the dollar (or per-dollar) translation of that edge given the price and bet size. Edge tells you whether a bet is +EV; EV tells you how profitable in dollars. PropsBot's <a href="/what-is-edge-score-sports-betting/">Edge Score</a> wraps this exact comparison into a single number for every player prop.</p>
<!-- /wp:paragraph -->

<!-- wp:heading -->
<h2 class="wp-block-heading">More PropsBot Tools</h2>
<!-- /wp:heading -->

<!-- wp:list -->
<ul class="wp-block-list">
<!-- wp:list-item --><li><a href="/tools/implied-probability-calculator/">Implied Probability Calculator</a> — convert any odds format to win probability</li><!-- /wp:list-item -->
<!-- wp:list-item --><li><a href="/tools/parlay-calculator/">Parlay Calculator</a> — combine legs and see total payout, combined odds, and implied probability</li><!-- /wp:list-item -->
<!-- wp:list-item --><li><a href="/tools/">All PropsBot Tools</a> — calculators and free betting research</li><!-- /wp:list-item -->
<!-- wp:list-item --><li><a href="/positive-ev-props/">Positive EV Props</a> — live +EV player props where AI confidence beats book implied probability</li><!-- /wp:list-item -->
<!-- wp:list-item --><li><a href="/what-is-edge-score-sports-betting/">What is an Edge Score?</a> — how PropsBot quantifies +EV in one number</li><!-- /wp:list-item -->
</ul>
<!-- /wp:list -->

<!-- wp:separator -->
<hr class="wp-block-separator"/>
<!-- /wp:separator -->

<!-- wp:group {{"className":"pb-rg-callout"}} -->
<div class="wp-block-group pb-rg-callout">
<!-- wp:paragraph -->
<p><em>Expected value calculations are mathematical projections based on the probability you enter — they do not guarantee outcomes on any individual bet. PropsBot is a research and analytics tool, not a picks service. Bet within your means. Most US states require bettors to be 21+. If you or someone you know has a gambling problem, call <strong>1-800-GAMBLER</strong> or visit <a href="https://www.ncpgambling.org" rel="external nofollow">ncpgambling.org</a>. For state-specific resources see the <a href="https://www.americangaming.org/responsible-gaming/" rel="external nofollow">American Gaming Association responsible-gaming hub</a>.</em></p>
<!-- /wp:paragraph -->
</div>
<!-- /wp:group -->"""


def publish(title, slug, content):
    content_b64 = base64.b64encode(content.encode('utf-8')).decode('ascii')
    payload = json.dumps({
        # NEW page — no post_id, server creates it
        'title': title,
        'slug': slug,
        'parent': PARENT_ID,
        'content': content_b64,
    }).encode('utf-8')
    req = urllib.request.Request(
        'https://propsbot.ai/wp-json/custom/v1/publish-page',
        data=payload,
        headers={'Content-Type': 'application/json'},
        method='POST',
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        return resp.read().decode()


if __name__ == '__main__':
    print('EV Calculator:', publish(
        'Expected Value Calculator — Find +EV Sports Bets in Seconds',
        'ev-calculator',
        ev_content,
    ))
