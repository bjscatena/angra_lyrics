/**
 * Popularity score UI (0–10 with bullets)
 */
(function (global) {
  "use strict";

  function renderScore(score) {
    var container = document.createElement("span");
    container.className = "popularity-score";
    container.setAttribute("aria-label", "Popularidade: " + score + " de 10");
    container.setAttribute("title", "Popularidade: " + score + "/10");

    var num = document.createElement("span");
    num.className = "pop-score-num";
    num.textContent = String(score);

    var sep = document.createElement("span");
    sep.className = "pop-score-sep";
    sep.textContent = "/";

    var max = document.createElement("span");
    max.className = "pop-score-max";
    max.textContent = "10";

    var bullets = document.createElement("span");
    bullets.className = "pop-score-bullets";
    bullets.setAttribute("aria-hidden", "true");

    for (var i = 1; i <= 10; i++) {
      var bullet = document.createElement("span");
      bullet.className = "bullet " + (i <= score ? "bullet--filled" : "bullet--empty");
      bullet.textContent = "\u25CF";
      bullets.appendChild(bullet);
    }

    container.appendChild(num);
    container.appendChild(sep);
    container.appendChild(max);
    container.appendChild(bullets);

    return container;
  }

  global.AngraPopularity = {
    renderScore: renderScore,
  };
})(window);
