/**
 * Pure ES6+ Utility Functions for RocketBank Frontend.
 * Unit tested with Node.js test runner.
 */

/**
 * Format numeric amount into localized currency string.
 * @param {number|string} amount
 * @param {string} currency - e.g. 'KZT', 'USD', 'EUR', 'RUB'
 * @param {string} locale
 * @returns {string}
 */
export function formatCurrency(amount, currency = 'KZT', locale = 'en-US') {
  const numeric = typeof amount === 'string' ? parseFloat(amount) : Number(amount);
  if (isNaN(numeric)) {
    return '0.00 ' + currency;
  }

  // Handle standard currencies
  try {
    return new Intl.NumberFormat(locale, {
      style: 'currency',
      currency: currency.toUpperCase(),
      minimumFractionDigits: 2,
      maximumFractionDigits: 2,
    }).format(numeric);
  } catch {
    // Fallback if currency code not recognized by runtime
    return `${numeric.toLocaleString(locale, { minimumFractionDigits: 2, maximumFractionDigits: 2 })} ${currency}`;
  }
}

/**
 * Validates international bank account numbers (IBAN) using ISO 7064 MOD-97 checksum.
 * @param {string} iban
 * @returns {boolean}
 */
export function validateIBAN(iban) {
  if (!iban || typeof iban !== 'string') {
    return false;
  }
  const clean = iban.toUpperCase().replace(/[\s-]/g, '');
  // Structure: 2 country letters, 2 check digits, 11-30 alphanumeric
  const regex = /^[A-Z]{2}\d{2}[A-Z0-9]{11,30}$/;
  if (!regex.test(clean)) {
    return false;
  }

  // Rearrange: Move first 4 characters to the end
  const rearranged = clean.slice(4) + clean.slice(0, 4);

  // Convert letters to numbers (A=10, B=11, ... Z=35)
  let numericString = '';
  for (let i = 0; i < rearranged.length; i++) {
    const code = rearranged.charCodeAt(i);
    if (code >= 65 && code <= 90) {
      numericString += (code - 55).toString();
    } else {
      numericString += rearranged[i];
    }
  }

  // Compute modulo 97 using chunking to prevent 64-bit integer overflow
  let remainder = 0;
  for (let i = 0; i < numericString.length; i += 7) {
    const chunk = remainder.toString() + numericString.slice(i, i + 7);
    remainder = parseInt(chunk, 10) % 97;
  }

  return remainder === 1;
}

/**
 * Calculate fixed monthly annuity payment for consumer/mortgage loans.
 * Formula: M = P * [ r * (1 + r)^n ] / [ (1 + r)^n - 1 ]
 * @param {number} principal - Loan amount
 * @param {number} annualRatePercent - Annual interest rate (e.g. 14.5)
 * @param {number} months - Total duration in months
 * @returns {number} Monthly payment rounded to 2 decimals
 */
export function calculateAnnuityPayment(principal, annualRatePercent, months) {
  const P = Number(principal);
  const n = parseInt(months, 10);
  const annualRate = Number(annualRatePercent);

  if (isNaN(P) || isNaN(n) || P <= 0 || n <= 0) {
    return 0;
  }

  if (annualRate <= 0) {
    return Math.round((P / n) * 100) / 100;
  }

  const r = annualRate / 100 / 12; // Monthly interest rate
  const factor = Math.pow(1 + r, n);
  const monthlyPayment = P * (r * factor) / (factor - 1);

  return Math.round(monthlyPayment * 100) / 100;
}

/**
 * Calculate expected maturity return and accrued interest on fixed-term deposits.
 * @param {number} principal - Initial deposit amount
 * @param {number} annualRatePercent - Annual interest rate (%)
 * @param {number} months - Term in months
 * @returns {{ totalMaturity: number, accruedInterest: number }}
 */
export function calculateDepositReturn(principal, annualRatePercent, months) {
  const P = Number(principal);
  const rate = Number(annualRatePercent);
  const m = parseInt(months, 10);

  if (isNaN(P) || isNaN(rate) || isNaN(m) || P <= 0 || m <= 0) {
    return { totalMaturity: 0, accruedInterest: 0 };
  }

  const years = m / 12;
  const accruedInterest = Math.round(P * (rate / 100) * years * 100) / 100;
  const totalMaturity = Math.round((P + accruedInterest) * 100) / 100;

  return { totalMaturity, accruedInterest };
}

/**
 * Creates a debounced function that delays invoking fn until delay ms have elapsed.
 * @param {Function} fn
 * @param {number} delay
 * @returns {Function}
 */
export function debounce(fn, delay = 300) {
  let timerId = null;

  const debounced = function (...args) {
    if (timerId !== null) {
      clearTimeout(timerId);
    }
    timerId = setTimeout(() => {
      timerId = null;
      fn.apply(this, args);
    }, delay);
  };

  debounced.cancel = () => {
    if (timerId !== null) {
      clearTimeout(timerId);
      timerId = null;
    }
  };

  return debounced;
}

/**
 * Sanitize untrusted text to prevent XSS injection.
 * @param {string} str
 * @returns {string}
 */
export function sanitizeHTML(str) {
  if (typeof str !== 'string') {
    return '';
  }
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#039;');
}

/**
 * Mask raw phone number string to +7 (XXX) XXX-XX-XX format.
 * @param {string} input
 * @returns {string}
 */
export function maskPhoneNumber(input) {
  if (!input) {
    return '';
  }
  const digits = input.replace(/\D/g, '');
  // Normalize 8XXXXXXXXXX or 7XXXXXXXXXX to 7...
  let normalized = digits;
  if (normalized.startsWith('8') || normalized.startsWith('7')) {
    normalized = normalized.slice(1);
  }
  normalized = normalized.slice(0, 10);

  let formatted = '+7';
  if (normalized.length > 0) {
    formatted += ' (' + normalized.slice(0, 3);
  }
  if (normalized.length >= 4) {
    formatted += ') ' + normalized.slice(3, 6);
  }
  if (normalized.length >= 7) {
    formatted += '-' + normalized.slice(6, 8);
  }
  if (normalized.length >= 9) {
    formatted += '-' + normalized.slice(8, 10);
  }
  return formatted;
}
