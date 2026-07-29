# -*- coding: utf-8 -*-
"""Tool definitions for CalcHub. Each tool is fully self-contained:
UI (body_html), inline calculator logic (script_js), SEO copy and FAQs.
Phase 2/3 tools slot in by appending dicts to TOOLS."""

RESULTS = '<div id="out"><p class="sub">Enter values above to see your results.</p></div>'

TOOLS = []

# ============================ FINANCE ============================

TOOLS.append({
 "slug":"mortgage-calculator","cat":"finance","icon":"🏠",
 "name":"Mortgage Calculator",
 "short":"Estimate your monthly home loan payment, taxes, insurance and total interest.",
 "lede":"Estimate your full monthly mortgage payment — principal, interest, property tax, insurance and HOA — plus total interest and a year-by-year payoff schedule.",
 "title":"Mortgage Calculator — Monthly Payment, Interest & Amortization",
 "desc":"Free mortgage calculator: estimate your monthly payment (PITI), total interest, and full amortization schedule. Include down payment, property tax, insurance and HOA.",
 "keywords":"mortgage calculator, monthly mortgage payment, home loan calculator, amortization",
 "body_html":"""
  <div class="field"><label for="m_price">Home price</label>
    <div class="inp has-pre"><span class="pre">$</span><input id="m_price" type="number" value="400000" min="0" step="1000"></div></div>
  <div class="row2">
    <div class="field"><label for="m_down">Down payment</label>
      <div class="inp has-pre"><span class="pre">$</span><input id="m_down" type="number" value="80000" min="0" step="1000"></div></div>
    <div class="field"><label for="m_term">Loan term <span class="hint">(years)</span></label>
      <input id="m_term" type="number" value="30" min="1" max="40" step="1"></div>
  </div>
  <div class="field"><label for="m_rate">Interest rate (APR)</label>
    <div class="inp has-suf"><input id="m_rate" type="number" value="6.5" min="0" step="0.01"><span class="suf">%</span></div></div>
  <p class="sub" style="margin:18px 0 8px;font-weight:600;color:#334155">Optional monthly costs</p>
  <div class="row2">
    <div class="field"><label for="m_tax">Property tax <span class="hint">(/yr)</span></label>
      <div class="inp has-pre"><span class="pre">$</span><input id="m_tax" type="number" value="4800" min="0" step="100"></div></div>
    <div class="field"><label for="m_ins">Home insurance <span class="hint">(/yr)</span></label>
      <div class="inp has-pre"><span class="pre">$</span><input id="m_ins" type="number" value="1800" min="0" step="100"></div></div>
  </div>
  <div class="field"><label for="m_hoa">HOA fees <span class="hint">(/mo)</span></label>
    <div class="inp has-pre"><span class="pre">$</span><input id="m_hoa" type="number" value="0" min="0" step="10"></div></div>
 """,
 "script_js":"""
 document.addEventListener('DOMContentLoaded',function(){var F=window.FIN;
  var ids=['m_price','m_down','m_rate','m_term','m_tax','m_ins','m_hoa'];
  function calc(){
   var price=F.num(F.el('m_price').value)||0,down=F.num(F.el('m_down').value)||0,
       rate=F.num(F.el('m_rate').value)||0,term=F.num(F.el('m_term').value)||0,
       tax=F.num(F.el('m_tax').value)||0,ins=F.num(F.el('m_ins').value)||0,hoa=F.num(F.el('m_hoa').value)||0;
   var loan=Math.max(price-down,0),months=Math.round(term*12),out=F.el('out');
   if(!(months>0)||loan<=0){out.innerHTML='<p class="sub">Enter a home price above the down payment and a loan term to see your payment.</p>';return;}
   var pi=F.pmt(loan,rate,months),mTax=tax/12,mIns=ins/12,total=pi+mTax+mIns+hoa;
   var am=F.amortize(loan,rate,months);
   var segs=[{label:'Principal & interest',value:pi,color:F.C.blue},{label:'Property tax',value:mTax,color:F.C.green},{label:'Home insurance',value:mIns,color:F.C.amber},{label:'HOA',value:hoa,color:F.C.violet}];
   var rows='',pP=0,pI=0,yr=0;
   am.schedule.forEach(function(s,i){pP+=s.principal;pI+=s.interest;if((i+1)%12===0||i===am.schedule.length-1){yr++;rows+='<tr><td>'+yr+'</td><td>'+F.money0(pP)+'</td><td>'+F.money0(pI)+'</td><td>'+F.money0(s.balance)+'</td></tr>';pP=0;pI=0;}});
   out.innerHTML='<div class="sub">Estimated monthly payment</div><div class="big-num">'+F.money0(total)+'</div>'+
    '<div class="chart-row">'+F.donut(segs)+F.legend(segs)+'</div>'+
    '<div class="stats"><div class="stat"><div class="k">Loan amount</div><div class="v">'+F.money0(loan)+'</div></div>'+
    '<div class="stat"><div class="k">Total interest</div><div class="v">'+F.money0(am.totalInterest)+'</div></div>'+
    '<div class="stat"><div class="k">Principal &amp; interest</div><div class="v">'+F.money0(pi)+'/mo</div></div>'+
    '<div class="stat"><div class="k">Total of payments</div><div class="v">'+F.money0(pi*am.months)+'</div></div></div>'+
    '<div class="tbl-wrap"><table><thead><tr><th>Year</th><th>Principal</th><th>Interest</th><th>Balance</th></tr></thead><tbody>'+rows+'</tbody></table></div>';
  }
  F.on(ids,calc);calc();
 });
 """,
 "intro_html":"""
  <h2>How the mortgage calculator works</h2>
  <p>Your monthly mortgage payment has two core parts — <strong>principal</strong> (the loan balance you pay down) and <strong>interest</strong> (the cost of borrowing) — often shown together as “P&amp;I”. Lenders usually also collect <strong>property tax</strong> and <strong>homeowners insurance</strong> monthly, and this is called your <strong>PITI</strong> payment. This calculator adds optional tax, insurance and HOA on top of P&amp;I so you see the true monthly cost.</p>
  <h3>The formula</h3>
  <p>Monthly principal &amp; interest is calculated with the standard amortization formula: <code>M = P · r · (1+r)ⁿ / ((1+r)ⁿ − 1)</code>, where <code>P</code> is the loan amount, <code>r</code> is the monthly interest rate (annual rate ÷ 12), and <code>n</code> is the number of monthly payments (years × 12).</p>
  <h3>Tips to lower your payment</h3>
  <p>A larger down payment reduces the loan amount and can remove private mortgage insurance. A lower interest rate or a longer term reduces the monthly payment (though a longer term means more total interest). Use the year-by-year table to see how much faster you build equity over time.</p>
 """,
 "faqs":[
  {"q":"What is included in a monthly mortgage payment?","a":"Principal, interest, and usually property taxes and homeowners insurance (together called PITI). If you have a condo or planned community you may also pay HOA dues. This calculator lets you include all of them."},
  {"q":"How much house can I afford?","a":"A common guideline is that your total monthly housing payment stays under about 28% of your gross monthly income, and total debts under about 36%. Try different home prices and down payments here to find a comfortable payment."},
  {"q":"Does a bigger down payment reduce my payment?","a":"Yes. A larger down payment lowers the loan amount, which lowers both your monthly principal &amp; interest and the total interest paid. Putting down 20% or more also typically removes the need for private mortgage insurance (PMI)."},
  {"q":"Is this the same as what a lender will quote?","a":"It's a close estimate for planning. Actual quotes depend on your credit, loan type, PMI, points, and exact tax and insurance figures, so treat this as a guide rather than an official offer."},
 ],
})

TOOLS.append({
 "slug":"loan-calculator","cat":"finance","icon":"🧾",
 "name":"Loan Calculator",
 "short":"Work out the monthly payment and total interest on any personal or fixed loan.",
 "lede":"Calculate the monthly payment, total interest and payoff schedule for any fixed-rate loan — personal loans, student loans, or anything with a set rate and term.",
 "title":"Loan Calculator — Monthly Payment & Total Interest",
 "desc":"Free loan calculator: find your monthly payment, total interest and amortization schedule for any fixed-rate personal or installment loan.",
 "keywords":"loan calculator, monthly payment calculator, personal loan calculator, interest calculator",
 "body_html":"""
  <div class="field"><label for="l_amt">Loan amount</label>
    <div class="inp has-pre"><span class="pre">$</span><input id="l_amt" type="number" value="20000" min="0" step="500"></div></div>
  <div class="field"><label for="l_rate">Interest rate (APR)</label>
    <div class="inp has-suf"><input id="l_rate" type="number" value="9.5" min="0" step="0.01"><span class="suf">%</span></div></div>
  <div class="field"><label for="l_term">Loan term <span class="hint">(years)</span></label>
    <input id="l_term" type="number" value="5" min="0.25" max="40" step="0.25"></div>
 """,
 "script_js":"""
 document.addEventListener('DOMContentLoaded',function(){var F=window.FIN;
  var ids=['l_amt','l_rate','l_term'];
  function calc(){
   var P=F.num(F.el('l_amt').value)||0,rate=F.num(F.el('l_rate').value)||0,term=F.num(F.el('l_term').value)||0;
   var months=Math.round(term*12),out=F.el('out');
   if(!(months>0)||P<=0){out.innerHTML='<p class="sub">Enter a loan amount and term to see your payment.</p>';return;}
   var pay=F.pmt(P,rate,months),am=F.amortize(P,rate,months);
   var segs=[{label:'Principal',value:P,color:F.C.blue},{label:'Interest',value:am.totalInterest,color:F.C.amber}];
   var rows='',pP=0,pI=0,yr=0;
   am.schedule.forEach(function(s,i){pP+=s.principal;pI+=s.interest;if((i+1)%12===0||i===am.schedule.length-1){yr++;rows+='<tr><td>'+yr+'</td><td>'+F.money0(pP)+'</td><td>'+F.money0(pI)+'</td><td>'+F.money0(s.balance)+'</td></tr>';pP=0;pI=0;}});
   out.innerHTML='<div class="sub">Monthly payment</div><div class="big-num">'+F.money0(pay)+'</div>'+
    '<div class="chart-row">'+F.donut(segs)+F.legend(segs)+'</div>'+
    '<div class="stats"><div class="stat"><div class="k">Total interest</div><div class="v">'+F.money0(am.totalInterest)+'</div></div>'+
    '<div class="stat"><div class="k">Total paid</div><div class="v">'+F.money0(am.totalPaid)+'</div></div></div>'+
    '<div class="tbl-wrap"><table><thead><tr><th>Year</th><th>Principal</th><th>Interest</th><th>Balance</th></tr></thead><tbody>'+rows+'</tbody></table></div>';
  }
  F.on(ids,calc);calc();
 });
 """,
 "intro_html":"""
  <h2>How to use the loan calculator</h2>
  <p>Enter the amount you're borrowing, the annual interest rate (APR), and how long you'll take to repay it. The calculator returns your fixed monthly payment, the total interest you'll pay over the life of the loan, and a year-by-year breakdown of how the balance falls.</p>
  <h3>The formula</h3>
  <p>Payments use the amortization formula <code>M = P · r · (1+r)ⁿ / ((1+r)ⁿ − 1)</code> — the same math banks use — where <code>P</code> is the amount borrowed, <code>r</code> is the monthly rate, and <code>n</code> is the number of months.</p>
  <p>Shortening the term raises the monthly payment but sharply cuts total interest. Even a small rate difference can change the total cost of a loan by thousands of dollars, so it pays to compare offers.</p>
 """,
 "faqs":[
  {"q":"What's the difference between interest rate and APR?","a":"The interest rate is the cost of borrowing the principal. APR (annual percentage rate) also includes certain fees, so it's usually slightly higher and is a better figure for comparing loans. Enter the APR here for the most realistic result."},
  {"q":"How can I pay less interest?","a":"Choose a shorter term, make extra payments toward principal, or secure a lower rate. Because interest is charged on the remaining balance, paying down principal early reduces every future interest charge."},
  {"q":"Does this work for student or business loans?","a":"Yes — any fixed-rate installment loan with a set term works. Variable-rate loans will differ over time as the rate changes."},
 ],
})

TOOLS.append({
 "slug":"auto-loan-calculator","cat":"finance","icon":"🚗",
 "name":"Auto Loan Calculator",
 "short":"Estimate a car loan payment including down payment, trade-in and sales tax.",
 "lede":"Estimate your monthly car payment and total interest, factoring in your down payment, trade-in value and sales tax.",
 "title":"Auto Loan Calculator — Car Payment with Tax & Trade-In",
 "desc":"Free auto loan calculator: estimate your monthly car payment and total interest including down payment, trade-in value and sales tax.",
 "keywords":"auto loan calculator, car payment calculator, car loan calculator",
 "body_html":"""
  <div class="field"><label for="a_price">Vehicle price</label>
    <div class="inp has-pre"><span class="pre">$</span><input id="a_price" type="number" value="35000" min="0" step="500"></div></div>
  <div class="row2">
    <div class="field"><label for="a_down">Down payment</label>
      <div class="inp has-pre"><span class="pre">$</span><input id="a_down" type="number" value="5000" min="0" step="500"></div></div>
    <div class="field"><label for="a_trade">Trade-in value</label>
      <div class="inp has-pre"><span class="pre">$</span><input id="a_trade" type="number" value="0" min="0" step="500"></div></div>
  </div>
  <div class="row2">
    <div class="field"><label for="a_rate">Interest rate (APR)</label>
      <div class="inp has-suf"><input id="a_rate" type="number" value="7.5" min="0" step="0.01"><span class="suf">%</span></div></div>
    <div class="field"><label for="a_term">Term <span class="hint">(months)</span></label>
      <input id="a_term" type="number" value="60" min="1" max="120" step="1"></div>
  </div>
  <div class="field"><label for="a_tax">Sales tax</label>
    <div class="inp has-suf"><input id="a_tax" type="number" value="6" min="0" step="0.1"><span class="suf">%</span></div></div>
 """,
 "script_js":"""
 document.addEventListener('DOMContentLoaded',function(){var F=window.FIN;
  var ids=['a_price','a_down','a_trade','a_rate','a_term','a_tax'];
  function calc(){
   var price=F.num(F.el('a_price').value)||0,down=F.num(F.el('a_down').value)||0,trade=F.num(F.el('a_trade').value)||0,
       rate=F.num(F.el('a_rate').value)||0,months=Math.round(F.num(F.el('a_term').value)||0),taxpct=F.num(F.el('a_tax').value)||0;
   var taxable=Math.max(price-trade,0),tax=taxable*taxpct/100;
   var loan=Math.max(price-down-trade+tax,0),out=F.el('out');
   if(!(months>0)||loan<=0){out.innerHTML='<p class="sub">Enter a vehicle price and term to see your payment.</p>';return;}
   var pay=F.pmt(loan,rate,months),am=F.amortize(loan,rate,months);
   var segs=[{label:'Vehicle (financed)',value:Math.max(loan-tax,0),color:F.C.blue},{label:'Sales tax',value:tax,color:F.C.green},{label:'Interest',value:am.totalInterest,color:F.C.amber}];
   out.innerHTML='<div class="sub">Monthly car payment</div><div class="big-num">'+F.money0(pay)+'</div>'+
    '<div class="chart-row">'+F.donut(segs)+F.legend(segs)+'</div>'+
    '<div class="stats"><div class="stat"><div class="k">Amount financed</div><div class="v">'+F.money0(loan)+'</div></div>'+
    '<div class="stat"><div class="k">Sales tax</div><div class="v">'+F.money0(tax)+'</div></div>'+
    '<div class="stat"><div class="k">Total interest</div><div class="v">'+F.money0(am.totalInterest)+'</div></div>'+
    '<div class="stat"><div class="k">Total cost</div><div class="v">'+F.money0(down+trade*0+am.totalPaid)+'</div></div></div>';
  }
  F.on(ids,calc);calc();
 });
 """,
 "intro_html":"""
  <h2>How the auto loan calculator works</h2>
  <p>Your amount financed is the vehicle price, plus sales tax, minus your down payment and any trade-in value. This calculator applies sales tax to the price after trade-in (as most U.S. states do), then amortizes the balance over your chosen term to find the monthly payment and total interest.</p>
  <h3>Ways to lower your car payment</h3>
  <p>A bigger down payment or trade-in reduces the amount financed. A shorter term raises the monthly payment but saves interest, while a longer term does the opposite. Because cars lose value quickly, a very long term can leave you owing more than the car is worth — so aim for the shortest term you can comfortably afford.</p>
 """,
 "faqs":[
  {"q":"Is sales tax included in my car loan?","a":"In most states, yes — sales tax is added to the amount you finance. Tax is usually charged on the price after your trade-in is deducted, which can save you money. Rules vary by state, so check locally."},
  {"q":"What car loan term should I choose?","a":"Common terms are 48–72 months. Shorter terms cost less interest and build equity faster; longer terms lower the monthly payment but cost more overall and increase the risk of owing more than the car is worth."},
  {"q":"Does a trade-in reduce my loan?","a":"Yes. Your trade-in value is subtracted from the price, reducing the amount you finance — and in most states it also reduces the taxable amount."},
 ],
})

TOOLS.append({
 "slug":"compound-interest-calculator","cat":"finance","icon":"📈",
 "name":"Compound Interest Calculator",
 "short":"See how savings and investments grow over time with regular contributions.",
 "lede":"See how your money grows with compound interest. Add an initial deposit and monthly contributions to project the future value of your savings or investments.",
 "title":"Compound Interest Calculator — Investment Growth Over Time",
 "desc":"Free compound interest calculator. Project how savings and investments grow with monthly contributions, and see the split between contributions and interest earned.",
 "keywords":"compound interest calculator, investment calculator, savings growth calculator",
 "body_html":"""
  <div class="row2">
    <div class="field"><label for="c_init">Initial deposit</label>
      <div class="inp has-pre"><span class="pre">$</span><input id="c_init" type="number" value="5000" min="0" step="100"></div></div>
    <div class="field"><label for="c_pmt">Monthly contribution</label>
      <div class="inp has-pre"><span class="pre">$</span><input id="c_pmt" type="number" value="300" min="0" step="50"></div></div>
  </div>
  <div class="row2">
    <div class="field"><label for="c_rate">Annual interest rate</label>
      <div class="inp has-suf"><input id="c_rate" type="number" value="7" min="0" step="0.1"><span class="suf">%</span></div></div>
    <div class="field"><label for="c_years">Years</label>
      <input id="c_years" type="number" value="20" min="1" max="70" step="1"></div>
  </div>
  <p class="sub">Interest is compounded monthly. Contributions are added at the end of each month.</p>
 """,
 "script_js":"""
 document.addEventListener('DOMContentLoaded',function(){var F=window.FIN;
  var ids=['c_init','c_pmt','c_rate','c_years'];
  function calc(){
   var P=F.num(F.el('c_init').value)||0,pmt=F.num(F.el('c_pmt').value)||0,rate=F.num(F.el('c_rate').value)||0,years=Math.round(F.num(F.el('c_years').value)||0);
   var out=F.el('out');if(!(years>0)){out.innerHTML='<p class="sub">Enter a number of years to project growth.</p>';return;}
   var r=rate/100/12,n=years*12;
   var fv=F.futureValue(P,pmt,r,n),contrib=P+pmt*n,interest=fv-contrib;
   var segs=[{label:'Your contributions',value:contrib,color:F.C.blue},{label:'Interest earned',value:interest,color:F.C.green}];
   var rows='';for(var y=1;y<=years;y++){var v=F.futureValue(P,pmt,r,y*12),cc=P+pmt*y*12;rows+='<tr><td>'+y+'</td><td>'+F.money0(cc)+'</td><td>'+F.money0(v-cc)+'</td><td>'+F.money0(v)+'</td></tr>';}
   out.innerHTML='<div class="sub">Future value after '+years+' years</div><div class="big-num">'+F.money0(fv)+'</div>'+
    '<div class="chart-row">'+F.donut(segs)+F.legend(segs)+'</div>'+
    '<div class="stats"><div class="stat"><div class="k">Total contributions</div><div class="v">'+F.money0(contrib)+'</div></div>'+
    '<div class="stat"><div class="k">Interest earned</div><div class="v">'+F.money0(interest)+'</div></div></div>'+
    '<div class="tbl-wrap"><table><thead><tr><th>Year</th><th>Contributions</th><th>Interest</th><th>Balance</th></tr></thead><tbody>'+rows+'</tbody></table></div>';
  }
  F.on(ids,calc);calc();
 });
 """,
 "intro_html":"""
  <h2>The power of compound interest</h2>
  <p>Compound interest means you earn interest on your interest, not just your original deposit. Over long periods this snowball effect does most of the heavy lifting — which is why starting early matters so much. This calculator combines an initial deposit with regular monthly contributions and compounds monthly.</p>
  <h3>The formula</h3>
  <p>Future value is <code>FV = P(1+r)ⁿ + PMT·[((1+r)ⁿ − 1) / r]</code>, where <code>P</code> is your starting balance, <code>PMT</code> is the monthly contribution, <code>r</code> is the monthly rate (annual ÷ 12), and <code>n</code> is the number of months.</p>
  <p>Notice how, over 20–30 years, the “interest earned” slice often grows larger than everything you actually contributed. That's compounding at work.</p>
 """,
 "faqs":[
  {"q":"What interest rate should I use?","a":"For a savings account, use its APY (often 0.5%–5%). For long-term stock market investing, many people model 6%–8% as a long-run average, though real returns vary year to year and are never guaranteed."},
  {"q":"What does compounded monthly mean?","a":"It means interest is calculated and added to your balance every month, so the next month you earn interest on a slightly larger amount. More frequent compounding produces slightly higher growth than annual compounding."},
  {"q":"Why is starting early so powerful?","a":"Because compounding multiplies over time, money invested in your 20s has decades to grow. Even small contributions started early often beat larger contributions started later."},
 ],
})

TOOLS.append({
 "slug":"savings-goal-calculator","cat":"finance","icon":"🎯",
 "name":"Savings Goal Calculator",
 "short":"Find out how much to save each month to hit a target by a set date.",
 "lede":"Set a savings goal and find out exactly how much to put away each month to reach it — accounting for interest earned along the way.",
 "title":"Savings Goal Calculator — How Much to Save Each Month",
 "desc":"Free savings goal calculator: find the monthly amount needed to reach a target by a certain date, including interest earned on your balance.",
 "keywords":"savings goal calculator, how much to save, savings calculator",
 "body_html":"""
  <div class="field"><label for="s_goal">Savings goal</label>
    <div class="inp has-pre"><span class="pre">$</span><input id="s_goal" type="number" value="30000" min="0" step="500"></div></div>
  <div class="row2">
    <div class="field"><label for="s_have">Current savings</label>
      <div class="inp has-pre"><span class="pre">$</span><input id="s_have" type="number" value="2000" min="0" step="100"></div></div>
    <div class="field"><label for="s_years">Time to goal <span class="hint">(years)</span></label>
      <input id="s_years" type="number" value="5" min="0.25" step="0.25"></div>
  </div>
  <div class="field"><label for="s_rate">Annual interest rate <span class="hint">(APY)</span></label>
    <div class="inp has-suf"><input id="s_rate" type="number" value="4" min="0" step="0.1"><span class="suf">%</span></div></div>
 """,
 "script_js":"""
 document.addEventListener('DOMContentLoaded',function(){var F=window.FIN;
  var ids=['s_goal','s_have','s_years','s_rate'];
  function calc(){
   var goal=F.num(F.el('s_goal').value)||0,have=F.num(F.el('s_have').value)||0,years=F.num(F.el('s_years').value)||0,rate=F.num(F.el('s_rate').value)||0;
   var n=Math.round(years*12),r=rate/100/12,out=F.el('out');
   if(!(n>0)||goal<=0){out.innerHTML='<p class="sub">Enter a goal and a time frame to see the monthly amount.</p>';return;}
   var monthly=F.contributionFor(goal,have,r,n);
   if(monthly<0)monthly=0;
   var contrib=have+monthly*n,interest=goal-contrib;
   var segs=[{label:'Current + contributions',value:contrib,color:F.C.blue},{label:'Interest earned',value:Math.max(interest,0),color:F.C.green}];
   out.innerHTML='<div class="sub">Save this much each month</div><div class="big-num">'+F.money0(monthly)+'</div>'+
    '<div class="chart-row">'+F.donut(segs)+F.legend(segs)+'</div>'+
    '<div class="stats"><div class="stat"><div class="k">You contribute</div><div class="v">'+F.money0(monthly*n)+'</div></div>'+
    '<div class="stat"><div class="k">Interest earned</div><div class="v">'+F.money0(Math.max(interest,0))+'</div></div>'+
    '<div class="stat"><div class="k">Starting balance</div><div class="v">'+F.money0(have)+'</div></div>'+
    '<div class="stat"><div class="k">Goal</div><div class="v">'+F.money0(goal)+'</div></div></div>';
  }
  F.on(ids,calc);calc();
 });
 """,
 "intro_html":"""
  <h2>Plan your savings goal</h2>
  <p>Whether you're building an emergency fund, saving a house deposit, or planning a big purchase, this calculator tells you the monthly amount needed to hit your target on time. It accounts for the interest your balance earns along the way, so the required contribution is a little lower than simply dividing the goal by the number of months.</p>
  <h3>How it's calculated</h3>
  <p>We solve the future-value formula for the monthly contribution: the goal must equal your current balance grown at interest, plus the future value of each monthly deposit. A higher interest rate or a longer timeframe both reduce how much you need to set aside each month.</p>
 """,
 "faqs":[
  {"q":"What rate should I enter?","a":"Use the APY of where you'll keep the money — for example a high-yield savings account or money-market fund for short-term goals. For very short timeframes, interest makes little difference, so you can even enter 0%."},
  {"q":"What if I can't afford the monthly amount?","a":"Extend the timeframe, lower the goal, or increase your starting balance. Small changes to the time to goal can significantly reduce the monthly amount required."},
 ],
})

TOOLS.append({
 "slug":"inflation-calculator","cat":"finance","icon":"💵",
 "name":"Inflation Calculator",
 "short":"See how inflation changes buying power and future prices over time.",
 "lede":"See how inflation erodes buying power over time — what a sum of money today will be worth in the future, and what you'll need to keep the same purchasing power.",
 "title":"Inflation Calculator — Future Buying Power of Money",
 "desc":"Free inflation calculator: see how inflation changes the buying power of money over time and what a future amount is worth in today's dollars.",
 "keywords":"inflation calculator, buying power calculator, future value of money",
 "body_html":"""
  <div class="field"><label for="i_amt">Amount today</label>
    <div class="inp has-pre"><span class="pre">$</span><input id="i_amt" type="number" value="10000" min="0" step="100"></div></div>
  <div class="row2">
    <div class="field"><label for="i_rate">Inflation rate <span class="hint">(/yr)</span></label>
      <div class="inp has-suf"><input id="i_rate" type="number" value="3" min="0" step="0.1"><span class="suf">%</span></div></div>
    <div class="field"><label for="i_years">Years</label>
      <input id="i_years" type="number" value="20" min="1" max="100" step="1"></div>
  </div>
 """,
 "script_js":"""
 document.addEventListener('DOMContentLoaded',function(){var F=window.FIN;
  var ids=['i_amt','i_rate','i_years'];
  function calc(){
   var amt=F.num(F.el('i_amt').value)||0,rate=F.num(F.el('i_rate').value)||0,years=Math.round(F.num(F.el('i_years').value)||0),out=F.el('out');
   if(!(years>0)||amt<=0){out.innerHTML='<p class="sub">Enter an amount and number of years.</p>';return;}
   var f=Math.pow(1+rate/100,years),needed=amt*f,worth=amt/f;
   var rows='';for(var y=1;y<=years;y++){var ff=Math.pow(1+rate/100,y);rows+='<tr><td>'+y+'</td><td>'+F.money0(amt*ff)+'</td><td>'+F.money0(amt/ff)+'</td></tr>';}
   out.innerHTML='<div class="sub">To buy today\\'s '+F.money0(amt)+' of goods in '+years+' years you\\'ll need</div><div class="big-num">'+F.money0(needed)+'</div>'+
    '<div class="stats"><div class="stat"><div class="k">Future buying power of '+F.money0(amt)+'</div><div class="v">'+F.money0(worth)+'</div></div>'+
    '<div class="stat"><div class="k">Total inflation</div><div class="v">'+F.pct((f-1)*100,1)+'</div></div></div>'+
    '<div class="tbl-wrap"><table><thead><tr><th>Year</th><th>Cost of today\\'s '+F.money0(amt)+'</th><th>Today\\'s money is worth</th></tr></thead><tbody>'+rows+'</tbody></table></div>';
  }
  F.on(ids,calc);calc();
 });
 """,
 "intro_html":"""
  <h2>How inflation affects your money</h2>
  <p>Inflation is the gradual rise in prices over time, which means each dollar buys a little less each year. This calculator shows two sides of the same coin: how much money you'll need in the future to buy what a set amount buys today, and how much your money's <em>buying power</em> shrinks if it isn't invested.</p>
  <h3>The formula</h3>
  <p>With an annual inflation rate <code>i</code> over <code>n</code> years, future cost is <code>Amount × (1 + i)ⁿ</code>, and today's money will have the buying power of <code>Amount ÷ (1 + i)ⁿ</code> in future dollars. Historically U.S. inflation has averaged roughly 3% per year, though it varies.</p>
  <p>This is why cash left idle loses value, and why long-term savings are often invested to earn a return that outpaces inflation.</p>
 """,
 "faqs":[
  {"q":"What inflation rate should I use?","a":"Long-run U.S. inflation has averaged around 3% per year, so that's a common default. For specific periods you can enter the actual figure — for example, inflation was higher in 2022 and lower in some earlier years."},
  {"q":"How can I protect against inflation?","a":"Keeping long-term savings in investments that historically outpace inflation (such as diversified stock funds) helps preserve buying power. Inflation-protected bonds (TIPS) and high-yield savings for short-term cash are other common approaches. This is general information, not advice."},
 ],
})

# ============================ UTILITY ============================

TOOLS.append({
 "slug":"percentage-calculator","cat":"utility","icon":"％",
 "name":"Percentage Calculator",
 "short":"Work out percentages three ways — of a number, as a ratio, or change.",
 "lede":"Three quick percentage calculators in one: find a percent of a number, work out what percent one number is of another, and calculate percentage increase or decrease.",
 "title":"Percentage Calculator — % of a Number, Ratio & Change",
 "desc":"Free percentage calculator. Find X% of a number, what percent one value is of another, and the percentage increase or decrease between two numbers.",
 "keywords":"percentage calculator, percent calculator, percentage increase, percent of a number",
 "body_html":"""
  <div class="field"><label>What is <input id="p1a" type="number" value="15" style="width:90px;display:inline-block"> % of
    <input id="p1b" type="number" value="200" style="width:110px;display:inline-block"> ?</label>
    <div class="stat"><div class="k">Result</div><div class="v" id="p1r">—</div></div></div>
  <hr style="border:none;border-top:1px solid var(--line);margin:18px 0">
  <div class="field"><label><input id="p2a" type="number" value="45" style="width:100px;display:inline-block"> is what % of
    <input id="p2b" type="number" value="180" style="width:110px;display:inline-block"> ?</label>
    <div class="stat"><div class="k">Result</div><div class="v" id="p2r">—</div></div></div>
  <hr style="border:none;border-top:1px solid var(--line);margin:18px 0">
  <div class="field"><label>Percentage change from <input id="p3a" type="number" value="120" style="width:100px;display:inline-block"> to
    <input id="p3b" type="number" value="150" style="width:100px;display:inline-block"></label>
    <div class="stat"><div class="k">Result</div><div class="v" id="p3r">—</div></div></div>
 """,
 "script_js":"""
 document.addEventListener('DOMContentLoaded',function(){var F=window.FIN;
  var ids=['p1a','p1b','p2a','p2b','p3a','p3b'];
  function calc(){
   var a=F.num(F.el('p1a').value),b=F.num(F.el('p1b').value);
   F.el('p1r').textContent=isFinite(a)&&isFinite(b)?F.nfmt(a/100*b):'—';
   var c=F.num(F.el('p2a').value),d=F.num(F.el('p2b').value);
   F.el('p2r').textContent=isFinite(c)&&isFinite(d)&&d!==0?F.pct(c/d*100):'—';
   var e=F.num(F.el('p3a').value),f=F.num(F.el('p3b').value);
   if(isFinite(e)&&isFinite(f)&&e!==0){var ch=(f-e)/Math.abs(e)*100;F.el('p3r').textContent=(ch>=0?'+':'')+F.pct(ch)+(ch>=0?' increase':' decrease');}else F.el('p3r').textContent='—';
   var o=F.el('out');if(o)o.innerHTML='<p class="sub">Results update instantly on the left as you type. This tool covers the three most common percentage questions.</p>';
  }
  F.on(ids,calc);calc();
 });
 """,
 "intro_html":"""
  <h2>How to calculate percentages</h2>
  <p>A percentage is just a fraction of 100. These three calculators cover the questions people ask most:</p>
  <h3>Percent of a number</h3>
  <p>To find <code>X%</code> of a number, multiply the number by X and divide by 100. Example: 15% of 200 = 200 × 15 ÷ 100 = <strong>30</strong>.</p>
  <h3>What percent one number is of another</h3>
  <p>Divide the part by the whole and multiply by 100. Example: 45 is 45 ÷ 180 × 100 = <strong>25%</strong> of 180.</p>
  <h3>Percentage change</h3>
  <p>Subtract the old value from the new value, divide by the old value, and multiply by 100. Example: from 120 to 150 is (150 − 120) ÷ 120 × 100 = <strong>+25%</strong>.</p>
 """,
 "faqs":[
  {"q":"How do I calculate a percentage increase?","a":"Subtract the original number from the new number, divide the result by the original number, then multiply by 100. A positive result is an increase; a negative result is a decrease."},
  {"q":"How do I add a percentage to a price?","a":"Multiply the price by (1 + percentage/100). For example, adding 8% tax to $50 is 50 × 1.08 = $54. Our discount &amp; sales-tax calculator does this automatically."},
 ],
})

TOOLS.append({
 "slug":"bmi-calculator","cat":"utility","icon":"⚖️",
 "name":"BMI Calculator",
 "short":"Calculate body mass index and see your healthy weight range.",
 "lede":"Calculate your Body Mass Index (BMI) in metric or imperial units, see which category it falls in, and find the healthy weight range for your height.",
 "title":"BMI Calculator — Body Mass Index (Metric & Imperial)",
 "desc":"Free BMI calculator for metric and imperial units. Find your body mass index, category, and the healthy weight range for your height.",
 "keywords":"bmi calculator, body mass index, healthy weight calculator",
 "body_html":"""
  <div class="field"><label>Units</label>
    <div class="seg" id="b_units"><button data-u="metric" class="on">Metric (cm, kg)</button><button data-u="imp">Imperial (ft/in, lb)</button></div></div>
  <div id="b_metric">
    <div class="field"><label for="b_cm">Height (cm)</label><input id="b_cm" type="number" value="175" min="0"></div>
    <div class="field"><label for="b_kg">Weight (kg)</label><input id="b_kg" type="number" value="72" min="0"></div>
  </div>
  <div id="b_imp" style="display:none">
    <div class="row2"><div class="field"><label for="b_ft">Height (ft)</label><input id="b_ft" type="number" value="5" min="0"></div>
      <div class="field"><label for="b_in">(in)</label><input id="b_in" type="number" value="9" min="0"></div></div>
    <div class="field"><label for="b_lb">Weight (lb)</label><input id="b_lb" type="number" value="160" min="0"></div>
  </div>
 """,
 "script_js":"""
 document.addEventListener('DOMContentLoaded',function(){var F=window.FIN;var unit='metric';
  function cat(b){if(b<18.5)return['Underweight',F.C.amber];if(b<25)return['Healthy weight',F.C.green];if(b<30)return['Overweight',F.C.amber];return['Obese',F.C.red];}
  function calc(){
   var m;if(unit==='metric'){var cm=F.num(F.el('b_cm').value),kg=F.num(F.el('b_kg').value);if(!(cm>0)||!(kg>0)){return set(null);}m=cm/100;var bmi=kg/(m*m);done(bmi,m);}
   else{var ft=F.num(F.el('b_ft').value)||0,inch=F.num(F.el('b_in').value)||0,lb=F.num(F.el('b_lb').value);var totIn=ft*12+inch;if(!(totIn>0)||!(lb>0)){return set(null);}m=totIn*0.0254;var bmi2=lb*0.453592/(m*m);done(bmi2,m);}
  }
  function set(x){F.el('out').innerHTML='<p class="sub">Enter your height and weight to see your BMI.</p>';}
  function done(bmi,m){var c=cat(bmi),lo=18.5*m*m,hi=24.9*m*m,disp;
   if(unit==='metric')disp=F.nfmt(lo,1)+'–'+F.nfmt(hi,1)+' kg';else disp=F.nfmt(lo/0.453592,0)+'–'+F.nfmt(hi/0.453592,0)+' lb';
   F.el('out').innerHTML='<div class="sub">Your BMI</div><div class="big-num" style="color:'+c[1]+'">'+F.nfmt(bmi,1)+'</div>'+
    '<div class="stats"><div class="stat"><div class="k">Category</div><div class="v" style="color:'+c[1]+'">'+c[0]+'</div></div>'+
    '<div class="stat"><div class="k">Healthy range for your height</div><div class="v">'+disp+'</div></div></div>'+
    '<p class="sub" style="margin-top:12px">BMI categories: under 18.5 underweight · 18.5–24.9 healthy · 25–29.9 overweight · 30+ obese.</p>';
  }
  F.el('b_units').addEventListener('click',function(e){var btn=e.target.closest('button');if(!btn)return;unit=btn.dataset.u;
   [].forEach.call(this.children,function(x){x.classList.toggle('on',x===btn);});
   F.el('b_metric').style.display=unit==='metric'?'':'none';F.el('b_imp').style.display=unit==='imp'?'':'none';calc();});
  F.on(['b_cm','b_kg','b_ft','b_in','b_lb'],calc);calc();
 });
 """,
 "intro_html":"""
  <h2>What is BMI?</h2>
  <p>Body Mass Index (BMI) is a simple screening number that compares your weight to your height. It's calculated as <code>weight (kg) ÷ height (m)²</code>. Because it's quick and requires no special equipment, it's widely used as a first check of whether someone is in a healthy weight range.</p>
  <h3>BMI categories</h3>
  <p>Under 18.5 is considered underweight, 18.5–24.9 healthy weight, 25–29.9 overweight, and 30 or above obese. The healthy-weight range shown is the weight that would put your BMI between 18.5 and 24.9 for your height.</p>
  <div class="callout"><strong>Note:</strong> BMI is a general guide, not a diagnosis. It doesn't distinguish muscle from fat, so very muscular people may read as “overweight”. Talk to a healthcare professional for personal advice.</div>
 """,
 "faqs":[
  {"q":"Is BMI accurate?","a":"BMI is a useful population-level screening tool but has limits for individuals. It doesn't account for muscle mass, body composition, age or sex, so athletes and some body types can be misclassified. Use it as a rough guide alongside other health measures."},
  {"q":"What is a healthy BMI?","a":"A BMI between 18.5 and 24.9 is generally considered healthy for adults. This tool shows the exact weight range that corresponds to a healthy BMI for your height."},
 ],
})

TOOLS.append({
 "slug":"age-calculator","cat":"utility","icon":"🎂",
 "name":"Age Calculator",
 "short":"Find exact age in years, months and days — plus your next birthday.",
 "lede":"Calculate exact age from a date of birth: years, months and days, total days lived, and a countdown to the next birthday.",
 "title":"Age Calculator — Exact Age in Years, Months & Days",
 "desc":"Free age calculator. Enter a date of birth to get exact age in years, months and days, total days lived, and days until the next birthday.",
 "keywords":"age calculator, date of birth calculator, how old am i",
 "body_html":"""
  <div class="field"><label for="ag_dob">Date of birth</label><input id="ag_dob" type="date" value="1995-06-15"></div>
  <div class="field"><label for="ag_to">Age at date <span class="hint">(defaults to today)</span></label><input id="ag_to" type="date"></div>
 """,
 "script_js":"""
 document.addEventListener('DOMContentLoaded',function(){var F=window.FIN;
  var toEl=F.el('ag_to');if(!toEl.value){var t=new Date();toEl.value=t.getFullYear()+'-'+String(t.getMonth()+1).padStart(2,'0')+'-'+String(t.getDate()).padStart(2,'0');}
  function calc(){
   var dob=new Date(F.el('ag_dob').value),to=new Date(F.el('ag_to').value),out=F.el('out');
   if(isNaN(dob)||isNaN(to)||to<dob){out.innerHTML='<p class="sub">Enter a valid date of birth (and an end date on or after it).</p>';return;}
   var y=to.getFullYear()-dob.getFullYear(),m=to.getMonth()-dob.getMonth(),d=to.getDate()-dob.getDate();
   if(d<0){m--;d+=new Date(to.getFullYear(),to.getMonth(),0).getDate();}
   if(m<0){y--;m+=12;}
   var totalDays=Math.floor((to-dob)/86400000);
   var nb=new Date(to.getFullYear(),dob.getMonth(),dob.getDate());if(nb<to)nb=new Date(to.getFullYear()+1,dob.getMonth(),dob.getDate());
   var daysToBd=Math.ceil((nb-to)/86400000);
   out.innerHTML='<div class="sub">Age</div><div class="big-num">'+y+' <span style="font-size:18px;color:var(--muted)">yr</span> '+m+' <span style="font-size:18px;color:var(--muted)">mo</span> '+d+' <span style="font-size:18px;color:var(--muted)">d</span></div>'+
    '<div class="stats"><div class="stat"><div class="k">Total days</div><div class="v">'+F.nfmt(totalDays,0)+'</div></div>'+
    '<div class="stat"><div class="k">Total months</div><div class="v">'+F.nfmt(y*12+m,0)+'</div></div>'+
    '<div class="stat"><div class="k">Total weeks</div><div class="v">'+F.nfmt(Math.floor(totalDays/7),0)+'</div></div>'+
    '<div class="stat"><div class="k">Next birthday in</div><div class="v">'+(daysToBd===0?'Today! 🎉':daysToBd+' days')+'</div></div></div>';
  }
  F.on(['ag_dob','ag_to'],calc);calc();
 });
 """,
 "intro_html":"""
  <h2>How the age calculator works</h2>
  <p>Enter a date of birth and the tool works out the exact time elapsed until today (or any date you choose), broken into years, months and days. It also totals the days, weeks and months lived and counts down to the next birthday.</p>
  <p>The calculation handles months of different lengths and leap years by comparing the actual calendar dates, so the result matches how we naturally count age — the day, month and year all have to “catch up” to the target date.</p>
 """,
 "faqs":[
  {"q":"Does it account for leap years?","a":"Yes. Because it compares real calendar dates rather than assuming fixed-length months, leap years and varying month lengths are handled automatically."},
  {"q":"Can I calculate age between two past dates?","a":"Yes — set the “age at date” field to any date. It's useful for finding someone's age at a past event, or the gap between two dates."},
 ],
})

TOOLS.append({
 "slug":"tip-calculator","cat":"utility","icon":"🍽️",
 "name":"Tip Calculator",
 "short":"Calculate the tip and split the bill between any number of people.",
 "lede":"Quickly calculate a tip and split the total between friends. Choose a tip percentage and the number of people to see the amount each person owes.",
 "title":"Tip Calculator — Gratuity & Bill Split",
 "desc":"Free tip calculator: work out gratuity at any percentage and split the bill evenly between any number of people.",
 "keywords":"tip calculator, gratuity calculator, bill split calculator",
 "body_html":"""
  <div class="field"><label for="t_bill">Bill amount</label>
    <div class="inp has-pre"><span class="pre">$</span><input id="t_bill" type="number" value="80" min="0" step="1"></div></div>
  <div class="field"><label for="t_tip">Tip percentage</label>
    <div class="inp has-suf"><input id="t_tip" type="number" value="18" min="0" step="1"><span class="suf">%</span></div>
    <div class="seg" style="margin-top:8px" id="t_quick"><button data-t="10">10%</button><button data-t="15">15%</button><button data-t="18" class="on">18%</button><button data-t="20">20%</button><button data-t="25">25%</button></div></div>
  <div class="field"><label for="t_people">Split between</label>
    <div class="inp has-suf"><input id="t_people" type="number" value="2" min="1" step="1"><span class="suf">people</span></div></div>
 """,
 "script_js":"""
 document.addEventListener('DOMContentLoaded',function(){var F=window.FIN;
  function calc(){
   var bill=F.num(F.el('t_bill').value)||0,tp=F.num(F.el('t_tip').value)||0,ppl=Math.max(1,Math.round(F.num(F.el('t_people').value)||1));
   var tip=bill*tp/100,total=bill+tip,out=F.el('out');
   out.innerHTML='<div class="sub">Each person pays</div><div class="big-num">'+F.money(total/ppl)+'</div>'+
    '<div class="stats"><div class="stat"><div class="k">Tip amount</div><div class="v">'+F.money(tip)+'</div></div>'+
    '<div class="stat"><div class="k">Total with tip</div><div class="v">'+F.money(total)+'</div></div>'+
    '<div class="stat"><div class="k">Tip per person</div><div class="v">'+F.money(tip/ppl)+'</div></div>'+
    '<div class="stat"><div class="k">People</div><div class="v">'+ppl+'</div></div></div>';
  }
  F.el('t_quick').addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;F.el('t_tip').value=b.dataset.t;
   [].forEach.call(this.children,function(x){x.classList.toggle('on',x===b);});calc();});
  F.on(['t_bill','t_tip','t_people'],calc);calc();
 });
 """,
 "intro_html":"""
  <h2>How much should you tip?</h2>
  <p>In the United States, tipping 15–20% of the pre-tax bill is standard for table service, with 18–20% common for good service. This calculator lets you pick any percentage, adds it to the bill, and splits the total evenly between however many people are dining.</p>
  <p>Enter the bill, tap a quick tip button (or type your own percentage), and set the number of people to instantly see the tip, the grand total, and what each person owes.</p>
 """,
 "faqs":[
  {"q":"Should I tip on the pre-tax or post-tax total?","a":"Customarily, tips are based on the pre-tax bill amount, though many people simply tip on the total for convenience. Enter whichever bill figure you prefer."},
  {"q":"What's a standard tip percentage?","a":"For sit-down restaurant service in the U.S., 15% is a baseline, 18–20% reflects good service, and 20%+ is generous. Norms differ by country and service type."},
 ],
})

TOOLS.append({
 "slug":"discount-calculator","cat":"utility","icon":"🏷️",
 "name":"Discount & Sales Tax Calculator",
 "short":"Find the sale price after a discount, and add sales tax to the total.",
 "lede":"Work out how much you save with a percentage discount, the final sale price, and the total after adding sales tax.",
 "title":"Discount Calculator — Sale Price & Sales Tax",
 "desc":"Free discount calculator: find the sale price after a percent-off discount and the final total including sales tax, plus how much you save.",
 "keywords":"discount calculator, sale price calculator, sales tax calculator, percent off",
 "body_html":"""
  <div class="field"><label for="d_price">Original price</label>
    <div class="inp has-pre"><span class="pre">$</span><input id="d_price" type="number" value="120" min="0" step="1"></div></div>
  <div class="row2">
    <div class="field"><label for="d_off">Discount</label>
      <div class="inp has-suf"><input id="d_off" type="number" value="25" min="0" max="100" step="1"><span class="suf">%</span></div></div>
    <div class="field"><label for="d_tax">Sales tax</label>
      <div class="inp has-suf"><input id="d_tax" type="number" value="7" min="0" step="0.1"><span class="suf">%</span></div></div>
  </div>
 """,
 "script_js":"""
 document.addEventListener('DOMContentLoaded',function(){var F=window.FIN;
  function calc(){
   var p=F.num(F.el('d_price').value)||0,off=F.num(F.el('d_off').value)||0,tax=F.num(F.el('d_tax').value)||0;
   var save=p*off/100,sale=p-save,total=sale*(1+tax/100),out=F.el('out');
   out.innerHTML='<div class="sub">Final price</div><div class="big-num">'+F.money(total)+'</div>'+
    '<div class="stats"><div class="stat"><div class="k">You save</div><div class="v" style="color:var(--green)">'+F.money(save)+'</div></div>'+
    '<div class="stat"><div class="k">Sale price</div><div class="v">'+F.money(sale)+'</div></div>'+
    '<div class="stat"><div class="k">Sales tax added</div><div class="v">'+F.money(total-sale)+'</div></div>'+
    '<div class="stat"><div class="k">Original</div><div class="v">'+F.money(p)+'</div></div></div>';
  }
  F.on(['d_price','d_off','d_tax'],calc);calc();
 });
 """,
 "intro_html":"""
  <h2>How to calculate a discount</h2>
  <p>To find a sale price, multiply the original price by the discount percentage to get the savings, then subtract it from the original. For example, 25% off $120 saves $30, for a sale price of $90. This calculator also adds sales tax so you see the true amount you'll pay at the register.</p>
  <h3>The formula</h3>
  <p>Sale price = <code>Price × (1 − discount%/100)</code>. Final total = <code>Sale price × (1 + tax%/100)</code>. Set sales tax to 0% if you just want the discounted price.</p>
 """,
 "faqs":[
  {"q":"How do I calculate percent off?","a":"Multiply the original price by the percentage and divide by 100 to get the dollars saved, then subtract that from the price. This tool does it instantly and also shows the tax-inclusive total."},
  {"q":"Is sales tax applied before or after the discount?","a":"Sales tax is normally charged on the discounted (sale) price, which is what this calculator does."},
 ],
})

TOOLS.append({
 "slug":"unit-converter","cat":"utility","icon":"📐",
 "name":"Unit Converter",
 "short":"Convert length, weight, temperature and volume between common units.",
 "lede":"A quick unit converter for everyday measurements — length, weight, temperature and volume — between metric and imperial units.",
 "title":"Unit Converter — Length, Weight, Temperature & Volume",
 "desc":"Free unit converter for length, weight, temperature and volume. Convert between metric and imperial units instantly.",
 "keywords":"unit converter, length converter, weight converter, temperature converter, cm to inches, kg to lbs",
 "body_html":"""
  <div class="field"><label for="u_cat">Category</label>
    <select id="u_cat"><option value="length">Length</option><option value="weight">Weight</option><option value="temp">Temperature</option><option value="volume">Volume</option></select></div>
  <div class="row2">
    <div class="field"><label for="u_val">Value</label><input id="u_val" type="number" value="10"></div>
    <div class="field"><label for="u_from">From</label><select id="u_from"></select></div>
  </div>
  <div class="field"><label for="u_to">To</label><select id="u_to"></select></div>
 """,
 "script_js":"""
 document.addEventListener('DOMContentLoaded',function(){var F=window.FIN;
  var U={length:{base:'m',units:{'Meters':1,'Kilometers':1000,'Centimeters':0.01,'Millimeters':0.001,'Miles':1609.344,'Yards':0.9144,'Feet':0.3048,'Inches':0.0254}},
         weight:{base:'kg',units:{'Kilograms':1,'Grams':0.001,'Pounds':0.45359237,'Ounces':0.0283495231,'Stone':6.35029318,'Tonnes':1000}},
         volume:{base:'L',units:{'Liters':1,'Milliliters':0.001,'US Gallons':3.785411784,'US Quarts':0.946352946,'US Cups':0.2365882365,'Fluid Ounces (US)':0.0295735296,'Imperial Gallons':4.54609}},
         temp:{units:{'Celsius':1,'Fahrenheit':1,'Kelvin':1}}};
  function fill(sel,cat,pick){sel.innerHTML='';Object.keys(U[cat].units).forEach(function(k){var o=document.createElement('option');o.value=k;o.textContent=k;sel.appendChild(o);});if(pick)sel.value=pick;}
  function conv(cat,v,from,to){
   if(cat==='temp'){var c;if(from==='Celsius')c=v;else if(from==='Fahrenheit')c=(v-32)*5/9;else c=v-273.15;
     if(to==='Celsius')return c;if(to==='Fahrenheit')return c*9/5+32;return c+273.15;}
   var u=U[cat].units;return v*u[from]/u[to];
  }
  function calc(){var cat=F.el('u_cat').value,v=F.num(F.el('u_val').value),from=F.el('u_from').value,to=F.el('u_to').value;var out=F.el('out');
   if(!isFinite(v)){out.innerHTML='<p class="sub">Enter a value to convert.</p>';return;}
   var r=conv(cat,v,from,to);
   out.innerHTML='<div class="sub">'+F.nfmt(v,4)+' '+from+' =</div><div class="big-num">'+F.nfmt(r,6)+'</div><div class="sub">'+to+'</div>';
  }
  function refill(){var cat=F.el('u_cat').value,keys=Object.keys(U[cat].units);fill(F.el('u_from'),cat,keys[0]);fill(F.el('u_to'),cat,keys[1]||keys[0]);calc();}
  F.el('u_cat').addEventListener('change',refill);F.on(['u_val'],calc);F.el('u_from').addEventListener('change',calc);F.el('u_to').addEventListener('change',calc);
  refill();
 });
 """,
 "intro_html":"""
  <h2>Convert everyday units instantly</h2>
  <p>This converter handles the measurements people look up most: length (meters, feet, miles, inches and more), weight (kilograms, pounds, ounces, stone), temperature (Celsius, Fahrenheit, Kelvin) and volume (liters, gallons, cups, fluid ounces). Pick a category, enter a value, and choose the units to convert between.</p>
  <p>Common quick conversions: 1 inch = 2.54 cm, 1 mile = 1.609 km, 1 kg = 2.205 lb, and 0°C = 32°F. Temperature uses proper offset formulas rather than simple ratios, so conversions are exact.</p>
 """,
 "faqs":[
  {"q":"How do I convert cm to inches?","a":"Divide centimeters by 2.54. For example, 10 cm ÷ 2.54 = 3.94 inches. Select Length, enter your value, and choose Centimeters → Inches."},
  {"q":"How do I convert kg to pounds?","a":"Multiply kilograms by 2.2046. For example, 70 kg × 2.2046 = 154.3 lb. Choose Weight and set Kilograms → Pounds."},
 ],
})
