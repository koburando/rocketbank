/**
 * Module 11: Textarea Live Character Counter
 * Tracks typed characters against maxlength attribute with warning thresholds.
 */

export function initCharCounter() {
  const textareas = document.querySelectorAll('textarea[maxlength], [data-char-counter]');

  textareas.forEach((textarea) => {
    const max = parseInt(textarea.getAttribute('maxlength') || textarea.dataset.charCounter, 10);
    if (!max) {
      return;
    }

    let counter = textarea.parentNode.querySelector('.char-counter');
    if (!counter) {
      counter = document.createElement('div');
      counter.className = 'char-counter text-muted text-right mt-xs';
      counter.style.fontSize = 'var(--font-size-xs, 0.75rem)';
      counter.setAttribute('aria-live', 'polite');
      textarea.parentNode.appendChild(counter);
    }

    const updateCount = () => {
      const current = textarea.value.length;
      counter.textContent = `${current} / ${max} characters`;

      counter.classList.remove('text-warning', 'text-danger');
      if (current >= max) {
        counter.classList.add('text-danger');
      } else if (current >= max * 0.85) {
        counter.classList.add('text-warning');
      }
    };

    textarea.addEventListener('input', updateCount);
    updateCount();
  });
}
