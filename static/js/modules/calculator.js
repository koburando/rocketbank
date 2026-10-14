/**
 * Module 16: Interactive Annuity Loan & Deposit Calculator
 * Live synchronized sliders, input fields, and output elements.
 */

import { calculateAnnuityPayment, calculateDepositReturn, formatCurrency } from '../utils.js';

export function initCalculator() {
  // 1. Loan Calculator
  const loanForms = document.querySelectorAll('[data-calculator="loan"], #loan-calculator-form');
  loanForms.forEach((form) => {
    const amountSlider = form.querySelector('[name="amount_slider"], [name="amount"]');
    const termSlider = form.querySelector('[name="term_slider"], [name="term"], [name="term_months"]');
    const rateInput = form.querySelector('[name="interest_rate"], [name="rate"]');

    const outputAmount = form.querySelector('[data-output="amount"], output[for*="amount"]');
    const outputTerm = form.querySelector('[data-output="term"], output[for*="term"]');
    const outputMonthly = form.querySelector('[data-output="monthly-payment"], #monthly-payment-output');
    const outputTotal = form.querySelector('[data-output="total-payment"], #total-payment-output');
    const outputOverpayment = form.querySelector('[data-output="overpayment"], #overpayment-output');

    const recalculateLoan = () => {
      const amount = parseFloat(amountSlider?.value || 1000000);
      const term = parseInt(termSlider?.value || 12, 10);
      const rate = parseFloat(rateInput?.value || 14.5);

      if (outputAmount) {
        outputAmount.textContent = formatCurrency(amount, 'KZT');
      }
      if (outputTerm) {
        outputTerm.textContent = `${term} months`;
      }

      const monthly = calculateAnnuityPayment(amount, rate, term);
      const total = monthly * term;
      const overpayment = Math.max(0, total - amount);

      if (outputMonthly) {
        outputMonthly.textContent = formatCurrency(monthly, 'KZT');
      }
      if (outputTotal) {
        outputTotal.textContent = formatCurrency(total, 'KZT');
      }
      if (outputOverpayment) {
        outputOverpayment.textContent = formatCurrency(overpayment, 'KZT');
      }
    };

    form.addEventListener('input', recalculateLoan);
    recalculateLoan();
  });

  // 2. Deposit Calculator
  const depositForms = document.querySelectorAll('[data-calculator="deposit"], #deposit-calculator-form');
  depositForms.forEach((form) => {
    const amountInput = form.querySelector('[name="amount"]');
    const termInput = form.querySelector('[name="term_months"], [name="term"]');
    const rateInput = form.querySelector('[name="interest_rate"], [name="rate"]');

    const outputAmount = form.querySelector('[data-output="deposit-amount"]');
    const outputTerm = form.querySelector('[data-output="deposit-term"]');
    const outputInterest = form.querySelector('[data-output="accrued-interest"], #accrued-interest-output');
    const outputMaturity = form.querySelector('[data-output="total-maturity"], #total-maturity-output');

    const recalculateDeposit = () => {
      const amount = parseFloat(amountInput?.value || 500000);
      const term = parseInt(termInput?.value || 12, 10);
      const rate = parseFloat(rateInput?.value || 15.0);

      if (outputAmount) {
        outputAmount.textContent = formatCurrency(amount, 'KZT');
      }
      if (outputTerm) {
        outputTerm.textContent = `${term} months`;
      }

      const { totalMaturity, accruedInterest } = calculateDepositReturn(amount, rate, term);

      if (outputInterest) {
        outputInterest.textContent = formatCurrency(accruedInterest, 'KZT');
      }
      if (outputMaturity) {
        outputMaturity.textContent = formatCurrency(totalMaturity, 'KZT');
      }
    };

    form.addEventListener('input', recalculateDeposit);
    recalculateDeposit();
  });
}
