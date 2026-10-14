/**
 * Module 23: Notification Bell Live Counter & Mark-All-Read
 * Fetches real-time unread count and handles mark-read POST actions.
 */

import { http } from '../api/http.js';
import { showToast } from './toast.js';

export async function refreshNotificationCount() {
  const badge = document.querySelector('[data-notification-badge], .dashboard-topbar .badge--danger');
  if (!badge) {
    return;
  }

  try {
    const res = await http.get('/api/v1/notifications/unread-count/');
    const count = res.unread_count || 0;

    badge.textContent = count;
    if (count > 0) {
      badge.style.display = 'inline-block';
      badge.setAttribute('aria-label', `${count} unread notifications`);
    } else {
      badge.style.display = 'none';
    }
  } catch {}
}

export async function markAllNotificationsRead(btn = null) {
  if (btn) {
    btn.disabled = true;
  }

  try {
    const res = await http.post('/api/v1/notifications/mark-all-read/');
    const badge = document.querySelector('[data-notification-badge], .dashboard-topbar .badge--danger');
    if (badge) {
      badge.style.display = 'none';
      badge.textContent = '0';
    }

    // Mark list items as read in UI
    const unreadItems = document.querySelectorAll('.notification-item--unread, [data-notification-unread="true"]');
    unreadItems.forEach((item) => {
      item.classList.remove('notification-item--unread');
      item.setAttribute('data-notification-unread', 'false');
      const dot = item.querySelector('.unread-indicator');
      if (dot) {
        dot.remove();
      }
    });

    showToast('All notifications marked as read', 'success');
  } catch (err) {
    showToast(err.message || 'Failed to mark notifications as read', 'danger');
  } finally {
    if (btn) {
      btn.disabled = false;
    }
  }
}

export function initNotificationBell() {
  // Initial count check if user is in dashboard
  if (document.querySelector('.dashboard-layout')) {
    refreshNotificationCount();
  }

  document.addEventListener('click', (e) => {
    const markAllBtn = e.target.closest('[data-mark-all-read], .btn-mark-all-read');
    if (markAllBtn) {
      e.preventDefault();
      markAllNotificationsRead(markAllBtn);
      return;
    }

    const markSingleBtn = e.target.closest('[data-mark-read]');
    if (markSingleBtn) {
      e.preventDefault();
      const notifId = markSingleBtn.dataset.markRead;
      http.post(`/api/v1/notifications/${notifId}/mark-read/`).then(() => {
        const item = markSingleBtn.closest('.notification-item');
        if (item) {
          item.classList.remove('notification-item--unread');
        }
        refreshNotificationCount();
      });
    }
  });
}
