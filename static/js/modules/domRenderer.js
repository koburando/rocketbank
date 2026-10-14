/**
 * Module 21: Safe DOM List Renderer
 * Strict XSS-protected template rendering engine using HTML5 <template> and textContent.
 * Eliminates injection vulnerabilities by avoiding unsafe innerHTML assignment with dynamic values.
 */

export class SafeDomRenderer {
  /**
   * @param {HTMLTemplateElement|string} template - Template element or its ID
   * @param {HTMLElement|string} container - Target container element or its ID
   */
  constructor(template, container) {
    this.template = typeof template === 'string' ? document.getElementById(template) : template;
    this.container = typeof container === 'string' ? document.getElementById(container) : container;
  }

  /**
   * Safely render a list of data objects into the container.
   * @param {Array<object>} items - Array of data models
   * @param {Function} [binder] - Optional custom field mapping function (clone, item) => void
   * @param {boolean} [append=false] - Whether to append or replace container contents
   */
  renderList(items, binder = null, append = false) {
    if (!this.container || !this.template) {
      return;
    }

    const fragment = document.createDocumentFragment();

    items.forEach((item) => {
      const clone = this.template.content.cloneNode(true);

      if (binder && typeof binder === 'function') {
        binder(clone, item);
      } else {
        // Automatic slot mapping: elements with [data-slot="fieldName"]
        const slots = clone.querySelectorAll('[data-slot]');
        slots.forEach((slot) => {
          const field = slot.dataset.slot;
          if (field in item && item[field] !== null && item[field] !== undefined) {
            slot.textContent = String(item[field]);
          }
        });
      }

      fragment.appendChild(clone);
    });

    if (!append) {
      this.container.innerHTML = '';
    }
    this.container.appendChild(fragment);
  }

  /**
   * Safely render a single item.
   * @param {object} item
   * @param {Function} [binder]
   */
  renderItem(item, binder = null) {
    this.renderList([item], binder, true);
  }
}

export function initDomRenderer() {
  // Expose on window for inline templates or components if needed
  window.SafeDomRenderer = SafeDomRenderer;
}
