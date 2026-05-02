<?php
/**
 * No-Vig Fair Odds Calculator — schema branch for WPCode snippet 38195.
 *
 * This is a *branch* to add to the existing snippet, not a standalone file.
 * Drop this `elseif` into the slug switch alongside the IPC and parlay branches.
 * Outputs WebApplication + FAQPage + HowTo + Article JSON-LD.
 *
 * Hooks: wp_head (gated to is_page() with this slug)
 * Slug:  no-vig-fair-odds-calculator
 *
 * Author / publisher / Person blocks reuse the same byline pattern as the
 * IPC and parlay schema branches (David Reilich, Founder of PropsBot.AI).
 */

// === Drop into the existing slug switch in snippet 38195 ===
// Existing snippet structure:
//   if      ($slug === 'implied-probability-calculator')   { ... }
//   elseif  ($slug === 'parlay-calculator')                { ... }
//   elseif  ($slug === 'no-vig-fair-odds-calculator')      { /* THIS BLOCK */ }

elseif ($slug === 'no-vig-fair-odds-calculator') {

    $page_url      = 'https://propsbot.ai/tools/no-vig-fair-odds-calculator/';
    $page_title    = 'No-Vig Fair Odds Calculator — Strip Sportsbook Margin to See True Prices';
    $page_descr    = 'Free no-vig fair odds calculator from PropsBot.AI. Enter American odds for both sides of a 2-way market and see the no-vig fair probability, fair American odds, and fair decimal odds for each side — with sportsbook margin removed.';
    $date_pub      = '2026-05-01T08:00:00-04:00';
    $date_mod      = gmdate('c');

    // ---------- WebApplication (the calculator itself) ----------
    $web_app = array(
        '@context'        => 'https://schema.org',
        '@type'           => 'WebApplication',
        '@id'             => $page_url . '#webapp',
        'name'            => 'No-Vig Fair Odds Calculator',
        'url'             => $page_url,
        'description'     => 'Strip sportsbook margin from a 2-way market to reveal the no-vig fair price each side would offer at zero hold. Outputs fair probability, fair American odds, and fair decimal odds for both sides.',
        'applicationCategory' => 'FinanceApplication',
        'operatingSystem' => 'Any (Web)',
        'browserRequirements' => 'JavaScript enabled',
        'offers'          => array(
            '@type'         => 'Offer',
            'price'         => '0',
            'priceCurrency' => 'USD',
        ),
        'isPartOf'        => array(
            '@type' => 'WebSite',
            'name'  => 'PropsBot.AI',
            'url'   => 'https://propsbot.ai',
        ),
        'creator'         => array(
            '@type' => 'Person',
            '@id'   => 'https://propsbot.ai/#david-reilich',
            'name'  => 'David Reilich',
        ),
        'publisher'       => array(
            '@type' => 'Organization',
            '@id'   => 'https://propsbot.ai/#org',
            'name'  => 'PropsBot.AI',
            'url'   => 'https://propsbot.ai',
        ),
        'featureList'     => array(
            'Convert American odds to no-vig fair probability',
            'Compute fair American and decimal odds for both sides of a 2-way market',
            'Display total hold (vig) removed as a percentage',
            'Validate American-odds inputs (rejects values in -99 to +99 range)',
            'One-click presets for common 2-way markets',
        ),
    );
    echo '<script type="application/ld+json">' . wp_json_encode($web_app, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE) . '</script>' . "\n";

    // ---------- FAQPage ----------
    $faq = array(
        '@context'   => 'https://schema.org',
        '@type'      => 'FAQPage',
        '@id'        => $page_url . '#faq',
        'mainEntity' => array(
            array(
                '@type'          => 'Question',
                'name'           => 'What does "no-vig" mean in sports betting?',
                'acceptedAnswer' => array(
                    '@type' => 'Answer',
                    'text'  => 'No-vig means the sportsbook\'s margin (vig, juice, or hold) has been removed from the price. A no-vig fair probability is the win rate the book is implying once you strip the bookmaker\'s profit margin out of the line. On a -110 / -110 market, the no-vig fair probability of each side is exactly 50.00% — the 4.76% margin is gone.',
                ),
            ),
            array(
                '@type'          => 'Question',
                'name'           => 'How do I calculate no-vig odds from -110 / -110?',
                'acceptedAnswer' => array(
                    '@type' => 'Answer',
                    'text'  => 'Each -110 line has implied probability 52.38%. Add them: 104.76%. Divide each side by the total: 52.38% / 104.76% = 50.00%. Convert 50.00% back to American odds: +100 (or -100 — equivalent at exactly 50%). Both sides are 50/50 in the no-vig market. The 4.76% over 100% is the hold the book was charging.',
                ),
            ),
            array(
                '@type'          => 'Question',
                'name'           => 'Are no-vig odds the same as Pinnacle\'s odds?',
                'acceptedAnswer' => array(
                    '@type' => 'Answer',
                    'text'  => 'Close, but not identical. Pinnacle runs roughly 2-3% margin on most major markets — much lower than DraftKings or FanDuel (4.5-6%), but not zero. Pinnacle\'s prices are the closest publicly available reference for fair odds, which is why sharps use them as a benchmark. To get strictly no-vig fair odds from Pinnacle\'s prices, you still run the same removal math.',
                ),
            ),
            array(
                '@type'          => 'Question',
                'name'           => 'Can I use no-vig odds to find +EV bets?',
                'acceptedAnswer' => array(
                    '@type' => 'Answer',
                    'text'  => 'Yes — that\'s the primary use case. If your model\'s true probability for an outcome is meaningfully higher than the no-vig fair probability the market is offering, the bet has positive expected value. Sharp bettors compare their estimate to the no-vig number rather than the raw implied probability because the no-vig number is what the book actually thinks the win rate is, with margin stripped out.',
                ),
            ),
            array(
                '@type'          => 'Question',
                'name'           => 'Does the no-vig formula work for 3-way markets?',
                'acceptedAnswer' => array(
                    '@type' => 'Answer',
                    'text'  => 'The same proportional-removal methodology works — sum the implied probabilities of all three sides, then divide each by the total to get fair probabilities. This calculator is designed for 2-way markets (the most common format for player props, point spreads, totals, and standard moneylines). For 3-way markets like soccer Home/Draw/Away or hockey 60-minute lines, the same math extends to a third input.',
                ),
            ),
        ),
    );
    echo '<script type="application/ld+json">' . wp_json_encode($faq, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE) . '</script>' . "\n";

    // ---------- HowTo ----------
    $howto = array(
        '@context'      => 'https://schema.org',
        '@type'         => 'HowTo',
        '@id'           => $page_url . '#howto',
        'name'          => 'How to calculate no-vig fair odds for a 2-way market',
        'description'   => 'Five-step procedure to strip the sportsbook\'s margin from a 2-way market and produce fair probabilities, fair American odds, and fair decimal odds for each side.',
        'totalTime'     => 'PT2M',
        'tool'          => array(
            array('@type' => 'HowToTool', 'name' => 'PropsBot.AI No-Vig Fair Odds Calculator'),
        ),
        'step'          => array(
            array(
                '@type' => 'HowToStep',
                'position' => 1,
                'name'  => 'Convert each side to implied probability',
                'text'  => 'Negative American odds (favorite): |odds| / (|odds| + 100). Positive American odds (underdog): 100 / (odds + 100). Example: -110 → 110/210 = 0.5238 (52.38%).',
            ),
            array(
                '@type' => 'HowToStep',
                'position' => 2,
                'name'  => 'Sum the two implied probabilities',
                'text'  => 'Add the two side probabilities. The total will exceed 1.00. The amount over 1.00 is the sportsbook\'s hold. Example: 0.5238 + 0.5238 = 1.0476 (4.76% hold).',
            ),
            array(
                '@type' => 'HowToStep',
                'position' => 3,
                'name'  => 'Normalize each side',
                'text'  => 'Divide each side\'s implied probability by the total. The two normalized values are the no-vig fair probabilities and now sum to exactly 1.00. Example: 0.5238 / 1.0476 = 0.5000 (50.00%).',
            ),
            array(
                '@type' => 'HowToStep',
                'position' => 4,
                'name'  => 'Convert fair probability back to American odds',
                'text'  => 'For probability ≥ 0.5: American = -1 × round(100 × p / (1 - p)). For probability < 0.5: American = round((100 - 100 × p) / p). Example: 0.5000 → +100.',
            ),
            array(
                '@type' => 'HowToStep',
                'position' => 5,
                'name'  => 'Compute fair decimal odds (optional)',
                'text'  => 'Fair decimal odds = 1 / fair probability. Example: 1 / 0.5000 = 2.00 decimal.',
            ),
        ),
    );
    echo '<script type="application/ld+json">' . wp_json_encode($howto, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE) . '</script>' . "\n";

    // ---------- Article (E-E-A-T) ----------
    $article = array(
        '@context'         => 'https://schema.org',
        '@type'            => 'Article',
        '@id'              => $page_url . '#article',
        'mainEntityOfPage' => $page_url,
        'headline'         => 'No-Vig Fair Odds Calculator — Strip Sportsbook Margin to See True Prices',
        'description'      => $page_descr,
        'datePublished'    => $date_pub,
        'dateModified'     => $date_mod,
        'author'           => array(
            '@type'      => 'Person',
            '@id'        => 'https://propsbot.ai/#david-reilich',
            'name'       => 'David Reilich',
            'jobTitle'   => 'Founder, PropsBot.AI',
            'url'        => 'https://propsbot.ai/about/',
            'sameAs'     => array(
                'https://x.com/propsbotai',
                'https://linkedin.com/company/propsbot',
            ),
        ),
        'publisher'        => array(
            '@type' => 'Organization',
            '@id'   => 'https://propsbot.ai/#org',
            'name'  => 'PropsBot.AI',
            'url'   => 'https://propsbot.ai',
            'logo'  => array(
                '@type' => 'ImageObject',
                'url'   => 'https://propsbot.ai/wp-content/uploads/2026/03/propsbot-logo.png',
            ),
        ),
        'about'            => array(
            array('@type' => 'Thing', 'name' => 'No-vig odds'),
            array('@type' => 'Thing', 'name' => 'Sportsbook margin'),
            array('@type' => 'Thing', 'name' => 'Vigorish'),
            array('@type' => 'Thing', 'name' => 'Positive expected value betting'),
        ),
        'isPartOf'         => array(
            '@type' => 'WebSite',
            'name'  => 'PropsBot.AI',
            'url'   => 'https://propsbot.ai',
        ),
    );
    echo '<script type="application/ld+json">' . wp_json_encode($article, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE) . '</script>' . "\n";
}
