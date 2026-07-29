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

# ==================== PHASE 2 — FINANCE ====================

TOOLS.append({
 "slug":"debt-payoff-calculator","cat":"finance","icon":"🏔️",
 "name":"Debt Payoff Calculator",
 "short":"Compare the snowball and avalanche methods to clear your debts faster.",
 "lede":"Enter your debts and an extra monthly payment to compare the snowball and avalanche strategies — see how fast you can be debt-free and how much interest you save.",
 "title":"Debt Payoff Calculator — Snowball vs Avalanche",
 "desc":"Free debt payoff calculator comparing the snowball and avalanche methods. See your debt-free date, total interest, and how much you save with an extra payment.",
 "keywords":"debt payoff calculator, debt snowball calculator, debt avalanche calculator, pay off debt",
 "body_html":"""
  <p class="sub" style="margin:0 0 10px;font-weight:600;color:#334155">Your debts <span class="hint" style="font-weight:400">balance · APR · min payment (leave blank if unused)</span></p>
  <div class="field"><label>Debt 1</label><div class="row3">
    <div class="inp has-pre"><span class="pre">$</span><input id="d1b" type="number" value="6000" min="0" step="100" aria-label="Debt 1 balance"></div>
    <div class="inp has-suf"><input id="d1r" type="number" value="22" min="0" step="0.1" aria-label="Debt 1 APR"><span class="suf">%</span></div>
    <div class="inp has-pre"><span class="pre">$</span><input id="d1m" type="number" value="150" min="0" step="10" aria-label="Debt 1 minimum"></div></div></div>
  <div class="field"><label>Debt 2</label><div class="row3">
    <div class="inp has-pre"><span class="pre">$</span><input id="d2b" type="number" value="3000" min="0" step="100" aria-label="Debt 2 balance"></div>
    <div class="inp has-suf"><input id="d2r" type="number" value="19" min="0" step="0.1" aria-label="Debt 2 APR"><span class="suf">%</span></div>
    <div class="inp has-pre"><span class="pre">$</span><input id="d2m" type="number" value="75" min="0" step="10" aria-label="Debt 2 minimum"></div></div></div>
  <div class="field"><label>Debt 3</label><div class="row3">
    <div class="inp has-pre"><span class="pre">$</span><input id="d3b" type="number" value="9000" min="0" step="100" aria-label="Debt 3 balance"></div>
    <div class="inp has-suf"><input id="d3r" type="number" value="7" min="0" step="0.1" aria-label="Debt 3 APR"><span class="suf">%</span></div>
    <div class="inp has-pre"><span class="pre">$</span><input id="d3m" type="number" value="200" min="0" step="10" aria-label="Debt 3 minimum"></div></div></div>
  <div class="field"><label>Debt 4</label><div class="row3">
    <div class="inp has-pre"><span class="pre">$</span><input id="d4b" type="number" value="0" min="0" step="100" aria-label="Debt 4 balance"></div>
    <div class="inp has-suf"><input id="d4r" type="number" value="0" min="0" step="0.1" aria-label="Debt 4 APR"><span class="suf">%</span></div>
    <div class="inp has-pre"><span class="pre">$</span><input id="d4m" type="number" value="0" min="0" step="10" aria-label="Debt 4 minimum"></div></div></div>
  <div class="field"><label for="dp_extra">Extra monthly payment</label>
    <div class="inp has-pre"><span class="pre">$</span><input id="dp_extra" type="number" value="300" min="0" step="25"></div></div>
  <div class="field"><label>Strategy</label>
    <div class="seg" id="dp_strat"><button data-v="avalanche" class="on">Avalanche</button><button data-v="snowball">Snowball</button></div></div>
 """,
 "script_js":"""
 document.addEventListener('DOMContentLoaded',function(){var F=window.FIN;var strat='avalanche';
  var ids=['d1b','d1r','d1m','d2b','d2r','d2m','d3b','d3r','d3m','d4b','d4r','d4m','dp_extra'];
  function debts(){var out=[];[1,2,3,4].forEach(function(i){
    var b=F.num(F.el('d'+i+'b').value)||0,r=F.num(F.el('d'+i+'r').value)||0,m=F.num(F.el('d'+i+'m').value)||0;
    if(b>0)out.push({bal:b,r:r/100/12,min:m});});return out;}
  function sim(list,extra,mode){
   var ds=list.map(function(d){return {bal:d.bal,r:d.r,min:d.min};});
   if(mode==='avalanche')ds.sort(function(a,b){return b.r-a.r;});else ds.sort(function(a,b){return a.bal-b.bal;});
   var month=0,ti=0,cap=1200;
   while(ds.some(function(d){return d.bal>0.005;})){
    if(month>=cap)return{stuck:true};
    month++;
    ds.forEach(function(d){if(d.bal>0){var it=d.bal*d.r;d.bal+=it;ti+=it;}});
    var pool=extra;ds.forEach(function(d){if(d.bal>0)pool+=d.min;});
    var left=pool,paid=0;
    ds.forEach(function(d){if(d.bal>0){var p=Math.min(d.min,d.bal,left);d.bal-=p;left-=p;paid+=p;}});
    for(var k=0;k<ds.length&&left>0.005;k++){if(ds[k].bal>0){var p2=Math.min(left,ds[k].bal);ds[k].bal-=p2;left-=p2;paid+=p2;}}
    if(paid<0.005)return{stuck:true};
   }
   return {months:month,interest:ti};
  }
  function fmtM(m){var y=Math.floor(m/12),mo=m%12;return (y>0?y+' yr ':'')+mo+' mo';}
  function calc(){
   var list=debts(),out=F.el('out'),extra=F.num(F.el('dp_extra').value)||0;
   if(!list.length){out.innerHTML='<p class="sub">Enter at least one debt balance to see your payoff plan.</p>';return;}
   var av=sim(list,extra,'avalanche'),sn=sim(list,extra,'snowball'),minOnly=sim(list,0,'avalanche');
   var sel=strat==='snowball'?sn:av;
   if(sel.stuck||minOnly.stuck){out.innerHTML='<div class="callout" style="background:#fef2f2;border-color:#fecaca;color:#991b1b">Your monthly payments do not cover the interest on these debts, so the balance never clears. Increase the minimum payments or the extra amount.</div>';return;}
   var totalBal=list.reduce(function(a,d){return a+d.bal;},0);
   var saved=Math.max(minOnly.interest-sel.interest,0);
   out.innerHTML='<div class="sub">Debt-free in ('+(strat==='snowball'?'snowball':'avalanche')+')</div><div class="big-num">'+fmtM(sel.months)+'</div>'+
    '<div class="stats"><div class="stat"><div class="k">Total interest paid</div><div class="v">'+F.money0(sel.interest)+'</div></div>'+
    '<div class="stat"><div class="k">Total paid</div><div class="v">'+F.money0(totalBal+sel.interest)+'</div></div>'+
    '<div class="stat"><div class="k">Interest saved vs minimums only</div><div class="v" style="color:var(--green)">'+F.money0(saved)+'</div></div>'+
    '<div class="stat"><div class="k">Total debt</div><div class="v">'+F.money0(totalBal)+'</div></div></div>'+
    '<div class="tbl-wrap" style="max-height:none"><table><thead><tr><th>Strategy</th><th>Payoff time</th><th>Total interest</th></tr></thead><tbody>'+
    '<tr><td>Avalanche (highest APR first)</td><td>'+fmtM(av.months)+'</td><td>'+F.money0(av.interest)+'</td></tr>'+
    '<tr><td>Snowball (smallest balance first)</td><td>'+fmtM(sn.months)+'</td><td>'+F.money0(sn.interest)+'</td></tr></tbody></table></div>'+
    '<p class="sub" style="margin-top:10px">Avalanche pays the least interest. Snowball clears small balances first for quick wins and motivation.</p>';
  }
  F.el('dp_strat').addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;strat=b.dataset.v;[].forEach.call(this.children,function(x){x.classList.toggle('on',x===b);});calc();});
  F.on(ids,calc);calc();
 });
 """,
 "intro_html":"""
  <h2>Snowball vs avalanche: which pays off debt faster?</h2>
  <p>Both methods have you pay the minimum on every debt and then throw a fixed extra amount at one target debt. The difference is which debt you target first. The <strong>avalanche</strong> method targets the highest interest rate first, which mathematically pays the least total interest. The <strong>snowball</strong> method targets the smallest balance first, which clears individual debts quickly and gives you motivating wins.</p>
  <p>As each debt is cleared, its payment rolls onto the next one — the "snowball" effect — so your payoff accelerates over time. This tool runs both strategies on your actual numbers so you can see the trade-off between interest saved and momentum.</p>
  <h3>How to use it</h3>
  <p>Enter each debt balance, its APR, and the minimum payment. Add any extra you can pay each month, then switch between avalanche and snowball to compare. The table always shows both so the difference is clear.</p>
 """,
 "faqs":[
  {"q":"Is the avalanche or snowball method better?","a":"The avalanche method always costs the least in interest and usually clears everything a little sooner, because it attacks your most expensive debt first. The snowball method costs slightly more but eliminates whole debts faster, which many people find more motivating. If the difference in interest is small, pick the one you will actually stick with."},
  {"q":"How does an extra payment help so much?","a":"Every extra dollar goes straight to principal, so it stops accruing interest immediately and, as debts clear, their freed-up minimum payments pile onto the next debt. Even a modest extra payment can cut months or years off your payoff and save a large amount of interest."},
  {"q":"What counts as the minimum payment?","a":"Use the minimum your lender requires each month for that account. For credit cards this is often a small percentage of the balance; enter a realistic flat figure. The extra-payment box is where you add anything above the minimums."},
 ],
})

TOOLS.append({
 "slug":"budget-calculator","cat":"finance","icon":"📊",
 "name":"Budget Calculator (50/30/20)",
 "short":"Split your take-home pay into needs, wants and savings with the 50/30/20 rule.",
 "lede":"Turn your monthly take-home pay into a simple, balanced budget using the popular 50/30/20 rule — 50% needs, 30% wants, 20% savings and debt.",
 "title":"50/30/20 Budget Calculator — Needs, Wants & Savings",
 "desc":"Free 50/30/20 budget calculator. Enter your monthly take-home pay to see how much to spend on needs and wants and how much to save each month.",
 "keywords":"budget calculator, 50/30/20 rule, monthly budget calculator, budgeting",
 "body_html":"""
  <div class="field"><label for="bg_income">Monthly take-home pay <span class="hint">(after tax)</span></label>
    <div class="inp has-pre"><span class="pre">$</span><input id="bg_income" type="number" value="4500" min="0" step="50"></div></div>
  <p class="sub">The 50/30/20 rule splits your after-tax income into three buckets. Adjust the split below if your situation differs (it should add up to 100%).</p>
  <div class="row3">
    <div class="field"><label for="bg_n">Needs</label><div class="inp has-suf"><input id="bg_n" type="number" value="50" min="0" step="1"><span class="suf">%</span></div></div>
    <div class="field"><label for="bg_w">Wants</label><div class="inp has-suf"><input id="bg_w" type="number" value="30" min="0" step="1"><span class="suf">%</span></div></div>
    <div class="field"><label for="bg_s">Savings</label><div class="inp has-suf"><input id="bg_s" type="number" value="20" min="0" step="1"><span class="suf">%</span></div></div>
  </div>
 """,
 "script_js":"""
 document.addEventListener('DOMContentLoaded',function(){var F=window.FIN;
  var ids=['bg_income','bg_n','bg_w','bg_s'];
  function calc(){
   var inc=F.num(F.el('bg_income').value)||0,pn=F.num(F.el('bg_n').value)||0,pw=F.num(F.el('bg_w').value)||0,ps=F.num(F.el('bg_s').value)||0,out=F.el('out');
   if(inc<=0){out.innerHTML='<p class="sub">Enter your monthly take-home pay to build your budget.</p>';return;}
   var sum=pn+pw+ps;var warn=(Math.abs(sum-100)>0.5)?'<div class="callout" style="margin-top:12px">Your percentages add up to '+F.nfmt(sum,0)+'%. For a standard budget they should total 100%.</div>':'';
   var needs=inc*pn/100,wants=inc*pw/100,save=inc*ps/100;
   var segs=[{label:'Needs',value:needs,color:F.C.blue},{label:'Wants',value:wants,color:F.C.amber},{label:'Savings & debt',value:save,color:F.C.green}];
   out.innerHTML='<div class="sub">Monthly budget on '+F.money0(inc)+'</div><div class="big-num" style="font-size:24px">'+F.money0(needs)+' · '+F.money0(wants)+' · '+F.money0(save)+'</div>'+
    '<div class="chart-row">'+F.donut(segs)+F.legend(segs)+'</div>'+
    '<div class="stats"><div class="stat"><div class="k">Needs ('+F.nfmt(pn,0)+'%)</div><div class="v">'+F.money0(needs)+'/mo</div></div>'+
    '<div class="stat"><div class="k">Wants ('+F.nfmt(pw,0)+'%)</div><div class="v">'+F.money0(wants)+'/mo</div></div>'+
    '<div class="stat"><div class="k">Savings &amp; debt ('+F.nfmt(ps,0)+'%)</div><div class="v">'+F.money0(save)+'/mo</div></div>'+
    '<div class="stat"><div class="k">Saved per year</div><div class="v">'+F.money0(save*12)+'</div></div></div>'+warn;
  }
  F.on(ids,calc);calc();
 });
 """,
 "intro_html":"""
  <h2>What is the 50/30/20 budget?</h2>
  <p>The 50/30/20 rule is a simple framework for dividing your after-tax income. Fifty percent goes to <strong>needs</strong> — rent or mortgage, groceries, utilities, insurance, minimum debt payments and transport. Thirty percent goes to <strong>wants</strong> — dining out, subscriptions, hobbies and travel. The final twenty percent goes to <strong>savings and extra debt payments</strong> — an emergency fund, retirement, or paying down loans faster.</p>
  <p>It is popular because it is easy to remember and flexible. If you live somewhere expensive your needs may run higher than 50%; if you are aggressively paying off debt or saving for a goal you might push savings above 20%. Adjust the percentages above to match your real life.</p>
  <h3>Make it work</h3>
  <p>Start from your take-home pay — the amount that actually lands in your account after taxes and deductions. Then check your spending against these targets for a month. Small, consistent shifts from wants into savings compound into big results over time.</p>
 """,
 "faqs":[
  {"q":"Should I use gross or take-home pay?","a":"Use your take-home (net) pay — what you receive after taxes and payroll deductions. The 50/30/20 split is designed around the money you can actually direct each month."},
  {"q":"What if my needs are more than 50%?","a":"That is common in high-cost areas. Trim the wants bucket first, and treat 20% savings as a target to grow toward. Even saving 5–10% consistently is far better than nothing, and raises or reduced expenses can move you closer to the ideal split over time."},
 ],
})

TOOLS.append({
 "slug":"retirement-calculator","cat":"finance","icon":"🏖️",
 "name":"Retirement Calculator",
 "short":"Project your retirement nest egg and the income it could provide.",
 "lede":"Project how much you could have saved by retirement from your current savings and monthly contributions, and estimate the yearly income it might provide.",
 "title":"Retirement Calculator — Nest Egg & Retirement Income",
 "desc":"Free retirement calculator: project your retirement savings from monthly contributions and expected returns, and estimate annual retirement income.",
 "keywords":"retirement calculator, retirement savings calculator, 401k calculator, nest egg calculator",
 "body_html":"""
  <div class="row2">
    <div class="field"><label for="ret_now">Current age</label><input id="ret_now" type="number" value="30" min="0" max="100"></div>
    <div class="field"><label for="ret_at">Retirement age</label><input id="ret_at" type="number" value="65" min="1" max="100"></div>
  </div>
  <div class="row2">
    <div class="field"><label for="ret_have">Current savings</label>
      <div class="inp has-pre"><span class="pre">$</span><input id="ret_have" type="number" value="25000" min="0" step="1000"></div></div>
    <div class="field"><label for="ret_pmt">Monthly contribution</label>
      <div class="inp has-pre"><span class="pre">$</span><input id="ret_pmt" type="number" value="500" min="0" step="50"></div></div>
  </div>
  <div class="field"><label for="ret_rate">Expected annual return</label>
    <div class="inp has-suf"><input id="ret_rate" type="number" value="7" min="0" step="0.1"><span class="suf">%</span></div></div>
 """,
 "script_js":"""
 document.addEventListener('DOMContentLoaded',function(){var F=window.FIN;
  var ids=['ret_now','ret_at','ret_have','ret_pmt','ret_rate'];
  function calc(){
   var now=F.num(F.el('ret_now').value)||0,at=F.num(F.el('ret_at').value)||0,have=F.num(F.el('ret_have').value)||0,pmt=F.num(F.el('ret_pmt').value)||0,rate=F.num(F.el('ret_rate').value)||0,out=F.el('out');
   var years=Math.round(at-now);
   if(!(years>0)){out.innerHTML='<p class="sub">Set a retirement age above your current age to project your savings.</p>';return;}
   var r=rate/100/12,n=years*12;
   var fv=F.futureValue(have,pmt,r,n),contrib=have+pmt*n,growth=fv-contrib,income=fv*0.04;
   var segs=[{label:'Contributions',value:contrib,color:F.C.blue},{label:'Investment growth',value:Math.max(growth,0),color:F.C.green}];
   var rows='';for(var y=1;y<=years;y++){var v=F.futureValue(have,pmt,r,y*12),cc=have+pmt*y*12;rows+='<tr><td>'+(now+y)+'</td><td>'+F.money0(cc)+'</td><td>'+F.money0(v-cc)+'</td><td>'+F.money0(v)+'</td></tr>';}
   out.innerHTML='<div class="sub">Projected savings at age '+at+'</div><div class="big-num">'+F.money0(fv)+'</div>'+
    '<div class="chart-row">'+F.donut(segs)+F.legend(segs)+'</div>'+
    '<div class="stats"><div class="stat"><div class="k">Total contributions</div><div class="v">'+F.money0(contrib)+'</div></div>'+
    '<div class="stat"><div class="k">Investment growth</div><div class="v">'+F.money0(Math.max(growth,0))+'</div></div>'+
    '<div class="stat"><div class="k">Est. annual income (4% rule)</div><div class="v">'+F.money0(income)+'</div></div>'+
    '<div class="stat"><div class="k">Est. monthly income</div><div class="v">'+F.money0(income/12)+'</div></div></div>'+
    '<div class="tbl-wrap"><table><thead><tr><th>Age</th><th>Contributions</th><th>Growth</th><th>Balance</th></tr></thead><tbody>'+rows+'</tbody></table></div>';
  }
  F.on(ids,calc);calc();
 });
 """,
 "intro_html":"""
  <h2>How much will you have at retirement?</h2>
  <p>This calculator grows your current savings and your ongoing monthly contributions at an expected annual return, compounded monthly, until your target retirement age. It then applies the well-known <strong>4% rule</strong> to estimate how much annual income that nest egg could safely provide — a rough guide that a portfolio can support withdrawals of about 4% in the first year, adjusted for inflation thereafter.</p>
  <h3>The formula</h3>
  <p>Future value combines a lump sum and a stream of deposits: <code>FV = P(1+r)ⁿ + PMT·[((1+r)ⁿ − 1) / r]</code>, where <code>P</code> is what you have now, <code>PMT</code> is the monthly contribution, <code>r</code> is the monthly return, and <code>n</code> is the months until retirement. Because of compounding, contributions made in your early years do far more work than the same dollars added later.</p>
 """,
 "faqs":[
  {"q":"What return rate should I assume?","a":"For a long-term, stock-heavy retirement portfolio many people model 6%–8% before inflation, though real returns vary widely year to year and are not guaranteed. If you want to think in today's dollars, use a lower 'real' return such as 4%–5% to account for inflation."},
  {"q":"What is the 4% rule?","a":"It is a rough retirement guideline suggesting you can withdraw about 4% of your portfolio in the first year of retirement, then adjust for inflation, with a good chance of the money lasting around 30 years. It is a starting point for planning, not a guarantee — your own plan should reflect your situation and may warrant professional advice."},
  {"q":"Does this include my employer match or 401(k)?","a":"Include any employer match in your monthly contribution figure to capture that free growth. The calculator treats all contributions the same regardless of the account type they go into."},
 ],
})

TOOLS.append({
 "slug":"credit-card-payoff-calculator","cat":"finance","icon":"💳",
 "name":"Credit Card Payoff Calculator",
 "short":"See how long it takes to clear a card — or the payment needed to hit a date.",
 "lede":"Find out how long it will take to pay off a credit card at a fixed monthly payment, or the payment needed to be debt-free by a target month — plus the interest cost.",
 "title":"Credit Card Payoff Calculator — Time & Interest",
 "desc":"Free credit card payoff calculator. See how many months to clear your balance at a set payment, or the monthly payment needed to pay it off by a target date.",
 "keywords":"credit card payoff calculator, credit card interest calculator, pay off credit card",
 "body_html":"""
  <div class="field"><label for="cc_bal">Card balance</label>
    <div class="inp has-pre"><span class="pre">$</span><input id="cc_bal" type="number" value="5000" min="0" step="100"></div></div>
  <div class="field"><label for="cc_apr">Interest rate (APR)</label>
    <div class="inp has-suf"><input id="cc_apr" type="number" value="22" min="0" step="0.1"><span class="suf">%</span></div></div>
  <div class="field"><label>Solve for</label>
    <div class="seg" id="cc_mode"><button data-v="pay" class="on">Fixed payment</button><button data-v="time">Target months</button></div></div>
  <div class="field" id="cc_pay_f"><label for="cc_pay">Monthly payment</label>
    <div class="inp has-pre"><span class="pre">$</span><input id="cc_pay" type="number" value="200" min="0" step="10"></div></div>
  <div class="field" id="cc_mon_f" style="display:none"><label for="cc_mon">Pay off in</label>
    <div class="inp has-suf"><input id="cc_mon" type="number" value="24" min="1" step="1"><span class="suf">months</span></div></div>
 """,
 "script_js":"""
 document.addEventListener('DOMContentLoaded',function(){var F=window.FIN;var mode='pay';
  function payoff(bal,apr,pay){var r=apr/100/12,m=0,ti=0,cap=1200;while(bal>0.005){if(m>=cap)return{never:true};var i=bal*r;var pr=pay-i;if(pr<=0)return{never:true};if(pr>bal)pr=bal;bal-=pr;ti+=i;m++;}return{months:m,interest:ti};}
  function fmtM(m){var y=Math.floor(m/12),mo=m%12;return (y>0?y+' yr ':'')+mo+' mo';}
  function calc(){
   var bal=F.num(F.el('cc_bal').value)||0,apr=F.num(F.el('cc_apr').value)||0,out=F.el('out');
   if(bal<=0){out.innerHTML='<p class="sub">Enter your card balance to begin.</p>';return;}
   if(mode==='pay'){
    var pay=F.num(F.el('cc_pay').value)||0;var res=payoff(bal,apr,pay);
    if(res.never){out.innerHTML='<div class="callout" style="background:#fef2f2;border-color:#fecaca;color:#991b1b">A payment of '+F.money0(pay)+' does not cover the monthly interest of '+F.money(bal*apr/100/12)+', so the balance would never be paid off. Increase the payment.</div>';return;}
    var segs=[{label:'Principal',value:bal,color:F.C.blue},{label:'Interest',value:res.interest,color:F.C.red}];
    out.innerHTML='<div class="sub">Time to pay off</div><div class="big-num">'+fmtM(res.months)+'</div>'+
     '<div class="chart-row">'+F.donut(segs)+F.legend(segs)+'</div>'+
     '<div class="stats"><div class="stat"><div class="k">Total interest</div><div class="v">'+F.money0(res.interest)+'</div></div>'+
     '<div class="stat"><div class="k">Total paid</div><div class="v">'+F.money0(bal+res.interest)+'</div></div></div>';
   } else {
    var months=Math.round(F.num(F.el('cc_mon').value)||0);
    if(!(months>0)){out.innerHTML='<p class="sub">Enter a target number of months.</p>';return;}
    var pmt=F.pmt(bal,apr,months),interest=pmt*months-bal;
    var segs2=[{label:'Principal',value:bal,color:F.C.blue},{label:'Interest',value:Math.max(interest,0),color:F.C.red}];
    out.innerHTML='<div class="sub">Pay this each month</div><div class="big-num">'+F.money(pmt)+'</div>'+
     '<div class="chart-row">'+F.donut(segs2)+F.legend(segs2)+'</div>'+
     '<div class="stats"><div class="stat"><div class="k">Total interest</div><div class="v">'+F.money0(Math.max(interest,0))+'</div></div>'+
     '<div class="stat"><div class="k">Total paid</div><div class="v">'+F.money0(bal+Math.max(interest,0))+'</div></div></div>';
   }
  }
  F.el('cc_mode').addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;mode=b.dataset.v;[].forEach.call(this.children,function(x){x.classList.toggle('on',x===b);});
   F.el('cc_pay_f').style.display=mode==='pay'?'':'none';F.el('cc_mon_f').style.display=mode==='time'?'':'none';calc();});
  F.on(['cc_bal','cc_apr','cc_pay','cc_mon'],calc);calc();
 });
 """,
 "intro_html":"""
  <h2>Pay off your credit card faster</h2>
  <p>Credit cards charge interest on your remaining balance every month, so a large chunk of a small payment can go straight to interest rather than reducing what you owe. This calculator works two ways: enter a fixed monthly payment to see how long the balance takes to clear and what it costs in interest, or set a target number of months to find the payment required to get there.</p>
  <h3>Why the minimum payment traps you</h3>
  <p>Paying only the minimum stretches a balance out for years and multiplies the interest. Because interest is charged on the balance, every extra dollar you pay reduces all future interest too. Try nudging the payment up and watch both the payoff time and total interest fall sharply.</p>
 """,
 "faqs":[
  {"q":"Why does my balance barely move?","a":"If your payment is only slightly above the monthly interest, almost all of it goes to interest and very little to principal. Raising the payment even a little dramatically shortens the payoff time because the extra goes entirely toward the balance."},
  {"q":"What if my payment does not cover the interest?","a":"Then the balance grows every month and the card can never be paid off — the calculator will warn you. You need a payment above the first month's interest charge, ideally well above it, to make real progress."},
  {"q":"Could a balance transfer help?","a":"A 0% or low-rate balance-transfer offer can pause interest so more of each payment reduces principal, but watch for transfer fees and the rate after the promotional period ends. Compare the total cost before moving a balance."},
 ],
})

TOOLS.append({
 "slug":"rent-vs-buy-calculator","cat":"finance","icon":"🔑",
 "name":"Rent vs Buy Calculator",
 "short":"Compare the true cost of renting versus buying a home over your time frame.",
 "lede":"Compare renting against buying over the years you plan to stay — accounting for the mortgage, taxes, maintenance, home appreciation, rent increases and investing the difference.",
 "title":"Rent vs Buy Calculator — Which Is Cheaper?",
 "desc":"Free rent vs buy calculator. Compare the net worth of renting and investing versus buying a home over your time horizon, including all major costs.",
 "keywords":"rent vs buy calculator, should i rent or buy, buy vs rent home calculator",
 "body_html":"""
  <div class="field"><label for="rb_price">Home price</label>
    <div class="inp has-pre"><span class="pre">$</span><input id="rb_price" type="number" value="400000" min="0" step="5000"></div></div>
  <div class="row2">
    <div class="field"><label for="rb_down">Down payment</label>
      <div class="inp has-suf"><input id="rb_down" type="number" value="20" min="0" max="100" step="1"><span class="suf">%</span></div></div>
    <div class="field"><label for="rb_rate">Mortgage rate</label>
      <div class="inp has-suf"><input id="rb_rate" type="number" value="6.5" min="0" step="0.01"><span class="suf">%</span></div></div>
  </div>
  <div class="row2">
    <div class="field"><label for="rb_term">Loan term <span class="hint">(yrs)</span></label><input id="rb_term" type="number" value="30" min="1" max="40"></div>
    <div class="field"><label for="rb_years">Years you will stay</label><input id="rb_years" type="number" value="7" min="1" max="40"></div>
  </div>
  <div class="row2">
    <div class="field"><label for="rb_rent">Monthly rent</label>
      <div class="inp has-pre"><span class="pre">$</span><input id="rb_rent" type="number" value="2200" min="0" step="50"></div></div>
    <div class="field"><label for="rb_rentinc">Rent increase <span class="hint">(/yr)</span></label>
      <div class="inp has-suf"><input id="rb_rentinc" type="number" value="3" min="0" step="0.1"><span class="suf">%</span></div></div>
  </div>
  <p class="sub" style="margin:16px 0 8px;font-weight:600;color:#334155">Assumptions</p>
  <div class="row3">
    <div class="field"><label for="rb_tax">Prop. tax <span class="hint">/yr</span></label><div class="inp has-suf"><input id="rb_tax" type="number" value="1.2" min="0" step="0.1"><span class="suf">%</span></div></div>
    <div class="field"><label for="rb_ins">Insurance <span class="hint">/yr</span></label><div class="inp has-suf"><input id="rb_ins" type="number" value="0.5" min="0" step="0.1"><span class="suf">%</span></div></div>
    <div class="field"><label for="rb_maint">Upkeep <span class="hint">/yr</span></label><div class="inp has-suf"><input id="rb_maint" type="number" value="1" min="0" step="0.1"><span class="suf">%</span></div></div>
  </div>
  <div class="row3">
    <div class="field"><label for="rb_appr">Home growth</label><div class="inp has-suf"><input id="rb_appr" type="number" value="3" min="0" step="0.1"><span class="suf">%</span></div></div>
    <div class="field"><label for="rb_inv">Invest return</label><div class="inp has-suf"><input id="rb_inv" type="number" value="6" min="0" step="0.1"><span class="suf">%</span></div></div>
    <div class="field"><label for="rb_sell">Buy+sell cost</label><div class="inp has-suf"><input id="rb_sell" type="number" value="8" min="0" step="0.1"><span class="suf">%</span></div></div>
  </div>
 """,
 "script_js":"""
 document.addEventListener('DOMContentLoaded',function(){var F=window.FIN;
  var ids=['rb_price','rb_down','rb_rate','rb_term','rb_years','rb_rent','rb_rentinc','rb_tax','rb_ins','rb_maint','rb_appr','rb_inv','rb_sell'];
  function calc(){
   var price=F.num(F.el('rb_price').value)||0,downp=F.num(F.el('rb_down').value)||0,rate=F.num(F.el('rb_rate').value)||0,
       term=F.num(F.el('rb_term').value)||0,years=Math.round(F.num(F.el('rb_years').value)||0),rent0=F.num(F.el('rb_rent').value)||0,
       rinc=F.num(F.el('rb_rentinc').value)||0,tax=F.num(F.el('rb_tax').value)||0,ins=F.num(F.el('rb_ins').value)||0,
       maint=F.num(F.el('rb_maint').value)||0,appr=F.num(F.el('rb_appr').value)||0,inv=F.num(F.el('rb_inv').value)||0,sell=F.num(F.el('rb_sell').value)||0;
   var out=F.el('out');
   if(price<=0||!(years>0)){out.innerHTML='<p class="sub">Enter a home price and how long you plan to stay.</p>';return;}
   var down=price*downp/100,loan=price-down,termM=Math.round(term*12),N=years*12;
   var closing=price*(sell/100)/2;
   var upfront=down+closing;
   var pi=F.pmt(loan,rate,termM),r=rate/100/12,invM=inv/100/12;
   var bal=loan,buyInv=0,rentInv=upfront;
   for(var m=1;m<=N;m++){
    var y=Math.floor((m-1)/12);
    var hv=price*Math.pow(1+appr/100,y),rentCur=rent0*Math.pow(1+rinc/100,y);
    var piThis=0;
    if(m<=termM&&bal>0.005){var it=bal*r;var pr=pi-it;if(pr>bal)pr=bal;bal-=pr;piThis=it+pr;}
    var costBuy=piThis+hv*(tax/100)/12+hv*(ins/100)/12+hv*(maint/100)/12;
    var costRent=rentCur;
    var budget=Math.max(costBuy,costRent);
    buyInv=buyInv*(1+invM)+(budget-costBuy);
    rentInv=rentInv*(1+invM)+(budget-costRent);
   }
   var hvEnd=price*Math.pow(1+appr/100,years);
   var equity=hvEnd*(1-sell/100/2)-Math.max(bal,0);
   var buyNW=equity+buyInv,rentNW=rentInv,diff=buyNW-rentNW;
   var winner=diff>=0?'Buying':'Renting',color=diff>=0?F.C.green:F.C.blue;
   out.innerHTML='<div class="sub">Over '+years+' years, the better financial choice is</div>'+
    '<div class="big-num" style="color:'+color+'">'+winner+'</div>'+
    '<div class="sub">ahead by '+F.money0(Math.abs(diff))+' in net worth</div>'+
    '<div class="stats" style="margin-top:14px"><div class="stat"><div class="k">Net worth if you buy</div><div class="v">'+F.money0(buyNW)+'</div></div>'+
    '<div class="stat"><div class="k">Net worth if you rent &amp; invest</div><div class="v">'+F.money0(rentNW)+'</div></div>'+
    '<div class="stat"><div class="k">Home value at sale</div><div class="v">'+F.money0(hvEnd)+'</div></div>'+
    '<div class="stat"><div class="k">Home equity after selling</div><div class="v">'+F.money0(equity)+'</div></div></div>'+
    '<p class="sub" style="margin-top:12px">Both scenarios assume the same monthly budget: whoever has the cheaper option each month invests the difference at your investment return. Buying costs include the mortgage, taxes, insurance, upkeep and buying/selling fees.</p>';
  }
  F.on(ids,calc);calc();
 });
 """,
 "intro_html":"""
  <h2>Is it cheaper to rent or buy?</h2>
  <p>There is no universal answer — it depends on prices, rates, how long you stay, and what you would do with the money you do not tie up in a house. This calculator compares the two paths fairly by tracking <strong>net worth</strong>. The buyer builds home equity but pays a mortgage, taxes, insurance, upkeep and transaction fees. The renter invests the down payment and any monthly savings instead. Whoever ends the period with more wealth "wins".</p>
  <h3>Why time horizon matters</h3>
  <p>Buying carries large upfront and selling costs, so it usually needs several years for home equity and appreciation to overcome them — the classic "break-even horizon". Stay only a couple of years and renting often wins; stay a long time and buying tends to pull ahead. Adjust the years-you-will-stay field to find the tipping point for your numbers.</p>
 """,
 "faqs":[
  {"q":"How is this comparison kept fair?","a":"Each month both scenarios spend the same total: whichever option is cheaper that month, the difference is invested at your chosen investment return. The renter also invests the down payment and closing costs the buyer would have spent upfront. At the end we compare total net worth — the buyer's home equity plus investments versus the renter's investment portfolio."},
  {"q":"What is the 'buy+sell cost'?","a":"It bundles the one-time costs of purchasing and later selling a home — closing costs, agent commissions and fees — as a percentage of the price. The calculator splits it between the purchase and the eventual sale. These costs are a big reason buying rarely pays off over very short stays."},
  {"q":"Does this account for the tax benefits of owning?","a":"It focuses on cash costs, equity and investment growth rather than mortgage-interest deductions, which many households no longer itemize for. Treat the result as a strong directional estimate; your own taxes, rent and market may shift the exact break-even point."},
 ],
})

TOOLS.append({
 "slug":"net-worth-calculator","cat":"finance","icon":"🧮",
 "name":"Net Worth Calculator",
 "short":"Add up what you own and owe to find your total net worth.",
 "lede":"Total your assets and subtract your debts to find your net worth — a single number that shows your overall financial position and how it is made up.",
 "title":"Net Worth Calculator — Assets Minus Liabilities",
 "desc":"Free net worth calculator. Add your cash, investments, property and other assets, subtract your debts, and see your total net worth with a breakdown.",
 "keywords":"net worth calculator, assets and liabilities calculator, personal net worth",
 "body_html":"""
  <p class="sub" style="margin:0 0 10px;font-weight:600;color:#334155">Assets — what you own</p>
  <div class="row2">
    <div class="field"><label for="nw_cash">Cash &amp; savings</label><div class="inp has-pre"><span class="pre">$</span><input id="nw_cash" type="number" value="15000" min="0" step="500"></div></div>
    <div class="field"><label for="nw_inv">Investments</label><div class="inp has-pre"><span class="pre">$</span><input id="nw_inv" type="number" value="30000" min="0" step="500"></div></div>
  </div>
  <div class="row2">
    <div class="field"><label for="nw_ret">Retirement accounts</label><div class="inp has-pre"><span class="pre">$</span><input id="nw_ret" type="number" value="45000" min="0" step="500"></div></div>
    <div class="field"><label for="nw_home">Home value</label><div class="inp has-pre"><span class="pre">$</span><input id="nw_home" type="number" value="350000" min="0" step="1000"></div></div>
  </div>
  <div class="row2">
    <div class="field"><label for="nw_auto">Vehicles</label><div class="inp has-pre"><span class="pre">$</span><input id="nw_auto" type="number" value="18000" min="0" step="500"></div></div>
    <div class="field"><label for="nw_other">Other assets</label><div class="inp has-pre"><span class="pre">$</span><input id="nw_other" type="number" value="5000" min="0" step="500"></div></div>
  </div>
  <p class="sub" style="margin:16px 0 10px;font-weight:600;color:#334155">Liabilities — what you owe</p>
  <div class="row2">
    <div class="field"><label for="nw_mort">Mortgage</label><div class="inp has-pre"><span class="pre">$</span><input id="nw_mort" type="number" value="240000" min="0" step="1000"></div></div>
    <div class="field"><label for="nw_carl">Auto loans</label><div class="inp has-pre"><span class="pre">$</span><input id="nw_carl" type="number" value="9000" min="0" step="500"></div></div>
  </div>
  <div class="row2">
    <div class="field"><label for="nw_stud">Student loans</label><div class="inp has-pre"><span class="pre">$</span><input id="nw_stud" type="number" value="12000" min="0" step="500"></div></div>
    <div class="field"><label for="nw_cc">Credit cards</label><div class="inp has-pre"><span class="pre">$</span><input id="nw_cc" type="number" value="3000" min="0" step="100"></div></div>
  </div>
  <div class="field"><label for="nw_odebt">Other debts</label><div class="inp has-pre"><span class="pre">$</span><input id="nw_odebt" type="number" value="0" min="0" step="100"></div></div>
 """,
 "script_js":"""
 document.addEventListener('DOMContentLoaded',function(){var F=window.FIN;
  var assetIds=['nw_cash','nw_inv','nw_ret','nw_home','nw_auto','nw_other'];
  var debtIds=['nw_mort','nw_carl','nw_stud','nw_cc','nw_odebt'];
  function calc(){
   var a=0;assetIds.forEach(function(i){a+=F.num(F.el(i).value)||0;});
   var l=0;debtIds.forEach(function(i){l+=F.num(F.el(i).value)||0;});
   var nw=a-l,out=F.el('out');
   var segs=[{label:'Cash & savings',value:F.num(F.el('nw_cash').value)||0,color:F.C.blue},
     {label:'Investments',value:F.num(F.el('nw_inv').value)||0,color:F.C.violet},
     {label:'Retirement',value:F.num(F.el('nw_ret').value)||0,color:F.C.green},
     {label:'Home',value:F.num(F.el('nw_home').value)||0,color:F.C.amber},
     {label:'Vehicles & other',value:(F.num(F.el('nw_auto').value)||0)+(F.num(F.el('nw_other').value)||0),color:F.C.slate}];
   out.innerHTML='<div class="sub">Your net worth</div><div class="big-num" style="color:'+(nw>=0?F.C.green:F.C.red)+'">'+F.money0(nw)+'</div>'+
    '<div class="stats"><div class="stat"><div class="k">Total assets</div><div class="v">'+F.money0(a)+'</div></div>'+
    '<div class="stat"><div class="k">Total liabilities</div><div class="v">'+F.money0(l)+'</div></div></div>'+
    '<p class="sub" style="margin:16px 0 6px;font-weight:600;color:#334155">How your assets break down</p>'+
    '<div class="chart-row">'+F.donut(segs)+F.legend(segs)+'</div>';
  }
  F.on(assetIds.concat(debtIds),calc);calc();
 });
 """,
 "intro_html":"""
  <h2>What is net worth?</h2>
  <p>Net worth is simply everything you own (your assets) minus everything you owe (your liabilities). It is the clearest single snapshot of your financial health. A positive and rising net worth means you are building wealth; a negative figure — common early in life with student loans or a new mortgage — is a starting point to grow from.</p>
  <h3>Assets and liabilities</h3>
  <p>Assets include cash and savings, investment and retirement accounts, the market value of your home and vehicles, and anything else of value. Liabilities include your mortgage, car and student loans, credit-card balances and any other debts. Enter current values for the most accurate picture.</p>
  <p>Tracking this number once or twice a year is one of the most motivating habits in personal finance — it captures the combined effect of saving, investing and paying down debt in one place.</p>
 """,
 "faqs":[
  {"q":"Should I include my home in net worth?","a":"Yes — include your home's current market value as an asset and the remaining mortgage as a liability. The difference is your home equity, which is a real part of your wealth even though it is not easily spendable."},
  {"q":"Is a negative net worth bad?","a":"Not necessarily. Many people have negative net worth early on due to student loans or a recent home purchase. What matters most is the trend: consistent saving, investing and debt repayment move the number in the right direction over time."},
 ],
})

# ==================== PHASE 3 — FINANCE ====================

TOOLS.append({
 "slug":"refinance-calculator","cat":"finance","icon":"🔁",
 "name":"Mortgage Refinance Calculator",
 "short":"See your new payment, monthly savings and break-even point on a refinance.",
 "lede":"Compare your current mortgage with a new one to see the new monthly payment, how much you would save each month, and how long it takes to break even on closing costs.",
 "title":"Refinance Calculator — Payment, Savings & Break-Even",
 "desc":"Free mortgage refinance calculator. Compare your current loan to a new rate and term to see monthly savings, break-even months and lifetime interest saved.",
 "keywords":"refinance calculator, mortgage refinance calculator, refinance break even calculator",
 "body_html":"""
  <p class="sub" style="margin:0 0 10px;font-weight:600;color:#334155">Current loan</p>
  <div class="field"><label for="rf_bal">Remaining balance</label>
    <div class="inp has-pre"><span class="pre">$</span><input id="rf_bal" type="number" value="250000" min="0" step="1000"></div></div>
  <div class="row2">
    <div class="field"><label for="rf_rate">Current rate</label><div class="inp has-suf"><input id="rf_rate" type="number" value="7.5" min="0" step="0.01"><span class="suf">%</span></div></div>
    <div class="field"><label for="rf_left">Years left</label><input id="rf_left" type="number" value="25" min="1" max="40" step="0.5"></div>
  </div>
  <p class="sub" style="margin:16px 0 10px;font-weight:600;color:#334155">New loan</p>
  <div class="row2">
    <div class="field"><label for="rf_nrate">New rate</label><div class="inp has-suf"><input id="rf_nrate" type="number" value="6" min="0" step="0.01"><span class="suf">%</span></div></div>
    <div class="field"><label for="rf_nterm">New term <span class="hint">(yrs)</span></label><input id="rf_nterm" type="number" value="25" min="1" max="40"></div>
  </div>
  <div class="field"><label for="rf_close">Closing costs</label>
    <div class="inp has-pre"><span class="pre">$</span><input id="rf_close" type="number" value="4000" min="0" step="100"></div></div>
 """,
 "script_js":"""
 document.addEventListener('DOMContentLoaded',function(){var F=window.FIN;
  var ids=['rf_bal','rf_rate','rf_left','rf_nrate','rf_nterm','rf_close'];
  function calc(){
   var bal=F.num(F.el('rf_bal').value)||0,rate=F.num(F.el('rf_rate').value)||0,left=F.num(F.el('rf_left').value)||0,
       nrate=F.num(F.el('rf_nrate').value)||0,nterm=F.num(F.el('rf_nterm').value)||0,close=F.num(F.el('rf_close').value)||0,out=F.el('out');
   var lm=Math.round(left*12),nm=Math.round(nterm*12);
   if(bal<=0||!(lm>0)||!(nm>0)){out.innerHTML='<p class="sub">Enter your current balance and terms to compare.</p>';return;}
   var curPay=F.pmt(bal,rate,lm),newPay=F.pmt(bal,nrate,nm);
   var curInt=curPay*lm-bal,newInt=newPay*nm-bal;
   var save=curPay-newPay;
   var be=save>0?close/save:Infinity;
   var lifeSave=(curPay*lm)-(newPay*nm+close);
   var beTxt=isFinite(be)?(Math.ceil(be)+' months ('+F.nfmt(be/12,1)+' yrs)'):'Never — new payment is higher';
   out.innerHTML='<div class="sub">'+(save>=0?'Monthly savings':'Monthly increase')+'</div>'+
    '<div class="big-num" style="color:'+(save>=0?F.C.green:F.C.red)+'">'+F.money(Math.abs(save))+'</div>'+
    '<div class="stats"><div class="stat"><div class="k">Current payment</div><div class="v">'+F.money0(curPay)+'/mo</div></div>'+
    '<div class="stat"><div class="k">New payment</div><div class="v">'+F.money0(newPay)+'/mo</div></div>'+
    '<div class="stat"><div class="k">Break-even on costs</div><div class="v">'+beTxt+'</div></div>'+
    '<div class="stat"><div class="k">Lifetime savings</div><div class="v" style="color:'+(lifeSave>=0?F.C.green:F.C.red)+'">'+F.money0(lifeSave)+'</div></div></div>'+
    '<div class="tbl-wrap" style="max-height:none"><table><thead><tr><th></th><th>Payment</th><th>Total interest</th></tr></thead><tbody>'+
    '<tr><td>Current loan</td><td>'+F.money0(curPay)+'</td><td>'+F.money0(curInt)+'</td></tr>'+
    '<tr><td>New loan</td><td>'+F.money0(newPay)+'</td><td>'+F.money0(newInt)+'</td></tr></tbody></table></div>'+
    '<p class="sub" style="margin-top:10px">Lifetime savings compares the total of all remaining payments on each loan, including closing costs on the new one.</p>';
  }
  F.on(ids,calc);calc();
 });
 """,
 "intro_html":"""
  <h2>Should you refinance your mortgage?</h2>
  <p>Refinancing replaces your current mortgage with a new one, usually to get a lower rate or change the term. The catch is closing costs, so the key question is the <strong>break-even point</strong> — how many months of savings it takes to recover those upfront costs. If you will keep the home well past break-even, refinancing usually makes sense; if you might move sooner, it may not.</p>
  <h3>What this calculator shows</h3>
  <p>Enter your remaining balance, current rate and years left, then the new rate, term and closing costs. You will see the new monthly payment, your monthly saving, the break-even month, and the total interest and lifetime cost of each loan side by side.</p>
  <p>Watch the term: refinancing a loan with 25 years left into a fresh 30-year term can lower the monthly payment while actually increasing total interest. Matching or shortening the term captures more of the benefit of a lower rate.</p>
 """,
 "faqs":[
  {"q":"What is the refinance break-even point?","a":"It is the number of months of payment savings needed to cover your closing costs — closing costs divided by monthly savings. If you plan to stay in the home longer than the break-even period, refinancing typically pays off; if not, the upfront costs may outweigh the savings."},
  {"q":"Does a lower payment always mean a better deal?","a":"No. Stretching the loan back out to a longer term lowers the monthly payment but can raise the total interest you pay over time. Compare the lifetime figures, not just the monthly payment, and keep the term as short as you can comfortably afford."},
  {"q":"Should I roll closing costs into the loan?","a":"You can, which avoids paying cash upfront, but it increases your balance and the interest you pay on it. This calculator treats closing costs as paid upfront; if you finance them, your real savings will be a little lower."},
 ],
})

TOOLS.append({
 "slug":"house-affordability-calculator","cat":"finance","icon":"🏡",
 "name":"House Affordability Calculator",
 "short":"Find the home price you can afford based on income, debts and down payment.",
 "lede":"Estimate how much house you can afford using the standard 28/36 debt-to-income guidelines, your down payment, and current rates, taxes and insurance.",
 "title":"How Much House Can I Afford? — Affordability Calculator",
 "desc":"Free house affordability calculator using the 28/36 rule. Estimate the home price you can afford from your income, monthly debts and down payment.",
 "keywords":"house affordability calculator, how much house can i afford, home affordability, 28/36 rule",
 "body_html":"""
  <div class="field"><label for="ha_inc">Annual gross income</label>
    <div class="inp has-pre"><span class="pre">$</span><input id="ha_inc" type="number" value="90000" min="0" step="1000"></div></div>
  <div class="row2">
    <div class="field"><label for="ha_debt">Monthly debt payments</label>
      <div class="inp has-pre"><span class="pre">$</span><input id="ha_debt" type="number" value="400" min="0" step="50"></div></div>
    <div class="field"><label for="ha_down">Down payment</label>
      <div class="inp has-pre"><span class="pre">$</span><input id="ha_down" type="number" value="40000" min="0" step="1000"></div></div>
  </div>
  <div class="row2">
    <div class="field"><label for="ha_rate">Mortgage rate</label><div class="inp has-suf"><input id="ha_rate" type="number" value="6.5" min="0" step="0.01"><span class="suf">%</span></div></div>
    <div class="field"><label for="ha_term">Loan term <span class="hint">(yrs)</span></label><input id="ha_term" type="number" value="30" min="1" max="40"></div>
  </div>
  <div class="row3">
    <div class="field"><label for="ha_tax">Prop. tax <span class="hint">/yr</span></label><div class="inp has-suf"><input id="ha_tax" type="number" value="1.2" min="0" step="0.1"><span class="suf">%</span></div></div>
    <div class="field"><label for="ha_ins">Insurance <span class="hint">/yr</span></label><div class="inp has-suf"><input id="ha_ins" type="number" value="0.5" min="0" step="0.1"><span class="suf">%</span></div></div>
    <div class="field"><label for="ha_dti">Max DTI</label><div class="inp has-suf"><input id="ha_dti" type="number" value="36" min="0" max="60" step="1"><span class="suf">%</span></div></div>
  </div>
 """,
 "script_js":"""
 document.addEventListener('DOMContentLoaded',function(){var F=window.FIN;
  var ids=['ha_inc','ha_debt','ha_down','ha_rate','ha_term','ha_tax','ha_ins','ha_dti'];
  function calc(){
   var inc=F.num(F.el('ha_inc').value)||0,debt=F.num(F.el('ha_debt').value)||0,down=F.num(F.el('ha_down').value)||0,
       rate=F.num(F.el('ha_rate').value)||0,term=F.num(F.el('ha_term').value)||0,tax=F.num(F.el('ha_tax').value)||0,
       ins=F.num(F.el('ha_ins').value)||0,dti=F.num(F.el('ha_dti').value)||36,out=F.el('out');
   var months=Math.round(term*12),monthlyInc=inc/12;
   if(inc<=0||!(months>0)){out.innerHTML='<p class="sub">Enter your income and loan term to estimate affordability.</p>';return;}
   var front=monthlyInc*0.28,back=monthlyInc*(dti/100)-debt;
   var maxPITI=Math.min(front,back),limiter=front<=back?'28% housing ratio':'total debt ratio ('+F.nfmt(dti,0)+'%)';
   if(maxPITI<=0){out.innerHTML='<div class="callout" style="background:#fef2f2;border-color:#fecaca;color:#991b1b">Your existing monthly debts already reach the debt-to-income limit, so there is no room in the budget for a mortgage payment. Reducing other debts would increase what you can afford.</div>';return;}
   var price=down;
   for(var k=0;k<40;k++){
    var mti=price*((tax+ins)/100)/12;
    var pi=maxPITI-mti;
    if(pi<=0){price=down;break;}
    var loan=F.principalFromPayment(pi,rate,months);
    var np=loan+down;
    if(Math.abs(np-price)<1){price=np;break;}
    price=np;
   }
   var loanF=Math.max(price-down,0),piF=F.pmt(loanF,rate,months),mtiF=price*((tax+ins)/100)/12;
   out.innerHTML='<div class="sub">Estimated home price you can afford</div><div class="big-num">'+F.money0(price)+'</div>'+
    '<div class="stats"><div class="stat"><div class="k">Max loan amount</div><div class="v">'+F.money0(loanF)+'</div></div>'+
    '<div class="stat"><div class="k">Monthly payment (PITI)</div><div class="v">'+F.money0(piF+mtiF)+'</div></div>'+
    '<div class="stat"><div class="k">Principal &amp; interest</div><div class="v">'+F.money0(piF)+'/mo</div></div>'+
    '<div class="stat"><div class="k">Taxes &amp; insurance</div><div class="v">'+F.money0(mtiF)+'/mo</div></div></div>'+
    '<p class="sub" style="margin-top:12px">Limited by your '+limiter+'. Lenders generally keep housing costs near 28% of gross income and total debt payments under about 36%.</p>';
  }
  F.on(ids,calc);calc();
 });
 """,
 "intro_html":"""
  <h2>How much house can you afford?</h2>
  <p>Lenders size your loan mostly on your income and existing debts, using two debt-to-income guidelines known as the <strong>28/36 rule</strong>. The front-end ratio says your monthly housing payment should stay around 28% of your gross monthly income. The back-end ratio says all your monthly debt payments — housing plus car loans, student loans and credit cards — should stay under about 36%. This calculator applies both and uses whichever is stricter.</p>
  <h3>What the estimate includes</h3>
  <p>Your maximum monthly housing budget has to cover principal, interest, property tax and insurance (PITI). The calculator works backward from that budget, at your rate and term, to the loan you can support, then adds your down payment to reach an affordable home price. A larger down payment, a lower rate, or clearing other debts all raise the number.</p>
 """,
 "faqs":[
  {"q":"What is the 28/36 rule?","a":"It is a common mortgage affordability guideline. The 28 refers to keeping your monthly housing payment (principal, interest, taxes and insurance) at or below 28% of your gross monthly income. The 36 refers to keeping all monthly debt payments combined at or below 36%. Some loan programs allow higher ratios, which is why you can adjust the max DTI here."},
  {"q":"Does a bigger down payment let me afford more?","a":"Yes. Your income sets the loan you can support through the monthly payment, and your down payment adds directly on top of that to reach the home price. A larger down payment also reduces or removes mortgage insurance, freeing up more of the payment for principal and interest."},
  {"q":"Is the amount I qualify for the amount I should spend?","a":"Not necessarily. These ratios are maximums lenders use; a comfortable budget is often lower, leaving room for savings, emergencies and life goals. Treat the result as a ceiling and choose a payment you feel good about."},
 ],
})

TOOLS.append({
 "slug":"financial-advisor-quiz","cat":"finance","icon":"🧭",
 "name":"Financial Advisor Match Quiz",
 "short":"Answer four questions to see what kind of financial help fits your situation.",
 "lede":"Not sure whether you need a financial advisor, a one-time plan, or a low-cost robo-advisor? Answer four quick questions to see which option best fits your situation.",
 "title":"Financial Advisor Quiz — What Kind of Advice Do You Need?",
 "desc":"Free financial advisor match quiz. Answer four questions about your assets, comfort and goals to see whether a robo-advisor, one-time planner or ongoing advisor fits.",
 "keywords":"financial advisor quiz, do i need a financial advisor, find a financial advisor, fee-only advisor",
 "body_html":"""
  <div class="field"><label>Investable assets (savings &amp; investments, excluding your home)</label>
    <div class="seg wrap" id="fa_assets"><button data-v="1" class="on">Under $50k</button><button data-v="2">$50k–$250k</button><button data-v="3">$250k–$1M</button><button data-v="4">Over $1M</button></div></div>
  <div class="field"><label>How comfortable are you managing money yourself?</label>
    <div class="seg" id="fa_comf"><button data-v="low">Not very</button><button data-v="med" class="on">Somewhat</button><button data-v="high">Very</button></div></div>
  <div class="field"><label>How complex is your situation? <span class="hint">(business, equity comp, taxes, estate)</span></label>
    <div class="seg" id="fa_cplx"><button data-v="simple" class="on">Simple</button><button data-v="some">Some</button><button data-v="complex">Complex</button></div></div>
  <div class="field"><label>What are you mainly looking for?</label>
    <div class="seg wrap" id="fa_want"><button data-v="invest" class="on">Just help investing</button><button data-v="plan">A one-time plan</button><button data-v="ongoing">Ongoing guidance</button></div></div>
 """,
 "script_js":"""
 document.addEventListener('DOMContentLoaded',function(){var F=window.FIN;
  var st={assets:'1',comf:'med',cplx:'simple',want:'invest'};
  function pick(id,key){F.el(id).addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;st[key]=b.dataset.v;[].forEach.call(this.children,function(x){x.classList.toggle('on',x===b);});calc();});}
  function calc(){
   var out=F.el('out');var title,body,tips;
   if(st.cplx==='complex'||st.assets==='4'){
    title='An experienced advisor for complex needs';
    body='With a larger portfolio or a complex situation — a business, equity compensation, estate planning or complicated taxes — coordinated advice usually pays for itself. Look for a fee-only Certified Financial Planner (CFP) or a fee-only wealth manager who works with clients like you and can bring in tax and estate expertise.';
   } else if(st.want==='invest'&&st.comf!=='low'){
    title='A robo-advisor or low-cost DIY investing';
    body='Your situation is straightforward and you are comfortable enough to keep things simple. A low-cost robo-advisor or a portfolio of broad index funds can handle diversified investing for a very small fee, without the cost of a full advisor. You can always add human advice later as your finances grow.';
   } else if(st.want==='plan'||(st.comf==='high'&&st.want!=='ongoing')){
    title='A one-time, fee-only financial plan';
    body='You mostly need a clear plan you can then run yourself. Consider an hourly or flat-fee CFP who will build a financial plan — covering saving, investing, debt and goals — as a one-off engagement. You get professional guidance without committing to ongoing fees.';
   } else if(st.want==='ongoing'||st.comf==='low'){
    title='An ongoing fee-only fiduciary advisor';
    body='You would value a professional in your corner over time. Look for a fee-only CFP who acts as a fiduciary and charges a flat or hourly fee (or a transparent percentage). They can manage investments and revisit your plan as life changes, so you are not navigating big decisions alone.';
   } else {
    title='A one-time financial plan to get started';
    body='A single session with a fee-only planner is a low-commitment way to get organized and confident, after which you can decide whether ongoing help is worth it.';
   }
   tips='<p class="sub" style="margin:14px 0 6px;font-weight:600;color:#334155">What to look for in an advisor</p>'+
    '<ul style="margin:0;padding-left:18px;color:#334155;font-size:14.5px;line-height:1.7">'+
    '<li><strong>Fiduciary:</strong> they are legally required to act in your best interest.</li>'+
    '<li><strong>Fee-only:</strong> paid by you, not by commissions on products they sell.</li>'+
    '<li><strong>Credentials:</strong> the CFP designation signals broad, tested competence.</li>'+
    '<li><strong>Clear fees:</strong> ask exactly how they are paid — flat, hourly or a percentage of assets.</li></ul>'+
    '<p class="sub" style="margin-top:10px">Directories to find fee-only fiduciaries include NAPFA, the CFP Board&rsquo;s Let&rsquo;s Make a Plan, and the XY Planning Network. This tool is educational and does not share your answers with anyone.</p>';
   out.innerHTML='<div class="sub">Based on your answers, consider</div><div class="big-num" style="font-size:22px;line-height:1.3">'+title+'</div>'+
    '<p style="color:#334155;font-size:15px;margin:12px 0 0">'+body+'</p>'+tips;
  }
  pick('fa_assets','assets');pick('fa_comf','comf');pick('fa_cplx','cplx');pick('fa_want','want');
  calc();
 });
 """,
 "intro_html":"""
  <h2>Do you actually need a financial advisor?</h2>
  <p>The right kind of financial help depends on how complex your finances are, how confident you feel managing money, and what you want out of the relationship. Some people are best served by a low-cost robo-advisor or simple index funds; others benefit from a one-time plan; and those with more assets or complexity often want an ongoing professional. This short quiz points you toward the option that tends to fit best.</p>
  <h3>Fee-only and fiduciary — the two words that matter</h3>
  <p>Whatever route you choose, favour advisors who are <strong>fee-only</strong> (paid directly by you rather than by commissions) and who act as a <strong>fiduciary</strong> (legally bound to put your interests first). The Certified Financial Planner (CFP) credential is a widely respected mark of competence. Always ask exactly how an advisor is paid before you engage them.</p>
  <div class="callout"><strong>Note:</strong> This quiz is general education, not personalised financial advice or a recommendation of any specific firm. Your answers stay in your browser and are never sent or shared.</div>
 """,
 "faqs":[
  {"q":"What is a fee-only fiduciary advisor?","a":"A fiduciary is legally required to act in your best interest. Fee-only means they are paid only by you — through a flat, hourly or percentage-of-assets fee — rather than earning commissions for selling products. This structure reduces conflicts of interest, which is why many people specifically seek fee-only fiduciaries."},
  {"q":"How much does a financial advisor cost?","a":"Models vary: some charge a percentage of assets managed (often around 1% per year), some a flat annual retainer, and some an hourly or one-time project fee for a plan. Robo-advisors charge much less, typically a small fraction of a percent. Ask for the fee in dollars so you can compare clearly."},
  {"q":"When is a robo-advisor enough?","a":"If your situation is straightforward and you mainly need diversified, automated investing, a low-cost robo-advisor or a simple index-fund portfolio can do the job for a fraction of a traditional advisor's cost. You can always add human, comprehensive advice as your wealth or complexity grows."},
 ],
})
