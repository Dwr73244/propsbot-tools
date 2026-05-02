// =====================================================================
// PropsBot Tools — Hold / Vig Calculator init
// Append this `initHoldVig()` function inside the existing IIFE in
// WPCode snippet 38188 (PropsBot Tools Calculator JS), and add
// `initHoldVig();` to the existing boot() call:
//
//   function boot() { initIPC(); initParlay(); initHoldVig(); }
//
// The `americanToImplied` and `impliedToAmerican` helpers below already
// exist inside `initIPC()` — they're duplicated here intentionally so
// `initHoldVig()` is self-contained and can be dropped in without
// touching the existing IPC code path. Inlining keeps the patch small
// and avoids cross-init coupling. Total added size is ~50 lines.
// =====================================================================

function initHoldVig() {
  var root = document.querySelector('.pb-vig');
  if (!root || root.__pbVigInit) return;
  root.__pbVigInit = true;

  var mount1 = root.querySelector('#pb-vig-input1-mount');
  var mount2 = root.querySelector('#pb-vig-input2-mount');
  if (!mount1 || !mount2) return;

  function makeInput(id, ariaLabelEl, placeholder) {
    var el = document.createElement('input');
    el.className = 'pb-vig__input';
    el.id = id;
    el.type = 'text';
    el.autocomplete = 'off';
    el.setAttribute('inputmode', 'text');
    el.placeholder = placeholder;
    if (ariaLabelEl) el.setAttribute('aria-labelledby', ariaLabelEl);
    return el;
  }

  var input1 = makeInput('pb-vig-input1', 'pb-vig-input1-label', '-110');
  var input2 = makeInput('pb-vig-input2', 'pb-vig-input2-label', '-110');
  // Default values so the result panel shows a usable state on load.
  input1.value = '-110';
  input2.value = '-110';
  mount1.appendChild(input1);
  mount2.appendChild(input2);

  var resultBox  = root.querySelector('#pb-vig-result');
  var holdEl     = root.querySelector('#pb-vig-hold');
  var holdSubEl  = root.querySelector('#pb-vig-hold-sub');
  var imp1El     = root.querySelector('#pb-vig-imp1');
  var imp2El     = root.querySelector('#pb-vig-imp2');
  var fairP1El   = root.querySelector('#pb-vig-fair-prob1');
  var fairP2El   = root.querySelector('#pb-vig-fair-prob2');
  var fairO1El   = root.querySelector('#pb-vig-fair-odds1');
  var fairO2El   = root.querySelector('#pb-vig-fair-odds2');
  var quickBtns  = root.querySelectorAll('.pb-vig__quick');

  // American odds → implied probability (0..1). Returns null on invalid.
  // Rejects 0 and any value strictly between -100 and +100 (inclusive of -99/+99
  // window per spec; American odds are conventionally |odds| >= 100).
  function americanToImplied(o) {
    var n = parseFloat(o);
    if (!isFinite(n) || n === 0 || (n > -100 && n < 100)) return null;
    if (n < 0) return Math.abs(n) / (Math.abs(n) + 100);
    return 100 / (n + 100);
  }

  // Implied probability (0..1) → American odds (rounded integer).
  // Returns null for non-finite or out-of-range probabilities.
  // At exactly p = 0.5 we return +100 (convention: pick-em is "+100" not "-100",
  // matches OddsJam, Pinnacle, and the spec's required -110/-110 → +100/+100 case).
  function impliedToAmerican(p) {
    if (!isFinite(p) || p <= 0 || p >= 1) return null;
    if (p === 0.5) return 100;
    if (p > 0.5) return -1 * Math.round(100 * p / (1 - p));
    return Math.round((100 - 100 * p) / p);
  }

  function fmtAmerican(a) {
    if (a === null || !isFinite(a)) return '—';
    return (a > 0 ? '+' : '') + a;
  }

  function setInvalid(msg) {
    resultBox.classList.add('pb-vig__result--invalid');
    holdEl.classList.add('pb-vig__hold-value--invalid');
    holdEl.textContent = 'Invalid odds';
    holdSubEl.textContent = msg || 'Enter American odds (e.g. -110 or +200) for both sides.';
    imp1El.textContent = '—';
    imp2El.textContent = '—';
    fairP1El.textContent = '—';
    fairP2El.textContent = '—';
    fairO1El.textContent = '—';
    fairO2El.textContent = '—';
  }

  function update() {
    var raw1 = (input1.value || '').toString().trim();
    var raw2 = (input2.value || '').toString().trim();

    // Empty input on either side → neutral "enter odds" state.
    if (!raw1 || !raw2) {
      resultBox.classList.remove('pb-vig__result--invalid');
      holdEl.classList.remove('pb-vig__hold-value--invalid');
      holdEl.textContent = '—';
      holdSubEl.textContent = 'Enter American odds for both sides of a 2-way market.';
      imp1El.textContent = '—';
      imp2El.textContent = '—';
      fairP1El.textContent = '—';
      fairP2El.textContent = '—';
      fairO1El.textContent = '—';
      fairO2El.textContent = '—';
      return;
    }

    var p1 = americanToImplied(raw1);
    var p2 = americanToImplied(raw2);
    if (p1 === null || p2 === null) {
      setInvalid('American odds must be ≤ -100 or ≥ +100. Examples: -110, +175, -200.');
      return;
    }

    var total = p1 + p2;
    if (!isFinite(total) || total <= 0) {
      setInvalid('Could not compute hold from those odds.');
      return;
    }

    var holdPct = (total - 1) * 100;
    var fairP1 = p1 / total;
    var fairP2 = p2 / total;
    var fairA1 = impliedToAmerican(fairP1);
    var fairA2 = impliedToAmerican(fairP2);

    resultBox.classList.remove('pb-vig__result--invalid');
    holdEl.classList.remove('pb-vig__hold-value--invalid');

    // Hold can be slightly negative (arb), or zero — display either cleanly.
    var holdLabel = holdPct.toFixed(2) + '%';
    holdEl.textContent = holdLabel;
    if (holdPct < -0.005) {
      holdSubEl.textContent = 'Negative hold — this 2-way market is an arbitrage on its face.';
    } else if (Math.abs(holdPct) < 0.005) {
      holdSubEl.textContent = 'Zero hold — a true no-vig market (rare outside exchanges).';
    } else if (holdPct < 3) {
      holdSubEl.textContent = 'Sharp pricing — typical of Pinnacle, Novig, or Sporttrade.';
    } else if (holdPct < 5) {
      holdSubEl.textContent = 'Standard US sportsbook hold.';
    } else {
      holdSubEl.textContent = 'High hold — shop this line at a sharper book before betting.';
    }

    imp1El.textContent = (p1 * 100).toFixed(2) + '%';
    imp2El.textContent = (p2 * 100).toFixed(2) + '%';
    fairP1El.textContent = (fairP1 * 100).toFixed(2) + '%';
    fairP2El.textContent = (fairP2 * 100).toFixed(2) + '%';
    fairO1El.textContent = fmtAmerican(fairA1);
    fairO2El.textContent = fmtAmerican(fairA2);
  }

  input1.addEventListener('input', update);
  input2.addEventListener('input', update);

  quickBtns.forEach(function(btn) {
    btn.addEventListener('click', function() {
      var s1 = btn.getAttribute('data-side1');
      var s2 = btn.getAttribute('data-side2');
      if (s1) input1.value = s1;
      if (s2) input2.value = s2;
      update();
      input1.focus();
    });
  });

  update();
}

// In the existing snippet 38188 IIFE, add `initHoldVig();` to boot():
//   function boot() { initIPC(); initParlay(); initHoldVig(); }
