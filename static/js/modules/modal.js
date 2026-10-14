/**
 * Module 5: Accessible Modal Controller
 * Features:
 * - Native <dialog> and custom modal support
 * - Focus Trap cycling (Tab / Shift+Tab)
 * - Escape key dismissal
 * - Dynamic aria-hidden / aria-expanded management
 * - Restores focus to trigger element upon closing
 */

let lastActiveTrigger = null;

const FOCUSABLE_SELECTOR = `
  button:not([disabled]),
  [href],
  input:not([disabled]):not([type="hidden"]),
  select:not([disabled]),
  textarea:not([disabled]),
  [tabindex]:not([tabindex="-1"])
`;

function trapFocus(modal, event) {
  if (event.key !== 'Tab') {
    return;
  }

  const focusable = Array.from(modal.querySelectorAll(FOCUSABLE_SELECTOR));
  if (!focusable.length) {
    event.preventDefault();
    return;
  }

  const first = focusable[0];
  const last = focusable[focusable.length - 1];

  if (event.shiftKey && document.activeElement === first) {
    event.preventDefault();
    last.focus();
  } else if (!event.shiftKey && document.activeElement === last) {
    event.preventDefault();
    first.focus();
  }
}

export function openModal(modalId, triggerElement = null) {
  const modal = typeof modalId === 'string' ? document.getElementById(modalId) : modalId;
  if (!modal) {
    return;
  }

  lastActiveTrigger = triggerElement || document.activeElement;

  if (typeof modal.showModal === 'function') {
    modal.showModal();
  } else {
    modal.classList.add('is-open');
    modal.setAttribute('aria-hidden', 'false');
    document.body.classList.add('modal-open');
  }

  // Set focus to first focusable element inside modal
  const firstFocusable = modal.querySelector(FOCUSABLE_SELECTOR);
  if (firstFocusable) {
    firstFocusable.focus();
  }

  modal.addEventListener('keydown', (e) => trapFocus(modal, e));
}

export function closeModal(modalId) {
  const modal = typeof modalId === 'string' ? document.getElementById(modalId) : modalId;
  if (!modal) {
    return;
  }

  if (typeof modal.close === 'function') {
    modal.close();
  } else {
    modal.classList.remove('is-open');
    modal.setAttribute('aria-hidden', 'true');
    document.body.classList.remove('modal-open');
  }

  // Restore focus to original trigger element
  if (lastActiveTrigger && typeof lastActiveTrigger.focus === 'function') {
    lastActiveTrigger.focus();
    lastActiveTrigger = null;
  }
}

export function initModal() {
  // Event delegation to open modals
  document.addEventListener('click', (e) => {
    const trigger = e.target.closest('[data-modal-target], [data-open-modal]');
    if (trigger) {
      e.preventDefault();
      const targetId = trigger.dataset.modalTarget || trigger.dataset.openModal;
      openModal(targetId, trigger);
      return;
    }

    const closeBtn = e.target.closest('[data-modal-close], .modal__close, [data-close-modal]');
    if (closeBtn) {
      e.preventDefault();
      const modal = closeBtn.closest('dialog, .modal');
      if (modal) {
        closeModal(modal);
      }
    }
  });

  // Close when clicking directly on dialog backdrop
  document.addEventListener('click', (e) => {
    if (e.target.tagName === 'DIALOG' && e.target.hasAttribute('open')) {
      const rect = e.target.getBoundingClientRect();
      const isInDialog = (
        rect.top <= e.clientY &&
        e.clientY <= rect.top + rect.height &&
        rect.left <= e.clientX &&
        e.clientX <= rect.left + rect.width
      );
      if (!isInDialog) {
        closeModal(e.target);
      }
    }
  });

  // Global Escape key close for non-native modals
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
      const openModalEl = document.querySelector('.modal.is-open');
      if (openModalEl) {
        closeModal(openModalEl);
      }
    }
  });
}
