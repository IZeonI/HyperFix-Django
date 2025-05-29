document.addEventListener("DOMContentLoaded", () => {
  fetch(CARRUSEL_URL)
    .then(response => response.text())
    .then(html => {
      document.getElementById("carrusel-wrapper").innerHTML = html;

      const container = document.querySelector(".carousel-container");
      if (!container) return;

      const track = container.querySelector(".carousel-track");
      const prevBtn = document.querySelector(".carousel-btn.prev");
      const nextBtn = document.querySelector(".carousel-btn.next");

      let currentIndex = 0;
      const cards = track.children;
      const cardWidth = cards[0].offsetWidth + 20;

      function updateButtons() {
        prevBtn.disabled = currentIndex === 0;
        nextBtn.disabled = currentIndex >= cards.length - Math.floor(container.offsetWidth / cardWidth);
      }

      function moveCarousel() {
        track.style.transform = `translateX(-${currentIndex * cardWidth}px)`;
        updateButtons();
      }

      prevBtn.addEventListener("click", () => {
        if (currentIndex > 0) {
          currentIndex--;
          moveCarousel();
        }
      });

      nextBtn.addEventListener("click", () => {
        if (currentIndex < cards.length - Math.floor(container.offsetWidth / cardWidth)) {
          currentIndex++;
          moveCarousel();
        }
      });

      updateButtons();
    });
});
