"""Integrate the 3 new calculators (Hold/Vig, EV, No-Vig) into the live WPCode snippets.

This is the cleaner v2: agents wrote different schema PHP shapes, so we ignore
those and hand-build a consistent schema snippet 38195 that supports all 5
calculators with the same WebApplication + FAQPage + HowTo + Article pattern.
"""
import base64, json, urllib.request

BASE = 'C:/Users/david/Daily-Pick/propsbot-tools'

def post_json(path, payload):
    req = urllib.request.Request(
        f'https://propsbot.ai/wp-json/custom/v1{path}',
        data=json.dumps(payload).encode('utf-8'),
        headers={'Content-Type': 'application/json'},
        method='POST'
    )
    with urllib.request.urlopen(req, timeout=60) as resp:
        return json.loads(resp.read().decode())

def update_snippet(snippet_id, content, mode='replace'):
    return post_json('/append-snippet', {
        'snippet_id': snippet_id,
        'content': base64.b64encode(content.encode('utf-8')).decode('ascii'),
        'mode': mode,
    })

# ============ JS: append to snippet 38188 ============
with open(f'{BASE}/hold-vig-calculator-init.js', 'r', encoding='utf-8') as f:
    holdvig_init = f.read()
with open(f'{BASE}/ev-calculator-init.js', 'r', encoding='utf-8') as f:
    ev_init = f.read()
with open(f'{BASE}/no-vig-fair-odds-calculator-init.js', 'r', encoding='utf-8') as f:
    novig_init = f.read()

new_js = """
/* =========================================================================
 * Round 2 calculators — Hold/Vig + EV + No-Vig
 * Self-contained IIFE, parallel to the existing initIPC/initParlay IIFE.
 * ========================================================================= */
(function() {
""" + holdvig_init + """

""" + ev_init + """

""" + novig_init + """

  function bootRound2() {
    if (typeof initHoldVig === 'function') initHoldVig();
    if (typeof initEV === 'function') initEV();
    if (typeof initNoVig === 'function') initNoVig();
  }
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', bootRound2);
  } else {
    bootRound2();
  }
})();
"""

print('--- Appending JS to snippet 38188 ---')
print(update_snippet(38188, new_js, mode='append'))

# ============ CSS: append to snippet 38192 ============
with open(f'{BASE}/hold-vig-calculator.css', 'r', encoding='utf-8') as f:
    holdvig_css = f.read()
with open(f'{BASE}/ev-calculator.css', 'r', encoding='utf-8') as f:
    ev_css = f.read()
with open(f'{BASE}/no-vig-fair-odds-calculator.css', 'r', encoding='utf-8') as f:
    novig_css = f.read()

new_css = (
    "\n/* === Round 2: Hold/Vig + EV + No-Vig === */\n\n"
    + holdvig_css + "\n\n" + ev_css + "\n\n" + novig_css
)
print('\n--- Appending CSS to snippet 38192 ---')
print(update_snippet(38192, new_css, mode='append'))

# ============ Nav: replace snippet 38191 ============
with open(f'{BASE}/nav-snippet-38191-update.js', 'r', encoding='utf-8') as f:
    nav_js = f.read()
print('\n--- Replacing nav snippet 38191 ---')
print(update_snippet(38191, nav_js, mode='replace'))

# ============ Schema: replace snippet 38195 (hand-crafted, all 5 calcs) ============
schema_php = r"""add_action('wp_head', function() {
    if (!is_page()) return;
    $slug = get_post_field('post_name', get_the_ID());
    $allowed = array(
        'implied-probability-calculator',
        'parlay-calculator',
        'hold-vig-calculator',
        'ev-calculator',
        'no-vig-fair-odds-calculator',
        'tools'
    );
    if (!in_array($slug, $allowed, true)) return;

    $url      = get_permalink();
    $title    = wp_get_document_title();
    $pubdate  = get_the_date('c');
    $moddate  = get_the_modified_date('c');
    $author   = array(
        '@type' => 'Person',
        'name'  => 'David Reilich',
        'jobTitle' => 'Founder, PropsBot.AI',
        'url'   => 'https://propsbot.ai/author/thehulkbets/',
        'sameAs' => array('https://x.com/propsbotai'),
    );
    $publisher = array(
        '@type' => 'Organization',
        'name'  => 'PropsBot.AI',
        'url'   => 'https://propsbot.ai',
        'logo'  => array(
            '@type' => 'ImageObject',
            'url'   => 'https://propsbot.ai/wp-content/uploads/2026/03/Untitled-350-x-100-px.svg',
        ),
    );

    $article_block = array(
        '@context' => 'https://schema.org',
        '@type'    => 'Article',
        'headline' => $title,
        'datePublished' => $pubdate,
        'dateModified'  => $moddate,
        'author'   => $author,
        'publisher'=> $publisher,
        'mainEntityOfPage' => $url,
        'inLanguage' => 'en-US',
    );

    $blocks = array();

    if ($slug === 'implied-probability-calculator') {
        $blocks[] = array(
            '@context' => 'https://schema.org', '@type' => 'WebApplication',
            'name' => 'Implied Probability Calculator',
            'description' => 'Free calculator that converts American, decimal, and fractional sportsbook odds into implied probability percentage.',
            'url' => $url, 'applicationCategory' => 'FinanceApplication', 'operatingSystem' => 'Any (web)',
            'offers' => array('@type' => 'Offer', 'price' => '0', 'priceCurrency' => 'USD'), 'creator' => $publisher,
        );
        $blocks[] = array(
            '@context' => 'https://schema.org', '@type' => 'FAQPage',
            'mainEntity' => array(
                array('@type' => 'Question', 'name' => 'What is the implied probability of -110 odds?',
                    'acceptedAnswer' => array('@type' => 'Answer', 'text' => 'The implied probability of -110 is 52.38%.')),
                array('@type' => 'Question', 'name' => 'How do I calculate vig from implied probabilities?',
                    'acceptedAnswer' => array('@type' => 'Answer', 'text' => 'Add the implied probability of both sides of a market. The amount over 100% is the sportsbook hold (vig).')),
                array('@type' => 'Question', 'name' => 'What is the difference between implied probability and true probability?',
                    'acceptedAnswer' => array('@type' => 'Answer', 'text' => 'Implied probability is what the sportsbook price implies. True probability is what you (or a model) believe the actual likelihood is.')),
                array('@type' => 'Question', 'name' => 'Are decimal odds the same as implied probability?',
                    'acceptedAnswer' => array('@type' => 'Answer', 'text' => 'No, but they are directly related. Convert decimal to implied with 1 / decimal x 100.')),
                array('@type' => 'Question', 'name' => 'How do I find the best implied probability across sportsbooks?',
                    'acceptedAnswer' => array('@type' => 'Answer', 'text' => 'For a bet you want to make, the lowest implied probability across books gives you the best price.')),
            ),
        );
        $blocks[] = array(
            '@context' => 'https://schema.org', '@type' => 'HowTo',
            'name' => 'How to calculate implied probability from American odds',
            'description' => 'Convert American sportsbook odds into an implied probability percentage.',
            'totalTime' => 'PT1M',
            'step' => array(
                array('@type' => 'HowToStep', 'position' => 1, 'name' => 'Identify the sign', 'text' => 'Determine if the odds are negative (favorite) or positive (underdog).'),
                array('@type' => 'HowToStep', 'position' => 2, 'name' => 'Apply the formula', 'text' => 'Negative: |odds|/(|odds|+100) x 100. Positive: 100/(odds+100) x 100.'),
                array('@type' => 'HowToStep', 'position' => 3, 'name' => 'Read the percentage', 'text' => 'The result is the implied probability.'),
            ),
        );
        $blocks[] = $article_block;
    }
    elseif ($slug === 'parlay-calculator') {
        $blocks[] = array(
            '@context' => 'https://schema.org', '@type' => 'WebApplication',
            'name' => 'Parlay Calculator',
            'description' => 'Free calculator that combines multiple bet legs into a parlay, showing total payout, profit, combined American and decimal odds, and implied probability.',
            'url' => $url, 'applicationCategory' => 'FinanceApplication', 'operatingSystem' => 'Any (web)',
            'offers' => array('@type' => 'Offer', 'price' => '0', 'priceCurrency' => 'USD'), 'creator' => $publisher,
        );
        $blocks[] = array(
            '@context' => 'https://schema.org', '@type' => 'FAQPage',
            'mainEntity' => array(
                array('@type' => 'Question', 'name' => 'How do you calculate a parlay payout?',
                    'acceptedAnswer' => array('@type' => 'Answer', 'text' => 'Convert each leg to decimal odds, multiply all decimal odds together, then multiply by your bet amount.')),
                array('@type' => 'Question', 'name' => 'What is a 3-leg parlay payout at -110?',
                    'acceptedAnswer' => array('@type' => 'Answer', 'text' => 'A 3-leg parlay where each leg is at -110 has combined decimal 6.97 and combined American +597. A $10 bet returns $69.65.')),
                array('@type' => 'Question', 'name' => 'Is the parlay calculator accurate for same-game parlays?',
                    'acceptedAnswer' => array('@type' => 'Answer', 'text' => 'Yes for the math, but no for the price. Sportsbooks adjust same-game-parlay (SGP) odds for correlation.')),
                array('@type' => 'Question', 'name' => 'How many legs can a parlay have?',
                    'acceptedAnswer' => array('@type' => 'Answer', 'text' => 'Most US sportsbooks allow up to 12-25 legs. PropsBot calculator supports up to 12.')),
                array('@type' => 'Question', 'name' => 'Can I use this for prop parlays on PrizePicks or Underdog?',
                    'acceptedAnswer' => array('@type' => 'Answer', 'text' => 'Yes, with one conversion step. Convert their multipliers directly into decimal odds.')),
            ),
        );
        $blocks[] = array(
            '@context' => 'https://schema.org', '@type' => 'HowTo',
            'name' => 'How to calculate a parlay payout',
            'totalTime' => 'PT2M',
            'step' => array(
                array('@type' => 'HowToStep', 'position' => 1, 'name' => 'Convert each leg to decimal', 'text' => 'For each American leg, convert to decimal odds.'),
                array('@type' => 'HowToStep', 'position' => 2, 'name' => 'Multiply', 'text' => 'Multiply all decimal odds together.'),
                array('@type' => 'HowToStep', 'position' => 3, 'name' => 'Multiply by bet', 'text' => 'Multiply combined decimal by your bet to see total payout.'),
            ),
        );
        $blocks[] = $article_block;
    }
    elseif ($slug === 'hold-vig-calculator') {
        $blocks[] = array(
            '@context' => 'https://schema.org', '@type' => 'WebApplication',
            'name' => 'Hold and Vig Calculator',
            'description' => 'Free calculator that computes the sportsbook hold (vig) from a 2-way market by summing the implied probabilities of both sides.',
            'url' => $url, 'applicationCategory' => 'FinanceApplication', 'operatingSystem' => 'Any (web)',
            'offers' => array('@type' => 'Offer', 'price' => '0', 'priceCurrency' => 'USD'), 'creator' => $publisher,
        );
        $blocks[] = array(
            '@context' => 'https://schema.org', '@type' => 'FAQPage',
            'mainEntity' => array(
                array('@type' => 'Question', 'name' => 'What is the hold on a -110/-110 market?',
                    'acceptedAnswer' => array('@type' => 'Answer', 'text' => 'The hold on a -110/-110 market is 4.76%. Both sides imply 52.38%, summing to 104.76%, so the sportsbook holds 4.76% margin.')),
                array('@type' => 'Question', 'name' => 'What is a typical sportsbook hold?',
                    'acceptedAnswer' => array('@type' => 'Answer', 'text' => 'Major US sportsbooks like DraftKings and FanDuel run 4.5-6% hold on standard markets. Pinnacle, Novig, and Sporttrade run 1-3%.')),
                array('@type' => 'Question', 'name' => 'Why does hold matter for sharp bettors?',
                    'acceptedAnswer' => array('@type' => 'Answer', 'text' => 'Lower hold means a tighter market with less margin baked into the price. Sharp bettors prefer low-hold books because their edge stays larger.')),
                array('@type' => 'Question', 'name' => 'Can hold be negative (an arbitrage)?',
                    'acceptedAnswer' => array('@type' => 'Answer', 'text' => 'Yes. If the implied probabilities sum to less than 100%, you can guarantee profit by betting both sides. This is called a "middling" or arbitrage opportunity.')),
                array('@type' => 'Question', 'name' => 'How do I calculate hold from two American odds?',
                    'acceptedAnswer' => array('@type' => 'Answer', 'text' => 'Convert both sides to implied probability, sum them, and subtract 100%. The result is the hold percentage.')),
            ),
        );
        $blocks[] = array(
            '@context' => 'https://schema.org', '@type' => 'HowTo',
            'name' => 'How to calculate sportsbook hold (vig)',
            'totalTime' => 'PT1M',
            'step' => array(
                array('@type' => 'HowToStep', 'position' => 1, 'name' => 'Convert side 1 to implied probability', 'text' => 'Use the American-to-implied formula on the first side of the market.'),
                array('@type' => 'HowToStep', 'position' => 2, 'name' => 'Convert side 2 to implied probability', 'text' => 'Repeat for the second side.'),
                array('@type' => 'HowToStep', 'position' => 3, 'name' => 'Sum and subtract 100', 'text' => 'Add both implied probabilities. Subtract 100%. The result is the hold percentage.'),
            ),
        );
        $blocks[] = $article_block;
    }
    elseif ($slug === 'ev-calculator') {
        $blocks[] = array(
            '@context' => 'https://schema.org', '@type' => 'WebApplication',
            'name' => 'Expected Value Calculator',
            'description' => 'Free calculator that computes expected value (EV) for a sports bet given American odds, your true probability estimate, and your bet amount.',
            'url' => $url, 'applicationCategory' => 'FinanceApplication', 'operatingSystem' => 'Any (web)',
            'offers' => array('@type' => 'Offer', 'price' => '0', 'priceCurrency' => 'USD'), 'creator' => $publisher,
        );
        $blocks[] = array(
            '@context' => 'https://schema.org', '@type' => 'FAQPage',
            'mainEntity' => array(
                array('@type' => 'Question', 'name' => 'What is expected value (EV) in sports betting?',
                    'acceptedAnswer' => array('@type' => 'Answer', 'text' => 'Expected value is the average dollar profit you can expect per bet over the long run, given your estimated true probability and the sportsbook odds.')),
                array('@type' => 'Question', 'name' => 'How do I calculate EV?',
                    'acceptedAnswer' => array('@type' => 'Answer', 'text' => 'EV = (true probability x profit if win) - ((1 - true probability) x bet amount). A positive EV means a profitable bet over the long run.')),
                array('@type' => 'Question', 'name' => 'What is a +EV bet?',
                    'acceptedAnswer' => array('@type' => 'Answer', 'text' => 'A bet with positive expected value — your estimated true probability is higher than the implied probability priced into the line.')),
                array('@type' => 'Question', 'name' => 'How big does the edge need to be?',
                    'acceptedAnswer' => array('@type' => 'Answer', 'text' => 'Sharp bettors typically target a 3-5% edge minimum to overcome variance. Smaller edges work but require larger sample sizes.')),
                array('@type' => 'Question', 'name' => 'Where do I get the true probability estimate?',
                    'acceptedAnswer' => array('@type' => 'Answer', 'text' => 'From a model, projections, or aggregating multiple sportsbook prices to find a no-vig consensus probability. PropsBot AI Confidence Scores provide this for player props.')),
            ),
        );
        $blocks[] = array(
            '@context' => 'https://schema.org', '@type' => 'HowTo',
            'name' => 'How to calculate expected value of a bet',
            'totalTime' => 'PT1M',
            'step' => array(
                array('@type' => 'HowToStep', 'position' => 1, 'name' => 'Convert odds to implied probability', 'text' => 'Convert the sportsbook American odds to implied probability.'),
                array('@type' => 'HowToStep', 'position' => 2, 'name' => 'Estimate true probability', 'text' => 'Estimate the true probability of the bet winning (your model, projections, etc.).'),
                array('@type' => 'HowToStep', 'position' => 3, 'name' => 'Calculate profit if win', 'text' => 'Negative odds: bet x 100 / |odds|. Positive: bet x odds / 100.'),
                array('@type' => 'HowToStep', 'position' => 4, 'name' => 'Apply EV formula', 'text' => 'EV = (true probability x profit if win) - ((1 - true probability) x bet amount).'),
                array('@type' => 'HowToStep', 'position' => 5, 'name' => 'Interpret', 'text' => 'Positive EV = profitable long-run bet. Negative EV = skip the bet.'),
            ),
        );
        $blocks[] = $article_block;
    }
    elseif ($slug === 'no-vig-fair-odds-calculator') {
        $blocks[] = array(
            '@context' => 'https://schema.org', '@type' => 'WebApplication',
            'name' => 'No-Vig Fair Odds Calculator',
            'description' => 'Free calculator that strips the sportsbook margin from a 2-way market to show the no-vig fair probability and fair American odds for each side.',
            'url' => $url, 'applicationCategory' => 'FinanceApplication', 'operatingSystem' => 'Any (web)',
            'offers' => array('@type' => 'Offer', 'price' => '0', 'priceCurrency' => 'USD'), 'creator' => $publisher,
        );
        $blocks[] = array(
            '@context' => 'https://schema.org', '@type' => 'FAQPage',
            'mainEntity' => array(
                array('@type' => 'Question', 'name' => 'What are no-vig fair odds?',
                    'acceptedAnswer' => array('@type' => 'Answer', 'text' => 'No-vig fair odds are the prices a sportsbook would offer with zero margin. They show the "true" probability the market is implying for each side after stripping the bookmaker hold.')),
                array('@type' => 'Question', 'name' => 'Why are no-vig odds useful for +EV betting?',
                    'acceptedAnswer' => array('@type' => 'Answer', 'text' => 'No-vig probability is the cleanest baseline for comparing your true probability estimate. If your estimate beats the no-vig probability, you have a +EV bet.')),
                array('@type' => 'Question', 'name' => 'How do I calculate no-vig fair odds?',
                    'acceptedAnswer' => array('@type' => 'Answer', 'text' => 'Convert both American odds to implied probability. Sum them. Divide each side by the sum to get no-vig probability. Convert back to American odds.')),
                array('@type' => 'Question', 'name' => 'Are no-vig odds the same as Pinnacle odds?',
                    'acceptedAnswer' => array('@type' => 'Answer', 'text' => 'Close but not identical. Pinnacle is one of the lowest-margin major books (1-3% hold). No-vig odds remove the margin entirely (0%).')),
                array('@type' => 'Question', 'name' => 'How do sharp bettors use no-vig odds?',
                    'acceptedAnswer' => array('@type' => 'Answer', 'text' => 'They compare no-vig probability across multiple sharp books to find consensus, then look for edges where their model or another book disagrees.')),
            ),
        );
        $blocks[] = array(
            '@context' => 'https://schema.org', '@type' => 'HowTo',
            'name' => 'How to calculate no-vig fair odds',
            'totalTime' => 'PT1M',
            'step' => array(
                array('@type' => 'HowToStep', 'position' => 1, 'name' => 'Convert both sides', 'text' => 'Convert each side American odds to implied probability.'),
                array('@type' => 'HowToStep', 'position' => 2, 'name' => 'Sum the probabilities', 'text' => 'Add side 1 and side 2 implied probability — the sum will be greater than 1 because of the bookmaker margin.'),
                array('@type' => 'HowToStep', 'position' => 3, 'name' => 'Divide each side by the sum', 'text' => 'side1 fair = side1 implied / sum. side2 fair = side2 implied / sum. Both fair probabilities sum to exactly 1.'),
                array('@type' => 'HowToStep', 'position' => 4, 'name' => 'Convert fair probability to American odds', 'text' => 'Use the implied-to-American formula on each fair probability.'),
            ),
        );
        $blocks[] = $article_block;
    }
    elseif ($slug === 'tools') {
        $blocks[] = array(
            '@context' => 'https://schema.org', '@type' => 'CollectionPage',
            'name' => 'PropsBot.AI Free Betting Tools',
            'url' => $url,
            'about' => array('@type' => 'Thing', 'name' => 'Sports betting calculators'),
            'mainEntity' => array(
                '@type' => 'ItemList',
                'itemListElement' => array(
                    array('@type' => 'ListItem', 'position' => 1, 'url' => 'https://propsbot.ai/tools/implied-probability-calculator/', 'name' => 'Implied Probability Calculator'),
                    array('@type' => 'ListItem', 'position' => 2, 'url' => 'https://propsbot.ai/tools/parlay-calculator/', 'name' => 'Parlay Calculator'),
                    array('@type' => 'ListItem', 'position' => 3, 'url' => 'https://propsbot.ai/tools/hold-vig-calculator/', 'name' => 'Hold and Vig Calculator'),
                    array('@type' => 'ListItem', 'position' => 4, 'url' => 'https://propsbot.ai/tools/ev-calculator/', 'name' => 'Expected Value Calculator'),
                    array('@type' => 'ListItem', 'position' => 5, 'url' => 'https://propsbot.ai/tools/no-vig-fair-odds-calculator/', 'name' => 'No-Vig Fair Odds Calculator'),
                ),
            ),
            'publisher' => $publisher,
        );
    }

    foreach ($blocks as $b) {
        echo '<script type="application/ld+json">' . wp_json_encode($b, JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT) . '</script>' . "\n";
    }
}, 20);

// Author byline (visible on calculator pages, just under the H1)
add_filter('the_content', function($content) {
    if (!is_page()) return $content;
    $slug = get_post_field('post_name', get_the_ID());
    if (!in_array($slug, array(
        'implied-probability-calculator', 'parlay-calculator',
        'hold-vig-calculator', 'ev-calculator', 'no-vig-fair-odds-calculator',
    ), true)) return $content;
    $byline = '<div class="pb-tool-byline" style="font-size:13px; color:rgba(200,215,230,0.7); margin:-12px 0 24px; padding:8px 0; border-bottom:1px solid rgba(100,200,220,0.07);">'
        . 'By <a href="https://propsbot.ai/author/thehulkbets/" rel="author" style="color:#15ffc2; text-decoration:none; font-weight:600;">David Reilich</a>'
        . ', Founder of PropsBot.AI &middot; Last updated ' . get_the_modified_date('F j, Y')
        . '</div>';
    return $byline . $content;
}, 9);
"""

print('\n--- Replacing schema snippet 38195 ---')
print(update_snippet(38195, schema_php, mode='replace'))

print('\nDone.')
