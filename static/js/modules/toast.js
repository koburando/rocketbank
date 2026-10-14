/**
 * Module 13: Toast Notification Manager
 * Programmatic toast dispatch with auto-dismiss and manual close buttons.
 */

import { sanitizeHTML } from '../utils.js';

let toastContainer = null;

function getToastContainer() {
  if (!toastContainer || !document.body.contains(toastContainer)) {
    toastContainer = document.querySelector('.toast-container');
    if (!toastContainer) {
      toastContainer = document.createElement('div');
      toastContainer.className = 'toast-container';
      toastContainer.setAttribute('aria-live', 'polite');
      toastContainer.setAttribute('aria-atomic', 'true');
      toastContainer.style.position = 'fixed';
      toastContainer.style.top = '1.5rem';
      toastContainer.style.right = '1.5rem';
      toastContainer.style.zIndex = '9999';
      toastContainer.style.display = 'flex';
      toastContainer.style.flexDirection = 'column';
      toastContainer.style.gap = '0.75rem';
      toastContainer.style.maxWidth = '380px';
      toastContainer.style.width = 'calc(100vw - 3rem)';
      document.body.appendChild(toastContainer);
    }
  }
  return toastContainer;
}

export function showToast(message, type = 'info', duration = 4000) {
  const container = getToastContainer();

  const toast = document.createElement('div');
  toast.className = `alert alert--${type} toast-item shadow-lg`;
  toast.setAttribute('role', type === 'danger' ? 'alert' : 'status');
  toast.style.margin = '0';
  toast.style.display = 'flex';
  toast.style.alignItems = 'center';
  toast.style.justifyContent = 'space-between';
  toast.style.gap = '0.75rem';
  toast.style.animation = 'fadeIn 0.25s ease-out forwards';

  const icons = {
    success: '✓',
    danger: '✕',
    warning: '⚠',
    info: 'ℹ',
  };

  const icon = icons[type] || 'ℹ';

  toast.innerHTML = `
    <div class="d-flex items-center gap-sm">
      <span class="toast-icon font-bold" aria-hidden="true">${icon}</span>
      <span class="toast-message">${sanitizeHTML(message)}</span>
    </div>
    <button type="button" class="btn-close-toast" aria-label="Close notification" style="background:none;border:none;cursor:pointer;font-size:1.25rem;color:inherit;opacity:0.75;padding:0;">&times;</button>
  `;

  let dismissTimer = null;

  const dismiss = () => {
    if (dismissTimer) {
      clearTimeout(dismissTimer);
      dismissTimer = null;
    }
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(-10px)';
    toast.style.transition = 'all 0.25s ease-in';
    setTimeout(() => {
      toast.remove();
    }, 250);
  };

  const closeBtn = toast.querySelector('.btn-close-toast');
  if (closeBtn) {
    closeBtn.addEventListener('click', dismiss);
  }

  // Pause on hover
  if (duration > 0) {
    dismissTimer = setTimeout(dismiss, duration);
    toast.addEventListener('mouseenter', () => {
      if (dismissTimer) {
        clearTimeout(dismissTimer);
      }
    });
    toast.addEventListener('mouseleave', () => {
      dismissTimer = setTimeout(dismiss, 1500);
    });
  }

  container.appendChild(toast);
  return toast;
}

export function initToast() {
  // Bind any server-rendered alert close buttons
  document.addEventListener('click', (e) => {
    const closeBtn = e.target.closest('.alert__close, .toast__close');
    if (closeBtn) {
      e.preventDefault();
      const alert = closeBtn.closest('.alert, .toast');
      if (alert) {
        alert.remove();
      }
    }
  });
}
