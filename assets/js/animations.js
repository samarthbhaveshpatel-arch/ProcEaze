/* ==========================================================================
   ProcEaze — animations.js
   Intro loader → hero entrance → control-plane request loop, scroll reveal,
   counters, chart animation, magnetic buttons, cursor light, scroll-driven
   "How it works". Everything degrades to a static, fully visible page under
   prefers-reduced-motion or without JavaScript.
   ========================================================================== */
(() => {
  'use strict';
  const PE = window.PE;
  const { $, $$, reduceMotion, canHover, whenVisible } = PE;
  const doc = document;
  const root = doc.documentElement;

  /* ------------------------------------------------------------------------
     Intro loader (~1s, first visit per session, click/key to skip)
     ------------------------------------------------------------------------ */
  function ready() {
    if (root.classList.contains('is-ready')) return;
    requestAnimationFrame(() => requestAnimationFrame(() => root.classList.add('is-ready')));
  }
  function initLoader() {
    const loader = $('[data-loader]');
    if (!loader || root.classList.contains('no-loader')) { ready(); return; }
    const start = performance.now();
    let done = false;
    const finish = () => {
      if (done) return;
      done = true;
      try { sessionStorage.setItem('pe-intro', '1'); } catch (_) { /* storage unavailable */ }
      loader.classList.add('is-done');
      ready();
      setTimeout(() => loader.remove(), 600);
    };
    const whenLoaded = () => setTimeout(finish, Math.max(0, 850 - (performance.now() - start)));
    if (doc.readyState === 'complete') whenLoaded(); else window.addEventListener('load', whenLoaded);
    setTimeout(finish, 1300); // hard cap
    loader.addEventListener('click', finish);
    doc.addEventListener('keydown', finish, { once: true });
  }

  /* ------------------------------------------------------------------------
     Control plane — a request travels Catalogue → … → Spend
     ------------------------------------------------------------------------ */
  function initControlPlane(cp) {
    const path = $('.cp-base', cp); // geometry source (the drawn twin uses pathLength for its dash animation)
    const packet = $('[data-cp-packet]', cp);
    const halo = $('[data-cp-halo]', cp);
    const nodes = $$('.cp-node', cp);
    const stage = $('[data-cp-stage]', cp);
    const stepEl = $('[data-cp-step]', cp);
    const timeEl = $('[data-cp-time]', cp);
    const segs = $$('[data-cp-progress] i', cp);
    if (!path || !nodes.length) return;
    const total = path.getTotalLength();
    // Length along the path at which each node sits
    const box = { w: 600, h: 400 };
    const pts = [];
    for (let l = 0; l <= total; l += 3) pts.push([l, path.getPointAtLength(l)]);
    const nodeLen = nodes.map((n) => {
      const x = parseFloat(n.style.getPropertyValue('--x')) / 100 * box.w;
      const y = parseFloat(n.style.getPropertyValue('--y')) / 100 * box.h;
      let best = 0, bd = Infinity;
      pts.forEach(([l, p]) => { const d = (p.x - x) ** 2 + (p.y - y) ** 2; if (d < bd) { bd = d; best = l; } });
      return best;
    });
    let current = -1;
    const setStage = (i) => {
      if (i === current) return;
      current = i;
      nodes.forEach((n, j) => { n.classList.toggle('is-done', j < i); n.classList.toggle('is-active', j === i); });
      segs.forEach((s, j) => s.classList.toggle('on', j <= i));
      stage.textContent = nodes[i].dataset.status;
      stage.classList.remove('flash'); void stage.offsetWidth; stage.classList.add('flash');
      stepEl.textContent = `${i + 1} / ${nodes.length}`;
      const secs = 9 * 3600 + 42 * 60 + 12 + i * 47 + (i > 3 ? 900 : 0);
      timeEl.textContent = [Math.floor(secs / 3600), Math.floor(secs / 60) % 60, secs % 60].map((v) => String(v).padStart(2, '0')).join(':');
    };
    const place = (len) => {
      const p = path.getPointAtLength(len);
      packet.setAttribute('cx', p.x); packet.setAttribute('cy', p.y);
      halo.setAttribute('cx', p.x); halo.setAttribute('cy', p.y);
    };
    if (reduceMotion.matches) { place(nodeLen[6]); setStage(6); return; }

    const TRAVEL = 9000, HOLD = 1400;
    let t0 = null, raf = null, running = false;
    const frame = (now) => {
      if (t0 === null) t0 = now;
      const el = now - t0;
      const t = Math.min(1, el / TRAVEL);
      const eased = t < .5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2;
      const len = eased * total;
      place(len);
      let idx = 0;
      nodeLen.forEach((l, i) => { if (len >= l - 4) idx = i; });
      setStage(idx);
      if (el >= TRAVEL + HOLD) t0 = now;
      raf = requestAnimationFrame(frame);
    };
    const play = () => { if (!running) { running = true; t0 = null; raf = requestAnimationFrame(frame); } };
    const pause = () => { running = false; cancelAnimationFrame(raf); };
    place(0); setStage(0);
    // Start after the hero entrance sequence
    const begin = () => whenVisible(cp, play, pause, 0.2);
    if (root.classList.contains('is-ready')) setTimeout(begin, 1400);
    else new MutationObserver((m, obs) => { if (root.classList.contains('is-ready')) { obs.disconnect(); setTimeout(begin, 1600); } })
      .observe(root, { attributes: true, attributeFilter: ['class'] });
    doc.addEventListener('visibilitychange', () => (doc.hidden ? pause() : play()));
  }

  /* ------------------------------------------------------------------------
     Scroll reveal, chart animation, counters
     ------------------------------------------------------------------------ */
  const REVEAL = '.reveal, .reveal-frame, .anim-bars, .lc-chart, .gauge, .funnel, [data-lifecycle]';
  /* Any figure counts up from 0: "5,00,000+", "56+", "100%", "₹24.8 Cr", "6.2 h", "312 POs".
     Text that isn't a plain figure ("24x7", "1–5", "Ready") is left as it is. */
  const COUNT_SEL = '[data-count], .stat-value, .m-kpi-value';
  const NUM = /^(\D*?)(\d[\d,]*(?:\.\d+)?)(\s*(?:[%+]|[A-Za-z][A-Za-z. ]*)?\+?)$/;
  function parseCount(el) {
    if (el.dataset.count) {
      return { pre: '', n: parseFloat(el.dataset.count), dec: 0, grouped: true, suf: el.dataset.suffix || '' };
    }
    if (el.querySelector('[data-count], *')) return null; // only plain-text figures
    const m = el.textContent.trim().match(NUM);
    if (!m) return null;
    const raw = m[2];
    return { pre: m[1], n: parseFloat(raw.replace(/,/g, '')), dec: (raw.split('.')[1] || '').length, grouped: raw.includes(','), suf: m[3] };
  }
  const fmt = (c, v) => c.pre + (c.grouped
    ? Math.round(v).toLocaleString('en-IN')
    : v.toFixed(c.dec)) + c.suf;
  function animateCount(el, c) {
    cancelAnimationFrame(c.raf);
    const start = performance.now(), dur = c.n > 1000 ? 1900 : 1500;
    const step = (now) => {
      const t = Math.min(1, (now - start) / dur);
      el.textContent = fmt(c, c.n * (1 - Math.pow(1 - t, 4)));
      if (t < 1) c.raf = requestAnimationFrame(step);
      else el.textContent = fmt(c, c.n);
    };
    c.raf = requestAnimationFrame(step);
  }
  function resetCount(el, c) {
    cancelAnimationFrame(c.raf);
    clearTimeout(c.timer);
    el.textContent = fmt(c, 0);
  }
  function initReveal(scope) {
    const els = $$(REVEAL, scope);
    if (reduceMotion.matches || !('IntersectionObserver' in window)) { els.forEach((e) => e.classList.add('is-visible')); return; }
    const io = new IntersectionObserver((entries) => entries.forEach((en) => {
      if (en.isIntersecting) { en.target.classList.add('is-visible'); io.unobserve(en.target); }
    }), { rootMargin: '0px 0px -6% 0px', threshold: 0.1 });
    els.forEach((e) => io.observe(e));
    // Every figure starts at 0 and counts up each time it scrolls into view;
    // once it is fully out of view it resets to 0, ready to count again
    const counts = new Map();
    $$(COUNT_SEL, scope).forEach((el) => {
      const c = parseCount(el);
      if (!c || !(c.n > 0)) return;
      c.armed = true;
      counts.set(el, c);
      el.textContent = fmt(c, 0);
    });
    const co = new IntersectionObserver((entries) => entries.forEach((en) => {
      const el = en.target, c = counts.get(el);
      if (!en.isIntersecting) {
        if (!c.armed) { resetCount(el, c); c.armed = true; }
        return;
      }
      if (en.intersectionRatio < 0.5 || !c.armed) return;
      c.armed = false;
      // Hero capsules count once the entrance sequence has revealed them
      const delay = el.closest('.capsule') && !root.classList.contains('is-ready') ? 1600 : 0;
      c.timer = setTimeout(() => animateCount(el, c), delay);
    }), { threshold: [0, 0.5] });
    counts.forEach((_, el) => co.observe(el));
    // Coming back with the browser's Back / Forward buttons: count again
    window.addEventListener('pageshow', (e) => {
      if (!e.persisted) return;
      counts.forEach((c, el) => {
        resetCount(el, c);
        const r = el.getBoundingClientRect();
        c.armed = !(r.bottom > 0 && r.top < window.innerHeight && el.offsetParent !== null);
        if (!c.armed) animateCount(el, c);
      });
    });
  }

  /* ------------------------------------------------------------------------
     Magnetic buttons + cursor-following light (pointer devices only)
     ------------------------------------------------------------------------ */
  function initPointerEffects() {
    if (reduceMotion.matches || !canHover.matches) return;
    $$('.magnetic').forEach((el) => {
      el.addEventListener('pointermove', (e) => {
        const r = el.getBoundingClientRect();
        const dx = (e.clientX - (r.left + r.width / 2)) / (r.width / 2);
        const dy = (e.clientY - (r.top + r.height / 2)) / (r.height / 2);
        el.style.transform = `translate(${dx * 6}px, ${dy * 5}px)`;
      });
      el.addEventListener('pointerleave', () => { el.style.transform = ''; });
    });
    $$('.section-dark, .cta-band').forEach((sec) => {
      sec.classList.add('cursor-light');
      sec.addEventListener('pointermove', (e) => {
        const r = sec.getBoundingClientRect();
        sec.style.setProperty('--mx', `${e.clientX - r.left}px`);
        sec.style.setProperty('--my', `${e.clientY - r.top}px`);
      });
      sec.addEventListener('pointerenter', () => sec.classList.add('is-lit'));
      sec.addEventListener('pointerleave', () => sec.classList.remove('is-lit'));
    });
  }

  /* ------------------------------------------------------------------------
     How it works — the line fills and steps activate as you scroll
     ------------------------------------------------------------------------ */
  function initHow() {
    $$('[data-how]').forEach((how) => {
      const list = $('.how-steps', how);
      const line = $('[data-how-line]', how);
      const steps = $$('[data-how-step]', how);
      if (reduceMotion.matches) { line.style.setProperty('--p', '100%'); steps.forEach((s) => s.classList.add('is-active')); return; }
      let ticking = false;
      const update = () => {
        ticking = false;
        const r = list.getBoundingClientRect();
        const mid = window.innerHeight * 0.6;
        const p = Math.max(0, Math.min(1, (mid - r.top) / r.height));
        line.style.setProperty('--p', `${(p * 100).toFixed(1)}%`);
        steps.forEach((s) => s.classList.toggle('is-active', s.getBoundingClientRect().top < mid));
      };
      const onScroll = () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } };
      window.addEventListener('scroll', onScroll, { passive: true });
      window.addEventListener('resize', onScroll);
      update();
    });
  }

  /* ------------------------------------------------------------------------
     Wire up
     ------------------------------------------------------------------------ */
  PE.onHydrate((scope) => {
    if (scope !== doc) {
      // Product tour: no scroll choreography, show everything immediately
      $$(REVEAL, scope).forEach((e) => e.classList.add('is-visible'));
      return;
    }
    initReveal(doc);
  });
  doc.addEventListener('DOMContentLoaded', () => {
    initLoader();
    $$('[data-control-plane]').forEach(initControlPlane);
    initPointerEffects();
    initHow();
  });
})();
