/**
 * RocketBank Progressive Web App (PWA) Service Worker
 * Version: 1.0.0
 * Handles offline caching, asset prefetching, and fallback routing.
 */

const CACHE_NAME = 'rocketbank-v1';
const OFFLINE_FALLBACK_URL = '/offline/';

const PRECACHE_ASSETS = [
  OFFLINE_FALLBACK_URL,
  '/static/site.webmanifest',
  '/static/favicon.svg',
  '/static/images/icon-192.svg',
  '/static/images/icon-512.svg',
  '/static/css/variables.css',
  '/static/css/base.css',
  '/static/css/layout.css',
  '/static/css/components.css',
  '/static/css/utilities.css',
  '/static/css/pages.css',
  '/static/css/print.css',
  '/static/js/main.js',
  '/static/js/api/http.js',
  '/static/js/utils.js',
];

// Install Event: Precaches core UI assets and offline fallback
self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(PRECACHE_ASSETS).catch((err) => {
        console.warn('[ServiceWorker] Pre-cache non-fatal warning:', err);
      });
    }).then(() => self.skipWaiting())
  );
});

// Activate Event: Clean up outdated caches
self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((name) => {
          if (name !== CACHE_NAME) {
            return caches.delete(name);
          }
        })
      );
    }).then(() => self.clients.claim())
  );
});

// Fetch Event: Network-first for navigations with offline fallback; cache-first for static assets
self.addEventListener('fetch', (event) => {
  const { request } = event;

  // Never cache POST, PUT, DELETE, PATCH requests (e.g. transfers, auth)
  if (request.method !== 'GET') {
    return;
  }

  const url = new URL(request.url);

  // Skip caching API requests, admin, or Django auth endpoints
  if (
    url.pathname.startsWith('/api/') ||
    url.pathname.startsWith('/admin/') ||
    url.pathname.startsWith('/users/logout')
  ) {
    return;
  }

  // Handle HTML document navigations (Network-first with offline fallback)
  if (request.mode === 'navigate') {
    event.respondWith(
      fetch(request).catch(async () => {
        const cache = await caches.open(CACHE_NAME);
        const cachedFallback = await cache.match(OFFLINE_FALLBACK_URL);
        return cachedFallback || Response.error();
      })
    );
    return;
  }

  // Handle static assets (Stale-while-revalidate / Cache-first)
  if (url.pathname.startsWith('/static/')) {
    event.respondWith(
      caches.match(request).then((cachedResponse) => {
        if (cachedResponse) {
          // Revalidate in background
          fetch(request).then((networkResponse) => {
            if (networkResponse && networkResponse.status === 200) {
              caches.open(CACHE_NAME).then((cache) => cache.put(request, networkResponse));
            }
          }).catch(() => {});
          return cachedResponse;
        }

        return fetch(request).then((networkResponse) => {
          if (!networkResponse || networkResponse.status !== 200) {
            return networkResponse;
          }
          const responseToCache = networkResponse.clone();
          caches.open(CACHE_NAME).then((cache) => {
            cache.put(request, responseToCache);
          });
          return networkResponse;
        });
      })
    );
  }
});
