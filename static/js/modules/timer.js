/**
 * Module 17: Promo & OTP Countdown Timer
 * Visual mm:ss timer with auto-disable/enable for OTP resend buttons.
 */

export function startCountdown(timerEl) {
  let seconds = parseInt(timerEl.dataset.seconds || 60, 10);
  const display = timerEl.querySelector('.timer-display') || timerEl;
  const resendBtn = timerEl.parentNode.querySelector('[data-resend-otp], .btn-resend-otp');

  if (resendBtn) {
    resendBtn.disabled = true;
  }

  const formatTime = (totalSec) => {
    const mins = Math.floor(totalSec / 60);
    const secs = totalSec % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  display.textContent = formatTime(seconds);

  const intervalId = setInterval(() => {
    seconds--;
    if (seconds <= 0) {
      clearInterval(intervalId);
      display.textContent = '00:00';
      timerEl.classList.add('is-expired');
      if (resendBtn) {
        resendBtn.disabled = false;
        resendBtn.classList.remove('btn--disabled');
      }
      timerEl.dispatchEvent(new CustomEvent('timer:expired', { bubbles: true }));
    } else {
      display.textContent = formatTime(seconds);
    }
  }, 1000);

  return intervalId;
}

export function initTimer() {
  const timers = document.querySelectorAll('[data-countdown-timer], .countdown-timer');
  timers.forEach((timer) => {
    startCountdown(timer);
  });

  // Re-start on resend click
  document.addEventListener('click', (e) => {
    const resendBtn = e.target.closest('[data-resend-otp], .btn-resend-otp');
    if (resendBtn && !resendBtn.disabled) {
      const timer = resendBtn.parentNode.querySelector('[data-countdown-timer], .countdown-timer');
      if (timer) {
        timer.classList.remove('is-expired');
        timer.dataset.seconds = timer.dataset.defaultSeconds || '60';
        startCountdown(timer);
      }
    }
  });
}
