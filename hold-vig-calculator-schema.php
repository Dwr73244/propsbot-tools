<?php
/**
 * PropsBot Tools — Hold / Vig Calculator schema injection.
 *
 * Append this block inside the existing wp_head action handler in
 * WPCode snippet 38195 (PropsBot Tools: Schema + Author Byline Injection).
 * Mirror the existing IPC + Parlay schema-block pattern: gate on slug,
 * emit four JSON-LD blocks (WebApplication + FAQPage + HowTo + Article).
 *
 * Slug guard: 'hold-vig-calculator' (parent /tools/ → permalink
 * /tools/hold-vig-calculator/).
 */

add_action( 'wp_head', function () {
    if ( ! is_page() ) return;
    $slug = get_post_field( 'post_name', get_queried_object_id() );
    if ( $slug !== 'hold-vig-calculator' ) return;

    $page_url     = 'https://propsbot.ai/tools/hold-vig-calculator/';
    $date_pub     = '2026-05-01';
    $date_mod     = '2026-05-01';
    $author_name  = 'David Reilich';
    $author_url   = 'https://propsbot.ai/about/';
    $org_name     = 'PropsBot.AI';
    $org_url      = 'https://propsbot.ai';
    $org_logo     = 'https://propsbot.ai/wp-content/uploads/2026/03/propsbot-logo.png';
    $page_title   = 'Hold / Vig Calculator — Calculate Sportsbook Margin & No-Vig Fair Odds | PropsBot.AI';
    $page_desc    = 'Free Hold / Vig Calculator. Enter American odds for both sides of a 2-way market and see total hold, no-vig fair probability, and no-vig fair American odds for each side.';

    /* ---------- WebApplication ---------- */
    $web_app = array(
        '@context'         => 'https://schema.org',
        '@type'            => 'WebApplication',
        '@id'              => $page_url . '#webapp',
        'name'             => 'PropsBot Hold / Vig Calculator',
        'url'              => $page_url,
        'applicationCategory' => 'FinanceApplication',
        'browserRequirements' => 'Requires JavaScript. Requires HTML5.',
        'operatingSystem'  => 'Any',
        'description'      => 'Compute the hold (vig) on any 2-way sportsbook market. Inputs American odds for both sides; outputs total hold percentage, implied probabilities, no-vig fair probabilities, and no-vig fair American odds.',
        'offers'           => array(
            '@type'         => 'Offer',
            'price'         => '0',
            'priceCurrency' => 'USD',
        ),
        'creator'          => array(
            '@type' => 'Organization',
            'name'  => $org_name,
            'url'   => $org_url,
            'logo'  => $org_logo,
        ),
        'inLanguage'       => 'en-US',
    );

    /* ---------- FAQPage ---------- */
    $faqs = array(
        array(
            'q' => 'What is the hold on a -110/-110 market?',
            'a' => 'The hold on a -110/-110 market is 4.76%. Both sides have an implied probability of 52.38%, summing to 104.76% — the 4.76% overage is the sportsbook\'s margin. The no-vig fair price for both sides is +100 (50.00% true probability each).',
        ),
        array(
            'q' => 'What is a "good" hold for a sportsbook?',
            'a' => 'From the bettor\'s perspective, lower hold is better. Pinnacle, Novig, and Sporttrade run 1-3% hold on most point spreads and totals. DraftKings, FanDuel, BetMGM, and Caesars typically run 4.5-6%. Player props and same-game parlays often exceed 8-10% hold.',
        ),
        array(
            'q' => 'What are no-vig fair odds?',
            'a' => 'No-vig fair odds are the price a 2-way market would offer at zero margin. To compute them: divide each side\'s implied probability by the sum of both sides, then convert that adjusted probability back to American odds. This baseline is what sharp bettors compare their model probabilities against to determine edge.',
        ),
        array(
            'q' => 'Can hold be negative?',
            'a' => 'Not on a single sportsbook. But when you combine the best price for Side 1 at one book with the best price for Side 2 at another, the combined implied probability can drop below 100% — that\'s an arbitrage opportunity. The calculator flags negative hold when inputs imply one.',
        ),
        array(
            'q' => 'How is hold different from house edge?',
            'a' => 'Hold is expressed as the overage in summed implied probability across a 2-way market — the book\'s theoretical profit on balanced action. House edge is the bettor\'s expected loss per dollar wagered. For a -110/-110 market, hold is 4.76% but expected loss per dollar wagered is about 2.38% — roughly half the hold, because the bettor only stakes one side.',
        ),
    );

    $faq_main_entity = array();
    foreach ( $faqs as $f ) {
        $faq_main_entity[] = array(
            '@type' => 'Question',
            'name'  => $f['q'],
            'acceptedAnswer' => array(
                '@type' => 'Answer',
                'text'  => $f['a'],
            ),
        );
    }
    $faq_page = array(
        '@context'   => 'https://schema.org',
        '@type'      => 'FAQPage',
        '@id'        => $page_url . '#faq',
        'mainEntity' => $faq_main_entity,
    );

    /* ---------- HowTo ---------- */
    $how_to = array(
        '@context'    => 'https://schema.org',
        '@type'       => 'HowTo',
        '@id'         => $page_url . '#howto',
        'name'        => 'How to calculate hold (vig) on a 2-way sportsbook market',
        'description' => 'Convert American odds for each side to implied probability, sum them, subtract 100% — the remainder is the hold. Then divide each side by the total to get no-vig fair probability, and convert back to American odds for no-vig fair odds.',
        'totalTime'   => 'PT1M',
        'tool'        => array(
            array(
                '@type' => 'HowToTool',
                'name'  => 'PropsBot Hold / Vig Calculator',
            ),
        ),
        'step'        => array(
            array(
                '@type' => 'HowToStep',
                'position' => 1,
                'name'  => 'Convert each side to implied probability',
                'text'  => 'Negative odds: |odds| / (|odds| + 100). Positive odds: 100 / (odds + 100). Multiply by 100 to express as a percentage.',
            ),
            array(
                '@type' => 'HowToStep',
                'position' => 2,
                'name'  => 'Sum the two implied probabilities',
                'text'  => 'Add Side 1 implied probability and Side 2 implied probability. The total will exceed 100% on any priced 2-way market.',
            ),
            array(
                '@type' => 'HowToStep',
                'position' => 3,
                'name'  => 'Subtract 100% to get hold',
                'text'  => 'Total minus 100% equals the hold (vig). For -110/-110, total = 104.76%, hold = 4.76%.',
            ),
            array(
                '@type' => 'HowToStep',
                'position' => 4,
                'name'  => 'Compute no-vig fair probabilities',
                'text'  => 'Divide each side\'s implied probability by the total. The two now sum to exactly 100% and represent the market\'s zero-margin estimate of true win probability.',
            ),
            array(
                '@type' => 'HowToStep',
                'position' => 5,
                'name'  => 'Convert fair probabilities back to American odds',
                'text'  => 'For probability p ≥ 0.5, no-vig fair American = -100 × p / (1 - p). For p < 0.5, no-vig fair American = (100 - 100p) / p. The result is the price the market would offer at zero margin.',
            ),
        ),
    );

    /* ---------- Article ---------- */
    $article = array(
        '@context'        => 'https://schema.org',
        '@type'           => 'Article',
        '@id'             => $page_url . '#article',
        'headline'        => 'Hold / Vig Calculator — Calculate Sportsbook Margin & No-Vig Fair Odds',
        'description'     => $page_desc,
        'url'             => $page_url,
        'datePublished'   => $date_pub,
        'dateModified'    => $date_mod,
        'inLanguage'      => 'en-US',
        'author'          => array(
            '@type' => 'Person',
            'name'  => $author_name,
            'url'   => $author_url,
        ),
        'publisher'       => array(
            '@type' => 'Organization',
            'name'  => $org_name,
            'url'   => $org_url,
            'logo'  => array(
                '@type' => 'ImageObject',
                'url'   => $org_logo,
            ),
        ),
        'mainEntityOfPage' => array(
            '@type' => 'WebPage',
            '@id'   => $page_url,
        ),
        'about'           => array(
            array( '@type' => 'Thing', 'name' => 'Sportsbook hold' ),
            array( '@type' => 'Thing', 'name' => 'Vigorish' ),
            array( '@type' => 'Thing', 'name' => 'No-vig fair odds' ),
            array( '@type' => 'Thing', 'name' => 'Implied probability' ),
        ),
    );

    $blocks = array( $web_app, $faq_page, $how_to, $article );
    foreach ( $blocks as $b ) {
        echo "\n" . '<script type="application/ld+json">' . wp_json_encode( $b, JSON_UNESCAPED_SLASHES | JSON_UNESCAPED_UNICODE ) . '</script>' . "\n";
    }
}, 20 );
