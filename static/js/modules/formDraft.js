/**
 * Module 19: Form Draft Auto-Save & Restore
 * Auto-saves form input progress into sessionStorage with user restore prompt.
 * Strictly excludes passwords and sensitive card CVVs.
 */

import { debounce } from '../utils.js';

const SENSITIVE_INPUT_TYPES = ['password'];
const SENSITIVE_FIELD_NAMES = ['password', 'password1', 'password2', 'cvv', 'pin', 'csrfmiddlewaretoken'];

export function initFormDraft() {
  const forms = document.querySelectorAll('form[data-draft-key], form[data-auto-draft]');

  forms.forEach((form) => {
    const draftKey = `draft_${form.dataset.draftKey || form.getAttribute('action') || window.location.pathname}`;

    const saveDraft = debounce(() => {
      const data = {};
      const elements = Array.from(form.elements);

      elements.forEach((el) => {
        if (!el.name || SENSITIVE_INPUT_TYPES.includes(el.type) || SENSITIVE_FIELD_NAMES.includes(el.name.toLowerCase())) {
          return;
        }

        if (el.type === 'checkbox') {
          data[el.name] = el.checked;
        } else if (el.type === 'radio') {
          if (el.checked) {
            data[el.name] = el.value;
          }
        } else if (el.value.trim()) {
          data[el.name] = el.value;
        }
      });

      if (Object.keys(data).length > 0) {
        sessionStorage.setItem(draftKey, JSON.stringify(data));
      }
    }, 500);

    form.addEventListener('input', saveDraft);
    form.addEventListener('change', saveDraft);

    // Clean up draft upon successful form submission
    form.addEventListener('submit', () => {
      sessionStorage.removeItem(draftKey);
    });

    // Check for existing draft on load
    const savedDraftRaw = sessionStorage.getItem(draftKey);
    if (savedDraftRaw) {
      try {
        const savedDraft = JSON.parse(savedDraftRaw);
        if (Object.keys(savedDraft).length > 0) {
          const banner = document.createElement('div');
          banner.className = 'alert alert--info d-flex items-center justify-between mb-lg';
          banner.innerHTML = `
            <span>You have an unsaved draft from a previous session.</span>
            <div class="d-flex gap-xs">
              <button type="button" class="btn btn--primary btn--sm btn-restore-draft">Restore Draft</button>
              <button type="button" class="btn btn--secondary btn--sm btn-discard-draft">&times; Discard</button>
            </div>
          `;

          form.parentNode.insertBefore(banner, form);

          banner.querySelector('.btn-restore-draft').addEventListener('click', () => {
            Object.entries(savedDraft).forEach(([name, val]) => {
              const el = form.elements[name];
              if (el) {
                if (el.type === 'checkbox') {
                  el.checked = Boolean(val);
                } else if (el.type === 'radio') {
                  const radio = form.querySelector(`input[name="${name}"][value="${val}"]`);
                  if (radio) {
                    radio.checked = true;
                  }
                } else {
                  el.value = val;
                }
                el.dispatchEvent(new Event('input', { bubbles: true }));
              }
            });
            banner.remove();
          });

          banner.querySelector('.btn-discard-draft').addEventListener('click', () => {
            sessionStorage.removeItem(draftKey);
            banner.remove();
          });
        }
      } catch {}
    }
  });
}
