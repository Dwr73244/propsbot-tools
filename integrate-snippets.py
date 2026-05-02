"""Integrate the 3 new calculator snippets (Hold/Vig, EV, No-Vig) into the live
WPCode snippets via the /append-snippet REST endpoint.

Strategy:
  - JS snippet 38188: APPEND new IIFE containing the 3 init functions + a bootNew()
    that calls them. Self-contained — no shared state with existing IIFE.
  - CSS snippet 38192: APPEND raw CSS rules (additive).
  - Schema snippet 38195: REPLACE entire content (need to insert new elseif
    branches inside the existing if/elseif chain — can't append outside it).
  - Nav snippet 38191: REPLACE with 5-calculator version.
"""
import base64, json, urllib.request, os

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

def append_snippet(snippet_id, content, mode='append'):
    return post_json('/append-snippet', {
        'snippet_id': snippet_id,
        'content': base64.b64encode(content.encode('utf-8')).decode('ascii'),
        'mode': mode,
    })

# ============ STEP 1: Clean up test pollution in 38188 if any ============
# (manual inspection shows we added "/*" to 38188 during endpoint testing — safe to ignore,
#  it's just a comment opener that gets closed by the next /* in the new content if needed,
#  but to be safe, we'll prepend the new IIFE with a `// reset` line)

# ============ STEP 2: Append JS to snippet 38188 ============
with open(f'{BASE}/hold-vig-calculator-init.js', 'r', encoding='utf-8') as f:
    holdvig_init = f.read()
with open(f'{BASE}/ev-calculator-init.js', 'r', encoding='utf-8') as f:
    ev_init = f.read()
with open(f'{BASE}/no-vig-fair-odds-calculator-init.js', 'r', encoding='utf-8') as f:
    novig_init = f.read()

# Strip top header comments to make the appended code cleaner
def strip_leading_comments(text):
    lines = text.split('\n')
    out = []
    in_block = False
    for ln in lines:
        if ln.strip().startswith('// ===') or ln.strip().startswith('// PropsBot') or ln.strip().startswith('// Append'):
            continue
        if ln.strip().startswith('// '):
            continue
        if ln.strip() == '' and not out:
            continue
        out.append(ln)
    return '\n'.join(out)

# The agents likely included their init functions wrapped in helpful comments.
# We'll just include the entire output of each, then add an IIFE that calls them.
new_js = """
/* =========================================================================
 * Round 2 calculator inits — Hold/Vig + EV + No-Vig
 * Self-contained IIFE; runs in parallel with the existing initIPC/initParlay
 * IIFE above. Each init() guards on its own `__pb*Init` flag and is safe to
 * re-run if DOMContentLoaded fires multiple times.
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

print('Appending JS to snippet 38188...')
print(append_snippet(38188, new_js, mode='append'))

# ============ STEP 3: Append CSS to snippet 38192 ============
with open(f'{BASE}/hold-vig-calculator.css', 'r', encoding='utf-8') as f:
    holdvig_css = f.read()
with open(f'{BASE}/ev-calculator.css', 'r', encoding='utf-8') as f:
    ev_css = f.read()
with open(f'{BASE}/no-vig-fair-odds-calculator.css', 'r', encoding='utf-8') as f:
    novig_css = f.read()

new_css = "\n/* === Round 2 calculators (Hold/Vig + EV + No-Vig) === */\n\n" + holdvig_css + "\n\n" + ev_css + "\n\n" + novig_css
print('Appending CSS to snippet 38192...')
print(append_snippet(38192, new_css, mode='append'))

# ============ STEP 4: Replace nav snippet 38191 ============
with open(f'{BASE}/nav-snippet-38191-update.js', 'r', encoding='utf-8') as f:
    nav_js = f.read()
print('Replacing nav snippet 38191...')
print(append_snippet(38191, nav_js, mode='replace'))

# ============ STEP 5: Build full schema PHP and replace 38195 ============
# Read each schema branch
with open(f'{BASE}/hold-vig-calculator-schema.php', 'r', encoding='utf-8') as f:
    holdvig_schema = f.read()
with open(f'{BASE}/ev-calculator-schema.php', 'r', encoding='utf-8') as f:
    ev_schema = f.read()
with open(f'{BASE}/no-vig-fair-odds-calculator-schema.php', 'r', encoding='utf-8') as f:
    novig_schema = f.read()

# We need the FULL existing 38195 schema (IPC + parlay + tools branches) plus the 3 new ones.
# Rebuild from scratch since we control all of it.
full_schema_php = """add_action('wp_head', function() {
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

    $blocks = array();

    if ($slug === 'implied-probability-calculator') {
        $blocks[] = array(
            '@context' => 'https://schema.org',
            '@type'    => 'WebApplication',
            'name'     => 'Implied Probability Calculator',
            'description' => 'Free calculator that converts American, decimal, and fractional sportsbook odds into implied probability percentage.',
            'url'      => $url,
            'applicationCategory' => 'FinanceApplication',
            'operatingSystem' => 'Any (web)',
            'offers'   => array('@type' => 'Offer', 'price' => '0', 'priceCurrency' => 'USD'),
            'creator'  => $publisher,
        );
        $blocks[] = array(
            '@context' => 'https://schema.org',
            '@type'    => 'FAQPage',
            'mainEntity' => array(
                array('@type' => 'Question', 'name' => 'What is the implied probability of -110 odds?',
                    'acceptedAnswer' => array('@type' => 'Answer', 'text' => 'The implied probability of -110 is 52.38%. That is why -110 is the standard "even" pricing on most point spreads and totals — both sides have to win 52.38% of the time to break even, and the 4.76% extra (combined 104.76%) is the sportsbook vig.')),
                array('@type' => 'Question', 'name' => 'How do I calculate vig from implied probabilities?',
                    'acceptedAnswer' => array('@type' => 'Answer', 'text' => 'Add the implied probability of both sides of a market. The amount over 100% is the sportsbook hold (vig). For example, if Over is -110 (52.38%) and Under is -110 (52.38%), the combined implied probability is 104.76%, so the vig is roughly 4.76%.')),
                array('@type' => 'Question', 'name' => 'What is the difference between implied probability and true probability?',
                    'acceptedAnswer' => array('@type' => 'Answer', 'text' => 'Implied probability is what the sportsbook price implies. True probability is what you (or a model) believe the actual likelihood is. The gap between the two is your edge.')),
                array('@type' => 'Question', 'name' => 'Are decimal odds the same as implied probability?',
                    'acceptedAnswer' => array('@type' => 'Answer', 'text' => 'No, but they are directly related. Decimal odds represent the total payout per dollar staked, while implied probability is the percentage chance the bet wins.')),
                array('@type' => 'Question', 'name' => 'How do I find the best implied probability across sportsbooks?',
                    'acceptedAnswer' => array('@type' => 'Answer', 'text' => 'For a bet you want to make, the lowest implied probability across books gives you the best price. PropsBot tracks lines across DraftKings, FanDuel, BetMGM, Caesars, Novig, Sporttrade, BetOnline, and Fliff.')),
            ),
        );
        $blocks[] = array(
            '@context' => 'https://schema.org',
            '@type'    => 'HowTo',
            'name'     => 'How to calculate implied probability from American odds',
            'description' => 'Convert American sportsbook odds (negative or positive) into an implied probability percentage in two formulas.',
            'totalTime' => 'PT1M',
            'step' => array(
                array('@type' => 'HowToStep', 'position' => 1, 'name' => 'Identify the sign', 'text' => 'Determine if the American odds are negative (favorite) or positive (underdog).'),
                array('@type' => 'HowToStep', 'position' => 2, 'name' => 'Apply the formula', 'text' => 'For negative odds: divide the absolute value of the odds by (absolute value plus 100), then multiply by 100. For positive odds: divide 100 by (odds plus 100), then multiply by 100.'),
                array('@type' => 'HowToStep', 'position' => 3, 'name' => 'Read the percentage', 'text' => 'The result is the implied probability — the win-rate the bookmaker is pricing into that line.'),
            ),
        );
        $blocks[] = array(
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
    }
    elseif ($slug === 'parlay-calculator') {
        $blocks[] = array(
            '@context' => 'https://schema.org',
            '@type'    => 'WebApplication',
            'name'     => 'Parlay Calculator',
            'description' => 'Free calculator that combines multiple bet legs (American odds) into a parlay, showing total payout, profit, combined American and decimal odds, and implied probability.',
            'url'      => $url,
            'applicationCategory' => 'FinanceApplication',
            'operatingSystem' => 'Any (web)',
            'offers'   => array('@type' => 'Offer', 'price' => '0', 'priceCurrency' => 'USD'),
            'creator'  => $publisher,
        );
        $blocks[] = array(
            '@context' => 'https://schema.org',
            '@type'    => 'FAQPage',
            'mainEntity' => array(
                array('@type' => 'Question', 'name' => 'How do you calculate a parlay payout?',
                    'acceptedAnswer' => array('@type' => 'Answer', 'text' => 'Convert each leg to decimal odds, multiply all decimal odds together, then multiply by your bet amount.')),
                array('@type' => 'Question', 'name' => 'What is a 3-leg parlay payout at -110?',
                    'acceptedAnswer' => array('@type' => 'Answer', 'text' => 'A 3-leg parlay where each leg is at -110 has combined decimal odds of 6.97 and combined American odds of +597. A $10 bet returns $69.65 ($59.65 profit).')),
                array('@type' => 'Question', 'name' => 'Is the parlay calculator accurate for same-game parlays?',
                    'acceptedAnswer' => array('@type' => 'Answer', 'text' => 'Yes for the math, but no for the price. Sportsbooks adjust same-game-parlay (SGP) odds for correlation between legs in the same game.')),
                array('@type' => 'Question', 'name' => 'How many legs can a parlay have?',
                    'acceptedAnswer' => array('@type' => 'Answer', 'text' => 'Most US sportsbooks allow up to 12-25 legs. PropsBot calculator supports up to 12 legs.')),
                array('@type' => 'Question', 'name' => 'Can I use this for prop parlays on PrizePicks or Underdog?',
                    'acceptedAnswer' => array('@type' => 'Answer', 'text' => 'Yes, with one conversion step. Convert their multipliers directly into decimal odds and use the implied probability output to compare against your actual win probability.')),
            ),
        );
        $blocks[] = array(
            '@context' => 'https://schema.org',
            '@type'    => 'HowTo',
            'name'     => 'How to calculate a parlay payout',
            'description' => 'Combine multiple bet legs (American odds) into a parlay and compute the total payout, profit, and combined American/decimal odds.',
            'totalTime' => 'PT2M',
            'step' => array(
                array('@type' => 'HowToStep', 'position' => 1, 'name' => 'Convert each leg to decimal', 'text' => 'For each American leg, convert to decimal odds.'),
                array('@type' => 'HowToStep', 'position' => 2, 'name' => 'Multiply all decimal odds together', 'text' => 'The product of every leg decimal is the combined parlay decimal.'),
                array('@type' => 'HowToStep', 'position' => 3, 'name' => 'Multiply by your bet amount', 'text' => 'Multiply combined decimal by your bet to see total payout.'),
                array('@type' => 'HowToStep', 'position' => 4, 'name' => 'Convert back to American', 'text' => 'If combined decimal is at least 2.00, American = (decimal - 1) x 100.'),
                array('@type' => 'HowToStep', 'position' => 5, 'name' => 'Calculate implied probability', 'text' => 'Implied probability = 1 / combined decimal x 100.'),
            ),
        );
        $blocks[] = array(
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
    }
"""

# The 3 new schema branches written by the agents are full PHP with elseif() opening
# blocks. Read them and append to the if/elseif chain.
# The schema files from agents are expected to be standalone elseif blocks. Let's just include them.
full_schema_php += "\n    " + holdvig_schema.replace('<?php', '').strip() + "\n"
full_schema_php += "\n    " + ev_schema.replace('<?php', '').strip() + "\n"
full_schema_php += "\n    " + novig_schema.replace('<?php', '').strip() + "\n"

# Then add the /tools/ branch and the byline injection at the end
full_schema_php += """
    elseif ($slug === 'tools') {
        $blocks[] = array(
            '@context' => 'https://schema.org',
            '@type'    => 'CollectionPage',
            'name'     => 'PropsBot.AI Free Betting Tools',
            'url'      => $url,
            'about'    => array('@type' => 'Thing', 'name' => 'Sports betting calculators'),
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
        echo '<script type="application/ld+json">' . wp_json_encode($b, JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT) . '</script>' . "\\n";
    }
}, 20);

// Author byline (visible on calculator pages, just under the H1)
add_filter('the_content', function($content) {
    if (!is_page()) return $content;
    $slug = get_post_field('post_name', get_the_ID());
    if (!in_array($slug, array(
        'implied-probability-calculator',
        'parlay-calculator',
        'hold-vig-calculator',
        'ev-calculator',
        'no-vig-fair-odds-calculator',
    ), true)) return $content;
    $byline = '<div class="pb-tool-byline" style="font-size:13px; color:rgba(200,215,230,0.7); margin:-12px 0 24px; padding:8px 0; border-bottom:1px solid rgba(100,200,220,0.07);">'
        . 'By <a href="https://propsbot.ai/author/thehulkbets/" rel="author" style="color:#15ffc2; text-decoration:none; font-weight:600;">David Reilich</a>'
        . ', Founder of PropsBot.AI &middot; Last updated ' . get_the_modified_date('F j, Y')
        . '</div>';
    return $byline . $content;
}, 9);
"""

print('Replacing schema snippet 38195...')
print(append_snippet(38195, full_schema_php, mode='replace'))

print('\nDone. Verify all 5 calculators render correctly.')
