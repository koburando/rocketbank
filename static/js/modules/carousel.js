/**
 * Module 8: Product & Card Carousel Slider
 * Vanilla touch-enabled and keyboard accessible carousel slider.
 */

export function setupCarousel(container) {
  const track = container.querySelector('.carousel__track, [data-carousel-track]');
  const slides = Array.from(container.querySelectorAll('.carousel__slide, [data-carousel-slide]'));
  const prevBtn = container.querySelector('[data-carousel-prev]');
  const nextBtn = container.querySelector('[data-carousel-next]');
  const indicatorsContainer = container.querySelector('.carousel__indicators');

  if (!track || slides.length <= 1) {
    return;
  }

  let currentIndex = 0;

  const updateSlide = (newIndex) => {
    currentIndex = (newIndex + slides.length) % slides.length;
    track.style.transform = `translateX(-${currentIndex * 100}%)`;

    slides.forEach((slide, idx) => {
      slide.setAttribute('aria-hidden', idx === currentIndex ? 'false' : 'true');
    });

    if (indicatorsContainer) {
      const dots = indicatorsContainer.querySelectorAll('.carousel__dot');
      dots.forEach((dot, idx) => {
        dot.classList.toggle('is-active', idx === currentIndex);
        dot.setAttribute('aria-current', idx === currentIndex ? 'true' : 'false');
      });
    }
  };

  if (prevBtn) {
    prevBtn.addEventListener('click', () => updateSlide(currentIndex - 1));
  }
  if (nextBtn) {
    nextBtn.addEventListener('click', () => updateSlide(currentIndex + 1));
  }

  // Create indicators if container exists
  if (indicatorsContainer) {
    indicatorsContainer.innerHTML = '';
    slides.forEach((_, idx) => {
      const dot = document.createElement('button');
      dot.className = `carousel__dot ${idx === 0 ? 'is-active' : ''}`;
      dot.setAttribute('aria-label', `Go to slide ${idx + 1}`);
      dot.addEventListener('click', () => updateSlide(idx));
      indicatorsContainer.appendChild(dot);
    });
  }

  // Touch swipe support
  let touchStartX = 0;
  let touchEndX = 0;

  container.addEventListener('touchstart', (e) => {
    touchStartX = e.changedTouches[0].screenX;
  }, { passive: true });

  container.addEventListener('touchend', (e) => {
    touchEndX = e.changedTouches[0].screenX;
    const diff = touchStartX - touchEndX;
    if (Math.abs(diff) > 40) {
      if (diff > 0) {
        updateSlide(currentIndex + 1); // Swipe left -> Next
      } else {
        updateSlide(currentIndex - 1); // Swipe right -> Prev
      }
    }
  }, { passive: true });

  // Keyboard navigation
  container.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowLeft') {
      updateSlide(currentIndex - 1);
    } else if (e.key === 'ArrowRight') {
      updateSlide(currentIndex + 1);
    }
  });

  updateSlide(0);
}

export function initCarousel() {
  const carousels = document.querySelectorAll('[data-carousel], .carousel');
  carousels.forEach(setupCarousel);
}
