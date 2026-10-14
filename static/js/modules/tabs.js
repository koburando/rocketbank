/**
 * Module 6: Interactive Accessible Tabs Component
 * WAI-ARIA tab pattern with keyboard ArrowLeft/ArrowRight/Home/End navigation.
 */

export function activateTab(tab, tablist) {
  const tabs = Array.from(tablist.querySelectorAll('[role="tab"], .tab-item'));
  const targetPanelId = tab.getAttribute('aria-controls') || tab.dataset.target;

  // Deactivate all tabs in this list
  tabs.forEach((t) => {
    t.setAttribute('aria-selected', 'false');
    t.setAttribute('tabindex', '-1');
    t.classList.remove('is-active', 'tab-item--active');
  });

  // Activate clicked tab
  tab.setAttribute('aria-selected', 'true');
  tab.setAttribute('tabindex', '0');
  tab.classList.add('is-active', 'tab-item--active');
  tab.focus();

  // Switch tabpanels
  const container = tablist.closest('.tabs-container') || document;
  const panels = Array.from(container.querySelectorAll('[role="tabpanel"], .tab-pane'));
  panels.forEach((p) => {
    if (p.id === targetPanelId) {
      p.hidden = false;
      p.classList.add('is-active', 'show');
    } else {
      p.hidden = true;
      p.classList.remove('is-active', 'show');
    }
  });
}

export function initTabs() {
  document.addEventListener('click', (e) => {
    const tab = e.target.closest('[role="tab"], .tab-item');
    if (!tab) {
      return;
    }
    const tablist = tab.closest('[role="tablist"], .tabs-nav');
    if (!tablist) {
      return;
    }

    e.preventDefault();
    activateTab(tab, tablist);
  });

  document.addEventListener('keydown', (e) => {
    const tab = e.target.closest('[role="tab"], .tab-item');
    if (!tab) {
      return;
    }
    const tablist = tab.closest('[role="tablist"], .tabs-nav');
    if (!tablist) {
      return;
    }

    const tabs = Array.from(tablist.querySelectorAll('[role="tab"], .tab-item'));
    const index = tabs.indexOf(tab);
    if (index === -1) {
      return;
    }

    let nextIndex = index;
    if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
      e.preventDefault();
      nextIndex = (index + 1) % tabs.length;
    } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
      e.preventDefault();
      nextIndex = (index - 1 + tabs.length) % tabs.length;
    } else if (e.key === 'Home') {
      e.preventDefault();
      nextIndex = 0;
    } else if (e.key === 'End') {
      e.preventDefault();
      nextIndex = tabs.length - 1;
    } else {
      return;
    }

    activateTab(tabs[nextIndex], tablist);
  });
}
