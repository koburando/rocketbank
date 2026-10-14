/**
 * Module 9: Infinite Scroll & Load More Pagination
 * Uses IntersectionObserver API to dynamically fetch and append paginated data.
 */

import { http } from '../api/http.js';

export function initInfiniteScroll() {
  const sentinel = document.querySelector('[data-infinite-scroll], [data-sentinel]');
  const loadMoreBtn = document.querySelector('[data-load-more-btn]');
  const container = document.querySelector('[data-scroll-container], [data-infinite-target]');

  if (!container || (!sentinel && !loadMoreBtn)) {
    return;
  }

  let isLoading = false;
  let nextUrl = (sentinel?.dataset.nextUrl || loadMoreBtn?.dataset.nextUrl);

  const loadNextPage = async () => {
    if (isLoading || !nextUrl) {
      return;
    }

    isLoading = true;
    if (loadMoreBtn) {
      loadMoreBtn.disabled = true;
      loadMoreBtn.classList.add('is-loading');
      loadMoreBtn.textContent = 'Loading...';
    }

    try {
      const data = await http.get(nextUrl, { abortKey: 'infiniteScroll' });
      nextUrl = data.next || null;

      // Update sentinel / loadMore button data-next-url
      if (sentinel) {
        sentinel.dataset.nextUrl = nextUrl || '';
      }
      if (loadMoreBtn) {
        loadMoreBtn.dataset.nextUrl = nextUrl || '';
      }

      const results = data.results || (Array.isArray(data) ? data : []);

      if (results.length > 0) {
        // Dispatch custom event for rendering or append template
        const event = new CustomEvent('infiniteScroll:data', {
          detail: { results, nextUrl },
          bubbles: true,
        });
        container.dispatchEvent(event);
      }

      if (!nextUrl) {
        if (sentinel) {
          sentinel.style.display = 'none';
        }
        if (loadMoreBtn) {
          loadMoreBtn.style.display = 'none';
        }
      }
    } catch (err) {
      if (err.name !== 'AbortError') {
        console.error('[InfiniteScroll] Error loading page:', err);
      }
    } finally {
      isLoading = false;
      if (loadMoreBtn) {
        loadMoreBtn.disabled = false;
        loadMoreBtn.classList.remove('is-loading');
        loadMoreBtn.textContent = 'Load More';
      }
    }
  };

  // IntersectionObserver for automatic infinite scroll
  if (sentinel && 'IntersectionObserver' in window) {
    const observer = new IntersectionObserver((entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting && !isLoading && nextUrl) {
          loadNextPage();
        }
      });
    }, { rootMargin: '200px' });

    observer.observe(sentinel);
  }

  // Click trigger for Load More button
  if (loadMoreBtn) {
    loadMoreBtn.addEventListener('click', (e) => {
      e.preventDefault();
      loadNextPage();
    });
  }
}
