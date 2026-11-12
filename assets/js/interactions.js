/* ==========================================================================
   ProcEaze — interactions.js
   Interactive product demonstrations (all data simulated, for illustration):
   FAQ · fragmentation → intelligence · lifecycle · ARC lock · approval engine ·
   reverse auction · AI negotiation panel · negotiation control tower ·
   category orbit / security vault · engagement switch · audit trail
   ========================================================================== */
(() => {
  'use strict';
  const PE = window.PE;
  const { $, $$, reduceMotion, inr, toast, whenVisible, ICON, svg } = PE;
  const doc = document;
  const once = (el, key) => (el[key] ? false : (el[key] = true));
  /** Stop an autoplaying demo as soon as the user touches it. */
  const onUserIntent = (el, fn) => ['pointerdown', 'keydown', 'focusin'].forEach((t) => el.addEventListener(t, (e) => { if (e.isTrusted) fn(); }, { passive: true }));

  /* ------------------------------------------------------------------------
     FAQ — accordion, search, topic filter
     ------------------------------------------------------------------------ */
  function initFaq() {
    $$('.faq-q').forEach((btn) => btn.addEventListener('click', () => {
      const item = btn.closest('.faq-item');
      const open = !item.classList.contains('is-open');
      item.classList.toggle('is-open', open);
      btn.setAttribute('aria-expanded', String(open));
    }));
    const search = $('[data-faq-search]');
    const chips = $$('[data-faq-topic]');
    if (!search && !chips.length) return;
    const empty = $('[data-faq-empty]');
    const count = $('[data-faq-count]');
    let topic = 'all';
    const apply = () => {
      const q = (search ? search.value : '').trim().toLowerCase();
      let shown = 0;
      $$('.faq-group').forEach((group) => {
        let n = 0;
        const topicOk = topic === 'all' || group.dataset.topic === topic;
        $$('.faq-item', group).forEach((item) => {
          const match = topicOk && (!q || item.textContent.toLowerCase().includes(q));
          item.hidden = !match;
          if (match) n++;
          if (q && match && !item.classList.contains('is-open')) { item.classList.add('is-open'); $('.faq-q', item).setAttribute('aria-expanded', 'true'); }
        });
        group.hidden = n === 0;
        shown += n;
      });
      if (empty) empty.hidden = shown > 0;
      if (count) count.textContent = `${shown} question${shown === 1 ? '' : 's'}`;
    };
    if (search) search.addEventListener('input', apply);
    chips.forEach((chip) => chip.addEventListener('click', () => {
      topic = chip.dataset.faqTopic;
      chips.forEach((c) => c.setAttribute('aria-pressed', String(c === chip)));
      apply();
    }));
  }

  /* ------------------------------------------------------------------------
     Lifecycle — progress line, guided autoplay until the user takes over
     ------------------------------------------------------------------------ */
  function initLifecycle(lc) {
    if (!once(lc, '_lc')) return;
    const n = $$('[role="tab"]', lc).length;
    const update = (i) => lc.style.setProperty('--progress', String(n > 1 ? i / (n - 1) : 1));
    lc.addEventListener('tabchange', (e) => update(e.detail.index));
    update(0);
    if (reduceMotion.matches) return;
    let timer = null, stopped = false, visible = false;
    const stop = () => { stopped = true; clearInterval(timer); };
    onUserIntent(lc, stop);
    lc.addEventListener('mouseenter', () => clearInterval(timer));
    lc.addEventListener('mouseleave', () => { if (!stopped && visible) start(); });
    const start = () => {
      clearInterval(timer);
      timer = setInterval(() => { if (lc._select) lc._select(lc._index() + 1); }, 3400);
    };
    whenVisible(lc, () => { visible = true; if (!stopped) start(); }, () => { visible = false; clearInterval(timer); }, 0.4);
  }

  /* ------------------------------------------------------------------------
     ARC lock — vendor price gives way to the contracted price
     ------------------------------------------------------------------------ */
  function initArcLock(el) {
    if (!once(el, '_arc')) return;
    const price = $('[data-arc-price]', el);
    let raf;
    const run = () => {
      cancelAnimationFrame(raf);
      el.classList.remove('is-locked');
      if (reduceMotion.matches) { price.textContent = '1,080'; el.classList.add('is-locked'); return; }
      price.textContent = '1,240';
      const from = 1240, to = 1080, start = performance.now() + 500, dur = 900;
      const step = (now) => {
        const t = Math.max(0, Math.min(1, (now - start) / dur));
        const e = 1 - Math.pow(1 - t, 3);
        price.textContent = Math.round(from + (to - from) * e).toLocaleString('en-IN');
        if (t < 1) raf = requestAnimationFrame(step); else el.classList.add('is-locked');
      };
      raf = requestAnimationFrame(step);
    };
    let played = false;
    whenVisible(el, () => { if (!played) { played = true; run(); } }, null, 0.5);
    const replay = $('[data-arc-replay]', el);
    replay && replay.addEventListener('click', run);
  }

  /* ------------------------------------------------------------------------
     Approval engine — approve / reject / send back through 1–5 levels
     ------------------------------------------------------------------------ */
  const APPROVERS = [
    { role: 'Manager', unit: 'Maintenance', init: 'MG' },
    { role: 'Department Head', unit: 'Plant 2', init: 'DH' },
    { role: 'Director', unit: 'Operations', init: 'DR' },
    { role: 'Finance Head', unit: 'Finance', init: 'FH' },
    { role: 'Managing Director', unit: 'Corporate', init: 'MD' },
  ];
  function initApprovalEngine(el) {
    if (!once(el, '_ae')) return;
    const chain = $('[data-ae-chain]', el);
    const acting = $('[data-ae-acting]', el);
    const log = $('[data-ae-log]', el);
    const btn = (k) => $(`[data-ae-act="${k}"]`, el);
    let s;
    let clock;
    const stamp = () => {
      clock += 60 * (3 + Math.floor(Math.random() * 40));
      const h = Math.floor(clock / 3600) % 24, m = Math.floor(clock / 60) % 60;
      return `${String(h).padStart(2, '0')}:${String(m).padStart(2, '0')}`;
    };
    const addLog = (text) => {
      const li = doc.createElement('li');
      li.innerHTML = `<time>${stamp()}</time><span></span>`;
      li.lastChild.textContent = text;
      log.prepend(li);
      while (log.children.length > 4) log.lastChild.remove();
    };
    const reset = (levels) => {
      s = { levels, idx: 0, status: 'pending' };
      clock = 9 * 3600 + 12 * 60;
      log.innerHTML = '';
      addLog('Buyer · Maintenance submitted PR-31082');
      render();
    };
    const CHIP = {
      approved: ['Approved', 'green'], pending: ['Your action', 'amber'], waiting: ['Waiting', 'grey'],
      rejected: ['Rejected', 'red'], sentback: ['Sent back', 'amber'], submitted: ['Submitted', 'blue'], revise: ['Revise & resubmit', 'amber'],
    };
    const node = (init, title, sub, state, current) =>
      `<li class="ae-node is-${state}${current ? ' is-current' : ''}"><span class="ae-avatar">${init}</span>`
      + `<span class="ae-who"><strong>${title}</strong><span>${sub}</span></span>`
      + `<span class="m-chip ${CHIP[state][1]}">${CHIP[state][0]}</span></li>`;
    const render = () => {
      const list = APPROVERS.slice(0, s.levels);
      let html = '';
      for (let i = list.length - 1; i >= 0; i--) {
        const a = list[i];
        let state = 'waiting';
        if (i < s.idx) state = 'approved';
        else if (i === s.idx && s.idx < s.levels) state = s.status === 'pending' ? 'pending' : s.status;
        html += node(a.init, `${a.role} · ${a.unit}`, `Level ${i + 1}`, state, i === s.idx && s.status === 'pending');
      }
      html += node('BY', 'Buyer · Maintenance', 'Requester', s.status === 'sentback' ? 'revise' : 'submitted', s.status === 'sentback');
      chain.innerHTML = html;
      const cur = list[s.idx];
      const done = s.idx >= s.levels;
      let text;
      if (done) text = 'Fully approved. PO released to the vendor and recorded.';
      else if (s.status === 'pending') text = `Acting as ${cur.role} · Level ${s.idx + 1} of ${s.levels}`;
      else if (s.status === 'rejected') text = `Rejected by ${cur.role}. Request closed on the record.`;
      else text = 'Sent back to the buyer with comments. Resubmit to restart the chain.';
      acting.textContent = text;
      const closed = done || s.status === 'rejected';
      btn('approve').disabled = closed;
      btn('reject').disabled = closed || s.status === 'sentback';
      btn('sendback').disabled = closed || s.status === 'sentback';
      btn('approve').lastChild.textContent = s.status === 'sentback' ? 'Resubmit' : 'Approve';
    };
    el.addEventListener('click', (e) => {
      const lv = e.target.closest('[data-ae-levels]');
      if (lv) {
        $$('[data-ae-levels]', el).forEach((b) => b.setAttribute('aria-pressed', String(b === lv)));
        reset(+lv.dataset.aeLevels);
        return;
      }
      const act = e.target.closest('[data-ae-act]');
      if (!act) return;
      const k = act.dataset.aeAct;
      const cur = APPROVERS[s.idx];
      if (k === 'reset') { reset(s.levels); return; }
      if (k === 'approve') {
        if (s.status === 'sentback') { s.status = 'pending'; s.idx = 0; addLog('Buyer resubmitted with revisions'); }
        else { addLog(`${cur.role} approved (Level ${s.idx + 1})`); s.idx++; if (s.idx >= s.levels) addLog('PO-24117 released to vendor'); }
      } else if (k === 'reject') { s.status = 'rejected'; addLog(`${cur.role} rejected: over budget for this quarter`); }
      else if (k === 'sendback') { s.status = 'sentback'; addLog(`${cur.role} sent back: confirm cable length`); }
      render();
    });
    reset(3);
  }

  /* ------------------------------------------------------------------------
     Reverse auction simulation (English + Japanese), parameterised by data-*
     ------------------------------------------------------------------------ */
  class AuctionSim {
    constructor(el) {
      this.el = el;
      this.q = (s) => el.querySelector(s);
      this.mode = 'english';
      this.ceiling = +el.dataset.ceiling || 650000;
      this.reserve = +el.dataset.reserve || 540000;
      this.dec = +el.dataset.dec || 2500;
      this.duration = +el.dataset.duration || 180;
      this.unit = el.dataset.unit || '';
      this.autoplay = el.hasAttribute('data-autoplay') && !reduceMotion.matches;
      this.toggleBtn = this.q('[data-au-toggle]');
      this.toggleBtn && this.toggleBtn.addEventListener('click', () => (this.running ? this.pause() : this.start()));
      const reset = this.q('[data-au-reset]');
      reset && reset.addEventListener('click', () => this.reset());
      $$('[data-au-mode]', el).forEach((b) => b.addEventListener('click', () => {
        $$('[data-au-mode]', el).forEach((x) => x.setAttribute('aria-pressed', String(x === b)));
        this.mode = b.dataset.auMode;
        this.reset();
        if (this.autoplay) this.start();
      }));
      this.reset();
      if (this.autoplay) whenVisible(el, () => { if (!this.running && !this.finished) this.start(); }, () => { if (this.running) this.pause(true); });
    }
    snap(v) { return Math.round(v / this.dec) * this.dec; }
    reset() {
      this.stop();
      Object.assign(this, { finished: false, timeLeft: this.duration, elapsed: 0, extensions: 0, idle: 0, round: 0, roundTick: 0, clockPrice: this.ceiling, history: [], points: [] });
      const c = this.ceiling;
      const jitter = () => (Math.random() * 0.018 - 0.009) * c;
      this.bidders = [['A', .825], ['B', .806], ['C', .843], ['D', .871], ['E', .896]]
        .map(([id, f]) => ({ id, floor: this.snap(c * f + jitter()), bid: null, at: null, active: true, exitAt: null }));
      const jp = this.mode === 'japanese';
      this.q('[data-au-clock]').hidden = !jp;
      this.q('[data-au-l1-label]').textContent = jp ? 'Clock price' : 'Current L1';
      this.q('[data-au-timer-label]').textContent = jp ? 'Next drop in' : 'Time left';
      this.q('[data-au-dec]').textContent = inr(jp ? this.dec * 2 : this.dec);
      this.log(jp ? 'Clock set at the ceiling price. Bidders confirm each round to stay in.' : 'Auction ready. Ceiling price published to bidders.', '', true);
      this.q('[data-au-result]').hidden = true;
      this.setStatus('idle', 'Ready');
      this.setToggle(false);
      this.render();
    }
    setStatus(cls, text) { const s = this.q('[data-au-status]'); s.className = 'au-live' + (cls ? ' ' + cls : ''); s.textContent = text; }
    setToggle(running) {
      if (!this.toggleBtn) return;
      this.toggleBtn.innerHTML = running ? `${ICON.pause} Pause` : `${ICON.play} ${this.finished ? 'Run again' : (this.elapsed ? 'Resume' : 'Start simulation')}`;
    }
    start() {
      if (this.finished) this.reset();
      this.running = true;
      this.setStatus('', 'Live');
      this.setToggle(true);
      if (!this.elapsed) this.log(this.mode === 'japanese' ? 'Clock started.' : 'Auction is live.', '', true);
      this.timer = setInterval(() => this.tick(), this.mode === 'japanese' ? 650 : 700);
    }
    pause(silent) { this.stop(); this.running = false; if (!silent) this.setStatus('idle', 'Paused'); this.setToggle(false); }
    stop() { clearInterval(this.timer); clearTimeout(this.restartTimer); this.running = false; }
    clock() {
      const b = 11 * 3600 + this.elapsed;
      return [Math.floor(b / 3600), Math.floor((b % 3600) / 60), b % 60].map((x) => String(x).padStart(2, '0')).join(':');
    }
    log(text, amount, sys) {
      this.history.unshift({ time: this.elapsed ? this.clock() : '11:00:00', text, amount, sys });
      this.history = this.history.slice(0, 8);
    }
    l1() { return this.bidders.filter((b) => b.bid !== null).sort((a, b) => a.bid - b.bid)[0]; }
    tick() {
      if (this.mode === 'japanese') return this.tickJapanese();
      const step = this.idle > 3 ? 9 : 3;
      this.elapsed += step;
      this.timeLeft = Math.max(0, this.timeLeft - step);
      const leader = this.l1();
      const current = leader ? leader.bid : this.ceiling;
      const cands = this.bidders.filter((b) => b !== leader && current - this.dec >= b.floor);
      let placed = null;
      if (cands.length && Math.random() < (leader ? 0.58 : 0.9)) {
        const b = cands[Math.floor(Math.random() * cands.length)];
        let amt = current - this.dec * (1 + Math.floor(Math.random() * 3));
        b.bid = this.snap(Math.max(amt < b.floor ? current - this.dec : amt, b.floor));
        b.at = this.clock();
        placed = b;
        this.idle = 0;
        this.log(`Bidder ${b.id} bid`, b.bid);
        this.points.push([this.elapsed, b.bid]);
        if (this.timeLeft <= 30 && this.extensions < 3) {
          this.timeLeft += 60;
          this.extensions++;
          this.log('Anti-sniping: bid in last 30s, +60s added', '', true);
          const f = this.q('[data-au-flag-snipe]'); f.classList.add('on'); setTimeout(() => f.classList.remove('on'), 2200);
        }
      } else if (!cands.length) this.idle++;
      this.render(placed && placed.id);
      if (this.timeLeft <= 0) this.finish();
    }
    tickJapanese() {
      this.roundTick++;
      this.elapsed += 1;
      if (this.roundTick >= 3) {
        this.roundTick = 0;
        this.round++;
        const next = this.clockPrice - this.dec * 2;
        const active = this.bidders.filter((b) => b.active);
        const leaving = active.filter((b) => next < b.floor);
        if (leaving.length >= active.length) {
          const w = active.sort((a, b) => a.floor - b.floor)[0];
          w.bid = this.clockPrice;
          this.render(w.id);
          return this.finish(w);
        }
        this.clockPrice = next;
        leaving.forEach((b) => { b.active = false; b.exitAt = this.clockPrice; this.log(`Bidder ${b.id} exited`, this.clockPrice + this.dec * 2); });
        this.bidders.filter((b) => b.active).forEach((b) => { b.bid = this.clockPrice; });
        this.points.push([this.round, this.clockPrice]);
        this.log(`Round ${this.round}: price dropped`, this.clockPrice, true);
        const left = this.bidders.filter((b) => b.active);
        this.render();
        if (left.length === 1) return this.finish(left[0]);
      } else this.render();
    }
    finish(winner) {
      this.stop();
      this.finished = true;
      const w = winner || this.l1();
      this.setStatus('done', 'Closed');
      this.setToggle(false);
      const r = this.q('[data-au-result]');
      if (w) {
        const met = w.bid <= this.reserve;
        r.textContent = `Auction closed. L1: Bidder ${w.id} at ${inr(w.bid)}${this.unit}. ${met ? 'Reserve met.' : 'Reserve not met.'} Award goes to NFA approval; the buyer decides.`;
        this.log(`Closed · L1 Bidder ${w.id}`, w.bid, true);
      } else r.textContent = 'Auction closed with no bids.';
      r.hidden = false;
      this.render();
      if (this.autoplay) {
        this.restartTimer = setTimeout(() => {
          const rect = this.el.getBoundingClientRect();
          if (!doc.hidden && rect.top < window.innerHeight && rect.bottom > 0) { this.reset(); this.start(); }
        }, 7000);
      }
    }
    render(flashId) {
      const jp = this.mode === 'japanese';
      const timerEl = this.q('[data-au-timer]');
      if (jp) {
        timerEl.textContent = `00:0${this.finished ? 0 : 3 - this.roundTick}`;
        timerEl.parentElement.classList.remove('urgent');
        this.q('[data-au-clock-price]').textContent = inr(this.clockPrice);
        const a = this.bidders.filter((b) => b.active).length;
        this.q('[data-au-clock-sub]').textContent = `Round ${this.round} · ${a} bidder${a === 1 ? '' : 's'} still in`;
        const bar = this.q('[data-au-clock-bar]');
        bar.style.transition = reduceMotion.matches ? 'none' : 'transform .6s linear';
        bar.style.transform = `scaleX(${this.finished ? 0 : 1 - this.roundTick / 3})`;
        this.q('[data-au-l1]').textContent = inr(this.clockPrice);
      } else {
        const m = Math.floor(this.timeLeft / 60), s = this.timeLeft % 60;
        timerEl.textContent = `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`;
        timerEl.parentElement.classList.toggle('urgent', this.timeLeft <= 30 && this.running);
        const l1 = this.l1();
        this.q('[data-au-l1]').textContent = l1 ? inr(l1.bid) : '—';
      }
      const sorted = jp
        ? [...this.bidders.filter((b) => b.active), ...this.bidders.filter((b) => !b.active).sort((a, b) => a.exitAt - b.exitAt)]
        : [...this.bidders].sort((a, b) => (a.bid === null) - (b.bid === null) || (a.bid || 0) - (b.bid || 0));
      this.q('[data-au-rank]').innerHTML = sorted.map((b, i) => {
        let rk = '—', sub = 'Waiting to bid', amt = '—', small = '';
        if (jp) {
          rk = b.active ? (this.finished ? 'L1' : 'IN') : 'OUT';
          sub = b.active ? (this.round ? `Confirmed at ${inr(this.clockPrice)}` : 'Ready') : `Exited at ${inr(b.exitAt + this.dec * 2)}`;
          amt = b.active ? inr(this.clockPrice) : '—';
        } else if (b.bid !== null) {
          rk = `L${i + 1}`; sub = `Last bid ${b.at}`; amt = inr(b.bid); small = `▼ ${inr(this.ceiling - b.bid)}`;
        }
        const cls = [b.id === flashId && !reduceMotion.matches ? 'flash' : '', jp && !b.active ? 'out' : ''].join(' ').trim();
        return `<li${cls ? ` class="${cls}"` : ''}><span class="rk">${rk}</span><span class="bidder">Bidder ${b.id}<small>${sub}</small></span>`
          + `<span class="amt">${amt}${small ? `<small>${small}</small>` : ''}</span></li>`;
      }).join('');
      const bids = this.bidders.filter((b) => b.bid !== null).length;
      this.q('[data-au-bids]').textContent = jp ? `Round ${this.round}` : `${this.history.filter((h) => !h.sys).length} bids · ${bids} bidders`;
      this.q('[data-au-history]').innerHTML = this.history.map((h) =>
        `<li><time>${h.time}</time><span class="${h.sys ? 'sys' : ''}">${h.text}</span><b>${h.amount ? inr(h.amount) : ''}</b></li>`).join('');
      const cur = jp ? this.clockPrice : (this.l1() ? this.l1().bid : this.ceiling);
      const rf = this.q('[data-au-flag-reserve]');
      rf.classList.toggle('met', cur <= this.reserve);
      rf.lastChild.textContent = cur <= this.reserve ? 'Reserve met' : 'Reserve not met';
      this.drawSpark();
    }
    drawSpark() {
      const top = this.ceiling, bottom = this.reserve - (this.ceiling - this.reserve) * 0.35;
      const y = (v) => 4 + (top - v) / (top - bottom) * 56;
      const maxX = this.mode === 'japanese' ? Math.max(12, this.round) : Math.max(this.duration, this.elapsed);
      const pts = [[0, this.ceiling], ...this.points];
      const coords = pts.map(([t, v]) => `${(t / maxX * 300).toFixed(1)},${y(v).toFixed(1)}`);
      const lastX = (pts[pts.length - 1][0] / maxX * 300).toFixed(1);
      this.q('[data-au-spark]').setAttribute('points', coords.join(' '));
      this.q('[data-au-area]').setAttribute('points', `0,64 ${coords.join(' ')} ${lastX},64`);
      const line = this.q('[data-au-reserve-line]');
      line.setAttribute('y1', y(this.reserve).toFixed(1));
      line.setAttribute('y2', y(this.reserve).toFixed(1));
    }
  }

  /* ------------------------------------------------------------------------
     AI negotiation panel (vendor discovery → buyer decision)
     ------------------------------------------------------------------------ */
  const NEGO_SCRIPT = [
    { wait: 500, step: 'discover', state: 'Discovering vendors', sys: 'Found 4 vendors matching “Nitrile gloves, 12-inch” in the vendor pool.' },
    { wait: 1100, step: 'verify', state: 'Verifying GSTIN', gst: ['A', 'B'] },
    { wait: 800, gst: ['C', 'D'], sys: 'GSTIN verified for 4 of 4 vendors.' },
    { wait: 900, step: 'negotiate', state: 'Negotiating with Vendor B', with: 'Vendor B', ai: 'Hello, this is the ProcEaze AI Negotiator, on behalf of the buyer for RFQ-2026-0318: 1,200 boxes of 12-inch nitrile gloves. Your quote is ₹425 per box. Our benchmark for this specification is lower. Can you revise?' },
    { wait: 1700, vendor: 'B', text: 'We can do ₹405 if delivery is within 10 days.', offer: ['B', 405] },
    { wait: 1500, ai: 'Delivery within 10 days works. Can you reach ₹385 for the full quantity in a single dispatch?' },
    { wait: 1700, vendor: 'B', text: '₹392 is our best for a single dispatch.', offer: ['B', 392] },
    { wait: 1400, ai: 'If we split the order into two dispatches a week apart, can you meet ₹386?' },
    { wait: 1800, vendor: 'B', text: 'Two dispatches: ₹384 per box, GST extra.', offer: ['B', 384] },
    { wait: 1300, ai: 'Noted: ₹384 per box, GST extra, two dispatches. I will share this with the buyer. The final award is made by the buyer.' },
    { wait: 900, ok: true, sys: 'Vendor B is below the ₹385 target. Added to the shortlist.' },
    { wait: 1100, state: 'Negotiating with Vendor A', with: 'Vendor A', ai: 'Vendor A, there is a lower offer than your quote of ₹438. Would you like to revise?' },
    { wait: 1600, vendor: 'A', text: 'We can revise to ₹389 per box with 7-day delivery.', offer: ['A', 389] },
    { wait: 1100, offer: ['C', 430], sys: 'Vendor C revised to ₹430 and holds. Reliability score 74.' },
    { wait: 1100, offer: ['D', 412], escalate: 'D', sys: 'Vendor D asked for 45-day credit terms, outside your policy. Escalated to the buyer.' },
    { wait: 1000, step: 'shortlist', state: 'Shortlist ready · awaiting buyer', ok: true, sys: 'Shortlist ready: Vendor B ₹384, Vendor A ₹389. Awaiting buyer decision.' },
    { wait: 500, step: 'decide' },
  ];
  const QUOTES = { A: 438, B: 425, C: 451, D: 446 };

  function chatMsg(container, cls, label, text, max = 9) {
    $$('.nego-typing', container).forEach((n) => n.remove());
    const el = doc.createElement('div');
    el.className = `nego-msg ${cls}`;
    if (label) { const s = doc.createElement('small'); s.textContent = label; el.appendChild(s); }
    el.appendChild(doc.createTextNode(text));
    container.appendChild(el);
    const msgs = $$('.nego-msg', container);
    if (msgs.length > max) msgs[0].remove();
  }
  function typing(container, who) {
    $$('.nego-typing', container).forEach((n) => n.remove());
    const el = doc.createElement('div');
    el.className = 'nego-typing';
    el.setAttribute('aria-hidden', 'true');
    if (who === 'ai') el.style.alignSelf = 'flex-end';
    el.innerHTML = '<span></span><span></span><span></span>';
    container.appendChild(el);
  }

  class NegotiationSim {
    constructor(el) {
      this.el = el;
      this.q = (s) => el.querySelector(s);
      this.thread = this.q('[data-nego-transcript]');
      this.timers = [];
      this.played = false;
      $$('[data-nego-channel]', el).forEach((b) => b.addEventListener('click', () => {
        $$('[data-nego-channel]', el).forEach((x) => x.setAttribute('aria-pressed', String(x === b)));
        el.dataset.channel = b.dataset.negoChannel;
        this.voiceLabel();
      }));
      ['[data-nego-run]', '[data-nego-reset]'].forEach((s) => { const b = this.q(s); b && b.addEventListener('click', () => this.run()); });
      $$('[data-nego-action]', el).forEach((b) => b.addEventListener('click', () => this.action(b.dataset.negoAction)));
      if (el.hasAttribute('data-autoplay') && !reduceMotion.matches) whenVisible(el, () => { if (!this.played) this.run(); });
    }
    clear() { this.timers.forEach(clearTimeout); this.timers = []; }
    reset() {
      this.clear();
      this.offers = { ...QUOTES };
      this.flags = {};
      this.with = null;
      this.thread.innerHTML = '';
      $$('[data-nego-steps] li', this.el).forEach((li) => li.classList.remove('active', 'done'));
      $$('[data-nego-pool] [data-gst]', this.el).forEach((s) => { s.className = 'gst-pending'; s.textContent = 'GSTIN pending'; });
      this.state('Ready · RFQ-2026-0318');
      this.board();
      this.voiceLabel();
    }
    run() {
      this.reset();
      this.played = true;
      let t = 0;
      NEGO_SCRIPT.forEach((ev) => {
        t += reduceMotion.matches ? Math.min(ev.wait, 500) : ev.wait;
        if ((ev.vendor || ev.ai) && !reduceMotion.matches) this.timers.push(setTimeout(() => typing(this.thread, ev.vendor ? 'vendor' : 'ai'), Math.max(0, t - 650)));
        this.timers.push(setTimeout(() => this.apply(ev), t));
      });
    }
    state(t) { const s = this.q('[data-nego-state]'); if (s) s.textContent = t; }
    step(key) {
      const items = $$('[data-nego-steps] li', this.el);
      const idx = items.findIndex((li) => li.dataset.step === key);
      items.forEach((li, i) => { li.classList.toggle('done', i < idx); li.classList.toggle('active', i === idx); });
    }
    voiceLabel() {
      const w = this.q('[data-nego-voice-who]');
      if (w) w.textContent = this.with ? `On call with ${this.with}` : 'Voice channel ready';
      const lab = this.q('[data-nego-with]');
      if (lab) lab.textContent = this.with ? `${this.el.dataset.channel === 'voice' ? 'Voice' : 'Chat'} · ${this.with}` : '—';
    }
    apply(ev) {
      if (ev.step) this.step(ev.step);
      if (ev.state) this.state(ev.state);
      if (ev.with) { this.with = ev.with; this.voiceLabel(); }
      if (ev.gst) ev.gst.forEach((v) => {
        const s = this.q(`[data-nego-pool] [data-vendor="${v}"] [data-gst]`);
        if (s) { s.className = 'gst-ok'; s.innerHTML = `${svg('<path d="M20 6 9 17l-5-5"/>')}GSTIN verified`; }
      });
      const voice = this.el.dataset.channel === 'voice';
      if (ev.ai) chatMsg(this.thread, 'ai', voice ? 'AI Negotiator · voice' : 'AI Negotiator', ev.ai);
      if (ev.vendor) chatMsg(this.thread, 'vendor', `Vendor ${ev.vendor}${voice ? ' · voice' : ''}`, ev.text);
      if (ev.sys) chatMsg(this.thread, `sys${ev.ok ? ' ok' : ''}`, '', ev.sys);
      if (ev.offer) { this.offers[ev.offer[0]] = ev.offer[1]; this.board(ev.offer[0]); }
      if (ev.escalate) { this.flags[ev.escalate] = 'escalated'; this.board(); }
      if (ev.step === 'decide') { this.state('Awaiting buyer decision'); this.with = null; this.voiceLabel(); }
    }
    board(changed) {
      const board = this.q('[data-nego-board]');
      if (!board) return;
      const rows = $$('li', board).sort((a, b) => this.offers[a.dataset.vendor] - this.offers[b.dataset.vendor]);
      rows.forEach((li, i) => {
        const v = li.dataset.vendor, offer = this.offers[v], diff = QUOTES[v] - offer;
        li.querySelector('.pos').textContent = i + 1;
        li.classList.toggle('lead', i === 0 && diff > 0);
        let note = '<small class="m-neutral">Quoted</small>';
        if (this.flags[v] === 'escalated') note = '<small style="color:var(--warning-ink)">Escalated</small>';
        else if (offer <= 385) note = '<small class="m-up">At target ✓</small>';
        else if (diff > 0) note = `<small class="m-up">▼ ₹${diff}</small>`;
        li.querySelector('[data-offer]').innerHTML = `₹${offer}${note}`;
        if (v === changed && !reduceMotion.matches) {
          li.style.transition = 'none'; li.style.background = '#DCE7FF';
          requestAnimationFrame(() => { li.style.transition = 'background-color 1s'; li.style.background = ''; });
        }
        board.appendChild(li);
      });
    }
    action(kind) {
      if (kind === 'approve') toast('Demo: the shortlist opens for the buyer to review. Any award goes through NFA approval.', 'info');
      else if (kind === 'escalate') { toast('Demo: negotiation escalated to the buyer with the full transcript.', 'info'); chatMsg(this.thread, 'sys', '', 'Escalated to the buyer with the full transcript.'); }
      else if (kind === 'override') {
        this.clear();
        chatMsg(this.thread, 'sys', '', 'Buyer took over the negotiation. The AI has paused.');
        this.state('Paused · buyer in control');
        toast('Demo: the buyer takes over. The AI pauses immediately.', 'info');
      }
    }
  }

  /* ------------------------------------------------------------------------
     Negotiation control tower (home / AI page / product tour)
     ------------------------------------------------------------------------ */
  const TOWER_BASE = { A: 1240, B: 1210, C: 1265, D: 1225 };
  const TOWER_SCRIPT = [
    { wait: 500, sys: 'Vendor pool loaded: 4 vendors, GSTIN verified. Target ₹1,100 / unit.' },
    { wait: 900, talk: 'B', ai: 'Can you improve the unit rate for 2,500 units?' },
    { wait: 1500, vendor: 'B', text: '₹1,180 / unit', offer: 1180, status: ['Countered', 'blue'], resp: '1m 42s' },
    { wait: 1300, talk: 'B', ai: 'Volume commitment available. Target: ₹1,100.' },
    { wait: 1500, vendor: 'B', text: '₹1,135 / unit', offer: 1135, status: ['Countered', 'blue'], resp: '2m 05s' },
    { wait: 1200, talk: 'A', ai: 'There is a lower offer for 2,500 pairs. Can you revise your rate?' },
    { wait: 1500, vendor: 'A', text: '₹1,150 / unit, delivery in 7 days.', offer: 1150, status: ['Countered', 'blue'], resp: '3m 10s' },
    { wait: 1200, talk: 'D', ai: 'Can you match ₹1,150 for 2,500 pairs?' },
    { wait: 1400, vendor: 'D', text: '₹1,160 with 60-day credit.', offer: 1160, status: ['Escalated', 'amber'], resp: '4m 22s', sys: '60-day credit is outside policy. Escalated to the buyer.' },
    { wait: 1100, talk: 'C', target: 'C', status: ['Holding', 'grey'], resp: '6m 40s', sys: 'Vendor C holds at ₹1,265.' },
    { wait: 1200, talk: 'B', ai: 'Two dispatches a week apart. Can you meet ₹1,120?' },
    { wait: 1500, vendor: 'B', text: '₹1,125 / unit, final.', offer: 1125, status: ['Shortlisted', 'green'], resp: '1m 18s' },
    { wait: 1000, done: true, ok: true, sys: 'Shortlist ready: Vendor B ₹1,125 · Vendor A ₹1,150. The buyer decides.' },
  ];

  class ControlTower {
    constructor(el) {
      this.el = el;
      this.thread = $('[data-tw-thread]', el);
      this.timers = [];
      this.played = false;
      const run = $('[data-tw-run]', el);
      run && run.addEventListener('click', () => this.run());
      const ov = $('[data-tw-action="override"]', el);
      ov && ov.addEventListener('click', () => this.override());
      this.reset(true);
      if (el.hasAttribute('data-autoplay') && !reduceMotion.matches) whenVisible(el, () => { if (!this.played) this.run(); }, null, 0.4);
    }
    card(v) { return $(`[data-tv="${v}"]`, this.el); }
    reset(initial) {
      this.timers.forEach(clearTimeout); this.timers = [];
      this.offers = { ...TOWER_BASE };
      $$('[data-tv]', this.el).forEach((c) => {
        c.classList.remove('is-talking');
        $('[data-tv-offer]', c).textContent = inr(this.offers[c.dataset.tv]);
        const st = $('[data-tv-status]', c); st.className = 'm-chip grey'; st.textContent = 'Quoted';
        $('[data-tv-resp]', c).textContent = 'Resp. —';
      });
      if (!initial) this.thread.innerHTML = '';
      this.ranks();
      this.el.classList.remove('is-running');
    }
    ranks() {
      const order = Object.keys(this.offers).sort((a, b) => this.offers[a] - this.offers[b]);
      order.forEach((v, i) => { const r = $('[data-tv-rank]', this.card(v)); r.textContent = `L${i + 1}`; r.classList.toggle('l1', i === 0); });
    }
    run() {
      this.reset();
      this.played = true;
      this.el.classList.add('is-running');
      let t = 0;
      TOWER_SCRIPT.forEach((ev) => {
        t += reduceMotion.matches ? Math.min(ev.wait, 450) : ev.wait;
        if ((ev.ai || ev.vendor) && !reduceMotion.matches) this.timers.push(setTimeout(() => typing(this.thread, ev.vendor ? 'vendor' : 'ai'), Math.max(0, t - 600)));
        this.timers.push(setTimeout(() => this.apply(ev), t));
      });
    }
    apply(ev) {
      if (ev.talk) $$('[data-tv]', this.el).forEach((c) => c.classList.toggle('is-talking', c.dataset.tv === ev.talk));
      if (ev.ai) chatMsg(this.thread, 'ai', `AI → Vendor ${ev.talk}`, ev.ai, 7);
      const v = ev.vendor || ev.target;
      if (ev.vendor) chatMsg(this.thread, 'vendor', `Vendor ${ev.vendor}`, ev.text, 7);
      if (v) {
        const c = this.card(v);
        if (ev.offer) {
          this.offers[v] = ev.offer;
          const o = $('[data-tv-offer]', c);
          o.textContent = inr(ev.offer);
          o.classList.add('drop'); setTimeout(() => o.classList.remove('drop'), 900);
          this.ranks();
        }
        if (ev.status) { const st = $('[data-tv-status]', c); st.className = `m-chip ${ev.status[1]}`; st.textContent = ev.status[0]; }
        if (ev.resp) $('[data-tv-resp]', c).textContent = `Resp. ${ev.resp}`;
      }
      if (ev.sys) chatMsg(this.thread, `sys${ev.ok ? ' ok' : ''}`, '', ev.sys, 7);
      if (ev.done) {
        $$('[data-tv]', this.el).forEach((c) => c.classList.remove('is-talking'));
        const a = $('[data-tv-status]', this.card('A')); a.className = 'm-chip green'; a.textContent = 'Shortlisted';
        this.el.classList.remove('is-running');
      }
    }
    override() {
      this.timers.forEach(clearTimeout); this.timers = [];
      $$('[data-tv]', this.el).forEach((c) => c.classList.remove('is-talking'));
      this.el.classList.remove('is-running');
      chatMsg(this.thread, 'sys', '', 'Buyer took over. The AI has paused; nothing is awarded without the buyer.', 7);
      toast('Demo: the buyer takes over. The AI pauses immediately.', 'info');
    }
  }

  /* ------------------------------------------------------------------------
     Orbit (categories) and vault (security)
     ------------------------------------------------------------------------ */
  function initOrbit(orbit) {
    if (!once(orbit, '_orbit')) return;
    const items = $$('[data-orbit-item]', orbit);
    const core = $('[data-orbit-core]', orbit);
    const isVault = orbit.classList.contains('vault');
    let idx = -1, timer = null, touched = false;
    const esc = (s) => s.replace(/[&<>"]/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
    const show = (i) => {
      idx = i;
      const it = items[i];
      items.forEach((x) => x.setAttribute('aria-pressed', String(x === it)));
      orbit.classList.add('has-active');
      orbit.style.setProperty('--ray', getComputedStyle(it).getPropertyValue('--a'));
      const { name, desc, ex } = it.dataset;
      core.innerHTML = isVault
        ? `<span class="vault-shield">${$('.orbit-ico', it).innerHTML}</span><strong>${esc(name)}</strong><span>${esc(desc)}</span>`
        : `<span class="orbit-k">Category</span><strong>${esc(name)}</strong><span>${esc(desc)}</span>${ex ? `<span class="orbit-k" style="margin-top:4px">${esc(ex)}</span>` : ''}`;
    };
    items.forEach((it, i) => {
      it.addEventListener('click', () => { touched = true; clearInterval(timer); show(i); });
      it.addEventListener('mouseenter', () => { touched = true; clearInterval(timer); show(i); });
      it.addEventListener('focus', () => show(i));
    });
    if (reduceMotion.matches) return;
    whenVisible(orbit, () => {
      if (touched) return;
      clearInterval(timer);
      timer = setInterval(() => show((idx + 1) % items.length), 2600);
      if (idx < 0) show(0);
    }, () => clearInterval(timer), 0.4);
  }

  /* ------------------------------------------------------------------------
     Engagement switch — RUN IT / RUN IT WITH US
     ------------------------------------------------------------------------ */
  function initEngage(el) {
    if (!once(el, '_es')) return;
    $$('.es-row', el).forEach((r, i) => r.style.setProperty('--i', i));
    $$('[data-es-mode]', el).forEach((b) => b.addEventListener('click', () => {
      el.dataset.mode = b.dataset.esMode;
      $$('[data-es-mode]', el).forEach((x) => x.setAttribute('aria-pressed', String(x === b)));
    }));
  }

  /* ------------------------------------------------------------------------
     Audit trail — select an event; autoplays through the record
     ------------------------------------------------------------------------ */
  function initAudit(el) {
    if (!once(el, '_audit')) return;
    const items = $$('[data-at-item]', el);
    const f = (k) => $(`[data-at-f="${k}"]`, el);
    let idx = 0, timer = null, touched = false;
    const show = (i) => {
      idx = i;
      items.forEach((it, j) => { it.setAttribute('aria-pressed', String(j === i)); it.classList.toggle('is-past', j < i); });
      const d = items[i].dataset;
      f('user').textContent = d.user; f('action').textContent = d.action;
      f('time').textContent = `14 Oct 2026, ${d.time} IST`; f('remark').textContent = d.remark;
      const dl = $('.at-detail dl', el); dl.style.animation = 'none'; void dl.offsetWidth; dl.style.animation = '';
    };
    items.forEach((it, i) => it.addEventListener('click', () => { touched = true; clearInterval(timer); show(i); }));
    const exp = $('[data-at-export]', el);
    exp && exp.addEventListener('click', () => toast('Demo: in the product, the audit trail downloads as CSV or PDF.', 'info'));
    if (reduceMotion.matches) return;
    whenVisible(el, () => {
      if (touched) return;
      clearInterval(timer);
      timer = setInterval(() => show((idx + 1) % items.length), 1900);
    }, () => clearInterval(timer), 0.4);
  }

  /* ------------------------------------------------------------------------
     Module carousel — scroll-snap track, arrows, progress dots, autoplay
     that pauses on hover / focus / off-screen and resumes after
     ------------------------------------------------------------------------ */
  function initCarousel(el) {
    if (!once(el, '_mc')) return;
    const track = $('[data-mc-track]', el);
    const slides = $$('.mc-slide', track);
    const dotsWrap = $('[data-mc-dots]', el);
    const prev = $('[data-mc-prev]', el), next = $('[data-mc-next]', el);
    const dur = parseFloat(getComputedStyle(el).getPropertyValue('--mc-dur')) || 4800;
    const noun = el.dataset.mcItem || 'capability';
    let idx = 0, max = 0, dots = [], timer = null, ticking = false;
    let focused = false, visible = false;

    const off = (i) => slides[i].offsetLeft - slides[0].offsetLeft;
    const maxScroll = () => track.scrollWidth - track.clientWidth;
    const go = (i) => track.scrollTo({ left: Math.min(off(i), maxScroll()), behavior: reduceMotion.matches ? 'auto' : 'smooth' });

    const render = () => {
      slides.forEach((s, j) => s.classList.toggle('is-current', j === idx));
      dots.forEach((d, j) => d.setAttribute('aria-current', String(j === idx)));
    };
    const build = () => {
      const m = maxScroll();
      max = slides.findIndex((_, i) => off(i) >= m - 2);
      if (max < 0) max = slides.length - 1;
      dotsWrap.innerHTML = '';
      dots = Array.from({ length: max + 1 }, (_, i) => {
        const b = doc.createElement('button');
        b.type = 'button'; b.className = 'mc-dot';
        b.setAttribute('aria-label', `Go to ${noun} ${i + 1}`);
        b.addEventListener('click', () => { go(i); restart(); });
        dotsWrap.appendChild(b);
        return b;
      });
      idx = Math.min(idx, max);
      render();
    };
    const sync = () => {
      ticking = false;
      const x = track.scrollLeft;
      let best = 0;
      if (x >= maxScroll() - 2) best = max;
      else slides.forEach((_, i) => { if (i <= max && Math.abs(off(i) - x) < Math.abs(off(best) - x)) best = i; });
      if (best !== idx) { idx = best; render(); restart(); }
    };

    const running = () => !focused && visible;
    function restart() {
      clearTimeout(timer);
      const on = running();
      el.classList.remove('is-playing');
      if (!on) return;
      void el.offsetWidth; // restart the dot progress animation
      el.classList.add('is-playing');
      timer = setTimeout(() => go(idx >= max ? 0 : idx + 1), dur);
    }

    prev.addEventListener('click', () => { go(idx <= 0 ? max : idx - 1); restart(); });
    next.addEventListener('click', () => { go(idx >= max ? 0 : idx + 1); restart(); });
    el.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowRight') { e.preventDefault(); next.click(); }
      else if (e.key === 'ArrowLeft') { e.preventDefault(); prev.click(); }
    });
    track.addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(sync); } }, { passive: true });
    // Pause only while a keyboard user is inside the cards; mouse hover keeps it moving
    track.addEventListener('focusin', (e) => { if (e.target.matches(':focus-visible')) { focused = true; restart(); } });
    track.addEventListener('focusout', (e) => { if (!track.contains(e.relatedTarget)) { focused = false; restart(); } });
    let rz;
    window.addEventListener('resize', () => { clearTimeout(rz); rz = setTimeout(() => { build(); go(idx); }, 150); });

    build();
    whenVisible(el, () => { visible = true; restart(); }, () => { visible = false; restart(); }, 0.3);
  }

  /* ------------------------------------------------------------------------
     Wire everything (document on load; Explore tour on first open)
     ------------------------------------------------------------------------ */
  PE.onHydrate((root) => {
    $$('[data-lifecycle]', root).forEach(initLifecycle);
    $$('[data-arc-lock]', root).forEach(initArcLock);
    $$('[data-approval-engine]', root).forEach(initApprovalEngine);
    $$('[data-auction]', root).forEach((el) => once(el, '_au') && new AuctionSim(el));
    $$('[data-negotiator]', root).forEach((el) => once(el, '_ng') && new NegotiationSim(el));
    $$('[data-tower]', root).forEach((el) => once(el, '_tw') && new ControlTower(el));
    $$('[data-orbit]', root).forEach(initOrbit);
    $$('[data-engage]', root).forEach(initEngage);
    $$('[data-audit]', root).forEach(initAudit);
    $$('[data-carousel]', root).forEach(initCarousel);
  });
  doc.addEventListener('DOMContentLoaded', initFaq);
})();
