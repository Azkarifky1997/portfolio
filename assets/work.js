// Work page filters. Without this script every project shows and the filters stay hidden.
(function () {
  var filters = document.querySelector(".filters");
  if (!filters) return;
  var projects = Array.prototype.slice.call(document.querySelectorAll(".project"));
  var buttons = Array.prototype.slice.call(filters.querySelectorAll(".filter"));
  var count = filters.querySelector(".filters__count");
  var clear = filters.querySelector(".filters__clear");
  var empty = document.querySelector(".projects__empty");
  filters.hidden = false;

  function update() {
    // OR within a group, AND across groups.
    var chosen = {};
    buttons.forEach(function (b) {
      if (b.getAttribute("aria-pressed") === "true") {
        (chosen[b.dataset.group] = chosen[b.dataset.group] || []).push(b.dataset.value);
      }
    });
    var shown = 0;
    projects.forEach(function (p) {
      var match = Object.keys(chosen).every(function (group) {
        var values = (p.dataset[group] || "").split(" ");
        return chosen[group].some(function (v) { return values.indexOf(v) !== -1; });
      });
      p.hidden = !match;
      if (match) shown++;
    });
    count.textContent = "Showing " + shown + " of " + projects.length + " projects";
    empty.hidden = shown !== 0;
    clear.disabled = Object.keys(chosen).length === 0;
  }

  buttons.forEach(function (b) {
    b.addEventListener("click", function () {
      b.setAttribute("aria-pressed", b.getAttribute("aria-pressed") === "true" ? "false" : "true");
      update();
    });
  });
  clear.addEventListener("click", function () {
    buttons.forEach(function (b) { b.setAttribute("aria-pressed", "false"); });
    update();
  });
  update();
})();
