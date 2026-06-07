/**
 * Angra Lyrics — client-side helpers
 */
(function () {
  "use strict";

  var assetPrefix = document.body.getAttribute("data-asset-prefix") || "";
  var assetVersion = document.body.getAttribute("data-asset-version") || "";

  /* Lyrics display toggle (Original / Tradução / Ambos) */
  var toggleContainer = document.querySelector(".lyrics-toggle");
  var lyricsSection = document.querySelector(".lyrics-section");

  if (toggleContainer && lyricsSection) {
    var buttons = toggleContainer.querySelectorAll(".toggle-btn");

    buttons.forEach(function (btn) {
      btn.addEventListener("click", function () {
        var mode = btn.getAttribute("data-mode");
        if (!mode) return;

        lyricsSection.setAttribute("data-lyrics-mode", mode);

        buttons.forEach(function (b) {
          var isActive = b === btn;
          b.classList.toggle("active", isActive);
          b.setAttribute("aria-selected", isActive ? "true" : "false");
        });
      });
    });
  }

  /* Client-side search (home page) */
  var searchInput = document.getElementById("site-search");
  var searchResults = document.getElementById("search-results");

  if (searchInput && searchResults) {
    var searchIndex = null;
    var searchReady = false;
    var activeIndex = -1;

    function normalizeQuery(text) {
      return text
        .toLowerCase()
        .normalize("NFD")
        .replace(/[\u0300-\u036f]/g, "");
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
          searchIndex = data;
          searchReady = true;
        })
        .catch(function () {
          searchIndex = [];
          searchReady = true;
        });
    }

    function filterTracks(query) {
      if (!searchIndex || !query) return [];

      var normalized = normalizeQuery(query);
      return searchIndex
        .filter(function (item) {
          var haystack = normalizeQuery(
            [item.title, item.album_title, item.summary || ""].join(" ")
          );
          return haystack.indexOf(normalized) !== -1;
        })
        .sort(function (a, b) {
          return (b.popularity || 0) - (a.popularity || 0);
        })
        .slice(0, 12);
    }

    function clearResults() {
      searchResults.innerHTML = "";
      searchResults.hidden = true;
      searchInput.setAttribute("aria-expanded", "false");
      activeIndex = -1;
    }

    function renderScore(score) {
      if (window.AngraPopularity && window.AngraPopularity.renderScore) {
        var node = window.AngraPopularity.renderScore(score);
        node.classList.add("search-result-score");
        return node;
      }
      var fallback = document.createElement("span");
      fallback.className = "popularity-score search-result-score";
      fallback.textContent = score + "/10";
      return fallback;
    }

    function renderResults(matches) {
      searchResults.innerHTML = "";

      if (!matches.length) {
        var empty = document.createElement("li");
        empty.className = "search-results-empty";
        empty.textContent = "Nenhuma faixa encontrada.";
        empty.setAttribute("role", "presentation");
        searchResults.appendChild(empty);
        searchResults.hidden = false;
        searchInput.setAttribute("aria-expanded", "true");
        return;
      }

      matches.forEach(function (item, index) {
        var li = document.createElement("li");
        li.setAttribute("role", "option");
        li.id = "search-option-" + index;

        var link = document.createElement("a");
        link.href = assetPrefix + item.url;
        link.className = "search-result-link";
        link.style.flexDirection = "row";
        link.style.alignItems = "center";
        link.style.gap = "0.75rem";

        var textWrap = document.createElement("span");
        textWrap.style.flex = "1";
        textWrap.style.minWidth = "0";
        textWrap.style.display = "flex";
        textWrap.style.flexDirection = "column";
        textWrap.style.gap = "0.15rem";

        var title = document.createElement("span");
        title.className = "search-result-title";
        title.textContent = item.title;

        var album = document.createElement("span");
        album.className = "search-result-album";
        album.textContent = item.album_title;

        textWrap.appendChild(title);
        textWrap.appendChild(album);
        link.appendChild(textWrap);
        link.appendChild(renderScore(item.popularity || 0));
        li.appendChild(link);
        searchResults.appendChild(li);
      });

      searchResults.hidden = false;
      searchInput.setAttribute("aria-expanded", "true");
      activeIndex = -1;
    }

    function runSearch() {
      var query = searchInput.value.trim();
      if (!query) {
        clearResults();
        return;
      }

      if (!searchReady) {
        loadIndex().then(function () {
          renderResults(filterTracks(query));
        });
        return;
      }

      renderResults(filterTracks(query));
    }

    searchInput.addEventListener("input", runSearch);

    searchInput.addEventListener("keydown", function (e) {
      var options = searchResults.querySelectorAll('[role="option"] a');

      if (e.key === "Escape") {
        clearResults();
        searchInput.blur();
        return;
      }

      if (e.key === "ArrowDown") {
        e.preventDefault();
        if (options.length) {
          activeIndex = Math.min(activeIndex + 1, options.length - 1);
          options[activeIndex].focus();
        }
        return;
      }

      if (e.key === "ArrowUp") {
        e.preventDefault();
        if (activeIndex <= 0) {
          activeIndex = -1;
          searchInput.focus();
        } else {
          activeIndex -= 1;
          options[activeIndex].focus();
        }
      }
    });

    document.addEventListener("click", function (e) {
      if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
        clearResults();
      }
    });

    loadIndex();
  }

  document.querySelectorAll('a[href^="#"]').forEach(function (link) {
    link.addEventListener("click", function (e) {
      var target = document.querySelector(link.getAttribute("href"));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: "smooth" });
      }
    });
  });
})();
