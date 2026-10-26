// About page: draws the chalk journey line, runs the map pins and the project banner.
(function () {
  var NS = "http://www.w3.org/2000/svg";

  // ---- Chalk line ----
  // Wide screens: down one side through each bubble, along the empty gap between stops,
  // then down the other side, with rounded corners. It never crosses text.
  // Below 900px: one straight line down the left through every bubble.
  var chalk = document.querySelector(".chalk");

  function drawChalk() {
    if (!chalk) return;
    var bubbles = Array.prototype.slice.call(chalk.querySelectorAll(".cstop__bubble"));
    if (!bubbles.length) return;
    var box = chalk.getBoundingClientRect();
    var wide = window.matchMedia("(min-width: 56.25rem)").matches;
    var r = 40;
    var pt = function (el) {
      var b = el.getBoundingClientRect();
      return { x: b.left + b.width / 2 - box.left, top: b.top - box.top, mid: b.top + b.height / 2 - box.top, bottom: b.bottom - box.top };
    };
    var first = pt(bubbles[0]);
    var firstChapter = chalk.querySelector(".chalk__chapter--first");
    var startY = firstChapter ? pt(firstChapter).mid : first.top;
    var today = chalk.querySelector(".chalk__star");
    var d = "M" + first.x + " " + startY;

    if (!wide) {
      var end = today ? pt(today).top : pt(bubbles[bubbles.length - 1]).mid;
      d += " L" + first.x + " " + end;
    } else {
      var stops = Array.prototype.slice.call(chalk.querySelectorAll(".cstop"));
      stops.forEach(function (stop, i) {
        var a = pt(stop.querySelector(".cstop__bubble"));
        d += " L" + a.x + " " + a.mid;
        // the gap below this stop: where the line turns
        var stopBottom = stop.getBoundingClientRect().bottom - box.top;
        var next = stops[i + 1];
        var nextTop, nx;
        if (next) {
          var nb = pt(next.querySelector(".cstop__bubble"));
          nextTop = next.getBoundingClientRect().top - box.top;
          nx = nb.x;
        } else if (today) {
          var t = pt(today);
          nextTop = t.top;
          nx = t.x;
        } else {
          return;
        }
        var gy = (stopBottom + nextTop) / 2;
        var mid = stop.parentNode !== (next && next.parentNode) && next ? chalk.querySelector(".chalk__chapter:not(.chalk__chapter--first)") : null;
        if (mid) gy = pt(mid).mid;
        var dir = nx > a.x ? 1 : -1;
        d += " L" + a.x + " " + (gy - r) + " Q" + a.x + " " + gy + " " + (a.x + dir * r) + " " + gy;
        d += " L" + (nx - dir * r) + " " + gy + " Q" + nx + " " + gy + " " + nx + " " + (gy + r);
        if (next) {
          d += " L" + nx + " " + pt(next.querySelector(".cstop__bubble")).mid;
        } else {
          d += " L" + nx + " " + pt(today).top;
        }
      });
    }

    var svg = chalk.querySelector(".chalk__line");
    if (!svg) {
      svg = document.createElementNS(NS, "svg");
      svg.setAttribute("class", "chalk__line");
      svg.setAttribute("aria-hidden", "true");
      svg.setAttribute("focusable", "false");
      svg.innerHTML =
        '<defs><filter id="chalk" filterUnits="userSpaceOnUse" x="-5%" y="-1%" width="110%" height="102%">' +
        '<feTurbulence type="fractalNoise" baseFrequency="1.1" numOctaves="3" seed="7" result="noise"/>' +
        '<feDisplacementMap in="SourceGraphic" in2="noise" scale="4" xChannelSelector="R" yChannelSelector="G"/>' +
        '</filter></defs><g filter="url(#chalk)"><path class="chalk__stroke"/><path class="chalk__texture"/></g>';
      chalk.insertBefore(svg, chalk.firstChild);
      chalk.classList.add("chalk--drawn");
    }
    svg.setAttribute("width", box.width);
    svg.setAttribute("height", box.height);
    svg.querySelectorAll("path").forEach(function (p) { p.setAttribute("d", d); });
  }

  drawChalk();
  window.addEventListener("resize", drawChalk);
  window.addEventListener("load", drawChalk);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(drawChalk);

  // ---- Map pins: a bubble opens on hover, keyboard focus or tap; Esc or tapping elsewhere closes ----
  var map = document.querySelector(".rmap__map");
  if (map) {
    document.querySelector(".rmap").classList.add("rmap--enhanced");
    var pins = Array.prototype.slice.call(map.querySelectorAll(".pin"));
    var open = null;
    var show = function (pin) {
      if (open && open !== pin) hide(open);
      pin.querySelector(".pin__bubble").hidden = false;
      pin.querySelector(".pin__btn").setAttribute("aria-expanded", "true");
      pin.classList.add("pin--open");
      open = pin;
    };
    var hide = function (pin) {
      pin.querySelector(".pin__bubble").hidden = true;
      pin.querySelector(".pin__btn").setAttribute("aria-expanded", "false");
      pin.classList.remove("pin--open");
      if (open === pin) open = null;
    };
    pins.forEach(function (pin) {
      var btn = pin.querySelector(".pin__btn");
      btn.addEventListener("click", function () { open === pin ? hide(pin) : show(pin); });
      btn.addEventListener("focus", function () { show(pin); });
      pin.addEventListener("mouseenter", function () { show(pin); });
      pin.addEventListener("mouseleave", function () { if (!pin.contains(document.activeElement)) hide(pin); });
      pin.addEventListener("focusout", function (e) { if (!pin.contains(e.relatedTarget)) hide(pin); });
    });
    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape" && open) { var b = open.querySelector(".pin__btn"); hide(open); b.focus(); }
    });
    document.addEventListener("click", function (e) { if (open && !open.contains(e.target)) hide(open); });
  }

  // ---- Project banner: moves slowly; pause button; pauses on hover or focus; still with reduced motion ----
  var ticker = document.querySelector(".ticker");
  if (!ticker) return;
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) return;
  var toggle = ticker.querySelector(".ticker__toggle");
  ticker.classList.add("ticker--moving");
  toggle.hidden = false;
  toggle.addEventListener("click", function () {
    // Paused: the cards settle into a still grid, so none are cut off at the edges.
    var paused = ticker.classList.toggle("ticker--paused");
    toggle.setAttribute("aria-pressed", String(paused));
  });
})();
