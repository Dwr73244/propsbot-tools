<?php
/**
 * EV Calculator schema branch — paste inside the wp_head action in WPCode
 * snippet 38195 (PropsBot Tools: Schema + Author Byline Injection), as a
 * parallel `elseif ($slug === 'ev-calculator')` branch alongside the existing
 * `implied-probability-calculator` and `parlay-calculator` branches.
 *
 * Outputs four JSON-LD blocks for /tools/ev-calculator/:
 *   - WebApplication  (the calculator itself)
 *   - FAQPage         (5 FAQ Q&As mirroring the page copy)
 *   - HowTo           (3-step EV calculation method)
 *   - Article         (E-E-A-T author + publisher metadata)
 *
 * Match the existing branches' indentation, quote style, and add_action hook.
 * The surrounding `if ($slug === 'implied-probability-calculator') { ... }`
 * structure is already in place — only this block is new.
 */

// ----- inside the wp_head function in snippet 38195 -----
elseif ($slug === 'ev-calculator') {
    // 1. WebApplication
    ?>
    <script type="application/ld+json">{
        "@context": "https://schema.org",
        "@type": "WebApplication",
        "name": "Expected Value (EV) Calculator",
        "description": "Free expected value calculator — enter American odds, your true probability estimate, and bet amount to see EV in dollars, EV%, edge, and long-run expected return.",
        "url": "https://propsbot.ai/tools/ev-calculator/",
        "applicationCategory": "FinanceApplication",
        "operatingSystem": "Any (web)",
        "offers": {
            "@type": "Offer",
            "price": "0",
            "priceCurrency": "USD"
        },
        "creator": {
            "@type": "Organization",
            "name": "PropsBot.AI",
            "url": "https://propsbot.ai",
            "logo": {
                "@type": "ImageObject",
                "url": "https://propsbot.ai/wp-content/uploads/2026/03/Untitled-350-x-100-px.svg"
            }
        }
    }</script>
    <script type="application/ld+json">{
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": "What does +EV mean in betting?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "+EV (positive expected value) means the bet is mathematically profitable over the long run. It exists when your estimated true probability of winning is higher than the book implied probability for that price. Sharp bettors only place +EV bets — over hundreds or thousands of wagers, the math compounds into real profit."
                }
            },
            {
                "@type": "Question",
                "name": "How do I find the true probability of a bet?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "True probability is your best estimate of how often the bet wins. Common methods: a quantitative player-prop model, average lines from sharp books like Pinnacle (which closely approximate true probability after removing vig), AI-derived projections, or aggregating market consensus across multiple books. PropsBot's Confidence Score is an AI-modeled true probability for every prop."
                }
            },
            {
                "@type": "Question",
                "name": "Is a +EV bet always going to win?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "No. +EV is a long-run expectation, not a single-game prediction. A bet with +5% EV will lose plenty of individual bets — variance is normal. The math only proves out over hundreds or thousands of wagers."
                }
            },
            {
                "@type": "Question",
                "name": "What is a good EV percentage?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Anything above 0% is mathematically profitable. In practice, professional bettors target +2% EV or higher to comfortably overcome variance and model uncertainty. Anything above +5% is a strong edge; +10% or higher is rare and usually indicates a stale line, mispriced prop, or news the book has not yet reacted to."
                }
            },
            {
                "@type": "Question",
                "name": "How is EV different from edge?",
                "acceptedAnswer": {
                    "@type": "Answer",
                    "text": "Edge is the percentage-point gap between your true probability and the book implied probability (e.g., 50% minus 40% equals +10 pp edge). EV is the dollar (or per-dollar) translation of that edge given the price and bet size. Edge tells you whether a bet is +EV; EV tells you how profitable in dollars."
                }
            }
        ]
    }</script>
    <script type="application/ld+json">{
        "@context": "https://schema.org",
        "@type": "HowTo",
        "name": "How to calculate expected value (EV) for a sports bet",
        "description": "Convert American odds, a true probability estimate, and a stake into expected value in dollars and EV percentage in three steps.",
        "totalTime": "PT1M",
        "step": [
            {
                "@type": "HowToStep",
                "position": 1,
                "name": "Calculate profit if win",
                "text": "For negative American odds (favorites), profit = bet × 100 / |odds|. For positive American odds (underdogs), profit = bet × odds / 100. Example: $100 at +150 wins $150 of profit."
            },
            {
                "@type": "HowToStep",
                "position": 2,
                "name": "Apply the EV formula",
                "text": "EV = (true_probability × profit_if_win) − ((1 − true_probability) × bet_amount). Express true probability as a decimal between 0 and 1. Example: 0.50 × $150 − 0.50 × $100 = +$25 EV."
            },
            {
                "@type": "HowToStep",
                "position": 3,
                "name": "Convert to EV% and edge",
                "text": "EV% = (EV / bet_amount) × 100. Edge = your_true_probability − book_implied_probability. Positive EV and edge indicate a profitable long-run bet; negative values mean skip."
            }
        ]
    }</script>
    <script type="application/ld+json">{
        "@context": "https://schema.org",
        "@type": "Article",
        "headline": "Expected Value Calculator — Find +EV Sports Bets in Seconds | PropsBot.AI",
        "datePublished": "<?php echo esc_js( get_the_date( 'c' ) ); ?>",
        "dateModified": "<?php echo esc_js( get_the_modified_date( 'c' ) ); ?>",
        "author": {
            "@type": "Person",
            "name": "David Reilich",
            "jobTitle": "Founder, PropsBot.AI",
            "url": "https://propsbot.ai/author/thehulkbets/",
            "sameAs": [
                "https://x.com/propsbotai"
            ]
        },
        "publisher": {
            "@type": "Organization",
            "name": "PropsBot.AI",
            "url": "https://propsbot.ai",
            "logo": {
                "@type": "ImageObject",
                "url": "https://propsbot.ai/wp-content/uploads/2026/03/Untitled-350-x-100-px.svg"
            }
        },
        "mainEntityOfPage": "https://propsbot.ai/tools/ev-calculator/",
        "inLanguage": "en-US"
    }</script>
    <?php
}
// ----- end branch -----
