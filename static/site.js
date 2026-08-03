/* TechShield Tools shared engine — finance math, formatting, and a dependency-free chart.
   All money math lives here so it's consistent and testable. */
(function (root) {
  "use strict";

  // ---------- parsing & formatting ----------
  function num(v) {
    if (v === null || v === undefined) return NaN;
    var n = parseFloat(String(v).replace(/[^0-9.\-]/g, ""));
    return isFinite(n) ? n : NaN;
  }
  function clamp(x, lo, hi) { return Math.min(Math.max(x, lo), hi); }

  function money(x, cur) {
    cur = cur || "$";
    if (!isFinite(x)) return "—";
    var neg = x < 0; x = Math.abs(x);
    return (neg ? "-" : "") + cur + x.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });
  }
  function money0(x, cur) {
    cur = cur || "$";
    if (!isFinite(x)) return "—";
    var neg = x < 0; x = Math.abs(x);
    return (neg ? "-" : "") + cur + Math.round(x).toLocaleString("en-US");
  }
  function pct(x, dp) { dp = dp == null ? 2 : dp; return isFinite(x) ? x.toFixed(dp) + "%" : "—"; }
  function nfmt(x, dp) { dp = dp == null ? 2 : dp; return isFinite(x) ? x.toLocaleString("en-US", { maximumFractionDigits: dp }) : "—"; }


  // Sync a number input with a range slider (painted fill) — used by widget-style calculators.
  function bindRange(numId, rngId, recalc) {
    var n = el(numId), r = el(rngId);
    if (!n || !r) return;
    function paint() {
      var min = num(r.min) || 0, max = num(r.max) || 100, v = num(r.value) || 0;
      var f = max > min ? ((v - min) / (max - min)) * 100 : 0;
      r.style.setProperty("--fill", clamp(f, 0, 100) + "%");
    }
    r.addEventListener("input", function () { n.value = r.value; paint(); if (recalc) recalc(); });
    n.addEventListener("input", function () {
      var v = num(n.value);
      if (isFinite(v)) r.value = clamp(v, num(r.min), num(r.max));
      paint();
    });
    paint();
  }

  // ---------- core finance ----------
  // Monthly payment for a fully-amortizing loan.
  function pmt(principal, annualRatePct, months) {
    var r = annualRatePct / 100 / 12;
    if (months <= 0) return 0;
    if (r === 0) return principal / months;
    return principal * r * Math.pow(1 + r, months) / (Math.pow(1 + r, months) - 1);
  }

  // Full amortization schedule, supporting an optional extra monthly payment.
  function amortize(principal, annualRatePct, months, extra) {
    extra = extra || 0;
    var r = annualRatePct / 100 / 12;
    var basePay = pmt(principal, annualRatePct, months);
    var bal = principal, totalInterest = 0, totalPaid = 0, n = 0;
    var schedule = [];
    var cap = months * 4 + 1200;
    while (bal > 0.005 && n < cap) {
      n++;
      var interest = bal * r;
      var princ = basePay + extra - interest;
      if (princ <= 0) {
        return { payment: basePay, months: Infinity, totalInterest: Infinity, totalPaid: Infinity, schedule: [], neverPayoff: true };
      }
      if (princ > bal) princ = bal;
      bal -= princ;
      var pay = princ + interest;
      totalInterest += interest; totalPaid += pay;
      schedule.push({ n: n, interest: interest, principal: princ, balance: Math.max(bal, 0), payment: pay });
    }
    return { payment: basePay, months: n, totalInterest: totalInterest, totalPaid: totalPaid, schedule: schedule, neverPayoff: false };
  }

  // Loan principal supported by a given monthly payment (inverse of pmt).
  function principalFromPayment(pay, annualRatePct, months) {
    var r = annualRatePct / 100 / 12;
    if (months <= 0 || pay <= 0) return 0;
    if (r === 0) return pay * months;
    return pay * (Math.pow(1 + r, months) - 1) / (r * Math.pow(1 + r, months));
  }

  // Future value of a lump sum plus recurring contributions (end-of-period).
  function futureValue(principal, contribution, ratePerPeriod, periods) {
    var r = ratePerPeriod;
    if (r === 0) return principal + contribution * periods;
    return principal * Math.pow(1 + r, periods) + contribution * ((Math.pow(1 + r, periods) - 1) / r);
  }

  // Contribution needed each period to reach a target future value.
  function contributionFor(target, principal, ratePerPeriod, periods) {
    var r = ratePerPeriod;
    var fromPrincipal = principal * Math.pow(1 + r, periods);
    var need = target - fromPrincipal;
    if (periods <= 0) return need;
    if (r === 0) return need / periods;
    return need / ((Math.pow(1 + r, periods) - 1) / r);
  }

  // ---------- chart: dependency-free SVG donut ----------
  // segments: [{label, value, color}]
  function donut(segments, opts) {
    opts = opts || {};
    var size = opts.size || 180, sw = opts.stroke || 26, cx = size / 2, cy = size / 2;
    var r = (size - sw) / 2 - 2, circ = 2 * Math.PI * r;
    var total = segments.reduce(function (a, s) { return a + (s.value > 0 ? s.value : 0); }, 0);
    var svg = '<svg viewBox="0 0 ' + size + ' ' + size + '" class="donut" role="img" aria-hidden="true">';
    svg += '<circle cx="' + cx + '" cy="' + cy + '" r="' + r + '" fill="none" stroke="var(--line)" stroke-width="' + sw + '"/>';
    if (total > 0) {
      var offset = 0;
      segments.forEach(function (s) {
        var v = s.value > 0 ? s.value : 0;
        var len = circ * (v / total);
        svg += '<circle cx="' + cx + '" cy="' + cy + '" r="' + r + '" fill="none" stroke="' + s.color +
          '" stroke-width="' + sw + '" stroke-dasharray="' + len + ' ' + (circ - len) +
          '" stroke-dashoffset="' + (-offset) + '" transform="rotate(-90 ' + cx + ' ' + cy + ')"/>';
        offset += len;
      });
    }
    svg += "</svg>";
    return svg;
  }

  function legend(segments, cur) {
    var total = segments.reduce(function (a, s) { return a + (s.value > 0 ? s.value : 0); }, 0);
    return '<ul class="legend">' + segments.map(function (s) {
      var p = total > 0 ? (s.value / total * 100) : 0;
      return '<li><span class="swatch" style="background:' + s.color + '"></span>' +
        '<span class="lg-label">' + s.label + '</span>' +
        '<span class="lg-val">' + money0(s.value, cur) + " <em>(" + p.toFixed(0) + "%)</em></span></li>";
    }).join("") + "</ul>";
  }

  // ---------- small helpers used by pages ----------
  function el(id) { return document.getElementById(id); }
  function on(ids, fn) {
    ids.forEach(function (id) {
      var e = el(id); if (!e) return;
      e.addEventListener("input", fn); e.addEventListener("change", fn);
    });
  }

  root.FIN = {
    num: num, clamp: clamp, money: money, money0: money0, pct: pct, nfmt: nfmt,
    pmt: pmt, amortize: amortize, principalFromPayment: principalFromPayment,
    futureValue: futureValue, contributionFor: contributionFor,
    donut: donut, legend: legend, el: el, on: on, bindRange: bindRange,
    C: { blue: "#2563eb", green: "#16a34a", amber: "#f59e0b", red: "#dc2626", violet: "#7c3aed", slate: "#64748b" }
  };
})(window);


/* ---------- site-wide widget enhancer: auto-sliders, result hero, CTA ---------- */
(function () {
  "use strict";
  function ready(fn) {
    if (document.readyState !== "loading") fn();
    else document.addEventListener("DOMContentLoaded", fn);
  }
  ready(function () {
    var F = window.FIN; if (!F) return;

    // ---- 1. auto-sliders under every numeric input in the inputs panel ----
    function niceCeil(x) {
      if (!(x > 0)) return 10;
      var p = Math.pow(10, Math.floor(Math.log(x) / Math.LN10));
      var m = x / p;
      var n = m <= 1 ? 1 : m <= 2 ? 2 : m <= 5 ? 5 : 10;
      return n * p;
    }
    function fmtScale(v, pre, suf) {
      var s = Math.abs(v) >= 1000 ? v.toLocaleString("en-US") : String(v);
      var sf = suf || ""; if (sf.length > 1) sf = " " + sf;
      return (pre || "") + s + sf;
    }
    var panel = document.querySelector(".calc-wrap .panel");
    if (panel) {
      var inputs = panel.querySelectorAll("input[type=number]");
      Array.prototype.forEach.call(inputs, function (inp) {
        if (inp.closest(".sfield") || inp.dataset.noslider) return;
        var v = F.num(inp.value); if (!isFinite(v)) v = 0;
        var min = inp.min !== "" ? F.num(inp.min) : 0;
        var max = inp.max !== "" ? F.num(inp.max) : niceCeil((Math.abs(v) || 10) * 5);
        if (!(max > min)) max = min + 10;
        var step = (inp.step && inp.step !== "any") ? F.num(inp.step) : 1;
        var wrap = inp.closest(".inp") || inp;
        var pre = "", suf = "";
        var preEl = inp.closest(".inp") && inp.closest(".inp").querySelector(".pre");
        var sufEl = inp.closest(".inp") && inp.closest(".inp").querySelector(".suf");
        if (preEl) pre = preEl.textContent.trim();
        if (sufEl) suf = sufEl.textContent.trim();
        var r = document.createElement("input");
        r.type = "range"; r.className = "sl auto-sl";
        r.min = min; r.max = max; r.step = step;
        r.value = Math.min(Math.max(v, min), max);
        r.setAttribute("aria-hidden", "true"); r.tabIndex = -1;
        var scale = document.createElement("div");
        scale.className = "sl-scale";
        scale.innerHTML = "<span>" + fmtScale(min, pre, suf) + "</span><span>" + fmtScale(max, pre, suf) + "</span>";
        wrap.parentNode.insertBefore(r, wrap.nextSibling);
        r.parentNode.insertBefore(scale, r.nextSibling);
        function paint() {
          var f = ((F.num(r.value) - min) / (max - min)) * 100;
          r.style.setProperty("--fill", F.clamp(f, 0, 100) + "%");
        }
        r.addEventListener("input", function () {
          inp.value = r.value; paint();
          inp.dispatchEvent(new Event("input", { bubbles: true }));
        });
        inp.addEventListener("input", function () {
          var nv = F.num(inp.value);
          if (isFinite(nv)) r.value = F.clamp(nv, min, max);
          paint();
        });
        paint();
      });
    }

    // ---- 2. result hero + CTA on every calculator render ----
    var out = document.getElementById("out");
    if (!out) return;
    function heroize() {
      var first = out.firstElementChild;
      if (first && first.classList.contains("sub") &&
          first.nextElementSibling && first.nextElementSibling.classList.contains("big-num") &&
          !out.querySelector(":scope > .res-hero")) {
        var big = first.nextElementSibling;
        var hero = document.createElement("div");
        hero.className = "res-hero";
        out.insertBefore(hero, first);
        hero.appendChild(first); hero.appendChild(big);
      }
      if (out.querySelector(".big-num, .res-big") && !out.querySelector(".res-cta")) {
        var cta = document.createElement("div");
        cta.className = "res-cta";
        cta.innerHTML = "<h3>Keep planning</h3><p>Try our other free money and everyday tools \u2014 no sign-up needed.</p>" +
          "<a class=\"btn block\" href=\"/all/\">Explore All Calculators</a>";
        out.appendChild(cta);
      }
    }
    new MutationObserver(heroize).observe(out, { childList: true });
    heroize();
  });
})();
