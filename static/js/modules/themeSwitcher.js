/**
 * Module 4: Light/Dark Theme Switcher
 * Synchronizes user theme preference across:
 * - document.documentElement data-theme attribute
 * - Browser localStorage
 * - Browser session/persistent cookie
 * - User Profile REST API endpoint (/api/v1/profile/theme/)
 */

import { http } from '../api/http.js';

export function applyTheme(theme) {
  const normalized = theme.toLowerCase();
  document.documentElement.setAttribute('data-theme', normalized);
  localStorage.setItem('theme', normalized);
  document.cookie = `theme=${normalized};path=/;max-age=31536000;SameSite=Lax`;

  // Update aria-pressed or icons on toggle buttons
  const buttons = document.querySelectorAll('#theme-toggle-btn, [data-theme-toggle]');
  buttons.forEach((btn) => {
    btn.setAttribute('aria-label', `Switch to ${normalized === 'dark' ? 'light' : 'dark'} mode`);
  });
}

export async function syncThemeWithApi(theme) {
  try {
    await http.post('/api/v1/profile/theme/', { theme: theme.toUpperCase() });
  } catch (err) {
    // Graceful fallback for unauthenticated users or offline mode
  }
}

export function initThemeSwitcher() {
  // Check initial preference from localStorage
  const saved = localStorage.getItem('theme');
  if (saved) {
    applyTheme(saved);
  }

  // Event delegation on theme switcher buttons
  document.addEventListener('click', (e) => {
    const toggleBtn = e.target.closest('#theme-toggle-btn, [data-theme-toggle]');
    if (!toggleBtn) {
      return;
    }

    e.preventDefault();
    const current = document.documentElement.getAttribute('data-theme') || 'dark';
    const next = current === 'dark' ? 'light' : 'dark';

    applyTheme(next);
    syncThemeWithApi(next);
  });
}
