window.addEventListener("scroll", () => {
  const navbar = document.getElementById("dars-navbar");
  if (window.scrollY > 20) {
    navbar.classList.add("scrolled");
  } else {
    navbar.classList.remove("scrolled");
  }

  const featuresSection = document.getElementById("features-section");
  if (featuresSection && !featuresSection.classList.contains("visible")) {
    const sectionPosition = featuresSection.getBoundingClientRect().top;
    const screenPosition = window.innerHeight / 1.5;

    if (sectionPosition < screenPosition) {
      featuresSection.classList.add("visible");

      const featureCards = document.querySelectorAll('[id^="feature-card-"]');
      featureCards.forEach((card, index) => {
        setTimeout(() => {
          card.style.opacity = "1";
          card.style.transform = "translateY(0)";
        }, index * 100);
      });
    }
  }
});

document.addEventListener('DOMContentLoaded', function () {
  const hamburgerBtn = document.getElementById('hamburger-btn');
  const mobileMenu = document.getElementById('mobile-menu');
  const body = document.body;

  if (hamburgerBtn && mobileMenu) {
    hamburgerBtn.addEventListener('click', function (e) {
      e.stopPropagation();
      const isOpen = mobileMenu.style.display === 'flex';

      if (isOpen) {
        // Cerrar menú
        mobileMenu.style.display = 'none';
        hamburgerBtn.classList.remove('menu-open');
        body.classList.remove('menu-open');
      } else {
        // Abrir menú
        mobileMenu.style.display = 'flex';
        hamburgerBtn.classList.add('menu-open');
        body.classList.add('menu-open');
      }
    });

    // Cerrar menú al hacer clic en un enlace
    mobileMenu.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', function () {
        mobileMenu.style.display = 'none';
        hamburgerBtn.classList.remove('menu-open');
        body.classList.remove('menu-open');
      });
    });

    // Cerrar menú al hacer clic fuera
    document.addEventListener('click', function (event) {
      if (!hamburgerBtn.contains(event.target) && !mobileMenu.contains(event.target)) {
        mobileMenu.style.display = 'none';
        hamburgerBtn.classList.remove('menu-open');
        body.classList.remove('menu-open');
      }
    });

    // Cerrar menú con tecla Escape
    document.addEventListener('keydown', function (event) {
      if (event.key === 'Escape' && mobileMenu.style.display === 'flex') {
        mobileMenu.style.display = 'none';
        hamburgerBtn.classList.remove('menu-open');
        body.classList.remove('menu-open');
      }
    });
  }
});