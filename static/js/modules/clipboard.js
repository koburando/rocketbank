/**
 * Module 12: One-Click Clipboard Copy Manager
 * Copies IBAN, card numbers, or transaction references to system clipboard with visual feedback.
 */

import { showToast } from './toast.js';

export async function copyToClipboard(text, triggerBtn = null) {
  if (!text) {
    return;
  }

  const cleanText = text.replace(/[\s-]/g, '');

  try {
    if (navigator.clipboard && window.isSecureContext) {
      await navigator.clipboard.writeText(text);
    } else {
      // Legacy fallback
      const textArea = document.createElement('textarea');
      textArea.value = text;
      textArea.style.position = 'fixed';
      textArea.style.left = '-999999px';
      document.body.appendChild(textArea);
      textArea.focus();
      textArea.select();
      document.execCommand('copy');
      textArea.remove();
    }

    if (triggerBtn) {
      const originalHTML = triggerBtn.innerHTML;
      triggerBtn.classList.add('is-copied', 'btn--success');
      triggerBtn.innerHTML = '<span aria-hidden="true">✓</span> Copied!';

      setTimeout(() => {
        triggerBtn.classList.remove('is-copied', 'btn--success');
        triggerBtn.innerHTML = originalHTML;
      }, 2000);
    }

    showToast('Copied to clipboard!', 'success', 2500);
  } catch (err) {
    console.error('[Clipboard] Failed to copy:', err);
    showToast('Failed to copy to clipboard', 'danger', 3000);
  }
}

export function initClipboard() {
  document.addEventListener('click', (e) => {
    const btn = e.target.closest('[data-copy], .btn-copy');
    if (!btn) {
      return;
    }

    e.preventDefault();
    const textToCopy = btn.dataset.copy || btn.getAttribute('data-clipboard-text') || btn.innerText.trim();
    copyToClipboard(textToCopy, btn);
  });
}
