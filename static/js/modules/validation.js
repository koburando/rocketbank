/**
 * Module 1: Real-time Form Validation
 * Provides instant inline visual feedback on input & blur events.
 * Validates required, email, IBAN, patterns, and custom rules.
 */

import { validateIBAN } from '../utils.js';

function setFieldStatus(input, isValid, message = '') {
  input.classList.remove('is-valid', 'is-invalid');
  input.classList.add(isValid ? 'is-valid' : 'is-invalid');

  let feedback = input.parentNode.querySelector('.form-feedback');
  if (!feedback) {
    feedback = document.createElement('small');
    feedback.className = 'form-feedback';
    feedback.setAttribute('aria-live', 'polite');
    input.parentNode.appendChild(feedback);
  }

  if (isValid) {
    feedback.textContent = '';
    feedback.className = 'form-feedback text-success';
  } else {
    feedback.textContent = message;
    feedback.className = 'form-feedback text-danger';
  }
}

export function validateInput(input) {
  // Skip disabled or hidden inputs
  if (input.disabled || input.type === 'hidden') {
    return true;
  }

  const value = input.value.trim();

  // Required check
  if (input.required && !value) {
    setFieldStatus(input, false, 'This field is required.');
    return false;
  }

  if (!value) {
    input.classList.remove('is-valid', 'is-invalid');
    const feedback = input.parentNode.querySelector('.form-feedback');
    if (feedback) {
      feedback.textContent = '';
    }
    return true;
  }

  // Email format check
  if (input.type === 'email') {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    if (!emailRegex.test(value)) {
      setFieldStatus(input, false, 'Please enter a valid email address.');
      return false;
    }
  }

  // Min / Max length checks
  if (input.minLength && input.minLength > 0 && value.length < input.minLength) {
    setFieldStatus(input, false, `Minimum ${input.minLength} characters required.`);
    return false;
  }

  // IBAN validation
  if (input.dataset.validate === 'iban') {
    if (!validateIBAN(value)) {
      setFieldStatus(input, false, 'Invalid IBAN format or checksum.');
      return false;
    }
  }

  // Password confirmation check
  if (input.dataset.matchField) {
    const target = document.getElementById(input.dataset.matchField);
    if (target && target.value !== value) {
      setFieldStatus(input, false, 'Passwords do not match.');
      return false;
    }
  }

  // Positive numeric check
  if (input.type === 'number' && input.min) {
    const num = parseFloat(value);
    if (isNaN(num) || num < parseFloat(input.min)) {
      setFieldStatus(input, false, `Value must be at least ${input.min}.`);
      return false;
    }
  }

  setFieldStatus(input, true);
  return true;
}

export function initFormValidation() {
  document.addEventListener('input', (e) => {
    if (e.target.matches('input, textarea, select') && e.target.form?.hasAttribute('data-validate-form')) {
      validateInput(e.target);
    }
  });

  document.addEventListener('blur', (e) => {
    if (e.target.matches('input, textarea, select') && e.target.form?.hasAttribute('data-validate-form')) {
      validateInput(e.target);
    }
  }, true);

  document.addEventListener('submit', (e) => {
    const form = e.target;
    if (form.hasAttribute('data-validate-form')) {
      const inputs = Array.from(form.querySelectorAll('input, textarea, select'));
      let formValid = true;
      for (const input of inputs) {
        if (!validateInput(input)) {
          formValid = false;
        }
      }
      if (!formValid) {
        e.preventDefault();
        const firstInvalid = form.querySelector('.is-invalid');
        if (firstInvalid) {
          firstInvalid.focus();
        }
      }
    }
  });
}
