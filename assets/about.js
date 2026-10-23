// About page: draws the winding journey line and runs the project banner.
(function () {
  // ---- Journey line: one smooth curve through every circle ----
  var journey = document.querySelector(".journey");
  var NS = "http://www.w3.org/2000/svg";

  // A cubic curve that leaves and arrives travelling straight down, so every join is smooth.
  function down(x1, y1, x2, y2, pull) {
    var k = (y2 - y1) * (pull || 0.5);
    return " C" + x1 + " " + (y1 + k) + " " + x2 + " " + (y2 - k) + " " + x2 + " " + y2;
  }

  function drawJourney() {
    if (!journey) return;
    var stops = journey.querySelectorAll(".stop");
    if (!stops.length) return;
    var box = journey.getBoundingClientRect();
    var wide = window.matchMedia("(min-width: 52rem)").matches;
    var bow = wide ? 36 : 0; // swing beside each stop on wide screens; straight on phones
    var marker = function (stop) { return stop.querySelector(".stop__circle, .stop__dot"); };
    var d = "";
    stops.forEach(function (stop, i) {
      var m = marker(stop);
      var c = m.getBoundingClientRect();
      var x = c.left + c.width / 2 - box.left;
      var top = c.top - box.top;
      if (m.classList.contains("stop__dot")) {
        // The star at the end: the line stops at its top point.
        if (i === 0) d += "M" + x + " " + top;
        return;
      }
      var bottom = c.bottom - box.top;
      var pad = parseFloat(getComputedStyle(stop).paddingBottom) || 0;
      var end = stop.getBoundingClientRect().bottom - box.top - pad;
      var dir = stop.classList.contains("stop--right") && wide ? 1 : -1;
      // Through the circle (hidden behind it)
      d += (i === 0 ? "M" : " L") + x + " " + top + " L" + x + " " + bottom;
      if (i === stops.length - 1) return;
      // Swing gently out beside the text and back...
      var bx = x + dir * bow;
      var by = bottom + (end - bottom) * 0.5;
      d += down(x, bottom, bx, by) + down(bx, by, x, end);
      // ...then sweep across the gap to the next stop.
      var n = marker(stops[i + 1]).getBoundingClientRect();
      var ny = n.top - box.top + (stops[i + 1].classList.contains("stop--today") ? n.height * 0.18 : 0);
      d += down(x, end, n.left + n.width / 2 - box.left, ny, 0.6);
    });
    var svg = journey.querySelector(".journey__line");
    if (!svg) {
      svg = document.createElementNS(NS, "svg");
      svg.setAttribute("class", "journey__line");
      svg.setAttribute("aria-hidden", "true");
      svg.setAttribute("focusable", "false");
      // A rough, grainy "chalk" look: wobble the edges, then speckle the stroke.
      svg.innerHTML =
        '<defs><filter id="chalk" filterUnits="userSpaceOnUse" x="-5%" y="-1%" width="110%" height="102%">' +
        '<feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="3" seed="7" result="noise"/>' +
        '<feDisplacementMap in="SourceGraphic" in2="noise" scale="3.5" xChannelSelector="R" yChannelSelector="G" result="rough"/>' +
        '<feColorMatrix in="noise" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  2.6 0 0 0 -0.55" result="grain"/>' +
        '<feComposite in="rough" in2="grain" operator="in"/>' +
        '</filter></defs><path filter="url(#chalk)"/>';
      journey.insertBefore(svg, journey.firstChild);
      journey.classList.add("journey--curved");
    }
    svg.setAttribute("width", box.width);
    svg.setAttribute("height", box.height);
    svg.querySelector("path").setAttribute("d", d);
  }

  drawJourney();
  window.addEventListener("resize", drawJourney);
  window.addEventListener("load", drawJourney);
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(drawJourney);

  // ---- Project banner: moves slowly; pause button, and pauses on hover or focus ----
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
