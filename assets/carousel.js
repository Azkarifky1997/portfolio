// Case study carousel on the home page.
// Without this script the cards still scroll sideways (swipe, trackpad or
// Shift + mouse wheel). The script adds the Previous and Next buttons.
(function () {
  var track = document.getElementById("cards");
  var buttons = document.querySelector(".carousel__buttons");
  if (!track || !buttons) return;

  var prev = buttons.querySelector('[data-dir="-1"]');
  var next = buttons.querySelector('[data-dir="1"]');
  var reduceMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;

  function step() {
    var card = track.querySelector(".card");
    var gap = parseFloat(getComputedStyle(track).columnGap) || 0;
    return card ? card.getBoundingClientRect().width + gap : track.clientWidth;
  }

  function update() {
    var max = track.scrollWidth - track.clientWidth - 2;
    prev.disabled = track.scrollLeft <= 2;
    next.disabled = track.scrollLeft >= max;
    // Hide the buttons when every card already fits on screen.
    buttons.hidden = max <= 0;
  }

  buttons.addEventListener("click", function (event) {
    var button = event.target.closest("button");
    if (!button) return;
    track.scrollBy({
      left: step() * Number(button.dataset.dir),
      behavior: reduceMotion ? "auto" : "smooth",
    });
  });

  track.addEventListener("scroll", function () {
    window.requestAnimationFrame(update);
  }, { passive: true });
  window.addEventListener("resize", update);
  update();
})();
