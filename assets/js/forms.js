/* ==========================================================================
   ProcEaze — forms.js
   Client-side validation and simulated submission for the demo-request and
   vendor-registration forms. No data leaves the browser unless a form is
   given data-endpoint="https://…" (it then POSTs JSON there first).
   ========================================================================== */
(() => {
  'use strict';
  const { $, $$, toast } = window.PE;

  const FREE_MAIL = ['gmail.com', 'googlemail.com', 'yahoo.com', 'yahoo.co.in', 'yahoo.in', 'hotmail.com', 'outlook.com', 'live.com',
    'msn.com', 'rediffmail.com', 'icloud.com', 'me.com', 'aol.com', 'proton.me', 'protonmail.com', 'ymail.com', 'zoho.com', 'gmx.com'];
  const EMAIL_RE = /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/;

  const RULES = {
    'email': (v) => (EMAIL_RE.test(v) ? '' : 'Enter a valid email address, e.g. name@company.com.'),
    'work-email': (v) => {
      if (!EMAIL_RE.test(v)) return 'Enter a valid email address, e.g. name@company.com.';
      return FREE_MAIL.includes(v.split('@')[1].toLowerCase()) ? 'Please use your work email address.' : '';
    },
    'phone-in': (v) => {
      let d = v.replace(/\D/g, '');
      if (d.length === 12 && d.startsWith('91')) d = d.slice(2);
      if (d.length === 11 && d.startsWith('0')) d = d.slice(1);
      return /^[6-9]\d{9}$/.test(d) ? '' : 'Enter a valid 10-digit mobile number.';
    },
    'gstin': (v) => (/^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z][1-9A-Z]Z[0-9A-Z]$/.test(v.trim().toUpperCase())
      ? '' : 'Enter a valid 15-character GSTIN, e.g. 24ABCDE1234F1Z5.'),
    'pan': (v, form) => {
      const pan = v.trim().toUpperCase();
      if (!/^[A-Z]{5}[0-9]{4}[A-Z]$/.test(pan)) return 'Enter a valid 10-character PAN, e.g. ABCDE1234F.';
      const g = form && form.querySelector('[data-rule="gstin"]');
      if (g && g.value.trim().length === 15 && g.value.trim().toUpperCase().slice(2, 12) !== pan) return 'PAN should match characters 3–12 of your GSTIN.';
      return '';
    },
  };

  const labelText = (el) => {
    const field = el.closest('.field');
    const lab = field && field.querySelector('label, legend');
    if (!lab) return 'this field';
    const c = lab.cloneNode(true);
    $$('.req, .opt, a', c).forEach((n) => n.remove());
    return c.textContent.trim().toLowerCase();
  };

  function validate(el, form) {
    if (el.matches('fieldset[data-required-group]')) {
      return $$('input[type="checkbox"]', el).some((c) => c.checked) ? '' : 'Select at least one option.';
    }
    if (el.type === 'checkbox') return el.required && !el.checked ? 'Please tick this box to continue.' : '';
    const v = el.value.trim();
    if (!v) {
      if (!el.required) return '';
      return el.tagName === 'SELECT' ? `Please select your ${labelText(el)}.` : `Please enter your ${labelText(el)}.`;
    }
    if (el.type === 'url' && !/^https?:\/\/[^\s.]+\.[^\s]{2,}/i.test(v)) return 'Enter a full web address, starting with https://';
    const rule = el.dataset.rule || (el.type === 'email' ? 'email' : null);
    return rule && RULES[rule] ? RULES[rule](v, form) : '';
  }

  function showError(el, msg) {
    const field = el.closest('.field');
    if (!field) return;
    field.classList.toggle('has-error', !!msg);
    const span = $('.field-error span', field);
    if (span) span.textContent = msg;
    if (el.matches('input, select, textarea')) el.setAttribute('aria-invalid', msg ? 'true' : 'false');
  }

  /** Restore a submitted form so it can be used again. */
  function resetForm(wrap) {
    if (!wrap) return;
    const form = $('form', wrap);
    const success = $('[data-form-success]', wrap);
    if (form && form.hidden) {
      form.reset();
      form.hidden = false;
      if (success) success.hidden = true;
      $$('.has-error', form).forEach((f) => f.classList.remove('has-error'));
    }
  }
  window.PE.resetForm = resetForm;

  function initForm(form) {
    if (form._ready) return;
    form._ready = true;
    const controls = () => $$('input:not([type="checkbox"]), select, textarea, input[type="checkbox"][required], fieldset[data-required-group]', form);

    controls().forEach((el) => {
      el.addEventListener('blur', (e) => {
        if (el.matches('fieldset') && el.contains(e.relatedTarget)) return;
        if (el.value === '' && !el.matches('fieldset, [type="checkbox"]') && !el.closest('.has-error')) return;
        showError(el, validate(el, form));
      }, true);
      const evt = el.matches('select, [type="checkbox"], fieldset') ? 'change' : 'input';
      el.addEventListener(evt, () => { if (el.closest('.field').classList.contains('has-error')) showError(el, validate(el, form)); });
    });

    $$('[data-rule="gstin"], [data-rule="pan"]', form).forEach((el) => el.addEventListener('input', () => {
      const pos = el.selectionStart;
      el.value = el.value.toUpperCase();
      try { el.setSelectionRange(pos, pos); } catch (_) { /* not supported on this input type */ }
    }));

    form.addEventListener('submit', async (e) => {
      e.preventDefault();
      let first = null;
      controls().forEach((el) => { const m = validate(el, form); showError(el, m); if (m && !first) first = el; });
      if (first) {
        (first.matches('fieldset') ? $('input', first) : first).focus();
        toast('Please check the highlighted fields.', 'error', 4000);
        return;
      }
      const btn = $('button[type="submit"]', form);
      btn.setAttribute('aria-busy', 'true');
      btn.disabled = true;
      try {
        if (form.dataset.endpoint) {
          const data = {};
          new FormData(form).forEach((v, k) => { data[k] = data[k] ? [].concat(data[k], v) : v; });
          const res = await fetch(form.dataset.endpoint, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(data) });
          if (!res.ok) throw new Error('Request failed');
        } else {
          await new Promise((r) => setTimeout(r, 900)); // simulated, nothing is sent
        }
        const wrap = form.closest('.form-wrap');
        const success = wrap && $('[data-form-success]', wrap);
        form.hidden = true;
        if (success) { success.hidden = false; success.focus(); }
        if (form.dataset.toast) toast(form.dataset.toast, 'success');
      } catch (err) {
        toast('Something went wrong sending your request. Please try again.', 'error');
      } finally {
        btn.removeAttribute('aria-busy');
        btn.disabled = false;
      }
    });
  }

  window.PE.onHydrate((root) => $$('form[data-form]', root).forEach(initForm));
  document.addEventListener('click', (e) => {
    const again = e.target.closest('[data-form-again]');
    if (again) resetForm(again.closest('.form-wrap'));
  });
})();
