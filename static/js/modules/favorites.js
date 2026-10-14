/**
 * Module 18: Guest Favorites Manager with Server Sync
 * Features:
 * - Offline guest favorites in localStorage
 * - Heart / Star button toggle with instant visual feedback
 * - Automatic background synchronization with /api/v1/favorites/sync/ upon login
 */

import { http } from '../api/http.js';
import { showToast } from './toast.js';

const GUEST_FAVORITES_KEY = 'rocketbank_guest_favorites';

export function getGuestFavorites() {
  try {
    const raw = localStorage.getItem(GUEST_FAVORITES_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch {
    return [];
  }
}

export function saveGuestFavorites(favs) {
  try {
    localStorage.setItem(GUEST_FAVORITES_KEY, JSON.stringify(favs));
  } catch {}
}

export function isFavorite(itemType, itemId) {
  const favs = getGuestFavorites();
  return favs.some((f) => f.item_type === itemType && f.item_id === itemId);
}

export function toggleGuestFavorite(itemType, itemId) {
  let favs = getGuestFavorites();
  const index = favs.findIndex((f) => f.item_type === itemType && f.item_id === itemId);
  let added = false;

  if (index >= 0) {
    favs.splice(index, 1);
  } else {
    favs.push({ item_type: itemType, item_id: itemId });
    added = true;
  }

  saveGuestFavorites(favs);
  return added;
}

export async function syncGuestFavoritesToServer() {
  const guestFavs = getGuestFavorites();
  if (!guestFavs.length) {
    return;
  }

  try {
    const res = await http.post('/api/v1/favorites/sync/', { favorites: guestFavs });
    if (res && res.status === 'synchronized') {
      localStorage.removeItem(GUEST_FAVORITES_KEY);
      showToast(`Synced ${res.created_count || 0} saved favorites to your account!`, 'success');
    }
  } catch (err) {
    // Unauthenticated or offline; retain in localStorage
  }
}

export function updateFavoriteButtonsUI() {
  const buttons = document.querySelectorAll('.btn-favorite, [data-favorite-type]');
  buttons.forEach((btn) => {
    const itemType = btn.dataset.favoriteType || 'card';
    const itemId = btn.dataset.favoriteId || btn.dataset.productId;
    if (isFavorite(itemType, itemId)) {
      btn.classList.add('is-favorite');
      btn.setAttribute('aria-pressed', 'true');
      btn.innerHTML = '<span aria-hidden="true">★</span>';
    } else {
      btn.classList.remove('is-favorite');
      btn.setAttribute('aria-pressed', 'false');
      btn.innerHTML = '<span aria-hidden="true">☆</span>';
    }
  });
}

export function initFavorites() {
  // Sync on startup if user is authenticated
  const isAuthenticated = document.body.dataset.userAuthenticated === 'true' ||
    document.querySelector('.dashboard-layout') !== null;

  if (isAuthenticated) {
    syncGuestFavoritesToServer();
  }

  updateFavoriteButtonsUI();
  document.addEventListener('catalog:rendered', updateFavoriteButtonsUI);

  // Toggle favorite on click
  document.addEventListener('click', async (e) => {
    const btn = e.target.closest('.btn-favorite, [data-favorite-type]');
    if (!btn) {
      return;
    }

    e.preventDefault();
    const itemType = (btn.dataset.favoriteType || 'card').toLowerCase();
    const itemId = btn.dataset.favoriteId || btn.dataset.productId;

    if (!itemId) {
      return;
    }

    // If authenticated, send to server toggle endpoint
    if (isAuthenticated) {
      try {
        const res = await http.post('/api/v1/favorites/toggle/', { item_type: itemType, item_id: itemId });
        if (res.is_favorite) {
          btn.classList.add('is-favorite');
          btn.setAttribute('aria-pressed', 'true');
          btn.innerHTML = '<span aria-hidden="true">★</span>';
          showToast('Added to your favorites!', 'success', 2000);
        } else {
          btn.classList.remove('is-favorite');
          btn.setAttribute('aria-pressed', 'false');
          btn.innerHTML = '<span aria-hidden="true">☆</span>';
          showToast('Removed from favorites', 'info', 2000);
        }
        return;
      } catch (err) {
        // Fall back to guest storage
      }
    }

    // Guest storage toggle
    const added = toggleGuestFavorite(itemType, itemId);
    if (added) {
      btn.classList.add('is-favorite');
      btn.setAttribute('aria-pressed', 'true');
      btn.innerHTML = '<span aria-hidden="true">★</span>';
      showToast('Saved to guest favorites (will sync upon login)', 'success', 2500);
    } else {
      btn.classList.remove('is-favorite');
      btn.setAttribute('aria-pressed', 'false');
      btn.innerHTML = '<span aria-hidden="true">☆</span>';
      showToast('Removed from favorites', 'info', 2000);
    }
  });
}
