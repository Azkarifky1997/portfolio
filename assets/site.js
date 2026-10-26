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

// Copy email (home page "Let's talk"). Without the script, the email link shows instead.
(function () {
  var btn = document.querySelector(".talk__copy");
  if (!btn || !navigator.clipboard) return;
  var status = document.querySelector("[data-copy-status]");
  var label = btn.querySelector(".talk__copy-label");
  btn.hidden = false;
  var mail = document.querySelector(".talk__mail");
  if (mail) mail.hidden = true;
  btn.addEventListener("click", function () {
    navigator.clipboard.writeText(btn.dataset.email).then(function () {
      status.textContent = "Email copied";
      label.textContent = "Copied";
      setTimeout(function () { label.textContent = "Copy email"; status.textContent = ""; }, 3000);
    });
  });
})();

// Testimonials: previous and next buttons (only when there is more than one quote).
(function () {
  var box = document.querySelector(".quotes");
  if (!box) return;
  var slides = Array.prototype.slice.call(box.querySelectorAll(".quote"));
  var i = 0;
  box.querySelectorAll(".quotes__btn").forEach(function (b) {
    b.addEventListener("click", function () {
      slides[i].hidden = true;
      i = (i + Number(b.dataset.dir) + slides.length) % slides.length;
      slides[i].hidden = false;
    });
  });
})();
