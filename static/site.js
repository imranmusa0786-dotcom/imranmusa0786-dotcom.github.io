/* CalcHub shared engine — finance math, formatting, and a dependency-free chart.
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
    pmt: pmt, amortize: amortize, futureValue: futureValue, contributionFor: contributionFor,
    donut: donut, legend: legend, el: el, on: on,
    C: { blue: "#2563eb", green: "#16a34a", amber: "#f59e0b", red: "#dc2626", violet: "#7c3aed", slate: "#64748b" }
  };
})(window);
