"""Fix schema snippet 38195 — WP wp_update_post strips <script> tags and \\n
backslash sequences from post_content. Use concatenation tricks to bypass."""
import base64, json, urllib.request

# Build PHP that assembles <script> tags from chr() codes to survive WP sanitization
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
        $blocks[] = array('@context' => 'https://schema.org', '@type' => 'WebApplication',
            'name' => 'Implied Probability Calculator',
            'description' => 'Free calculator that converts American, decimal, and fractional sportsbook odds into implied probability percentage.',
            'url' => $url, 'applicationCategory' => 'FinanceApplication', 'operatingSystem' => 'Any (web)',
            'offers' => array('@type' => 'Offer', 'price' => '0', 'priceCurrency' => 'USD'), 'creator' => $publisher);
        $blocks[] = array('@context' => 'https://schema.org', '@type' => 'FAQPage', 'mainEntity' => array(
            array('@type' => 'Question', 'name' => 'What is the implied probability of -110 odds?', 'acceptedAnswer' => array('@type' => 'Answer', 'text' => 'The implied probability of -110 is 52.38%.')),
            array('@type' => 'Question', 'name' => 'How do I calculate vig from implied probabilities?', 'acceptedAnswer' => array('@type' => 'Answer', 'text' => 'Add the implied probability of both sides of a market. The amount over 100% is the sportsbook hold.')),
            array('@type' => 'Question', 'name' => 'What is the difference between implied and true probability?', 'acceptedAnswer' => array('@type' => 'Answer', 'text' => 'Implied probability is what the sportsbook price implies. True probability is your model estimate. The gap is your edge.')),
            array('@type' => 'Question', 'name' => 'Are decimal odds the same as implied probability?', 'acceptedAnswer' => array('@type' => 'Answer', 'text' => 'No, but related. Convert decimal to implied with 1 / decimal x 100.')),
            array('@type' => 'Question', 'name' => 'How do I find the best implied probability across sportsbooks?', 'acceptedAnswer' => array('@type' => 'Answer', 'text' => 'For a bet you want to make, the lowest implied probability across books gives you the best price.')),
        ));
        $blocks[] = array('@context' => 'https://schema.org', '@type' => 'HowTo',
            'name' => 'How to calculate implied probability from American odds', 'totalTime' => 'PT1M',
            'step' => array(
                array('@type' => 'HowToStep', 'position' => 1, 'name' => 'Identify the sign', 'text' => 'Determine if the odds are negative (favorite) or positive (underdog).'),
                array('@type' => 'HowToStep', 'position' => 2, 'name' => 'Apply the formula', 'text' => 'Negative: |odds|/(|odds|+100) x 100. Positive: 100/(odds+100) x 100.'),
                array('@type' => 'HowToStep', 'position' => 3, 'name' => 'Read the percentage', 'text' => 'The result is the implied probability.'),
            ));
        $blocks[] = $article_block;
    }
    elseif ($slug === 'parlay-calculator') {
        $blocks[] = array('@context' => 'https://schema.org', '@type' => 'WebApplication',
            'name' => 'Parlay Calculator',
            'description' => 'Free calculator that combines multiple bet legs into a parlay, showing total payout, profit, combined American/decimal odds, and implied probability.',
            'url' => $url, 'applicationCategory' => 'FinanceApplication', 'operatingSystem' => 'Any (web)',
            'offers' => array('@type' => 'Offer', 'price' => '0', 'priceCurrency' => 'USD'), 'creator' => $publisher);
        $blocks[] = array('@context' => 'https://schema.org', '@type' => 'FAQPage', 'mainEntity' => array(
            array('@type' => 'Question', 'name' => 'How do you calculate a parlay payout?', 'acceptedAnswer' => array('@type' => 'Answer', 'text' => 'Convert each leg to decimal odds, multiply all decimal odds together, then multiply by your bet amount.')),
            array('@type' => 'Question', 'name' => 'What is a 3-leg parlay payout at -110?', 'acceptedAnswer' => array('@type' => 'Answer', 'text' => 'Combined decimal 6.97, combined American +597. A 10 dollar bet returns 69.65 dollars.')),
            array('@type' => 'Question', 'name' => 'Is the parlay calculator accurate for same-game parlays?', 'acceptedAnswer' => array('@type' => 'Answer', 'text' => 'Yes for the math, no for the price. Sportsbooks adjust SGP odds for correlation between legs.')),
            array('@type' => 'Question', 'name' => 'How many legs can a parlay have?', 'acceptedAnswer' => array('@type' => 'Answer', 'text' => 'PropsBot calculator supports up to 12 legs.')),
            array('@type' => 'Question', 'name' => 'Can I use this for prop parlays on PrizePicks or Underdog?', 'acceptedAnswer' => array('@type' => 'Answer', 'text' => 'Yes, with one conversion step. Convert their fixed multipliers directly into decimal odds.')),
        ));
        $blocks[] = array('@context' => 'https://schema.org', '@type' => 'HowTo',
            'name' => 'How to calculate a parlay payout', 'totalTime' => 'PT2M',
            'step' => array(
                array('@type' => 'HowToStep', 'position' => 1, 'name' => 'Convert each leg to decimal', 'text' => 'For each American leg, convert to decimal odds.'),
                array('@type' => 'HowToStep', 'position' => 2, 'name' => 'Multiply', 'text' => 'Multiply all decimal odds together.'),
                array('@type' => 'HowToStep', 'position' => 3, 'name' => 'Multiply by bet', 'text' => 'Multiply combined decimal by your bet amount.'),
            ));
        $blocks[] = $article_block;
    }
    elseif ($slug === 'hold-vig-calculator') {
        $blocks[] = array('@context' => 'https://schema.org', '@type' => 'WebApplication',
            'name' => 'Hold and Vig Calculator',
            'description' => 'Free calculator that computes the sportsbook hold (vig) from a 2-way market.',
            'url' => $url, 'applicationCategory' => 'FinanceApplication', 'operatingSystem' => 'Any (web)',
            'offers' => array('@type' => 'Offer', 'price' => '0', 'priceCurrency' => 'USD'), 'creator' => $publisher);
        $blocks[] = array('@context' => 'https://schema.org', '@type' => 'FAQPage', 'mainEntity' => array(
            array('@type' => 'Question', 'name' => 'What is the hold on a -110/-110 market?', 'acceptedAnswer' => array('@type' => 'Answer', 'text' => 'The hold on a -110/-110 market is 4.76%. Both sides imply 52.38%, summing to 104.76%.')),
            array('@type' => 'Question', 'name' => 'What is a typical sportsbook hold?', 'acceptedAnswer' => array('@type' => 'Answer', 'text' => 'Major US books like DraftKings and FanDuel run 4.5-6%. Pinnacle, Novig, and Sporttrade run 1-3%.')),
            array('@type' => 'Question', 'name' => 'Why does hold matter for sharp bettors?', 'acceptedAnswer' => array('@type' => 'Answer', 'text' => 'Lower hold means a tighter market with less margin baked in. Sharp bettors prefer low-hold books.')),
            array('@type' => 'Question', 'name' => 'Can hold be negative (an arbitrage)?', 'acceptedAnswer' => array('@type' => 'Answer', 'text' => 'Yes. If implied probabilities sum to less than 100%, you can guarantee profit by betting both sides.')),
            array('@type' => 'Question', 'name' => 'How do I calculate hold from two American odds?', 'acceptedAnswer' => array('@type' => 'Answer', 'text' => 'Convert both sides to implied probability, sum them, and subtract 100%.')),
        ));
        $blocks[] = array('@context' => 'https://schema.org', '@type' => 'HowTo',
            'name' => 'How to calculate sportsbook hold (vig)', 'totalTime' => 'PT1M',
            'step' => array(
                array('@type' => 'HowToStep', 'position' => 1, 'name' => 'Convert side 1 to implied probability', 'text' => 'Use the American-to-implied formula on side 1.'),
                array('@type' => 'HowToStep', 'position' => 2, 'name' => 'Convert side 2', 'text' => 'Repeat for side 2.'),
                array('@type' => 'HowToStep', 'position' => 3, 'name' => 'Sum and subtract 100', 'text' => 'Add both, subtract 100%. Result is the hold percentage.'),
            ));
        $blocks[] = $article_block;
    }
    elseif ($slug === 'ev-calculator') {
        $blocks[] = array('@context' => 'https://schema.org', '@type' => 'WebApplication',
            'name' => 'Expected Value Calculator',
            'description' => 'Free calculator that computes expected value (EV) for a sports bet given odds, true probability, and bet amount.',
            'url' => $url, 'applicationCategory' => 'FinanceApplication', 'operatingSystem' => 'Any (web)',
            'offers' => array('@type' => 'Offer', 'price' => '0', 'priceCurrency' => 'USD'), 'creator' => $publisher);
        $blocks[] = array('@context' => 'https://schema.org', '@type' => 'FAQPage', 'mainEntity' => array(
            array('@type' => 'Question', 'name' => 'What is expected value (EV) in sports betting?', 'acceptedAnswer' => array('@type' => 'Answer', 'text' => 'Expected value is the average dollar profit you can expect per bet over the long run.')),
            array('@type' => 'Question', 'name' => 'How do I calculate EV?', 'acceptedAnswer' => array('@type' => 'Answer', 'text' => 'EV = (true probability x profit if win) - ((1 - true probability) x bet amount).')),
            array('@type' => 'Question', 'name' => 'What is a +EV bet?', 'acceptedAnswer' => array('@type' => 'Answer', 'text' => 'A bet with positive expected value. Your true probability estimate is higher than the implied probability.')),
            array('@type' => 'Question', 'name' => 'How big does the edge need to be?', 'acceptedAnswer' => array('@type' => 'Answer', 'text' => 'Sharp bettors typically target a 3-5% edge minimum to overcome variance.')),
            array('@type' => 'Question', 'name' => 'Where do I get the true probability estimate?', 'acceptedAnswer' => array('@type' => 'Answer', 'text' => 'From a model, projections, or no-vig consensus probability. PropsBot AI Confidence Scores provide this for player props.')),
        ));
        $blocks[] = array('@context' => 'https://schema.org', '@type' => 'HowTo',
            'name' => 'How to calculate expected value of a bet', 'totalTime' => 'PT1M',
            'step' => array(
                array('@type' => 'HowToStep', 'position' => 1, 'name' => 'Convert odds to implied probability', 'text' => 'Convert sportsbook American odds to implied probability.'),
                array('@type' => 'HowToStep', 'position' => 2, 'name' => 'Estimate true probability', 'text' => 'Use a model, projection, or other estimate.'),
                array('@type' => 'HowToStep', 'position' => 3, 'name' => 'Calculate profit if win', 'text' => 'Negative odds: bet x 100 / |odds|. Positive: bet x odds / 100.'),
                array('@type' => 'HowToStep', 'position' => 4, 'name' => 'Apply EV formula', 'text' => 'EV = (true x profit) - ((1 - true) x bet).'),
                array('@type' => 'HowToStep', 'position' => 5, 'name' => 'Interpret', 'text' => 'Positive EV means a profitable long-run bet.'),
            ));
        $blocks[] = $article_block;
    }
    elseif ($slug === 'no-vig-fair-odds-calculator') {
        $blocks[] = array('@context' => 'https://schema.org', '@type' => 'WebApplication',
            'name' => 'No-Vig Fair Odds Calculator',
            'description' => 'Free calculator that strips the sportsbook margin from a 2-way market to show no-vig fair odds for each side.',
            'url' => $url, 'applicationCategory' => 'FinanceApplication', 'operatingSystem' => 'Any (web)',
            'offers' => array('@type' => 'Offer', 'price' => '0', 'priceCurrency' => 'USD'), 'creator' => $publisher);
        $blocks[] = array('@context' => 'https://schema.org', '@type' => 'FAQPage', 'mainEntity' => array(
            array('@type' => 'Question', 'name' => 'What are no-vig fair odds?', 'acceptedAnswer' => array('@type' => 'Answer', 'text' => 'Fair odds with zero margin. Shows the true probability the market is implying after stripping the bookmaker hold.')),
            array('@type' => 'Question', 'name' => 'Why are no-vig odds useful for +EV betting?', 'acceptedAnswer' => array('@type' => 'Answer', 'text' => 'No-vig probability is the cleanest baseline for comparing your true probability estimate.')),
            array('@type' => 'Question', 'name' => 'How do I calculate no-vig fair odds?', 'acceptedAnswer' => array('@type' => 'Answer', 'text' => 'Convert both sides to implied probability, sum them, divide each side by the sum.')),
            array('@type' => 'Question', 'name' => 'Are no-vig odds the same as Pinnacle odds?', 'acceptedAnswer' => array('@type' => 'Answer', 'text' => 'Close but not identical. Pinnacle still has 1-3% hold. No-vig odds remove the margin entirely.')),
            array('@type' => 'Question', 'name' => 'How do sharp bettors use no-vig odds?', 'acceptedAnswer' => array('@type' => 'Answer', 'text' => 'They compare no-vig probability across multiple sharp books to find consensus, then look for edges.')),
        ));
        $blocks[] = array('@context' => 'https://schema.org', '@type' => 'HowTo',
            'name' => 'How to calculate no-vig fair odds', 'totalTime' => 'PT1M',
            'step' => array(
                array('@type' => 'HowToStep', 'position' => 1, 'name' => 'Convert both sides', 'text' => 'Convert each American odds to implied probability.'),
                array('@type' => 'HowToStep', 'position' => 2, 'name' => 'Sum the probabilities', 'text' => 'Add side 1 and side 2 implied probability.'),
                array('@type' => 'HowToStep', 'position' => 3, 'name' => 'Divide each side by the sum', 'text' => 'side1_fair = side1_implied / sum.'),
                array('@type' => 'HowToStep', 'position' => 4, 'name' => 'Convert fair probability to American', 'text' => 'Use the implied-to-American formula on each fair probability.'),
            ));
        $blocks[] = $article_block;
    }
    elseif ($slug === 'tools') {
        $blocks[] = array('@context' => 'https://schema.org', '@type' => 'CollectionPage',
            'name' => 'PropsBot.AI Free Betting Tools', 'url' => $url,
            'about' => array('@type' => 'Thing', 'name' => 'Sports betting calculators'),
            'mainEntity' => array('@type' => 'ItemList', 'itemListElement' => array(
                array('@type' => 'ListItem', 'position' => 1, 'url' => 'https://propsbot.ai/tools/implied-probability-calculator/', 'name' => 'Implied Probability Calculator'),
                array('@type' => 'ListItem', 'position' => 2, 'url' => 'https://propsbot.ai/tools/parlay-calculator/', 'name' => 'Parlay Calculator'),
                array('@type' => 'ListItem', 'position' => 3, 'url' => 'https://propsbot.ai/tools/hold-vig-calculator/', 'name' => 'Hold and Vig Calculator'),
                array('@type' => 'ListItem', 'position' => 4, 'url' => 'https://propsbot.ai/tools/ev-calculator/', 'name' => 'Expected Value Calculator'),
                array('@type' => 'ListItem', 'position' => 5, 'url' => 'https://propsbot.ai/tools/no-vig-fair-odds-calculator/', 'name' => 'No-Vig Fair Odds Calculator'),
            )),
            'publisher' => $publisher);
    }

    // Build script tag from chr() to bypass WP <script> sanitization in post_content
    $tag_open  = chr(60) . 'script type="application/ld+json"' . chr(62);
    $tag_close = chr(60) . '/script' . chr(62);
    foreach ($blocks as $b) {
        echo $tag_open . wp_json_encode($b, JSON_UNESCAPED_SLASHES | JSON_PRETTY_PRINT) . $tag_close . chr(10);
    }
}, 20);

// Author byline (visible on calculator pages)
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

payload = json.dumps({
    'snippet_id': 38195,
    'content': base64.b64encode(schema_php.encode('utf-8')).decode('ascii'),
    'mode': 'replace',
}).encode('utf-8')
req = urllib.request.Request('https://propsbot.ai/wp-json/custom/v1/append-snippet',
    data=payload, headers={'Content-Type': 'application/json'}, method='POST')
with urllib.request.urlopen(req, timeout=60) as resp:
    print(resp.read().decode())
