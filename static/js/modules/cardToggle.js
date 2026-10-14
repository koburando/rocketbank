/**
 * Module 22: Card Freeze / Unfreeze Instant Toggle
 * Instant optimistic UI toggle sending PATCH/POST to /api/v1/cards/<id>/
 */

import { http } from '../api/http.js';
import { showToast } from './toast.js';

export async function toggleCardFreeze(btn) {
  const cardId = btn.dataset.cardId;
  const currentStatus = btn.dataset.status || 'ACTIVE';
  const isBlocked = currentStatus === 'BLOCKED';
  const nextStatus = isBlocked ? 'ACTIVE' : 'BLOCKED';
  const actionPath = isBlocked ? 'unfreeze' : 'freeze';

  // Optimistic UI update
  btn.disabled = true;
  btn.dataset.status = nextStatus;
  btn.classList.toggle('btn--danger', !isBlocked);
  btn.classList.toggle('btn--outline', isBlocked);
  btn.textContent = isBlocked ? 'Freeze Card' : 'Unfreeze Card';

  const statusBadge = document.querySelector(`[data-card-status-badge="${cardId}"]`);
  if (statusBadge) {
    statusBadge.textContent = nextStatus;
    statusBadge.className = `badge badge--${nextStatus === 'ACTIVE' ? 'success' : 'danger'}`;
  }

  try {
    const res = await http.post(`/api/v1/cards/${cardId}/${actionPath}/`);
    showToast(res.message || `Card ${isBlocked ? 'unblocked' : 'frozen'} successfully.`, 'success');
  } catch (err) {
    // Revert optimistic update on failure
    btn.dataset.status = currentStatus;
    btn.classList.toggle('btn--danger', isBlocked);
    btn.classList.toggle('btn--outline', !isBlocked);
    btn.textContent = isBlocked ? 'Unfreeze Card' : 'Freeze Card';
    if (statusBadge) {
      statusBadge.textContent = currentStatus;
      statusBadge.className = `badge badge--${currentStatus === 'ACTIVE' ? 'success' : 'danger'}`;
    }
    showToast(err.message || 'Failed to update card status.', 'danger');
  } finally {
    btn.disabled = false;
  }
}

export function initCardToggle() {
  document.addEventListener('click', (e) => {
    const btn = e.target.closest('[data-card-toggle], .btn-card-freeze');
    if (btn) {
      e.preventDefault();
      toggleCardFreeze(btn);
    }
  });
}
