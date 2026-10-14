/**
 * Modern HTTP client wrapper using Fetch API and async/await.
 * Features:
 * - Automatic CSRF token header from cookies or meta tags
 * - AbortController management for cancelling in-flight/stale requests
 * - Configurable retry logic with exponential backoff
 * - Unified error handling with custom HttpError class
 * - Skeleton / Loader state management helper
 */

export class HttpError extends Error {
  constructor(status, data, message) {
    super(message || `HTTP ${status}`);
    this.name = 'HttpError';
    this.status = status;
    this.data = data;
  }
}

/**
 * Extract CSRF token from document cookies or meta tag.
 * @returns {string}
 */
export function getCsrfToken() {
  const meta = document.querySelector('meta[name="csrf-token"]');
  if (meta && meta.content) {
    return meta.content;
  }

  const name = 'csrftoken=';
  const decoded = decodeURIComponent(document.cookie);
  const parts = decoded.split(';');
  for (let part of parts) {
    part = part.trim();
    if (part.indexOf(name) === 0) {
      return part.substring(name.length);
    }
  }
  return '';
}

// Active abort controllers map indexed by key for request cancellation
const activeControllers = new Map();

/**
 * Core HTTP request engine.
 * @param {string} url
 * @param {object} options
 * @returns {Promise<any>}
 */
export async function request(url, options = {}) {
  const {
    method = 'GET',
    headers = {},
    body = null,
    abortKey = null,
    retries = 1,
    retryDelay = 500,
    signal = null,
    loader = null,
  } = options;

  // Cancel any existing request registered under the same abortKey
  if (abortKey) {
    if (activeControllers.has(abortKey)) {
      activeControllers.get(abortKey).abort();
    }
    const controller = new AbortController();
    activeControllers.set(abortKey, controller);
    options.signal = controller.signal;
  }

  // Set CSRF token on mutating requests
  const normalizedMethod = method.toUpperCase();
  const isMutating = !['GET', 'HEAD', 'OPTIONS'].includes(normalizedMethod);

  const requestHeaders = new Headers(headers);
  if (isMutating && !requestHeaders.has('X-CSRFToken')) {
    const token = getCsrfToken();
    if (token) {
      requestHeaders.set('X-CSRFToken', token);
    }
  }

  let finalBody = body;
  if (body && typeof body === 'object' && !(body instanceof FormData) && !(body instanceof Blob)) {
    if (!requestHeaders.has('Content-Type')) {
      requestHeaders.set('Content-Type', 'application/json');
    }
    finalBody = JSON.stringify(body);
  }

  // Show visual loader state
  if (loader && loader instanceof HTMLElement) {
    loader.classList.add('is-loading');
    loader.setAttribute('aria-busy', 'true');
  }

  let attempt = 0;
  while (true) {
    try {
      const response = await fetch(url, {
        method: normalizedMethod,
        headers: requestHeaders,
        body: finalBody,
        signal: options.signal || signal,
      });

      if (abortKey) {
        activeControllers.delete(abortKey);
      }

      // Parse JSON if possible, otherwise text
      let data = null;
      const contentType = response.headers.get('content-type') || '';
      if (contentType.includes('application/json')) {
        data = await response.json();
      } else {
        data = await response.text();
      }

      if (!response.ok) {
        const errorMsg = data && data.message ? data.message : `Request failed with status ${response.status}`;
        throw new HttpError(response.status, data, errorMsg);
      }

      return data;
    } catch (err) {
      // Do not retry if request was intentionally aborted
      if (err.name === 'AbortError') {
        throw err;
      }

      // Retry on network errors or 5xx server errors
      if (attempt < retries && (!err.status || err.status >= 500)) {
        attempt++;
        await new Promise((res) => setTimeout(res, retryDelay * Math.pow(2, attempt - 1)));
        continue;
      }

      if (abortKey) {
        activeControllers.delete(abortKey);
      }
      throw err;
    } finally {
      if (loader && loader instanceof HTMLElement) {
        loader.classList.remove('is-loading');
        loader.removeAttribute('aria-busy');
      }
    }
  }
}

export const http = {
  get: (url, options = {}) => request(url, { ...options, method: 'GET' }),
  post: (url, body, options = {}) => request(url, { ...options, method: 'POST', body }),
  put: (url, body, options = {}) => request(url, { ...options, method: 'PUT', body }),
  patch: (url, body, options = {}) => request(url, { ...options, method: 'PATCH', body }),
  delete: (url, options = {}) => request(url, { ...options, method: 'DELETE' }),
};
