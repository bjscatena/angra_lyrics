/**
 * Popular tracks page — search and filter by popularity
 */
(function () {
  "use strict";

  var assetPrefix = document.body.getAttribute("data-asset-prefix") || "";
  var assetVersion = document.body.getAttribute("data-asset-version") || "";
  var searchInput = document.getElementById("popular-search");
  var resultsList = document.getElementById("popular-results");
  var countEl = document.getElementById("popular-count");
  var emptyEl = document.getElementById("popular-empty");
  var filterButtons = document.querySelectorAll(".filter-btn");

  if (!searchInput || !resultsList) return;

  var searchIndex = null;
  var minScore = 0;

  function normalizeQuery(text) {
    return text
      .toLowerCase()
      .normalize("NFD")
      .replace(/[\u0300-\u036f]/g, "");
  }

  function renderScore(score) {
    if (window.AngraPopularity && window.AngraPopularity.renderScore) {
      return window.AngraPopularity.renderScore(score);
    }
    var fallback = document.createElement("span");
    fallback.className = "popularity-score";
    fallback.textContent = score + "/10";
    return fallback;
  }

  function indexUrl() {
    var url = assetPrefix + "search-index.json";
    return assetVersion ? url + "?v=" + encodeURIComponent(assetVersion) : url;
  }

  function loadIndex() {
    return fetch(indexUrl())
      .then(function (res) {
        if (!res.ok) throw new Error("search-index unavailable");
        return res.json();
      })
      .then(function (data) {
        searchIndex = data.sort(function (a, b) {
          var popDiff = (b.popularity || 0) - (a.popularity || 0);
          if (popDiff !== 0) return popDiff;
          return a.title.localeCompare(b.title, "pt-BR");
        });
      })
      .catch(function () {
        searchIndex = [];
      });
  }

  function filterTracks() {
    if (!searchIndex) return [];

    var query = normalizeQuery(searchInput.value.trim());

    return searchIndex.filter(function (item) {
      var popularity = item.popularity || 0;
      if (popularity < minScore) return false;

      if (!query) return true;

      var haystack = normalizeQuery(
        [item.title, item.album_title, item.summary || ""].join(" ")
      );
      return haystack.indexOf(query) !== -1;
    });
  }

  function renderResults() {
    var matches = filterTracks();

    resultsList.innerHTML = "";

    if (countEl) {
      countEl.textContent =
        matches.length === 1
          ? "1 faixa encontrada"
          : matches.length + " faixas encontradas";
    }

    if (!matches.length) {
      if (emptyEl) emptyEl.hidden = false;
      return;
    }

    if (emptyEl) emptyEl.hidden = true;

    matches.forEach(function (item) {
      var li = document.createElement("li");
      li.className = "popular-result-item";

      var link = document.createElement("a");
      link.href = assetPrefix + item.url;
      link.className = "popular-result-link";

      var title = document.createElement("span");
      title.className = "popular-result-title";
      title.textContent = item.title;

      var album = document.createElement("span");
      album.className = "popular-result-album";
      album.textContent = item.album_title;

      link.appendChild(title);
      link.appendChild(album);
      li.appendChild(link);
      li.appendChild(renderScore(item.popularity || 0));

      resultsList.appendChild(li);
    });
  }

  searchInput.addEventListener("input", renderResults);

  filterButtons.forEach(function (btn) {
    btn.addEventListener("click", function () {
      minScore = parseInt(btn.getAttribute("data-min-score"), 10) || 0;

      filterButtons.forEach(function (b) {
        b.classList.toggle("active", b === btn);
      });

      renderResults();
    });
  });

  loadIndex().then(renderResults);
})();
