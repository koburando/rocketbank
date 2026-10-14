/**
 * Module 24: Review Rating Star Picker & Helpful Vote Button
 * Features:
 * - Interactive 1-5 star rating selector with hover preview
 * - Helpful vote button calling POST /api/v1/reviews/<id>/helpful/
 */

import { http } from '../api/http.js';
import { showToast } from './toast.js';

export function setupStarRatingPicker(container) {
  const stars = Array.from(container.querySelectorAll('.star-btn, [data-star-val]'));
  const hiddenInput = container.querySelector('input[type="hidden"], [name="rating"]');

  if (!stars.length || !hiddenInput) {
    return;
  }

  const highlightStars = (count) => {
    stars.forEach((star, idx) => {
      if (idx < count) {
        star.classList.add('is-filled');
        star.innerHTML = '<span aria-hidden="true">★</span>';
      } else {
        star.classList.remove('is-filled');
        star.innerHTML = '<span aria-hidden="true">☆</span>';
      }
    });
  };

  const getSelectedValue = () => parseInt(hiddenInput.value || 0, 10);

  stars.forEach((star, index) => {
    const val = index + 1;
    star.addEventListener('mouseenter', () => highlightStars(val));
    star.addEventListener('mouseleave', () => highlightStars(getSelectedValue()));

    star.addEventListener('click', (e) => {
      e.preventDefault();
      hiddenInput.value = val;
      highlightStars(val);
      container.dispatchEvent(new CustomEvent('rating:change', { detail: { rating: val }, bubbles: true }));
    });
  });

  highlightStars(getSelectedValue());
}

export async function castHelpfulVote(btn) {
  const reviewId = btn.dataset.helpfulReviewId || btn.dataset.reviewId;
  if (!reviewId) {
    return;
  }

  btn.disabled = true;

  try {
    const res = await http.post(`/api/v1/reviews/${reviewId}/helpful/`);
    const countSpan = btn.querySelector('.helpful-count') || btn;
    if (res.is_helpful_count !== undefined) {
      countSpan.textContent = `Helpful (${res.is_helpful_count})`;
    }
    btn.classList.add('is-voted', 'btn--success');
    showToast('Thank you for your feedback!', 'success', 2000);
  } catch (err) {
    btn.disabled = false;
    showToast(err.message || 'Unable to submit vote.', 'danger');
  }
}

export function initReviewRating() {
  const pickers = document.querySelectorAll('.star-rating-picker, [data-rating-picker]');
  pickers.forEach(setupStarRatingPicker);

  document.addEventListener('click', (e) => {
    const helpfulBtn = e.target.closest('[data-helpful-review-id], .btn-helpful');
    if (helpfulBtn) {
      e.preventDefault();
      castHelpfulVote(helpfulBtn);
    }
  });
}
