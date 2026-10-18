/*
================================================================================
  RocketBank — Modern Financial Platform
  Template: templatemo-623-novapay
  JavaScript
  Adapted from TemplateMo  (https://templatemo.com)

  Modules:
    1. Live ticker         — infinite CSS scroll with hover-pause
    2. Trusted-by logos    — infinite CSS scroll
    3. Nav scroll behavior — translateY snap on scroll past ticker
    4. Mobile menu         — body-scroll-lock + landscape-safe layout
    5. Stats counter       — IntersectionObserver count-up + bar fill
    6. Sticky stack        — scroll-driven feature switcher with right-panel swap
    7. Pricing toggle      — monthly / annual with dual price display
    8. FAQ                 — independent accordion + expand/collapse all
    9. Testimonials        — auto-scroll carousel with play/pause
   10. Period switcher     — dashboard time range toggle (7D/1M/3M/1Y)
   11. Silk reveals        — IntersectionObserver scroll-triggered animations
   12. Phone 3D tilt       — window-wide mouse tracking with lerp easing
================================================================================
*/

document.addEventListener('DOMContentLoaded', () => {
  // 1. Live Ticker
  const track = document.getElementById('tickerTrack');
  if (track) {
    const tickerData = [
      { sym: 'USD/KZT', price: '₸495.20', chg: '+0.15%', up: true },
      { sym: 'EUR/KZT', price: '₸538.40', chg: '-0.12%', up: false },
      { sym: 'RUB/KZT', price: '₸5.15', chg: '+0.35%', up: true },
      { sym: 'BTC/USD', price: '$67,240', chg: '+2.14%', up: true },
      { sym: 'ETH/USD', price: '$3,480', chg: '+1.82%', up: true },
      { sym: 'EUR/USD', price: '1.0841', chg: '-0.12%', up: false },
      { sym: 'GBP/USD', price: '1.2620', chg: '+0.08%', up: true },
      { sym: 'USD/JPY', price: '154.32', chg: '+0.24%', up: false },
      { sym: 'S&P 500', price: '5,248', chg: '+0.62%', up: true },
      { sym: 'XAU/USD', price: '$2,318', chg: '+0.44%', up: true },
    ];
    [...tickerData, ...tickerData].forEach(t => {
      const el = document.createElement('div');
      el.className = 'ticker-item';
      el.innerHTML = `<span class="ticker-sym">${t.sym}</span><span class="ticker-price">${t.price}</span><span class="${t.up ? 'ticker-up' : 'ticker-dn'}">${t.chg}</span>`;
      track.appendChild(el);
    });
  }

  // 2. Trusted Logos
  const lt = document.getElementById('logosTrack');
  if (lt) {
    const logos = ['Stripe', 'Shopify', 'Notion', 'Linear', 'Vercel', 'Figma', 'Supabase', 'Railway', 'Loom', 'Calendly', 'Webflow', 'Intercom'];
    [...logos, ...logos].forEach(l => {
      const el = document.createElement('div');
      el.className = 'logo-item';
      el.textContent = l;
      lt.appendChild(el);
    });
  }

  // 3. Nav Scroll Behavior
  const nav = document.getElementById('mainNav');
  if (nav) {
    window.addEventListener('scroll', () => {
      nav.classList.toggle('scrolled', window.scrollY > 10);
    });
  }

  // Silk reveals on load
  document.querySelectorAll('.hero-content, .hero-visual').forEach((el, i) => {
    setTimeout(() => el.classList.add('visible'), i * 150 + 100);
  });

  // 4. Mobile Menu
  const hamburger = document.getElementById('hamburger');
  const mobileMenu = document.getElementById('mobileMenu');
  let scrollY = 0;
  if (hamburger && mobileMenu) {
    hamburger.addEventListener('click', () => {
      const open = mobileMenu.classList.contains('open');
      if (open) {
        mobileMenu.classList.remove('open');
        hamburger.classList.remove('open');
        hamburger.setAttribute('aria-expanded', 'false');
        document.body.style.position = '';
        document.body.style.top = '';
        window.scrollTo({ top: scrollY, behavior: 'instant' });
      } else {
        scrollY = window.scrollY;
        document.body.style.position = 'fixed';
        document.body.style.top = `-${scrollY}px`;
        mobileMenu.classList.add('open');
        hamburger.classList.add('open');
        hamburger.setAttribute('aria-expanded', 'true');
      }
    });

    mobileMenu.querySelectorAll('a').forEach(a => {
      a.addEventListener('click', () => {
        mobileMenu.classList.remove('open');
        hamburger.classList.remove('open');
        hamburger.setAttribute('aria-expanded', 'false');
        document.body.style.position = '';
        document.body.style.top = '';
        window.scrollTo({ top: scrollY, behavior: 'instant' });
      });
    });
  }

  // Sparkline in Sticky Analytics panel
  const sparklineEl = document.getElementById('sparkline');
  if (sparklineEl) {
    const sparkBars = [60, 75, 50, 90, 65, 85, 70, 95];
    sparklineEl.innerHTML = sparkBars.map(h => `<div class="pm-spark-bar" style="height:${h}%"></div>`).join('');
  }

  // 6. Sticky Stack Features
  const stickyCards = document.querySelectorAll('.sticky-card');
  const panelViews = document.querySelectorAll('.panel-view');
  const panelLabel = document.getElementById('panelLabel');
  const panelLabels = [
    panelLabel ? (panelLabel.dataset.label0 || 'Transfers') : 'Transfers',
    panelLabel ? (panelLabel.dataset.label1 || 'Analytics') : 'Analytics',
    panelLabel ? (panelLabel.dataset.label2 || 'Multi-currency') : 'Multi-currency',
    panelLabel ? (panelLabel.dataset.label3 || 'Security') : 'Security',
  ];

  if (stickyCards.length > 0 && panelViews.length > 0) {
    stickyCards.forEach((card, i) => {
      card.addEventListener('click', () => {
        stickyCards.forEach(c => c.classList.remove('active'));
        panelViews.forEach(p => p.classList.remove('active'));
        card.classList.add('active');
        const targetPanel = document.getElementById('panel-' + i);
        if (targetPanel) targetPanel.classList.add('active');
        if (panelLabel && panelLabels[i]) panelLabel.textContent = panelLabels[i];
      });
    });

    const observer = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          stickyCards.forEach((card, i) => {
            const rect = card.getBoundingClientRect();
            const viewH = window.innerHeight;
            if (rect.top < viewH * 0.6 && rect.bottom > viewH * 0.3) {
              stickyCards.forEach(c => c.classList.remove('active'));
              panelViews.forEach(p => p.classList.remove('active'));
              card.classList.add('active');
              const targetPanel = document.getElementById('panel-' + i);
              if (targetPanel) targetPanel.classList.add('active');
              if (panelLabel && panelLabels[i]) panelLabel.textContent = panelLabels[i];
            }
          });
        }
      });
    }, { threshold: 0.3 });
    stickyCards.forEach(c => observer.observe(c));
  }

  // 5. Stats Counter
  const statNums = document.querySelectorAll('.stat-num[data-target]');
  if (statNums.length > 0) {
    const statsObs = new IntersectionObserver((entries) => {
      entries.forEach(e => {
        if (e.isIntersecting) {
          const el = e.target;
          const target = parseFloat(el.dataset.target);
          const suffix = el.dataset.suffix || '';
          const decimal = parseInt(el.dataset.decimal, 10) || 0;
          const prefix = el.dataset.prefix || '';
          const duration = 1800;
          let startTime = null;
          function animate(ts) {
            if (!startTime) startTime = ts;
            const progress = Math.min((ts - startTime) / duration, 1);
            const ease = 1 - Math.pow(1 - progress, 3);
            const val = target * ease;
            el.textContent = prefix + (decimal ? val.toFixed(decimal) : Math.round(val)) + suffix;
            if (progress < 1) requestAnimationFrame(animate);
          }
          requestAnimationFrame(animate);
          const block = el.closest('.stat-block');
          const bar = block ? block.querySelector('.stat-bar') : null;
          if (bar && bar.dataset.width) {
            setTimeout(() => { bar.style.width = bar.dataset.width; }, 200);
          }
          statsObs.unobserve(el);
        }
      });
    }, { threshold: 0.5 });
    statNums.forEach(el => statsObs.observe(el));
  }

  // 8. FAQ Accordion
  const faqList = document.getElementById('faqList');
  if (faqList) {
    const existingItems = faqList.querySelectorAll('.faq-item');
    if (existingItems.length > 0) {
      existingItems.forEach(item => {
        const q = item.querySelector('.faq-q');
        if (q) {
          q.addEventListener('click', () => {
            item.classList.toggle('open');
          });
        }
      });
    } else {
      const faqs = [
        { q: 'How quickly can I open an account and start sending payments?', a: 'You can be up and running in under 3 minutes. Register your account online, verify with instant biometric/document check, and start transacting with zero paperwork.' },
        { q: 'What are the transaction fees for domestic and global transfers?', a: 'All standard domestic transfers and peer-to-peer RocketBank transfers are 100% free with 0.00 KZT commission. Multi-currency international rails start at interbank live FX rates with zero hidden markups.' },
        { q: 'Are deposits insured by the Kazakhstan Deposit Insurance Fund?', a: 'Yes. All deposits held in RocketBank are fully guaranteed up to 20,000,000 KZT per depositor in savings deposits by the KDIF under the laws of the Republic of Kazakhstan.' },
        { q: 'How does RocketBank protect client funds and cards from fraud?', a: 'We employ bank-grade 256-bit AES encryption, row-level ACID transactional concurrency locks, SOC 2 compliance, and AI-powered real-time anomaly detection to block fraud instantly.' },
        { q: 'Can I integrate RocketBank with accounting tools and REST APIs?', a: 'Yes! RocketBank provides a full OpenAPI 3.0 / Swagger REST API with JWT authentication, webhook notifications, and automated export tools for finance and ERP platforms.' },
        { q: 'How can I freeze my bank card if it is lost or compromised?', a: 'You can freeze or unfreeze any debit or credit card instantly from your Client Dashboard or mobile interface with a single tap, blocking all physical and online transactions immediately.' },
      ];
      faqs.forEach(f => {
        const item = document.createElement('div');
        item.className = 'faq-item';
        item.innerHTML = `<div class="faq-q"><span class="faq-q-text">${f.q}</span><svg class="faq-chevron" viewBox="0 0 24 24"><polyline points="6,9 12,15 18,9"/></svg></div><div class="faq-a">${f.a}</div>`;
        item.querySelector('.faq-q').addEventListener('click', () => {
          item.classList.toggle('open');
        });
        faqList.appendChild(item);
      });
    }
  }

  // 9. Testimonials Carousel
  const tt = document.getElementById('testiTrack');
  if (tt) {
    if (tt.children.length > 0) {
      // Elements are server-rendered and localized. Clone once for marquee loop
      const cards = Array.from(tt.children);
      cards.forEach(card => tt.appendChild(card.cloneNode(true)));
    } else {
      const testimonials = [
        { q: 'RocketBank cut our corporate international settlement time from 3 days to under 2 seconds. It completely redefined our treasury speed.', name: 'Sarah Kim', role: 'CFO at Hive Commerce', init: 'SK' },
        { q: 'The multi-currency IBAN accounts saved us over ₸18M in FX conversions this year. The exchange rate transparency is unparalleled.', name: 'James Adler', role: 'Finance Director, Nomad Labs', init: 'JA' },
        { q: 'Finally a modern digital banking platform that feels ultra-fast and engineered for modern engineers and tech businesses.', name: 'Priya Mehta', role: 'Head of Ops, Stackflow', init: 'PM' },
        { q: 'Migrated our business accounts in one afternoon. The REST API documentation and instant webhooks are exceptional.', name: 'Tom Brennan', role: 'CTO at Vaulted', init: 'TB' },
        { q: 'The automated fraud detection and instant card freeze give our executive team complete peace of mind.', name: 'Liu Wei', role: 'Founder, CloudMint', init: 'LW' },
        { q: 'Automated payroll and batch payments save our accounting team over 25 hours every month.', name: 'Amara Osei', role: 'Controller, Drift Studio', init: 'AO' },
      ];
      [...testimonials, ...testimonials].forEach(t => {
        const el = document.createElement('div');
        el.className = 'testi-card';
        el.innerHTML = `<div class="testi-stars">${[...Array(5)].map(() => '<svg viewBox="0 0 24 24"><polygon points="12,2 15.09,8.26 22,9.27 17,14.14 18.18,21.02 12,17.77 5.82,21.02 7,14.14 2,9.27 8.91,8.26"/></svg>').join('')}</div><p class="testi-quote">"${t.q}"</p><div class="testi-author"><div class="testi-avatar">${t.init}</div><div><div class="testi-name">${t.name}</div><div class="testi-role">${t.role}</div></div></div>`;
        tt.appendChild(el);
      });
    }
  }

  const testiToggle = document.getElementById('testiToggle');
  if (testiToggle && tt) {
    let testiPaused = false;
    testiToggle.addEventListener('click', () => {
      testiPaused = !testiPaused;
      tt.style.animationPlayState = testiPaused ? 'paused' : 'running';
      const icon = document.getElementById('testiIcon');
      const label = document.getElementById('testiLabel');
      const playTxt = label ? (label.dataset.playText || 'Play') : 'Play';
      const pauseTxt = label ? (label.dataset.pauseText || 'Pause') : 'Pause';
      if (testiPaused) {
        if (icon) icon.innerHTML = '<polygon points="6,4 20,12 6,20"/>';
        if (label) label.textContent = playTxt;
        testiToggle.setAttribute('aria-label', playTxt);
      } else {
        if (icon) icon.innerHTML = '<rect x="6" y="5" width="4" height="14" rx="1"/><rect x="14" y="5" width="4" height="14" rx="1"/>';
        if (label) label.textContent = pauseTxt;
        testiToggle.setAttribute('aria-label', pauseTxt);
      }
    });
  }

  // Smooth hash link scrolling
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
      const href = a.getAttribute('href');
      if (href === '#' || !href) return;
      const target = document.querySelector(href);
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });

  // Silk reveals
  const revealObs = new IntersectionObserver((entries) => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        e.target.classList.add('visible');
        revealObs.unobserve(e.target);
      }
    });
  }, { threshold: 0.12 });
  document.querySelectorAll('.silk-reveal, .silk-reveal-left, .silk-reveal-right').forEach((el, i) => {
    el.style.animationDelay = (i % 4) * 0.08 + 's';
    revealObs.observe(el);
  });

  // 12. Phone 3D Tilt
  const phoneFrame = document.getElementById('phoneFrame');
  if (phoneFrame) {
    let targetX = 0, targetY = 0, currentX = 0, currentY = 0, rafId = null;
    const MAX_TILT = 16;
    function animateTilt() {
      currentX += (targetX - currentX) * 0.06;
      currentY += (targetY - currentY) * 0.06;
      phoneFrame.style.transform = `rotateX(${currentY}deg) rotateY(${currentX}deg) translateZ(0)`;
      if (Math.abs(targetX - currentX) > 0.02 || Math.abs(targetY - currentY) > 0.02) {
        rafId = requestAnimationFrame(animateTilt);
      } else {
        rafId = null;
      }
    }
    function kickTilt() {
      if (!rafId) rafId = requestAnimationFrame(animateTilt);
    }
    window.addEventListener('mousemove', e => {
      const x = e.clientX / window.innerWidth - 0.5;
      const y = e.clientY / window.innerHeight - 0.5;
      targetX = x * MAX_TILT * 4;
      targetY = -y * MAX_TILT * 2;
      kickTilt();
    });
    window.addEventListener('mouseleave', () => {
      targetX = 0; targetY = 0;
      kickTilt();
    });
  }
});

// Period Switcher (Global)
window.switchPeriod = function(btn, period) {
  document.querySelectorAll('.dp-period-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  const lang = (document.documentElement.lang || 'en').toLowerCase();
  const todayLabel = lang === 'ru' ? 'сегодня' : (lang === 'kk' ? 'бүгін' : 'today');
  const monthLabel = lang === 'ru' ? 'за месяц' : (lang === 'kk' ? 'айда' : 'month');
  const quarterLabel = lang === 'ru' ? 'за квартал' : (lang === 'kk' ? 'тоқсанда' : 'quarter');
  const yearLabel = lang === 'ru' ? 'за год' : (lang === 'kk' ? 'жылына' : 'year');
  const configs = {
    '7d': { val: '₸142,460,000', change: `▲ +₸6,420,000 (4.72%) ${todayLabel}` },
    '1m': { val: '₸184,920,000', change: `▲ +₸37,460,000 (25.4%) ${monthLabel}` },
    '3m': { val: '₸228,500,000', change: `▲ +₸52,400,000 (29.7%) ${quarterLabel}` },
    '1y': { val: '₸450,000,000', change: `▲ +₸164,000,000 (57.3%) ${yearLabel}` },
  };
  const c = configs[period] || configs['7d'];
  const vEl = document.getElementById('dpChartVal');
  const cEl = document.getElementById('dpChartChange');
  if (vEl) vEl.textContent = c.val;
  if (cEl) cEl.textContent = c.change;
};

// Pricing Toggle (Global)
let isAnnual = false;
window.togglePricing = function() {
  isAnnual = !isAnnual;
  const toggle = document.getElementById('pricingToggle');
  if (toggle) toggle.classList.toggle('on', isAnnual);
  document.querySelectorAll('.price-num').forEach(el => {
    el.textContent = isAnnual ? el.dataset.annual : el.dataset.monthly;
  });
  document.querySelectorAll('.period-label').forEach(el => {
    const annualTxt = el.dataset.annual || 'annually';
    const monthlyTxt = el.dataset.monthly || 'monthly';
    el.textContent = isAnnual ? annualTxt : monthlyTxt;
  });
  document.querySelectorAll('.price-alt-monthly').forEach(el => {
    el.style.display = isAnnual ? 'none' : 'inline';
  });
  document.querySelectorAll('.price-alt-annual').forEach(el => {
    el.style.display = isAnnual ? 'inline' : 'none';
  });
};

// FAQ Toggle All (Global)
let allExpanded = false;
window.toggleAllFaq = function() {
  allExpanded = !allExpanded;
  document.querySelectorAll('.faq-item').forEach(el => {
    allExpanded ? el.classList.add('open') : el.classList.remove('open');
  });
  const lbl = document.getElementById('faqToggleLabel');
  if (lbl) {
    const expandTxt = lbl.dataset.expandText || 'Expand all';
    const collapseTxt = lbl.dataset.collapseText || 'Collapse all';
    lbl.textContent = allExpanded ? collapseTxt : expandTxt;
  }
  const icon = document.getElementById('faqToggleIcon');
  if (icon) {
    icon.innerHTML = allExpanded
      ? '<line x1="5" y1="12" x2="19" y2="12"/>'
      : '<line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>';
  }
};
