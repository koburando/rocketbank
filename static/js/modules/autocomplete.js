/**
 * Module 2: Live Search Autocomplete
 * Features:
 * - 300ms debounced queries
 * - Substring match highlighting with <mark>
 * - Full keyboard navigation (ArrowDown, ArrowUp, Enter, Escape)
 * - Accessible WAI-ARIA combobox pattern
 */

import { http } from '../api/http.js';
import { debounce, sanitizeHTML } from '../utils.js';

export function highlightMatch(text, query) {
  if (!query) {
    return sanitizeHTML(text);
  }
  const escapedQuery = query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  const regex = new RegExp(`(${escapedQuery})`, 'gi');
  return sanitizeHTML(text).replace(regex, '<mark>$1</mark>');
}

export function initAutocomplete() {
  const inputs = document.querySelectorAll('[data-autocomplete]');
  if (!inputs.length) {
    return;
  }

  inputs.forEach((input) => {
    const endpoint = input.dataset.autocomplete || '/api/v1/card-products/';
    const dropdown = document.createElement('ul');
    dropdown.className = 'autocomplete-dropdown';
    dropdown.setAttribute('role', 'listbox');
    dropdown.setAttribute('aria-label', 'Search suggestions');
    dropdown.style.display = 'none';

    // Position relative to parent
    input.parentNode.style.position = 'relative';
    input.parentNode.appendChild(dropdown);
    input.setAttribute('aria-autocomplete', 'list');
    input.setAttribute('aria-expanded', 'false');

    let activeIndex = -1;
    let items = [];

    const closeDropdown = () => {
      dropdown.style.display = 'none';
      input.setAttribute('aria-expanded', 'false');
      activeIndex = -1;
      items = [];
    };

    const fetchSuggestions = debounce(async (query) => {
      if (query.length < 2) {
        closeDropdown();
        return;
      }

      try {
        const url = `${endpoint}?search=${encodeURIComponent(query)}`;
        const res = await http.get(url, { abortKey: 'autocomplete' });
        const results = res.results || res || [];

        dropdown.innerHTML = '';
        activeIndex = -1;
        items = results.slice(0, 8);

        if (!items.length) {
          const emptyLi = document.createElement('li');
          emptyLi.className = 'autocomplete-item autocomplete-item--empty';
          emptyLi.textContent = 'No matching products found';
          dropdown.appendChild(emptyLi);
          dropdown.style.display = 'block';
          input.setAttribute('aria-expanded', 'true');
          return;
        }

        items.forEach((item, index) => {
          const li = document.createElement('li');
          li.className = 'autocomplete-item';
          li.setAttribute('role', 'option');
          li.setAttribute('id', `autocomplete-opt-${index}`);
          li.dataset.index = index;

          const title = item.title || item.name || item.iban || 'Item';
          const subtitle = item.tier || item.category?.name || item.description || '';

          li.innerHTML = `
            <div class="autocomplete-title">${highlightMatch(title, query)}</div>
            ${subtitle ? `<div class="autocomplete-subtitle">${sanitizeHTML(subtitle.slice(0, 60))}</div>` : ''}
          `;

          li.addEventListener('click', () => {
            selectItem(item);
          });

          dropdown.appendChild(li);
        });

        dropdown.style.display = 'block';
        input.setAttribute('aria-expanded', 'true');
      } catch (err) {
        if (err.name !== 'AbortError') {
          closeDropdown();
        }
      }
    }, 300);

    const selectItem = (item) => {
      input.value = item.title || item.name || item.iban || '';
      closeDropdown();
      if (item.slug) {
        // If it's a card product or catalog item, trigger custom select or navigate
        input.dispatchEvent(new CustomEvent('autocomplete:select', { detail: item, bubbles: true }));
      }
    };

    const updateActiveItem = () => {
      const optionElements = dropdown.querySelectorAll('.autocomplete-item:not(.autocomplete-item--empty)');
      optionElements.forEach((el, idx) => {
        if (idx === activeIndex) {
          el.classList.add('is-active');
          el.setAttribute('aria-selected', 'true');
          input.setAttribute('aria-activedescendant', el.id);
          el.scrollIntoView({ block: 'nearest' });
        } else {
          el.classList.remove('is-active');
          el.removeAttribute('aria-selected');
        }
      });
    };

    input.addEventListener('input', (e) => {
      fetchSuggestions(e.target.value.trim());
    });

    input.addEventListener('keydown', (e) => {
      const optionElements = dropdown.querySelectorAll('.autocomplete-item:not(.autocomplete-item--empty)');
      if (!optionElements.length) {
        return;
      }

      if (e.key === 'ArrowDown') {
        e.preventDefault();
        activeIndex = (activeIndex + 1) % optionElements.length;
        updateActiveItem();
      } else if (e.key === 'ArrowUp') {
        e.preventDefault();
        activeIndex = (activeIndex - 1 + optionElements.length) % optionElements.length;
        updateActiveItem();
      } else if (e.key === 'Enter') {
        if (activeIndex >= 0 && items[activeIndex]) {
          e.preventDefault();
          selectItem(items[activeIndex]);
        }
      } else if (e.key === 'Escape') {
        closeDropdown();
      }
    });

    document.addEventListener('click', (e) => {
      if (!input.contains(e.target) && !dropdown.contains(e.target)) {
        closeDropdown();
      }
    });
  });
}
