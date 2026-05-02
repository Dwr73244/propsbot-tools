/* PropsBot Tools — Expected Value (EV) Calculator init
 * Append this function inside the IIFE in WPCode snippet 38188 (PropsBot Tools
 * Calculator JS), alongside initIPC() and initParlay(), and call it from boot().
 *
 * Pattern matches initIPC / initParlay:
 *   - Idempotent guard (root.__pbEvInit)
 *   - Inputs created programmatically (WP strips <input> from post content)
 *   - All numeric output uses --pb-mono via CSS classes
 *   - aria-live result region
 */
function initEV() {
  var root = document.querySelector('.pb-ev');
  if (!root || root.__pbEvInit) return;
  root.__pbEvInit = true;

  var oddsMount = root.querySelector('#pb-ev-odds-mount');
  var probMount = root.querySelector('#pb-ev-prob-mount');
  var betMount = root.querySelector('#pb-ev-bet-mount');
  if (!oddsMount || !probMount || !betMount) return;

  var oddsInput = document.createElement('input');
  oddsInput.className = 'pb-ev__input';
  oddsInput.id = 'pb-ev-odds';
  oddsInput.type = 'text';
  oddsInput.autocomplete = 'off';
  oddsInput.setAttribute('inputmode', 'text');
  oddsInput.placeholder = '+150';
  oddsInput.value = '+150';
  oddsMount.appendChild(oddsInput);

  var probInput = document.createElement('input');
  probInput.className = 'pb-ev__input pb-ev__input--with-suffix';
  probInput.id = 'pb-ev-prob';
  probInput.type = 'text';
  probInput.autocomplete = 'off';
  probInput.setAttribute('inputmode', 'decimal');
  probInput.placeholder = '50';
  probInput.value = '50';
  probMount.appendChild(probInput);

  var betInput = document.createElement('input');
  betInput.className = 'pb-ev__input pb-ev__input--with-prefix';
  betInput.id = 'pb-ev-bet';
  betInput.type = 'text';
  betInput.autocomplete = 'off';
  betInput.setAttribute('inputmode', 'decimal');
  betInput.placeholder = '100';
  betInput.value = '100';
  betMount.appendChild(betInput);

  var resultBox = root.querySelector('#pb-ev-result');
  var verdictEl = root.querySelector('#pb-ev-verdict');
  var dollarsEl = root.querySelector('#pb-ev-dollars');
  var pctEl = root.querySelector('#pb-ev-pct');
  var edgeEl = root.querySelector('#pb-ev-edge');
  var impliedEl = root.querySelector('#pb-ev-implied');
  var longrunEl = root.querySelector('#pb-ev-longrun');

  // Validators per spec:
  //   reject odds in (-99, +99)  (inclusive of -99..+99 exclusive of -100/+100)
  //   reject true_prob outside (0, 100)
  //   reject bet <= 0
  function parseOdds(raw) {
    var n = parseFloat(raw);
    if (!isFinite(n) || n === 0) return null;
    if (n > -100 && n < 100) return null;
    return n;
  }
  function parseProb(raw) {
    var n = parseFloat(raw);
    if (!isFinite(n)) return null;
    if (n <= 0 || n >= 100) return null;
    return n;
  }
  function parseBet(raw) {
    var n = parseFloat(raw);
    if (!isFinite(n) || n <= 0) return null;
    return n;
  }

  // profit_if_win:
  //   negative American: bet * 100 / |odds|
  //   positive American: bet * odds / 100
  function profitIfWin(odds, bet) {
    if (odds < 0) return bet * 100 / Math.abs(odds);
    return bet * odds / 100;
  }

  // Implied probability from American odds (returns 0..1)
  function impliedFromAmerican(odds) {
    if (odds < 0) return Math.abs(odds) / (Math.abs(odds) + 100);
    return 100 / (odds + 100);
  }

  function fmtDollars(v) {
    var sign = v >= 0 ? '+' : '-';
    return sign + '$' + Math.abs(v).toFixed(2);
  }
  function fmtPct(v) {
    var sign = v >= 0 ? '+' : '';
    return sign + v.toFixed(2) + '%';
  }

  function setInvalid(msg) {
    resultBox.classList.remove('pb-ev__result--positive');
    resultBox.classList.remove('pb-ev__result--negative');
    resultBox.classList.remove('pb-ev__result--breakeven');
    resultBox.classList.add('pb-ev__result--invalid');
    verdictEl.classList.remove('pb-ev__verdict--positive');
    verdictEl.classList.remove('pb-ev__verdict--negative');
    verdictEl.classList.remove('pb-ev__verdict--breakeven');
    verdictEl.classList.add('pb-ev__verdict--invalid');
    verdictEl.textContent = msg;
    dollarsEl.textContent = '—';
    dollarsEl.classList.remove('pb-ev__metric-value--positive');
    dollarsEl.classList.remove('pb-ev__metric-value--negative');
    pctEl.textContent = 'EV%: —';
    edgeEl.textContent = '—';
    edgeEl.classList.remove('pb-ev__metric-value--positive');
    edgeEl.classList.remove('pb-ev__metric-value--negative');
    impliedEl.textContent = 'Book implied: —';
    longrunEl.textContent = 'Long-run expected return on $1,000 of bets at this edge: —';
  }

  function update() {
    var odds = parseOdds(oddsInput.value);
    var probPct = parseProb(probInput.value);
    var bet = parseBet(betInput.value);

    if (odds === null) { setInvalid('Enter valid American odds (e.g. -110, +200).'); return; }
    if (probPct === null) { setInvalid('Enter true probability between 0 and 100.'); return; }
    if (bet === null) { setInvalid('Enter a positive bet amount.'); return; }

    var trueProb = probPct / 100;                      // 0..1
    var implied = impliedFromAmerican(odds);           // 0..1
    var profit = profitIfWin(odds, bet);
    var ev = (trueProb * profit) - ((1 - trueProb) * bet);
    var evPct = (ev / bet) * 100;
    var edgePct = probPct - (implied * 100);
    var longrun = (ev / bet) * 1000;

    // Reset class state
    resultBox.classList.remove('pb-ev__result--invalid');
    resultBox.classList.remove('pb-ev__result--positive');
    resultBox.classList.remove('pb-ev__result--negative');
    resultBox.classList.remove('pb-ev__result--breakeven');
    verdictEl.classList.remove('pb-ev__verdict--invalid');
    verdictEl.classList.remove('pb-ev__verdict--positive');
    verdictEl.classList.remove('pb-ev__verdict--negative');
    verdictEl.classList.remove('pb-ev__verdict--breakeven');
    dollarsEl.classList.remove('pb-ev__metric-value--positive');
    dollarsEl.classList.remove('pb-ev__metric-value--negative');
    edgeEl.classList.remove('pb-ev__metric-value--positive');
    edgeEl.classList.remove('pb-ev__metric-value--negative');

    // Treat near-zero EV (|ev| < 0.005 → less than half a cent) as break-even
    if (Math.abs(ev) < 0.005) {
      resultBox.classList.add('pb-ev__result--breakeven');
      verdictEl.classList.add('pb-ev__verdict--breakeven');
      verdictEl.textContent = 'Break-even';
    } else if (ev > 0) {
      resultBox.classList.add('pb-ev__result--positive');
      verdictEl.classList.add('pb-ev__verdict--positive');
      verdictEl.textContent = '+EV (place bet)';
      dollarsEl.classList.add('pb-ev__metric-value--positive');
      edgeEl.classList.add('pb-ev__metric-value--positive');
    } else {
      resultBox.classList.add('pb-ev__result--negative');
      verdictEl.classList.add('pb-ev__verdict--negative');
      verdictEl.textContent = '−EV (skip)';
      dollarsEl.classList.add('pb-ev__metric-value--negative');
      edgeEl.classList.add('pb-ev__metric-value--negative');
    }

    dollarsEl.textContent = fmtDollars(ev);
    pctEl.textContent = 'EV%: ' + fmtPct(evPct);
    edgeEl.textContent = fmtPct(edgePct);
    impliedEl.textContent = 'Book implied: ' + (implied * 100).toFixed(2) + '%';
    longrunEl.textContent = 'Long-run expected return on $1,000 of bets at this edge: ' + fmtDollars(longrun);
  }

  oddsInput.addEventListener('input', update);
  probInput.addEventListener('input', update);
  betInput.addEventListener('input', update);

  update();
}
