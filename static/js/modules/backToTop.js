/**
 * Module 14: Smooth "Back to Top" Floating Button
 * Appears when page is scrolled down (>300px) and smoothly returns user to top.
 */

export function initBackToTop() {
  let btn = document.getElementById('back-to-top');

  if (!btn) {
    btn = document.createElement('button');
    btn.id = 'back-to-top';
    btn.type = 'button';
    btn.className = 'btn btn--secondary btn-back-to-top shadow-lg';
    btn.setAttribute('aria-label', 'Back to top of page');
    btn.innerHTML = '<span aria-hidden="true">↑</span>';
    btn.style.position = 'fixed';
    btn.style.bottom = '2rem';
    btn.style.right = '2rem';
    btn.style.zIndex = '900';
    btn.style.borderRadius = '50%';
    btn.style.width = '48px';
    btn.style.height = '48px';
    btn.style.display = 'none';
    btn.style.alignItems = 'center';
    btn.style.justifyContent = 'center';
    btn.style.fontSize = '1.25rem';
    btn.style.cursor = 'pointer';
    btn.style.transition = 'opacity 0.2s ease, transform 0.2s ease';
    document.body.appendChild(btn);
  }

  const handleScroll = () => {
    if (window.scrollY > 300) {
      btn.style.display = 'flex';
      setTimeout(() => {
        btn.style.opacity = '1';
        btn.style.transform = 'translateY(0)';
      }, 10);
    } else {
      btn.style.opacity = '0';
      btn.style.transform = 'translateY(10px)';
      setTimeout(() => {
        if (window.scrollY <= 300) {
          btn.style.display = 'none';
        }
      }, 200);
    }
  };

  window.addEventListener('scroll', handleScroll, { passive: true });

  btn.addEventListener('click', (e) => {
    e.preventDefault();
    window.scrollTo({
      top: 0,
      behavior: 'smooth',
    });
    // Restore focus to top skip-link or document body
    const skipLink = document.querySelector('.skip-link');
    if (skipLink) {
      skipLink.focus();
    }
  });
}
