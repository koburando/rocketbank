/**
 * Module 4: Light/Dark Theme Switcher
 * Synchronizes user theme preference across:
 * - document.documentElement data-theme attribute
 * - Browser localStorage ('theme')
 * - Cookies ('django_theme' and 'theme')
 * - User Profile REST API endpoint (/api/v1/auth/profile/ for Profile.theme_preference)
 */

import { http } from '../api/http.js';

const SUN_ICON_SVG = `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="theme-icon-svg theme-icon-sun"><circle cx="12" cy="12" r="5"/><line x1="12" y1="1" x2="12" y2="3"/><line x1="12" y1="21" x2="12" y2="23"/><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/><line x1="1" y1="12" x2="3" y2="12"/><line x1="21" y1="12" x2="23" y2="12"/><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/></svg>`;

const MOON_ICON_SVG = `<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="theme-icon-svg theme-icon-moon"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>`;

export function updateToggleIcons(theme) {
  const isDark = (theme || 'dark').toLowerCase() === 'dark';
  const label = isDark ? 'Switch to light mode' : 'Switch to dark mode';
  const buttons = document.querySelectorAll('#theme-toggle-btn, [data-theme-toggle], .theme-toggle-btn');

  buttons.forEach((btn) => {
    btn.setAttribute('aria-label', label);
    btn.setAttribute('title', label);
    btn.setAttribute('data-theme-state', isDark ? 'dark' : 'light');

    const sunEl = btn.querySelector('.theme-icon-sun');
    const moonEl = btn.querySelector('.theme-icon-moon');
    if (sunEl && moonEl) {
      sunEl.style.display = isDark ? 'inline-flex' : 'none';
      moonEl.style.display = isDark ? 'none' : 'inline-flex';
    } else {
      btn.innerHTML = isDark ? SUN_ICON_SVG : MOON_ICON_SVG;
    }
  });
}

export function applyTheme(theme) {
  const normalized = (theme || 'dark').toLowerCase() === 'light' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', normalized);
  localStorage.setItem('theme', normalized);
  document.cookie = `django_theme=${normalized};path=/;max-age=31536000;SameSite=Lax`;
  document.cookie = `theme=${normalized};path=/;max-age=31536000;SameSite=Lax`;

  updateToggleIcons(normalized);

  document.dispatchEvent(new CustomEvent('rocketbank:theme-changed', {
    detail: { theme: normalized }
  }));
}

export async function syncThemeWithApi(theme) {
  const isAuth = document.querySelector('meta[name="user-authenticated"]')?.content === 'true'
    || window.userIsAuthenticated === true;

  if (!isAuth) {
    return;
  }

  const themeUpper = (theme || 'dark').toLowerCase() === 'light' ? 'LIGHT' : 'DARK';

  try {
    // Fire asynchronous PATCH /api/v1/auth/profile/ to save Profile.theme_preference
    await http.patch('/api/v1/auth/profile/', {
      theme_preference: themeUpper,
      preferred_theme: themeUpper,
      theme: themeUpper,
    });
  } catch (err) {
    // Fallback to /api/v1/profile/theme/
    try {
      await http.post('/api/v1/profile/theme/', { theme: themeUpper });
    } catch (fallbackErr) {
      // Gracefully silent for offline / network errors
    }
  }
}

export function toggleTheme() {
  const current = document.documentElement.getAttribute('data-theme') || 'dark';
  const next = current === 'dark' ? 'light' : 'dark';
  applyTheme(next);
  syncThemeWithApi(next);
  return next;
}

// Global hooks
if (typeof window !== 'undefined') {
  window.applyRocketTheme = applyTheme;
  window.toggleRocketTheme = toggleTheme;
  window.updateRocketThemeIcons = updateToggleIcons;
}

export function initThemeSwitcher() {
  const saved = localStorage.getItem('theme')
    || document.documentElement.getAttribute('data-theme')
    || 'dark';
  applyTheme(saved);

  // Event delegation on theme toggle buttons
  document.addEventListener('click', (e) => {
    const toggleBtn = e.target.closest('#theme-toggle-btn, [data-theme-toggle], .theme-toggle-btn');
    if (!toggleBtn) {
      return;
    }

    e.preventDefault();
    toggleTheme();
  });
}
