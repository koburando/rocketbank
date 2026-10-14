/**
 * Unit tests for RocketBank frontend utility functions.
 * Run with Node.js built-in test runner: `node --test static/js/__tests__/utils.test.js`
 */

import { describe, it } from 'node:test';
import assert from 'node:assert/strict';

import {
  formatCurrency,
  validateIBAN,
  calculateAnnuityPayment,
  calculateDepositReturn,
  debounce,
  maskPhoneNumber,
  sanitizeHTML,
} from '../utils.js';

describe('RocketBank Frontend Utility Functions', () => {
  // 1. Currency Formatter
  describe('formatCurrency', () => {
    it('should format numbers with currency symbol and 2 decimals', () => {
      const res = formatCurrency(1250000.5, 'USD');
      assert.ok(res.includes('1,250,000.50') || res.includes('$1,250,000.50'));
    });

    it('should handle zero and string numeric values gracefully', () => {
      const res = formatCurrency('0', 'KZT');
      assert.ok(res.includes('0.00'));
    });

    it('should handle invalid input without throwing', () => {
      const res = formatCurrency('invalid', 'EUR');
      assert.strictEqual(res, '0.00 EUR');
    });
  });

  // 2. IBAN Validator
  describe('validateIBAN', () => {
    it('should correctly validate valid IBANs using MOD-97 algorithm', () => {
      // Test known valid IBANs
      assert.strictEqual(validateIBAN('GB82 WEST 1234 5698 7654 32'), true);
      assert.strictEqual(validateIBAN('DE89 3704 0044 0532 0130 00'), true);
      assert.strictEqual(validateIBAN('FR14 2004 1010 0505 0001 3M02 606'), true);
    });

    it('should reject invalid IBAN check digits or invalid characters', () => {
      assert.strictEqual(validateIBAN('GB82 WEST 1234 5698 7654 33'), false); // Tampered digit
      assert.strictEqual(validateIBAN('INVALID_IBAN_123'), false);
      assert.strictEqual(validateIBAN(''), false);
      assert.strictEqual(validateIBAN(null), false);
    });
  });

  // 3. Annuity Loan Calculator
  describe('calculateAnnuityPayment', () => {
    it('should calculate accurate monthly annuity loan payments', () => {
      // P = 1,000,000 KZT, annual rate = 12%, term = 12 months
      // r = 0.01
      // M = 1000000 * (0.01 * 1.01^12) / (1.01^12 - 1) ≈ 88,848.79
      const payment = calculateAnnuityPayment(1000000, 12, 12);
      assert.ok(Math.abs(payment - 88848.79) < 0.5, `Expected ~88848.79, got ${payment}`);
    });

    it('should handle 0% interest rate as straight division', () => {
      const payment = calculateAnnuityPayment(120000, 0, 12);
      assert.strictEqual(payment, 10000);
    });

    it('should return 0 for non-positive principals or terms', () => {
      assert.strictEqual(calculateAnnuityPayment(0, 15, 12), 0);
      assert.strictEqual(calculateAnnuityPayment(100000, 15, 0), 0);
    });
  });

  // 4. Deposit Return Calculator
  describe('calculateDepositReturn', () => {
    it('should calculate accurate maturity and interest on fixed-term deposits', () => {
      // P = 500,000, rate = 15%, term = 12 months
      // Interest = 500,000 * 0.15 = 75,000
      const res = calculateDepositReturn(500000, 15, 12);
      assert.strictEqual(res.accruedInterest, 75000);
      assert.strictEqual(res.totalMaturity, 575000);
    });
  });

  // 5. Debounce Utility
  describe('debounce', () => {
    it('should delay function invocation and coalesce multiple calls', async () => {
      let callCount = 0;
      let lastVal = null;
      const fn = (val) => {
        callCount++;
        lastVal = val;
      };

      const debounced = debounce(fn, 50);
      debounced(1);
      debounced(2);
      debounced(3);

      assert.strictEqual(callCount, 0);

      await new Promise((resolve) => setTimeout(resolve, 80));

      assert.strictEqual(callCount, 1);
      assert.strictEqual(lastVal, 3);
    });

    it('should allow cancellation via .cancel()', async () => {
      let callCount = 0;
      const debounced = debounce(() => callCount++, 50);
      debounced();
      debounced.cancel();

      await new Promise((resolve) => setTimeout(resolve, 80));
      assert.strictEqual(callCount, 0);
    });
  });

  // 6. Phone Number Masking
  describe('maskPhoneNumber', () => {
    it('should format raw digits into standard +7 (XXX) XXX-XX-XX format', () => {
      assert.strictEqual(maskPhoneNumber('77011234567'), '+7 (701) 123-45-67');
      assert.strictEqual(maskPhoneNumber('87059876543'), '+7 (705) 987-65-43');
      assert.strictEqual(maskPhoneNumber('7701'), '+7 (701');
    });
  });

  // 7. HTML Sanitizer
  describe('sanitizeHTML', () => {
    it('should escape dangerous script and tag characters to prevent XSS', () => {
      const malicious = '<script>alert("XSS & attack")</script>';
      const clean = sanitizeHTML(malicious);
      assert.strictEqual(clean, '&lt;script&gt;alert(&quot;XSS &amp; attack&quot;)&lt;/script&gt;');
    });
  });
});
