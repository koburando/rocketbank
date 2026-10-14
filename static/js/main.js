/**
 * RocketBank Vanilla ES6+ Main Entry Point
 * Orchestrates modular architecture and initializes all 25 interactive features.
 * Zero jQuery, zero global pollutions, strict event delegation.
 */

import { initFormValidation } from './modules/validation.js';
import { initAutocomplete } from './modules/autocomplete.js';
import { initCatalogFilter } from './modules/catalogFilter.js';
import { initThemeSwitcher } from './modules/themeSwitcher.js';
import { initModal } from './modules/modal.js';
import { initTabs } from './modules/tabs.js';
import { initAccordion } from './modules/accordion.js';
import { initCarousel } from './modules/carousel.js';
import { initInfiniteScroll } from './modules/infiniteScroll.js';
import { initFileUpload } from './modules/fileUpload.js';
import { initCharCounter } from './modules/charCounter.js';
import { initClipboard } from './modules/clipboard.js';
import { initToast } from './modules/toast.js';
import { initBackToTop } from './modules/backToTop.js';
import { initPhoneMask } from './modules/phoneMask.js';
import { initCalculator } from './modules/calculator.js';
import { initTimer } from './modules/timer.js';
import { initFavorites } from './modules/favorites.js';
import { initFormDraft } from './modules/formDraft.js';
import { initAnalyticsChart } from './modules/analyticsChart.js';
import { initDomRenderer } from './modules/domRenderer.js';
import { initCardToggle } from './modules/cardToggle.js';
import { initNotificationBell } from './modules/notificationBell.js';
import { initReviewRating } from './modules/reviewRating.js';
import { initExportPrint } from './modules/exportPrint.js';

// Register PWA Service Worker
function registerServiceWorker() {
  if ('serviceWorker' in navigator && window.isSecureContext) {
    window.addEventListener('load', () => {
      navigator.serviceWorker.register('/static/service-worker.js')
        .then((reg) => {
          // Service worker active
        })
        .catch((err) => {
          console.warn('[ServiceWorker] Registration ignored:', err);
        });
    });
  }
}

// Master initialization routine
function initRocketBank() {
  // PWA Service Worker
  registerServiceWorker();

  // Core UI Systems (Section 4 — 25 Modules)
  initFormValidation();      // 1. Real-time form validation
  initAutocomplete();        // 2. Live search autocomplete
  initCatalogFilter();       // 3. Catalog AJAX filtering & URL pushState
  initThemeSwitcher();       // 4. Light/Dark theme switcher with API sync
  initModal();               // 5. Accessible Modal controller with focus trap
  initTabs();                // 6. Interactive tabs with keyboard navigation
  initAccordion();           // 7. Accordion component
  initCarousel();            // 8. Product / Cards carousel slider
  initInfiniteScroll();      // 9. Load more pagination / infinite scroll
  initFileUpload();          // 10. Drag & Drop file upload with preview
  initCharCounter();         // 11. Textarea character counter
  initClipboard();           // 12. One-click clipboard copy manager
  initToast();               // 13. Toast notification manager
  initBackToTop();           // 14. Smooth back to top floating button
  initPhoneMask();           // 15. Phone number mask
  initCalculator();          // 16. Annuity loan & deposit calculator
  initTimer();               // 17. Promo / OTP countdown timer
  initFavorites();           // 18. Guest favorites in localStorage with sync
  initFormDraft();           // 19. Form draft auto-save and restore
  initAnalyticsChart();      // 20. Interactive Financial Analytics Chart (Chart.js)
  initDomRenderer();         // 21. Safe DOM template list renderer
  initCardToggle();          // 22. Card freeze/unfreeze instant toggle
  initNotificationBell();    // 23. Notification bell live counter & mark-read
  initReviewRating();        // 24. Review 1-5 star picker & helpful vote
  initExportPrint();         // 25. Print receipt trigger & table CSV export
}

// Run when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initRocketBank);
} else {
  initRocketBank();
}
