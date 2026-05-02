// PropsBot Tools — No-Vig Fair Odds Calculator init
// Append this function to WPCode snippet 38188 (PropsBot Tools Calculator JS)
// alongside initIPC and initParlay. Then append `initNoVig();` to the boot()
// call so it runs on page load. Idempotent: safe if root not present.
//
// Inputs are created programmatically because WordPress strips <input> elements
// from post content. CSS lives in WPCode snippet 38192 because wptexturize
// corrupts CSS variables (-- → en-dash) inside post content.
function initNoVig() {
  var root = document.querySelector('.pb-novig');
  if (!root || root.__pbNoVigInit) return;
  root.__pbNoVigInit = true;

  var mount1 = root.querySelector('#pb-novig-input1-mount');
  var mount2 = root.querySelector('#pb-novig-input2-mount');
  if (!mount1 || !mount2) return;

  var input1 = document.createElement('input');
  input1.className = 'pb-novig__input';
  input1.id = 'pb-novig-input1';
  input1.type = 'text';
  input1.autocomplete = 'off';
  input1.setAttribute('inputmode', 'text');
  input1.setAttribute('aria-label', 'Side 1 American odds');
  input1.placeholder = '-110';
  input1.value = '-110';
  mount1.appendChild(input1);

  var input2 = document.createElement('input');
  input2.className = 'pb-novig__input';
  input2.id = 'pb-novig-input2';
  input2.type = 'text';
  input2.autocomplete = 'off';
  input2.setAttribute('inputmode', 'text');
  input2.setAttribute('aria-label', 'Side 2 American odds');
  input2.placeholder = '-110';
  input2.value = '-110';
  mount2.appendChild(input2);

  var quickButtons = root.querySelectorAll('.pb-novig__quick');
  var resultBox = root.querySelector('#pb-novig-result');
  var holdEl = root.querySelector('#pb-novig-hold');
  var subEl = root.querySelector('#pb-novig-sub');
  var side1ProbEl = root.querySelector('#pb-novig-side1-prob');
  var side2ProbEl = root.querySelector('#pb-novig-side2-prob');
  var side1AmerEl = root.querySelector('#pb-novig-side1-american');
  var side2AmerEl = root.querySelector('#pb-novig-side2-american');
  var side1DecEl = root.querySelector('#pb-novig-side1-decimal');
  var side2DecEl = root.querySelector('#pb-novig-side2-decimal');

  function americanToImplied(o) {
    var n = parseFloat(o);
    if (!isFinite(n) || n === 0 || (n > -100 && n < 100)) return null;
    if (n < 0) return Math.abs(n) / (Math.abs(n) + 100);
    return 100 / (n + 100);
  }

  function impliedToAmerican(p) {
    if (!isFinite(p) || p <= 0 || p >= 1) return null;
    // Convention: at exactly 50% (or numerically equivalent), use +100
    // because most US sportsbooks display +100 rather than -100 for evens.
    if (Math.abs(p - 0.5) < 1e-9) return 100;
    if (p > 0.5) return -1 * Math.round(100 * p / (1 - p));
    return Math.round((100 - 100 * p) / p);
  }

  function fmtAmerican(a) {
    if (a === null || !isFinite(a)) return '—';
    return (a > 0 ? '+' : '') + a;
  }

  function setInvalid(message) {
    resultBox.classList.add('pb-novig__result--invalid');
    side1ProbEl.textContent = '—';
    side2ProbEl.textContent = '—';
    side1AmerEl.textContent = '—';
    side2AmerEl.textContent = '—';
    side1DecEl.textContent = '— decimal';
    side2DecEl.textContent = '— decimal';
    holdEl.textContent = 'Hold removed: —';
    holdEl.classList.add('pb-novig__hold-pill--invalid');
    subEl.textContent = message;
  }

  function update() {
    var raw1 = (input1.value || '').toString().trim();
    var raw2 = (input2.value || '').toString().trim();

    if (!raw1 || !raw2) {
      resultBox.classList.remove('pb-novig__result--invalid');
      holdEl.classList.remove('pb-novig__hold-pill--invalid');
      side1ProbEl.textContent = '—';
      side2ProbEl.textContent = '—';
      side1AmerEl.textContent = '—';
      side2AmerEl.textContent = '—';
      side1DecEl.textContent = '— decimal';
      side2DecEl.textContent = '— decimal';
      holdEl.textContent = 'Hold removed: —';
      subEl.textContent = 'Enter American odds for both sides above to see the no-vig fair price.';
      return;
    }

    var imp1 = americanToImplied(raw1);
    var imp2 = americanToImplied(raw2);
    if (imp1 === null) { setInvalid('Side 1 odds are invalid. Use values like -150 or +200 (not between -99 and +99).'); return; }
    if (imp2 === null) { setInvalid('Side 2 odds are invalid. Use values like -150 or +200 (not between -99 and +99).'); return; }

    var total = imp1 + imp2;
    if (!isFinite(total) || total <= 0) { setInvalid('Could not compute no-vig odds from the provided values.'); return; }

    var fair1 = imp1 / total;
    var fair2 = imp2 / total;
    var holdPct = (total - 1) * 100;

    var amer1 = impliedToAmerican(fair1);
    var amer2 = impliedToAmerican(fair2);
    var dec1 = 1 / fair1;
    var dec2 = 1 / fair2;

    resultBox.classList.remove('pb-novig__result--invalid');
    holdEl.classList.remove('pb-novig__hold-pill--invalid');
    side1ProbEl.textContent = (fair1 * 100).toFixed(2) + '%';
    side2ProbEl.textContent = (fair2 * 100).toFixed(2) + '%';
    side1AmerEl.textContent = fmtAmerican(amer1) + ' American';
    side2AmerEl.textContent = fmtAmerican(amer2) + ' American';
    side1DecEl.textContent = dec1.toFixed(2) + ' decimal';
    side2DecEl.textContent = dec2.toFixed(2) + ' decimal';

    if (holdPct < 0.005) {
      holdEl.textContent = 'Market is already no-vig (0.00% hold)';
    } else {
      holdEl.textContent = 'Hold removed: ' + holdPct.toFixed(2) + '%';
    }
    subEl.textContent = 'Fair price assumes the book’s margin is split evenly across both sides. Compare these to your model’s true probability — if your estimate beats the no-vig probability on a side, that side has +EV.';
  }

  input1.addEventListener('input', update);
  input2.addEventListener('input', update);

  quickButtons.forEach(function(b) {
    b.addEventListener('click', function() {
      input1.value = b.getAttribute('data-preset1');
      input2.value = b.getAttribute('data-preset2');
      update();
    });
  });

  update();
}
