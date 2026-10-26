// Site-wide: the phone menu button. Without this script the menu is simply always shown.
(function () {
  var toggle = document.querySelector(".nav-toggle");
  var nav = document.getElementById("site-nav");
  if (!toggle || !nav) return;
  var small = window.matchMedia("(max-width: 47.99rem)");
  function setup() {
    if (small.matches) {
      toggle.hidden = false;
      nav.hidden = toggle.getAttribute("aria-expanded") !== "true";
    } else {
      toggle.hidden = true;
      nav.hidden = false;
    }
  }
  toggle.addEventListener("click", function () {
    var open = toggle.getAttribute("aria-expanded") !== "true";
    toggle.setAttribute("aria-expanded", String(open));
    nav.hidden = !open;
    if (open) nav.querySelector("a").focus();
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && toggle.getAttribute("aria-expanded") === "true") {
      toggle.setAttribute("aria-expanded", "false");
      nav.hidden = true;
      toggle.focus();
    }
  });
  (small.addEventListener ? small.addEventListener("change", setup) : small.addListener(setup));
  setup();
})();
