// Function to animate card content
function animateCardContent(card, xOffset, yOffset, scale) {
    gsap.fromTo(
      card.querySelector(".card-content"),
      { x: xOffset, y: yOffset, scale: scale, opacity: 0 },
      {
        x: 0,
        y: 0,
        scale: 1,
        opacity: 1,
        duration: 0.6,
        ease: "power3.out",
      }
    );
  }
  
  // Initial setup for card animations
  function setupCardAnimations() {
    const cards = document.querySelectorAll(".card");
  
    cards.forEach((card, index) => {
      card.addEventListener("mouseenter", () => {
        const xOffset = index % 2 === 0 ? -40 : 40;
        animateCardContent(card, xOffset, -20, 0.95);
      });
  
      card.addEventListener("mouseleave", () => {
        const xOffset = index % 2 === 0 ? -40 : 40;
        animateCardContent(card, xOffset, -20, 0.95);
      });
    });
  }
  
  // Initialize pagination progress animation
  function initializePaginationProgress() {
    const progressForeground = document.querySelector(".progress-sub-foreground");
  
    gsap.to(progressForeground, {
      scaleX: 1,
      duration: 3,
      ease: "power1.out",
    });
  }
  
  // Initialize script after DOM loaded
  document.addEventListener("DOMContentLoaded", () => {
    setupCardAnimations();
    initializePaginationProgress();
  });
  

// Calculadora
  document.getElementById('energia_tipo').addEventListener('change', function() {
    const kwhInput = document.getElementById('kwh_input');
    const contaInput = document.getElementById('conta_input');

    if (this.value == 'kwh') {
        kwhInput.style.display = 'block';
        contaInput.style.display = 'none';
    } else if (this.value == 'conta') {
        kwhInput.style.display = 'none';
        contaInput.style.display = 'block';
    } else {
        kwhInput.style.display = 'none';
        contaInput.style.display = 'none';
    }
});