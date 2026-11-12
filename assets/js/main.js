/* ==========================================================================
   ProcEaze — main.js
   Core: shared namespace (PE), toasts, header, mega menus, mobile menu,
   tabs, demo modal, back-to-top.
   Loaded first (defer); forms.js, interactions.js and animations.js build on PE.
   ========================================================================== */
(() => {
  'use strict';

  const doc = document;
  const $ = (s, c = doc) => c.querySelector(s);
  const $$ = (s, c = doc) => Array.from(c.querySelectorAll(s));
  const reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)');
  const canHover = window.matchMedia('(hover: hover) and (pointer: fine)');
  const inr = (n) => '₹' + Math.round(n).toLocaleString('en-IN');
  const svg = (p) => `<svg class="icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">${p}</svg>`;
  const ICON = {
    success: svg('<circle cx="12" cy="12" r="10"/><path d="m9 12 2 2 4-4"/>'),
    info: svg('<circle cx="12" cy="12" r="10"/><path d="M12 16v-4M12 8h.01"/>'),
    error: svg('<circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/>'),
    close: svg('<path d="M18 6 6 18M6 6l12 12"/>'),
    play: svg('<polygon points="6 3 20 12 6 21 6 3"/>'),
    pause: svg('<rect x="14" y="4" width="4" height="16" rx="1"/><rect x="6" y="4" width="4" height="16" rx="1"/>'),
    check: svg('<path d="M20 6 9 17l-5-5"/>'),
  };

  /** Run fn when el scrolls into view (and optional onLeave). */
  function whenVisible(el, onEnter, onLeave, threshold = 0.35) {
    if (!('IntersectionObserver' in window)) { onEnter(); return; }
    new IntersectionObserver((entries) => {
      entries.forEach((en) => (en.isIntersecting ? onEnter() : onLeave && onLeave()));
    }, { threshold }).observe(el);
  }

  /* ------------------------------------------------------------------------
     Toasts
     ------------------------------------------------------------------------ */
  function toast(message, type = 'info', timeout = 5200) {
    const region = $('[data-toasts]');
    if (!region) return;
    const el = doc.createElement('div');
    el.className = `toast ${type}`;
    el.setAttribute('role', type === 'error' ? 'alert' : 'status');
    el.innerHTML = `${ICON[type] || ICON.info}<div></div><button type="button" aria-label="Dismiss notification">${ICON.close}</button>`;
    el.children[1].textContent = message;
    const remove = () => {
      el.classList.add('out');
      setTimeout(() => { el.remove(); doc.body.classList.toggle('has-toast', region.children.length > 0); }, 280);
    };
    el.querySelector('button').addEventListener('click', remove);
    region.appendChild(el);
    doc.body.classList.add('has-toast');
    if (timeout) setTimeout(remove, timeout);
  }

  /* ------------------------------------------------------------------------
     Tabs (WAI-ARIA). Emits "tabchange" {index} on the [data-tabs] wrapper.
     wrap._select(i) lets other modules drive a tab set programmatically.
     ------------------------------------------------------------------------ */
  function initTabs(root = doc) {
    $$('[data-tabs]', root).forEach((wrap) => {
      if (wrap._tabsReady) return;
      wrap._tabsReady = true;
      const tabs = $$('[role="tab"]', wrap).filter((t) => t.closest('[data-tabs]') === wrap);
      if (!tabs.length) return;
      const select = (tab, focus, silent) => {
        tabs.forEach((t) => {
          const on = t === tab;
          t.setAttribute('aria-selected', String(on));
          t.tabIndex = on ? 0 : -1;
          const panel = doc.getElementById(t.getAttribute('aria-controls'));
          if (panel) {
            panel.hidden = !on;
            if (on) $$('.reveal, .reveal-frame, .anim-bars, .lc-chart, .gauge, .funnel', panel).forEach((el) => el.classList.add('is-visible'));
          }
        });
        if (focus) tab.focus();
        const list = tab.closest('[role="tablist"]');
        if (list && list.scrollWidth > list.clientWidth + 2) {
          list.scrollTo({ left: tab.offsetLeft - list.clientWidth / 2 + tab.offsetWidth / 2, behavior: reduceMotion.matches ? 'auto' : 'smooth' });
        }
        wrap.dispatchEvent(new CustomEvent('tabchange', { detail: { index: tabs.indexOf(tab), user: !silent } }));
      };
      wrap._select = (i) => select(tabs[(i + tabs.length) % tabs.length], false, true);
      wrap._index = () => tabs.findIndex((t) => t.getAttribute('aria-selected') === 'true');
      tabs.forEach((tab, i) => {
        tab.addEventListener('click', () => select(tab));
        tab.addEventListener('keydown', (e) => {
          let idx = null;
          if (e.key === 'ArrowRight' || e.key === 'ArrowDown') idx = (i + 1) % tabs.length;
          else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') idx = (i - 1 + tabs.length) % tabs.length;
          else if (e.key === 'Home') idx = 0;
          else if (e.key === 'End') idx = tabs.length - 1;
          if (idx !== null) { e.preventDefault(); select(tabs[idx], true); }
        });
      });
    });
  }

  /* ------------------------------------------------------------------------
     Header: transparent → glass on scroll; hides while scrolling down,
     returns on scroll up (stays while the mobile menu is open or it has focus),
     with a reading-progress line along its bottom edge
     ------------------------------------------------------------------------ */
  const header = $('[data-header]');
  function initHeader() {
    if (!header) return;
    let lastY = window.scrollY, ticking = false;
    const pinned = () => header.classList.contains('is-solid') || doc.body.classList.contains('nav-open') || header.contains(doc.activeElement);
    const bar = $('[data-scroll-progress]', header);
    const update = () => {
      ticking = false;
      const y = Math.max(0, window.scrollY), dy = y - lastY;
      header.classList.toggle('is-scrolled', y > 12);
      if (bar) {
        const max = doc.documentElement.scrollHeight - window.innerHeight;
        bar.style.setProperty('--progress', max > 0 ? Math.min(1, y / max).toFixed(4) : 0);
      }
      if (y < 160 || pinned()) header.classList.remove('is-hidden');
      else if (dy > 6) header.classList.add('is-hidden');
      else if (dy < -6) header.classList.remove('is-hidden');
      if (Math.abs(dy) > 6) lastY = y;
    };
    update();
    const onScroll = () => { if (!ticking) { ticking = true; requestAnimationFrame(update); } };
    window.addEventListener('scroll', onScroll, { passive: true });
    window.addEventListener('resize', onScroll);
    header.addEventListener('focusin', () => header.classList.remove('is-hidden'));
  }

  /* ------------------------------------------------------------------------
     Nav pill: glides to the hovered / focused link, rests on the current page
     ------------------------------------------------------------------------ */
  function initNavPill() {
    const track = $('[data-nav-track]');
    if (!track) return;
    const pill = $('.nav-pill', track);
    const links = $$('.nav-link', track);
    const current = links.find((a) => a.getAttribute('aria-current') === 'page');
    const moveTo = (link, instant) => {
      if (!link) { track.classList.remove('has-pill'); return; }
      const t = track.getBoundingClientRect(), r = link.getBoundingClientRect();
      if (instant) track.classList.add('pill-instant');
      track.style.setProperty('--pill-x', `${r.left - t.left}px`);
      track.style.setProperty('--pill-w', `${r.width}px`);
      track.classList.add('has-pill');
      if (instant) { void pill.offsetWidth; track.classList.remove('pill-instant'); }
    };
    const rest = (instant) => moveTo(current, instant);
    links.forEach((a) => {
      a.addEventListener('mouseenter', () => moveTo(a));
      a.addEventListener('focus', () => moveTo(a));
    });
    track.addEventListener('mouseleave', () => rest());
    track.addEventListener('focusout', (e) => { if (!track.contains(e.relatedTarget)) rest(); });
    rest(true);
    window.addEventListener('resize', () => rest(true));
    // Re-measure once web fonts and the header entrance have settled
    doc.fonts && doc.fonts.ready.then(() => rest(true));
    setTimeout(() => rest(true), 1200);
  }

  /* ------------------------------------------------------------------------
     Mobile navigation (full screen)
     ------------------------------------------------------------------------ */
  let closeMobileNav = () => {};
  function initMobileNav() {
    const toggle = $('[data-nav-toggle]');
    const nav = $('[data-mobile-nav]');
    if (!toggle || !nav) return;
    const set = (open) => {
      nav.classList.toggle('is-open', open);
      toggle.setAttribute('aria-expanded', String(open));
      toggle.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      doc.body.classList.toggle('nav-open', open);
      header && header.classList.toggle('is-solid', open);
      if (open) { const f = $('a', nav); f && setTimeout(() => f.focus({ preventScroll: true }), 300); }
    };
    closeMobileNav = () => nav.classList.contains('is-open') && set(false);
    toggle.addEventListener('click', () => set(!nav.classList.contains('is-open')));
    $$('a', nav).forEach((a) => a.addEventListener('click', () => set(false)));
    doc.addEventListener('keydown', (e) => { if (e.key === 'Escape' && nav.classList.contains('is-open')) { set(false); toggle.focus(); } });
    window.addEventListener('resize', () => { if (window.innerWidth > 1260) closeMobileNav(); });
  }

  /* ------------------------------------------------------------------------
     Request a Demo page: pre-tick an interest passed as ?interest=…
     ------------------------------------------------------------------------ */
  function initDemoInterest() {
    const interest = new URLSearchParams(location.search).get('interest');
    if (!interest) return;
    $$('input[data-interest]').forEach((cb) => { if (cb.dataset.interest === interest) cb.checked = true; });
  }

  /* ------------------------------------------------------------------------
     Back to top
     ------------------------------------------------------------------------ */
  function initToTop() {
    const btn = $('[data-to-top]');
    if (!btn) return;
    const onScroll = () => btn.classList.toggle('is-visible', window.scrollY > 900);
    onScroll();
    window.addEventListener('scroll', onScroll, { passive: true });
    btn.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: reduceMotion.matches ? 'auto' : 'smooth' });
      const m = $('#main'); m && m.focus({ preventScroll: true });
    });
  }

  /* ------------------------------------------------------------------------
     Public namespace
     ------------------------------------------------------------------------ */
  const hydrators = [];
  const PE = window.PE = {
    $, $$, reduceMotion, canHover, inr, svg, ICON, toast, whenVisible, initTabs,
    /** Register a function(root) that wires interactive components inside root. */
    onHydrate(fn) { hydrators.push(fn); },
    hydrate(root) { hydrators.forEach((fn) => fn(root)); },
  };
  window.ProcEaze = { toast };

  doc.addEventListener('DOMContentLoaded', () => {
    initHeader();
    initNavPill();
    initMobileNav();
    initTabs();
    initDemoInterest();
    initToTop();
    PE.hydrate(doc);
  });
})();
