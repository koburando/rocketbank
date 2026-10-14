/**
 * Module 7: Accessible Accordion Component
 * Handles collapsible FAQ/Content sections with aria-expanded management.
 */

export function toggleAccordionItem(header) {
  const isExpanded = header.getAttribute('aria-expanded') === 'true';
  const accordion = header.closest('.accordion');
  const panelId = header.getAttribute('aria-controls') || header.dataset.target;
  const panel = panelId ? document.getElementById(panelId) : header.nextElementSibling;

  if (!panel) {
    return;
  }

  // Single-open accordion: close other panels unless multi is enabled
  if (accordion && !accordion.hasAttribute('data-multi-open') && !isExpanded) {
    const activeHeaders = accordion.querySelectorAll('.accordion__header[aria-expanded="true"]');
    activeHeaders.forEach((h) => {
      h.setAttribute('aria-expanded', 'false');
      const pId = h.getAttribute('aria-controls') || h.dataset.target;
      const p = pId ? document.getElementById(pId) : h.nextElementSibling;
      if (p) {
        p.hidden = true;
        p.classList.remove('is-open');
      }
    });
  }

  header.setAttribute('aria-expanded', isExpanded ? 'false' : 'true');
  panel.hidden = isExpanded;
  panel.classList.toggle('is-open', !isExpanded);
}

export function initAccordion() {
  document.addEventListener('click', (e) => {
    const header = e.target.closest('.accordion__header, [data-accordion-toggle]');
    if (header) {
      e.preventDefault();
      toggleAccordionItem(header);
    }
  });

  document.addEventListener('keydown', (e) => {
    const header = e.target.closest('.accordion__header, [data-accordion-toggle]');
    if (!header) {
      return;
    }

    if (e.key === 'Enter' || e.key === ' ') {
      e.preventDefault();
      toggleAccordionItem(header);
    }
  });
}
