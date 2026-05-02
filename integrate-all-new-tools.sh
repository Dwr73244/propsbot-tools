#!/bin/bash
# Master integration script — runs after agents have written their files.
# Combines outputs from Hold/Vig + EV + No-Vig agents into a single deploy.
#
# Pre-flight: agents must have written these files to ./propsbot-tools/:
#   hold-vig-calculator.html, hold-vig-calculator-init.js, hold-vig-calculator.css,
#   hold-vig-calculator-publish.py, hold-vig-calculator-schema.php
#   ev-calculator.html, ev-calculator-init.js, ev-calculator.css,
#   ev-calculator-publish.py, ev-calculator-schema.php
#   no-vig-fair-odds-calculator.html, no-vig-fair-odds-calculator-init.js, ...

set -e
cd "$(dirname "$0")"

# Verify all expected files exist
REQUIRED=(
  hold-vig-calculator.html hold-vig-calculator-init.js hold-vig-calculator.css
  hold-vig-calculator-publish.py hold-vig-calculator-schema.php
  ev-calculator.html ev-calculator-init.js ev-calculator.css
  ev-calculator-publish.py ev-calculator-schema.php
  no-vig-fair-odds-calculator.html no-vig-fair-odds-calculator-init.js no-vig-fair-odds-calculator.css
  no-vig-fair-odds-calculator-publish.py no-vig-fair-odds-calculator-schema.php
)
for f in "${REQUIRED[@]}"; do
  if [ ! -f "$f" ]; then echo "MISSING: $f"; exit 1; fi
done
echo "All 15 agent files present."

# Stitch combined CSS — append new calculator CSS to canonical file
cat hold-vig-calculator.css ev-calculator.css no-vig-fair-odds-calculator.css >> calculators.css
echo "CSS appended."

# Stitch combined JS init functions
cat hold-vig-calculator-init.js ev-calculator-init.js no-vig-fair-odds-calculator-init.js > _new-inits-combined.js
echo "JS inits combined."

# Stitch combined PHP schema blocks
cat hold-vig-calculator-schema.php ev-calculator-schema.php no-vig-fair-odds-calculator-schema.php > _new-schema-combined.php
echo "PHP schema combined."

# 1. Reactivate snippet 38181 (page-publish endpoint) — manual step or via WP admin
echo ">>> MANUAL STEP: Reactivate WPCode snippet 38181 in WP admin before continuing."
echo ">>> Press enter once snippet 38181 is active, or Ctrl+C to abort."
read -r _

# 2. Publish each new calculator page
echo "Publishing Hold/Vig page..."
python hold-vig-calculator-publish.py
echo "Publishing EV page..."
python ev-calculator-publish.py
echo "Publishing No-Vig page..."
python no-vig-fair-odds-calculator-publish.py

# 3. Update /tools/ landing page
echo "Updating /tools/ landing page..."
python update-tools-landing.py

echo ">>> MANUAL STEP: Deactivate snippet 38181."
echo ">>> Then update snippets 38188 (JS), 38192 (CSS), 38191 (nav), and 38195 (schema) per files in this directory."
echo ">>> Press enter once all snippets are updated, or Ctrl+C to abort."
read -r _

# 4. Submit to IndexNow
echo "Submitting to IndexNow..."
curl -s -X POST "https://api.indexnow.org/indexnow" \
  -H "Content-Type: application/json" \
  -d '{
    "host": "propsbot.ai",
    "key": "01c61ffc9d2c459aac2eba939118f057",
    "keyLocation": "https://propsbot.ai/01c61ffc9d2c459aac2eba939118f057.txt",
    "urlList": [
      "https://propsbot.ai/tools/",
      "https://propsbot.ai/tools/hold-vig-calculator/",
      "https://propsbot.ai/tools/ev-calculator/",
      "https://propsbot.ai/tools/no-vig-fair-odds-calculator/"
    ]
  }' -w "\nIndexNow: HTTP %{http_code}\n"

echo "Done. Verify all 5 calculators live, then commit + push to GitHub."
