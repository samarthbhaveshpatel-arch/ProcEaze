/* ==========================================================================
   ProcEaze — tools.js
   Free procurement tools: RFQ template generator, supplier evaluation
   matrix, MRO procurement checklist and procurement savings calculator.
   Everything runs in the browser. Nothing is sent over the network.
   Loaded only on tool pages (defer, after main.js). Each tool initialises
   only when its root element ([data-rfq], [data-se], [data-mro], [data-sav])
   is on the page.
   ========================================================================== */
(() => {
  'use strict';

  const doc = document;
  const $ = (s, c = doc) => c.querySelector(s);
  const $$ = (s, c = doc) => Array.from(c.querySelectorAll(s));

  /* ------------------------------------------------------------------------
     Shared helpers
     ------------------------------------------------------------------------ */
  const toast = (msg, type = 'info') => {
    if (window.PE && typeof window.PE.toast === 'function') window.PE.toast(msg, type);
  };

  const escHtml = (s) => String(s == null ? '' : s)
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;').replace(/'/g, '&#39;');

  const csvCell = (v) => {
    const s = String(v == null ? '' : v);
    return /[",\r\n]/.test(s) ? `"${s.replace(/"/g, '""')}"` : s;
  };
  const toCsv = (rows) => rows.map((r) => r.map(csvCell).join(',')).join('\r\n') + '\r\n';

  /** Debounce: run fn after ms of quiet. */
  const debounce = (fn, ms) => {
    let t;
    return (...a) => { clearTimeout(t); t = setTimeout(() => fn(...a), ms); };
  };

  /** Offer a file generated in the browser for download (no network). */
  function download(filename, content, mime) {
    const blob = new Blob([content], { type: mime });
    const url = URL.createObjectURL(blob);
    const a = doc.createElement('a');
    a.href = url;
    a.download = filename;
    a.rel = 'noopener';
    doc.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(() => URL.revokeObjectURL(url), 2000);
  }

  /** Copy text to the clipboard, with a fallback for older browsers. */
  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) {
      return navigator.clipboard.writeText(text);
    }
    return new Promise((resolve, reject) => {
      const ta = doc.createElement('textarea');
      ta.value = text;
      ta.setAttribute('readonly', '');
      ta.style.position = 'fixed';
      ta.style.opacity = '0';
      doc.body.appendChild(ta);
      ta.select();
      let ok = false;
      try { ok = doc.execCommand('copy'); } catch (e) { ok = false; }
      ta.remove();
      ok ? resolve() : reject(new Error('copy failed'));
    });
  }

  /** Print only one element: CSS hides everything else while body has .tool-printing. */
  function printOnly(el) {
    el.classList.add('tool-print-target');
    doc.body.classList.add('tool-printing');
    let done = false;
    const cleanup = () => {
      if (done) return;
      done = true;
      el.classList.remove('tool-print-target');
      doc.body.classList.remove('tool-printing');
      window.removeEventListener('afterprint', cleanup);
    };
    window.addEventListener('afterprint', cleanup);
    window.print();
    // Some browsers don't fire afterprint; print() blocks until the dialog closes in most
    setTimeout(cleanup, 1000);
  }

  /** ₹ with Indian digit grouping: 1234567 -> ₹12,34,567. */
  function inrFull(n) {
    const v = Math.round(Number(n) || 0);
    const neg = v < 0;
    const s = String(Math.abs(v));
    let last3 = s.slice(-3);
    const rest = s.slice(0, -3);
    if (rest) last3 = ',' + last3;
    return (neg ? '-' : '') + '₹' + rest.replace(/\B(?=(\d{2})+(?!\d))/g, ',') + last3;
  }

  /** Short form: ₹12.3 lakh, ₹1.65 crore; below one lakh, the full figure. */
  function inrShort(n) {
    const v = Number(n) || 0;
    const a = Math.abs(v);
    if (a >= 1e7) return '₹' + Number((v / 1e7).toFixed(2)) + ' crore';
    if (a >= 1e5) return '₹' + Number((v / 1e5).toFixed(a < 1e6 ? 2 : 1)) + ' lakh';
    return inrFull(v);
  }

  /** Plain Indian grouping without the ₹ sign (for counts). */
  const groupIN = (n) => inrFull(n).replace('₹', '');

  const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  /** 2026-11-12 -> 12 Nov 2026 */
  function fmtDate(iso) {
    const m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(iso || '');
    if (!m) return iso || '';
    return `${Number(m[3])} ${MONTHS[Number(m[2]) - 1]} ${m[1]}`;
  }
  function todayIso() {
    const d = new Date();
    const p = (x) => String(x).padStart(2, '0');
    return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}`;
  }
  const safeName = (s, fallback) => (String(s || '').trim().replace(/[^A-Za-z0-9._-]+/g, '-').replace(/^-+|-+$/g, '') || fallback).slice(0, 60);

  /* ------------------------------------------------------------------------
     RFQ template generator
     ------------------------------------------------------------------------ */
  function initRfq(root) {
    const list = $('[data-rfq-items]', root);
    const tpl = $('template[data-rfq-row]', root);
    const preview = $('[data-rfq-preview]', root);
    const status = $('[data-rfq-status]', root);
    const addBtn = $('[data-rfq-add]', root);
    if (!list || !tpl || !preview) return;
    let uid = 0;

    const field = (name) => {
      const el = $(`[data-rfq-field="${name}"]`, root);
      return el ? el.value.trim() : '';
    };

    function renumber() {
      const rows = $$('[data-rfq-line]', list);
      rows.forEach((row, i) => {
        $('[data-rfq-line-no]', row).textContent = String(i + 1);
        const rm = $('[data-rfq-remove]', row);
        rm.setAttribute('aria-label', `Remove line item ${i + 1}`);
        rm.disabled = rows.length === 1;
      });
    }

    function addRow(focus) {
      uid += 1;
      const frag = tpl.content.cloneNode(true);
      // Give every input a unique id and point its label at it
      $$('[data-li]', frag).forEach((input) => {
        const id = `rfq-li-${uid}-${input.dataset.li}`;
        const label = $(`label[data-for="${input.dataset.li}"]`, frag);
        input.id = id;
        if (label) label.htmlFor = id;
      });
      const row = $('[data-rfq-line]', frag);
      list.appendChild(frag);
      renumber();
      if (focus) $('[data-li="desc"]', row).focus();
      update();
    }

    function lines() {
      return $$('[data-rfq-line]', list).map((row) => {
        const v = (k) => $(`[data-li="${k}"]`, row).value.trim();
        return { desc: v('desc'), spec: v('spec'), qty: v('qty'), uom: v('uom'), date: v('date') };
      }).filter((l) => l.desc || l.spec || l.qty || l.uom || l.date);
    }

    function data() {
      return {
        company: field('company'), contact: field('contact'), email: field('email'), phone: field('phone'),
        number: field('number'), title: field('title'), issued: field('issued'), due: field('due'),
        location: field('location'), payment: field('payment'), delivery: field('delivery'),
        validity: field('validity'), evaluation: field('evaluation'), notes: field('notes'),
        lines: lines(),
      };
    }

    const INSTRUCTIONS = [
      'Quote item-wise rates in Indian Rupees (₹) per unit of measure, with GST shown separately (state the GST rate and HSN code for each item).',
      'State the make / brand offered for each item and list any deviation from the specification. Quotes with unlisted deviations may be treated as non-compliant.',
      'State the delivery lead time from the date of purchase order, and whether freight, packing and insurance are included.',
      'State the validity of your quotation.',
      'Include your GSTIN, PAN and contact details with the quotation.',
      'Submitting a quotation does not oblige the buyer to place an order.',
    ];

    const ph = (v, label) => (v ? escHtml(v) : `<span class="rfq-ph">[${escHtml(label)}]</span>`);
    const lineVal = (v) => (v ? escHtml(v) : '<span class="rfq-ph">-</span>');

    function toHtml(d) {
      const rows = d.lines.length
        ? d.lines.map((l, i) => `<tr><td>${i + 1}</td><td>${lineVal(l.desc)}</td><td>${lineVal(l.spec)}</td><td class="num">${lineVal(l.qty)}</td><td>${lineVal(l.uom)}</td><td>${l.date ? escHtml(fmtDate(l.date)) : lineVal('')}</td></tr>`).join('')
        : '<tr><td colspan="6"><span class="rfq-ph">[Add at least one line item]</span></td></tr>';
      const contact = [d.contact, d.email, d.phone].filter(Boolean).map(escHtml).join(' · ');
      return `<header class="rfq-doc-head">
  <p class="rfq-doc-kicker">Request for Quotation</p>
  <h3 class="rfq-doc-title">${ph(d.title, 'RFQ title')}</h3>
  <p class="rfq-doc-company">${ph(d.company, 'Buyer company')}</p>
  <dl class="rfq-doc-meta">
    <div><dt>RFQ number</dt><dd>${ph(d.number, 'RFQ number')}</dd></div>
    <div><dt>Date of issue</dt><dd>${d.issued ? escHtml(fmtDate(d.issued)) : ph('', 'Date')}</dd></div>
    <div><dt>Quotes due by</dt><dd>${d.due ? escHtml(fmtDate(d.due)) : ph('', 'Due date')}</dd></div>
    <div><dt>Contact</dt><dd>${contact || ph('', 'Contact')}</dd></div>
  </dl>
</header>
<h4>1. Requirement</h4>
<div class="rfq-doc-table"><table>
  <thead><tr><th>#</th><th>Description</th><th>Specification / make</th><th class="num">Qty</th><th>UoM</th><th>Required by</th></tr></thead>
  <tbody>${rows}</tbody>
</table></div>
<h4>2. Delivery location</h4>
<p class="rfq-pre">${ph(d.location, 'Delivery address')}</p>
<h4>3. Commercial terms</h4>
<ul>
  <li><strong>Payment terms:</strong> ${ph(d.payment, 'Payment terms')}</li>
  <li><strong>Delivery terms:</strong> ${ph(d.delivery, 'Delivery terms')}</li>
  <li><strong>Quote validity required:</strong> ${d.validity ? escHtml(d.validity) + ' days from the due date' : ph('', 'Validity in days')}</li>
</ul>
<h4>4. Evaluation basis</h4>
<p class="rfq-pre">${ph(d.evaluation, 'How quotes will be evaluated')}</p>
<h4>5. Instructions to suppliers</h4>
<ol>${INSTRUCTIONS.map((t) => `<li>${escHtml(t)}</li>`).join('')}</ol>
${d.notes ? `<h4>6. Additional notes</h4><p class="rfq-pre">${escHtml(d.notes)}</p>` : ''}
<p class="rfq-doc-foot">Please send your quotation by ${d.due ? escHtml(fmtDate(d.due)) : '[due date]'}${d.contact || d.email ? ' to ' + escHtml([d.contact, d.email].filter(Boolean).join(', ')) : ''}, quoting RFQ number ${d.number ? escHtml(d.number) : '[RFQ number]'}.</p>`;
    }

    function toText(d) {
      const t = (v, label) => v || `[${label}]`;
      const out = [];
      const rule = '='.repeat(64);
      out.push('REQUEST FOR QUOTATION', rule);
      out.push(`Title:          ${t(d.title, 'RFQ title')}`);
      out.push(`Buyer:          ${t(d.company, 'Buyer company')}`);
      out.push(`RFQ number:     ${t(d.number, 'RFQ number')}`);
      out.push(`Date of issue:  ${d.issued ? fmtDate(d.issued) : '[Date]'}`);
      out.push(`Quotes due by:  ${d.due ? fmtDate(d.due) : '[Due date]'}`);
      const contact = [d.contact, d.email, d.phone].filter(Boolean).join(' | ');
      out.push(`Contact:        ${contact || '[Contact]'}`, '');
      out.push('1. REQUIREMENT', '-'.repeat(64));
      if (!d.lines.length) out.push('[Add at least one line item]');
      d.lines.forEach((l, i) => {
        out.push(`${i + 1}. ${l.desc || '-'}`);
        if (l.spec) out.push(`   Specification / make: ${l.spec}`);
        out.push(`   Quantity: ${l.qty || '-'} ${l.uom || ''}`.trimEnd());
        if (l.date) out.push(`   Required by: ${fmtDate(l.date)}`);
      });
      out.push('', '2. DELIVERY LOCATION', '-'.repeat(64), t(d.location, 'Delivery address'), '');
      out.push('3. COMMERCIAL TERMS', '-'.repeat(64));
      out.push(`Payment terms:  ${t(d.payment, 'Payment terms')}`);
      out.push(`Delivery terms: ${t(d.delivery, 'Delivery terms')}`);
      out.push(`Quote validity: ${d.validity ? d.validity + ' days from the due date' : '[Validity in days]'}`, '');
      out.push('4. EVALUATION BASIS', '-'.repeat(64), t(d.evaluation, 'How quotes will be evaluated'), '');
      out.push('5. INSTRUCTIONS TO SUPPLIERS', '-'.repeat(64));
      INSTRUCTIONS.forEach((x, i) => out.push(`${i + 1}. ${x}`));
      if (d.notes) out.push('', '6. ADDITIONAL NOTES', '-'.repeat(64), d.notes);
      out.push('', rule);
      out.push(`Please send your quotation by ${d.due ? fmtDate(d.due) : '[due date]'}${d.contact || d.email ? ' to ' + [d.contact, d.email].filter(Boolean).join(', ') : ''}, quoting RFQ number ${d.number || '[RFQ number]'}.`);
      return out.join('\r\n') + '\r\n';
    }

    function toDocument(d) {
      const title = `RFQ ${d.number || ''} ${d.title || ''}`.trim();
      return `<!doctype html>
<html lang="en-IN"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>${escHtml(title || 'Request for Quotation')}</title>
<style>
body{font-family:Arial,Helvetica,sans-serif;color:#111;line-height:1.5;max-width:860px;margin:0 auto;padding:32px 24px}
h3{font-size:1.5rem;margin:4px 0}h4{font-size:1rem;margin:24px 0 8px;border-bottom:1px solid #ccc;padding-bottom:4px}
.rfq-doc-kicker{text-transform:uppercase;letter-spacing:.12em;font-size:.78rem;font-weight:bold;color:#184AC3;margin:0}
.rfq-doc-company{font-weight:bold;margin:0 0 12px}
dl{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px 24px;margin:0}dt{font-size:.75rem;text-transform:uppercase;color:#555}dd{margin:0;font-weight:bold}
table{border-collapse:collapse;width:100%;font-size:.9rem}th,td{border:1px solid #999;padding:6px 8px;text-align:left;vertical-align:top}th{background:#f2f4f8}.num{text-align:right}
.rfq-pre{white-space:pre-wrap}.rfq-ph{color:#888}.rfq-doc-foot{margin-top:24px;font-weight:bold}
@media print{body{padding:0}}
</style></head><body>
${toHtml(d)}
</body></html>
`;
    }

    const announce = debounce(() => {
      const n = lines().length;
      if (status) status.textContent = `Preview updated: ${n} line item${n === 1 ? '' : 's'}.`;
    }, 900);

    function update() {
      preview.innerHTML = toHtml(data());
      announce();
    }

    const fileBase = () => `RFQ-${safeName(field('number') || field('title'), 'request-for-quotation')}`;

    root.addEventListener('input', update);
    root.addEventListener('change', update);
    if (addBtn) addBtn.addEventListener('click', () => addRow(true));

    list.addEventListener('click', (e) => {
      const btn = e.target.closest('[data-rfq-remove]');
      if (!btn) return;
      const row = btn.closest('[data-rfq-line]');
      const rows = $$('[data-rfq-line]', list);
      if (rows.length <= 1) return;
      const idx = rows.indexOf(row);
      row.remove();
      renumber();
      update();
      const remaining = $$('[data-rfq-line]', list);
      const next = remaining[Math.min(idx, remaining.length - 1)];
      (next ? $('[data-li="desc"]', next) : addBtn).focus();
      if (status) status.textContent = `Line item removed. ${remaining.length} remaining.`;
    });

    $$('[data-rfq-action]', root).forEach((btn) => btn.addEventListener('click', () => {
      const d = data();
      const act = btn.dataset.rfqAction;
      if (act === 'print') {
        printOnly(preview);
      } else if (act === 'copy') {
        copyText(toText(d)).then(
          () => { if (status) status.textContent = 'RFQ copied to the clipboard as text.'; toast('RFQ copied to the clipboard.', 'success'); },
          () => { if (status) status.textContent = 'Could not copy. Use Download .txt instead.'; toast('Could not copy. Use Download .txt instead.', 'error'); });
      } else if (act === 'txt') {
        download(`${fileBase()}.txt`, toText(d), 'text/plain;charset=utf-8');
        if (status) status.textContent = 'RFQ downloaded as a text file.';
      } else if (act === 'html') {
        download(`${fileBase()}.html`, toDocument(d), 'text/html;charset=utf-8');
        if (status) status.textContent = 'RFQ downloaded as an HTML file.';
      } else if (act === 'reset') {
        if (!window.confirm('Clear the form and start a new RFQ?')) return;
        $$('[data-rfq-field]', root).forEach((el) => {
          if (el.tagName === 'SELECT') {
            const def = Array.from(el.options).findIndex((o) => o.defaultSelected);
            el.selectedIndex = def < 0 ? 0 : def;
          } else {
            el.value = el.defaultValue;
          }
        });
        const issued = $('[data-rfq-field="issued"]', root);
        if (issued) issued.value = todayIso();
        list.innerHTML = '';
        addRow(false);
        if (status) status.textContent = 'Form cleared.';
        const first = $('[data-rfq-field="company"]', root);
        if (first) first.focus();
      }
    }));

    const issued = $('[data-rfq-field="issued"]', root);
    if (issued && !issued.value) issued.value = todayIso();
    addRow(false);
  }

  /* ------------------------------------------------------------------------
     Supplier evaluation matrix (weighted scoring)
     ------------------------------------------------------------------------ */
  const SE_DEFAULTS = {
    criteria: [
      ['Price / total cost', 30], ['Quality', 20], ['Delivery reliability', 15], ['Technical compliance', 15],
      ['Payment terms', 5], ['Service & support', 10], ['Compliance & documentation', 5],
    ],
    suppliers: ['Supplier A', 'Supplier B', 'Supplier C'],
  };

  function initSupplierEval(root) {
    const host = $('[data-se-table]', root);
    const totalEl = $('[data-se-total]', root);
    const warn = $('[data-se-warn]', root);
    const rankEl = $('[data-se-rank]', root);
    const live = $('[data-se-live]', root);
    if (!host) return;
    const MIN_S = 2, MAX_S = 5;
    let uid = 0;
    let state;

    function fresh() {
      state = {
        criteria: SE_DEFAULTS.criteria.map(([name, weight]) => ({ id: ++uid, name, weight: String(weight) })),
        suppliers: SE_DEFAULTS.suppliers.map((name) => ({ id: ++uid, name })),
        scores: {},
      };
    }
    const key = (c, s) => `${c}:${s}`;
    const num = (v) => { const n = parseFloat(v); return Number.isFinite(n) ? n : 0; };
    const sName = (s, i) => s.name.trim() || `Supplier ${i + 1}`;
    const cName = (c, i) => c.name.trim() || `Criterion ${i + 1}`;

    function render(focusSel) {
      const sup = state.suppliers;
      const head = sup.map((s, i) => `<th scope="col"><div class="se-sup">
          <label class="sr-only" for="se-s-${s.id}">Name of supplier ${i + 1}</label>
          <input class="input se-name" id="se-s-${s.id}" type="text" value="${escHtml(s.name)}" data-se-sname="${s.id}" autocomplete="off">
          <button class="se-x" type="button" data-se-sremove="${s.id}" aria-label="Remove ${escHtml(sName(s, i))}"${sup.length <= MIN_S ? ' disabled' : ''}>×</button>
        </div></th>`).join('');
      const body = state.criteria.map((c, ci) => {
        const cells = sup.map((s, si) => {
          const v = state.scores[key(c.id, s.id)] || '';
          const opts = ['', '1', '2', '3', '4', '5'].map((o) => `<option value="${o}"${o === v ? ' selected' : ''}>${o || '–'}</option>`).join('');
          return `<td><select class="select se-score" data-se-score="${c.id}:${s.id}" aria-label="${escHtml(sName(s, si))}: score for ${escHtml(cName(c, ci))} (1 to 5)">${opts}</select></td>`;
        }).join('');
        return `<tr>
          <th scope="row"><div class="se-crit">
            <label class="sr-only" for="se-c-${c.id}">Criterion ${ci + 1}</label>
            <input class="input se-name" id="se-c-${c.id}" type="text" value="${escHtml(c.name)}" data-se-cname="${c.id}" autocomplete="off">
            <button class="se-x" type="button" data-se-cremove="${c.id}" aria-label="Remove criterion ${escHtml(cName(c, ci))}"${state.criteria.length <= 1 ? ' disabled' : ''}>×</button>
          </div></th>
          <td><label class="sr-only" for="se-w-${c.id}">Weight for ${escHtml(cName(c, ci))} (%)</label>
            <div class="se-weight"><input class="input" id="se-w-${c.id}" type="number" inputmode="decimal" min="0" max="100" step="1" value="${escHtml(c.weight)}" data-se-weight="${c.id}"><span aria-hidden="true">%</span></div></td>
          ${cells}
        </tr>`;
      }).join('');
      const foot = sup.map((s) => `<td><output class="se-score-out" data-se-out="${s.id}">0.00</output></td>`).join('');
      const rank = sup.map((s) => `<td><span class="se-rank-out" data-se-rankcell="${s.id}">–</span></td>`).join('');
      host.innerHTML = `<table class="se-table">
        <caption class="sr-only">Supplier evaluation matrix: criteria, weights and scores from 1 to 5</caption>
        <thead><tr><th scope="col">Criterion</th><th scope="col">Weight</th>${head}</tr></thead>
        <tbody>${body}</tbody>
        <tfoot>
          <tr><th scope="row">Weighted score <span class="se-sub">out of 5</span></th><td><span class="se-total" data-se-wtotal>0%</span></td>${foot}</tr>
          <tr><th scope="row">Rank</th><td></td>${rank}</tr>
        </tfoot></table>`;
      const addS = $('[data-se-addsupplier]', root);
      if (addS) addS.disabled = sup.length >= MAX_S;
      compute();
      if (focusSel) { const f = $(focusSel, root); if (f) f.focus(); }
    }

    function results() {
      const totalW = state.criteria.reduce((a, c) => a + num(c.weight), 0);
      const rows = state.suppliers.map((s, i) => {
        let sum = 0, scored = 0;
        state.criteria.forEach((c) => {
          const v = state.scores[key(c.id, s.id)];
          if (v) { scored += 1; sum += num(c.weight) * num(v); }
        });
        return { id: s.id, name: sName(s, i), score: sum / 100, scored };
      });
      const sorted = rows.slice().sort((a, b) => b.score - a.score);
      sorted.forEach((r, i) => {
        r.rank = i > 0 && Math.abs(r.score - sorted[i - 1].score) < 1e-9 ? sorted[i - 1].rank : i + 1;
      });
      return { totalW, rows, sorted };
    }

    const announce = debounce((text) => { if (live) live.textContent = text; }, 800);

    function compute() {
      const { totalW, rows, sorted } = results();
      const ok = Math.abs(totalW - 100) < 1e-9;
      const tw = Number(totalW.toFixed(2));
      if (totalEl) totalEl.textContent = `${tw}%`;
      const wt = $('[data-se-wtotal]', root);
      if (wt) { wt.textContent = `${tw}%`; wt.classList.toggle('is-bad', !ok); }
      if (warn) {
        warn.hidden = ok;
        warn.querySelector('span').textContent = `Weights total ${tw}%. Adjust them so they add up to exactly 100% before relying on the ranking.`;
      }
      root.classList.toggle('se-weights-bad', !ok);
      const nCrit = state.criteria.length;
      rows.forEach((r) => {
        const out = $(`[data-se-out="${r.id}"]`, root);
        if (out) out.textContent = r.score.toFixed(2);
        const rk = $(`[data-se-rankcell="${r.id}"]`, root);
        if (rk) { rk.textContent = r.scored ? `#${r.rank}` : '–'; rk.classList.toggle('is-top', r.rank === 1 && r.scored > 0); }
      });
      if (rankEl) {
        const anyScored = rows.some((r) => r.scored);
        rankEl.innerHTML = anyScored
          ? sorted.map((r) => `<li${r.rank === 1 ? ' class="is-top"' : ''}><span class="se-rank-n">${r.rank}</span><span class="se-rank-name">${escHtml(r.name)}</span><span class="se-rank-score">${r.score.toFixed(2)} / 5</span>${r.scored < nCrit ? `<span class="se-rank-note">${r.scored} of ${nCrit} criteria scored</span>` : ''}</li>`).join('')
          : '<li class="se-rank-empty">Score the suppliers to see the ranking.</li>';
      }
      announce(rows.some((r) => r.scored)
        ? `Weights total ${tw}%${ok ? '' : ', not 100%'}. Ranking: ${sorted.map((r) => `${r.rank}. ${r.name}, ${r.score.toFixed(2)} out of 5`).join('; ')}.`
        : `Weights total ${tw}%${ok ? '' : ', not 100%'}. No scores entered yet.`);
    }

    host.addEventListener('input', (e) => {
      const t = e.target;
      if (t.dataset.seWeight) { state.criteria.find((c) => String(c.id) === t.dataset.seWeight).weight = t.value; compute(); }
      else if (t.dataset.seCname) { state.criteria.find((c) => String(c.id) === t.dataset.seCname).name = t.value; compute(); }
      else if (t.dataset.seSname) { state.suppliers.find((s) => String(s.id) === t.dataset.seSname).name = t.value; compute(); }
    });
    host.addEventListener('change', (e) => {
      const t = e.target;
      if (t.dataset.seScore) { state.scores[t.dataset.seScore] = t.value; compute(); }
      // Refresh accessible names once a criterion or supplier name is committed
      if (t.dataset.seCname || t.dataset.seSname) relabel();
    });

    /** Keep aria-labels in step with edited names without rebuilding the table (focus stays put). */
    function relabel() {
      state.criteria.forEach((c, ci) => {
        const cn = cName(c, ci);
        const rm = $(`[data-se-cremove="${c.id}"]`, host);
        if (rm) rm.setAttribute('aria-label', `Remove criterion ${cn}`);
        const wl = $(`label[for="se-w-${c.id}"]`, host);
        if (wl) wl.textContent = `Weight for ${cn} (%)`;
        state.suppliers.forEach((s, si) => {
          const sel = $(`[data-se-score="${c.id}:${s.id}"]`, host);
          if (sel) sel.setAttribute('aria-label', `${sName(s, si)}: score for ${cn} (1 to 5)`);
        });
      });
      state.suppliers.forEach((s, si) => {
        const rm = $(`[data-se-sremove="${s.id}"]`, host);
        if (rm) rm.setAttribute('aria-label', `Remove ${sName(s, si)}`);
      });
    }
    host.addEventListener('click', (e) => {
      const c = e.target.closest('[data-se-cremove]');
      const s = e.target.closest('[data-se-sremove]');
      if (c && state.criteria.length > 1) {
        const i = state.criteria.findIndex((x) => String(x.id) === c.dataset.seCremove);
        state.criteria.splice(i, 1);
        const next = state.criteria[Math.min(i, state.criteria.length - 1)];
        render(`#se-c-${next.id}`);
        announce('Criterion removed.');
      } else if (s && state.suppliers.length > MIN_S) {
        const i = state.suppliers.findIndex((x) => String(x.id) === s.dataset.seSremove);
        state.suppliers.splice(i, 1);
        const next = state.suppliers[Math.min(i, state.suppliers.length - 1)];
        render(`#se-s-${next.id}`);
        announce('Supplier removed.');
      }
    });

    const addC = $('[data-se-addcriterion]', root);
    if (addC) addC.addEventListener('click', () => {
      const c = { id: ++uid, name: '', weight: '0' };
      state.criteria.push(c);
      render(`#se-c-${c.id}`);
    });
    const addS = $('[data-se-addsupplier]', root);
    if (addS) addS.addEventListener('click', () => {
      if (state.suppliers.length >= MAX_S) return;
      const s = { id: ++uid, name: `Supplier ${String.fromCharCode(65 + state.suppliers.length)}` };
      state.suppliers.push(s);
      render(`#se-s-${s.id}`);
    });
    const reset = $('[data-se-reset]', root);
    if (reset) reset.addEventListener('click', () => { fresh(); render(); announce('Matrix reset to the default criteria.'); });

    const dl = $('[data-se-csv]', root);
    if (dl) dl.addEventListener('click', () => {
      const { totalW, rows } = results();
      const sup = state.suppliers;
      const out = [['Criterion', 'Weight (%)', ...sup.map((s, i) => `${sName(s, i)} score (1-5)`), ...sup.map((s, i) => `${sName(s, i)} weighted`)]];
      state.criteria.forEach((c, ci) => {
        const sc = sup.map((s) => state.scores[key(c.id, s.id)] || '');
        const wtd = sup.map((s) => {
          const v = state.scores[key(c.id, s.id)];
          return v ? (num(c.weight) * num(v) / 100).toFixed(2) : '';
        });
        out.push([cName(c, ci), num(c.weight), ...sc, ...wtd]);
      });
      out.push(['Total weight', Number(totalW.toFixed(2))]);
      out.push(['Weighted score (out of 5)', '', ...rows.map((r) => r.score.toFixed(2))]);
      out.push(['Rank', '', ...rows.map((r) => (r.scored ? r.rank : ''))]);
      out.push([]);
      out.push(['Weighted score = sum of (weight x score) / 100. Scores: 1 = does not meet, 3 = meets, 5 = clearly exceeds.']);
      download('supplier-evaluation.csv', '﻿' + toCsv(out), 'text/csv;charset=utf-8');
      toast('Supplier evaluation downloaded as CSV.', 'success');
    });

    fresh();
    render();
  }

  /* ------------------------------------------------------------------------
     MRO procurement checklist (ticks persist in localStorage when available)
     ------------------------------------------------------------------------ */
  function initMro(root) {
    const boxes = $$('input[data-mro-item]', root);
    const bar = $('[data-mro-bar]', root);
    const fill = $('[data-mro-fill]', root);
    const count = $('[data-mro-count]', root);
    if (!boxes.length) return;
    const KEY = 'pe-tools-mro-checklist-v1';

    const load = () => {
      try { return JSON.parse(localStorage.getItem(KEY) || '[]') || []; } catch (e) { return []; }
    };
    const save = () => {
      try { localStorage.setItem(KEY, JSON.stringify(boxes.filter((b) => b.checked).map((b) => b.dataset.mroItem))); } catch (e) { /* storage unavailable: ticks last for this visit only */ }
    };

    function update() {
      const done = boxes.filter((b) => b.checked).length;
      const pct = Math.round((done / boxes.length) * 100);
      if (bar) { bar.setAttribute('aria-valuenow', String(done)); bar.setAttribute('aria-valuetext', `${done} of ${boxes.length} items done (${pct}%)`); }
      if (fill) fill.style.width = `${pct}%`;
      if (count) count.textContent = `${done} of ${boxes.length} items done (${pct}%)`;
      $$('[data-mro-stage]', root).forEach((stage) => {
        const sb = $$('input[data-mro-item]', stage);
        const d = sb.filter((b) => b.checked).length;
        const out = $('[data-mro-stage-count]', stage);
        if (out) out.textContent = `${d}/${sb.length}`;
        stage.classList.toggle('is-complete', d === sb.length);
      });
    }

    const saved = load();
    if (Array.isArray(saved)) boxes.forEach((b) => { b.checked = saved.indexOf(b.dataset.mroItem) !== -1; });
    root.addEventListener('change', (e) => { if (e.target.matches('input[data-mro-item]')) { save(); update(); } });

    const reset = $('[data-mro-reset]', root);
    if (reset) reset.addEventListener('click', () => {
      if (!boxes.some((b) => b.checked)) return;
      if (!window.confirm('Clear all ticks on this checklist?')) return;
      boxes.forEach((b) => { b.checked = false; });
      save();
      update();
      boxes[0].focus();
      toast('Checklist cleared.', 'info');
    });
    const print = $('[data-mro-print]', root);
    const area = $('[data-mro-print-area]', root) || root;
    if (print) print.addEventListener('click', () => printOnly(area));
    update();
  }

  /* ------------------------------------------------------------------------
     Procurement savings calculator: only the user's own inputs
     ------------------------------------------------------------------------ */
  function initSavings(root) {
    const inputs = {};
    $$('[data-sav-in]', root).forEach((el) => { inputs[el.dataset.savIn] = el; });
    if (!inputs.spend) return;
    const out = (k) => $(`[data-sav-out="${k}"]`, root);
    const set = (k, text) => { const el = out(k); if (el) el.textContent = text; };
    const live = $('[data-sav-live]', root);
    const notes = $('[data-sav-notes]', root);

    const read = (k, max) => {
      const raw = String(inputs[k].value).replace(/[,\s₹%]/g, '');
      let n = parseFloat(raw);
      const field = inputs[k].closest('.field');
      const bad = raw !== '' && (!Number.isFinite(n) || n < 0 || (max != null && n > max));
      if (field) field.classList.toggle('has-error', bad);
      const err = field && $('.field-error span', field);
      if (err) err.textContent = bad ? (max != null ? `Enter a number from 0 to ${max}.` : 'Enter a number of 0 or more.') : '';
      inputs[k].setAttribute('aria-invalid', String(bad));
      if (!Number.isFinite(n) || n < 0) n = 0;
      if (max != null && n > max) n = max;
      return n;
    };
    const pct = (n) => `${Number(n.toFixed(2))}%`;

    const announce = debounce((t) => { if (live) live.textContent = t; }, 900);

    function compute() {
      const spend = read('spend');
      const cur = read('current', 100);
      const target = read('target', 100);
      const diff = read('diff', 100);
      const pos = read('pos');
      const cpo = read('cpo');
      const red = read('reduction', 100);

      const shift = Math.max(0, target - cur);
      const moved = spend * shift / 100;
      const price = moved * diff / 100;
      const processCost = pos * cpo;
      const process = processCost * red / 100;
      const total = price + process;

      const hint = $('[data-sav-hint="spend"]', root);
      if (hint) hint.textContent = spend ? `${inrFull(spend)} (${inrShort(spend)})` : 'Enter your annual spend in rupees.';
      const hintC = $('[data-sav-hint="cpo"]', root);
      if (hintC) hintC.textContent = `Current process cost: ${groupIN(pos)} POs × ${inrFull(cpo)} = ${inrFull(processCost)} a year.`;

      set('moved', inrFull(moved));
      set('price', inrFull(price));
      set('price-short', inrShort(price));
      set('process', inrFull(process));
      set('process-short', inrShort(process));
      set('total', inrFull(total));
      set('total-short', inrShort(total));

      set('f-moved', `${inrFull(spend)} × (${pct(target)} − ${pct(cur)}) = ${inrFull(moved)}`);
      set('f-price', `${inrFull(moved)} × ${pct(diff)} = ${inrFull(price)}`);
      set('f-process', `${groupIN(pos)} POs × ${inrFull(cpo)} × ${pct(red)} = ${inrFull(process)}`);
      set('f-total', `${inrFull(price)} + ${inrFull(process)} = ${inrFull(total)}`);

      if (notes) {
        const msgs = [];
        if (target < cur) msgs.push('Your target share on contract is lower than your current share, so no price savings are estimated. Check the two percentages.');
        if (target === cur && spend) msgs.push('Target and current share on contract are the same, so no additional spend moves onto contract.');
        if (!spend) msgs.push('Enter your annual indirect / MRO spend to estimate price savings.');
        notes.hidden = !msgs.length;
        notes.querySelector('span').textContent = msgs.join(' ');
      }
      announce(`Estimated total annual savings ${inrFull(total)} (${inrShort(total)}): price savings ${inrShort(price)}, process savings ${inrShort(process)}.`);
    }

    root.addEventListener('input', compute);
    const reset = $('[data-sav-reset]', root);
    if (reset) reset.addEventListener('click', () => {
      Object.values(inputs).forEach((el) => { el.value = el.defaultValue; });
      compute();
      inputs.spend.focus();
      toast('Example values restored. Replace them with your own.', 'info');
    });
    const clear = $('[data-sav-clear]', root);
    if (clear) clear.addEventListener('click', () => {
      Object.values(inputs).forEach((el) => { el.value = ''; });
      compute();
      inputs.spend.focus();
    });
    compute();
  }

  /* ------------------------------------------------------------------------
     Boot: each tool only where its root exists
     ------------------------------------------------------------------------ */
  function boot() {
    $$('[data-rfq]').forEach(initRfq);
    $$('[data-se]').forEach(initSupplierEval);
    $$('[data-mro]').forEach(initMro);
    $$('[data-sav]').forEach(initSavings);
  }
  if (doc.readyState === 'loading') doc.addEventListener('DOMContentLoaded', boot);
  else boot();
})();
