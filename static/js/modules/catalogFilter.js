/**
 * Module 3: Catalog AJAX Filtering & Sorting
 * Features:
 * - Updates catalog items dynamically via AJAX
 * - Synchronizes state with URLSearchParams and window.history.pushState
 * - Handles browser Back and Forward navigation via popstate
 * - Preserves bookmarkable URLs
 */

import { http } from '../api/http.js';
import { formatCurrency, sanitizeHTML } from '../utils.js';

function renderCardProductCard(product) {
  return `
    <article class="card card--interactive catalog-card" data-product-id="${product.id}" data-tier="${product.tier}">
      <div class="card__header d-flex justify-between items-center">
        <div>
          <span class="badge badge--info">${sanitizeHTML(product.tier)}</span>
          <h3 class="card__title mt-xs">${sanitizeHTML(product.title)}</h3>
        </div>
        <button type="button" class="btn-favorite" data-favorite-type="card" data-favorite-id="${product.slug}" aria-label="Save to favorites">
          <span aria-hidden="true">★</span>
        </button>
      </div>
      <div class="card__body">
        <p class="text-secondary">${sanitizeHTML(product.description || '')}</p>
        <div class="d-flex gap-lg my-md">
          <div>
            <small class="text-muted d-block">Cashback</small>
            <strong class="text-brand font-mono">${product.cashback_percent}%</strong>
          </div>
          <div>
            <small class="text-muted d-block">Annual Fee</small>
            <strong class="font-mono">${formatCurrency(product.annual_fee, 'KZT')}</strong>
          </div>
        </div>
      </div>
      <div class="card__footer d-flex gap-sm">
        <a href="/cards/apply/?product=${product.slug}" class="btn btn--primary btn--sm flex-1">Apply Now</a>
        <a href="/cards/${product.slug}/" class="btn btn--secondary btn--sm">Details</a>
      </div>
    </article>
  `;
}

export function initCatalogFilter() {
  const filterForm = document.querySelector('[data-catalog-filter]');
  const resultsContainer = document.querySelector('[data-catalog-results]');

  if (!filterForm || !resultsContainer) {
    return;
  }

  const endpoint = filterForm.dataset.apiEndpoint || '/api/v1/card-products/';

  const applyFilters = async (pushState = true) => {
    const formData = new FormData(filterForm);
    const searchParams = new URLSearchParams();
    const apiParams = new URLSearchParams();

    for (const [key, val] of formData.entries()) {
      if (val && val.trim() !== '') {
        const cleanVal = val.trim();
        searchParams.set(key, cleanVal);

        if (key === 'q') {
          apiParams.set('search', cleanVal);
        } else if (key === 'sort') {
          if (cleanVal === 'cashback') apiParams.set('ordering', '-cashback_percent');
          else if (cleanVal === 'fee') apiParams.set('ordering', 'annual_fee');
          else apiParams.set('ordering', cleanVal);
        } else {
          apiParams.set(key, cleanVal);
        }
      }
    }

    if (pushState) {
      const qs = searchParams.toString();
      const newUrl = `${window.location.pathname}${qs ? '?' + qs : ''}`;
      window.history.pushState({ path: newUrl }, '', newUrl);
    }

    resultsContainer.setAttribute('aria-busy', 'true');
    resultsContainer.classList.add('is-loading');

    try {
      const apiUrl = `${endpoint}${apiParams.toString() ? '?' + apiParams.toString() : ''}`;
      const data = await http.get(apiUrl, { abortKey: 'catalogFilter' });
      const items = data.results || data || [];

      if (!items.length) {
        resultsContainer.innerHTML = `
          <div class="empty-state text-center p-3xl col-span-full">
            <span style="font-size: 3rem;" aria-hidden="true">🔍</span>
            <h3 class="mt-md">No matching products found</h3>
            <p class="text-secondary">Try adjusting your filters or search keywords.</p>
          </div>
        `;
      } else {
        resultsContainer.innerHTML = items.map(renderCardProductCard).join('');
      }

      // Re-initialize favorite buttons for newly rendered elements
      document.dispatchEvent(new CustomEvent('catalog:rendered'));
    } catch (err) {
      if (err.name !== 'AbortError') {
        resultsContainer.innerHTML = `
          <div class="alert alert--danger col-span-full">
            Failed to load products. Please check your connection and try again.
          </div>
        `;
      }
    } finally {
      resultsContainer.removeAttribute('aria-busy');
      resultsContainer.classList.remove('is-loading');
    }
  };

  filterForm.addEventListener('change', () => {
    applyFilters(true);
  });

  filterForm.addEventListener('submit', (e) => {
    e.preventDefault();
    applyFilters(true);
  });

  // Restore filter values and content on browser back/forward buttons
  window.addEventListener('popstate', () => {
    const currentParams = new URLSearchParams(window.location.search);
    for (const element of filterForm.elements) {
      if (element.name) {
        if (currentParams.has(element.name)) {
          element.value = currentParams.get(element.name);
        } else if (element.type === 'checkbox' || element.type === 'radio') {
          element.checked = false;
        } else {
          element.value = '';
        }
      }
    }
    applyFilters(false);
  });
}
