/**
 * Module 15: Phone Number Input Mask
 * Formats phone number inputs in real-time to +7 (XXX) XXX-XX-XX format.
 */

import { maskPhoneNumber } from '../utils.js';

export function applyPhoneMask(input) {
  const previousValue = input.value;
  const digits = previousValue.replace(/\D/g, '');

  if (!digits) {
    input.value = '';
    return;
  }

  const masked = maskPhoneNumber(previousValue);
  input.value = masked;
}

export function initPhoneMask() {
  document.addEventListener('input', (e) => {
    const input = e.target;
    if (
      input.matches('input[type="tel"], [data-phone-mask], input[name*="phone"]')
    ) {
      applyPhoneMask(input);
    }
  });

  document.addEventListener('focusin', (e) => {
    const input = e.target;
    if (
      input.matches('input[type="tel"], [data-phone-mask], input[name*="phone"]') &&
      !input.value
    ) {
      input.value = '+7 (';
    }
  });

  document.addEventListener('focusout', (e) => {
    const input = e.target;
    if (
      input.matches('input[type="tel"], [data-phone-mask], input[name*="phone"]') &&
      input.value === '+7 ('
    ) {
      input.value = '';
    }
  });
}
