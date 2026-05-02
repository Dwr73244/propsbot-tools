// PropsBot Nav: Inject calculator links into the "Props Tools" section of the
// accordion menu. The base menu lives in WPCode snippet 37813. This snippet
// injects new links at runtime — works for both desktop and mobile (single
// hamburger UI at #pb-nav-overlay).
//
// Updated to include all 5 calculators after Hold/Vig + EV + No-Vig launch.

(function() {
  function inject() {
    var overlay = document.querySelector('#pb-nav-overlay');
    if (!overlay) return false;
    if (overlay.__pbToolsInjected) return true;

    var labels = overlay.querySelectorAll('.pb-sec-label');
    var propsToolsLabel = null;
    for (var i = 0; i < labels.length; i++) {
      if (labels[i].textContent.trim() === 'Props Tools') {
        propsToolsLabel = labels[i];
        break;
      }
    }
    if (!propsToolsLabel) return false;

    var secHdr = propsToolsLabel.closest('.pb-sec-hdr');
    if (!secHdr) return false;
    var linksContainer = secHdr.nextElementSibling;
    while (linksContainer && !linksContainer.classList.contains('pb-nav-links')) {
      linksContainer = linksContainer.nextElementSibling;
    }
    if (!linksContainer) return false;

    var existingLink = linksContainer.querySelector('a');
    if (!existingLink) return false;
    var linkClass = existingLink.className || '';
    var existingArrow = existingLink.querySelector('.pb-lnk-arr');
    var arrowClass = existingArrow ? existingArrow.className : 'pb-lnk-arr';
    var arrowText = existingArrow ? existingArrow.textContent : '›';

    var toolsToAdd = [
      { href: '/tools/implied-probability-calculator/',  label: 'Implied Probability Calculator' },
      { href: '/tools/parlay-calculator/',                label: 'Parlay Calculator' },
      { href: '/tools/hold-vig-calculator/',              label: 'Hold & Vig Calculator' },
      { href: '/tools/ev-calculator/',                    label: 'Expected Value Calculator' },
      { href: '/tools/no-vig-fair-odds-calculator/',      label: 'No-Vig Fair Odds Calculator' },
      { href: '/tools/',                                   label: 'All Free Tools' }
    ];

    var existingHrefs = {};
    linksContainer.querySelectorAll('a').forEach(function(a) {
      try { existingHrefs[new URL(a.href).pathname] = true; } catch(e) {}
    });

    toolsToAdd.forEach(function(tool) {
      if (existingHrefs[tool.href]) return;
      var a = document.createElement('a');
      a.href = tool.href;
      if (linkClass) a.className = linkClass;
      var labelSpan = document.createElement('span');
      labelSpan.textContent = tool.label;
      var arrSpan = document.createElement('span');
      arrSpan.className = arrowClass;
      arrSpan.textContent = arrowText;
      a.appendChild(labelSpan);
      a.appendChild(arrSpan);
      linksContainer.appendChild(a);
    });

    overlay.__pbToolsInjected = true;
    return true;
  }

  function boot() {
    if (inject()) return;
    var tries = 0;
    var iv = setInterval(function() {
      tries++;
      if (inject() || tries > 20) clearInterval(iv);
    }, 250);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', boot);
  } else {
    boot();
  }
})();
