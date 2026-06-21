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
  var sortSelect = document.getElementById("popular-sort");

  var modal = document.getElementById("playlist-modal");
  var openModalBtn = document.getElementById("create-playlist-btn");
  var closeModalX = document.getElementById("modal-close-x");
  var cancelModalBtn = document.getElementById("modal-cancel-btn");
  var submitModalBtn = document.getElementById("modal-submit-btn");
  var copyModalBtn = document.getElementById("modal-copy-btn");
  
  var trackCountInput = document.getElementById("playlist-track-count");
  var clientIdInput = document.getElementById("spotify-client-id");
  var authSection = document.getElementById("spotify-auth-section");
  var statusContainer = document.getElementById("playlist-status-container");
  var uriHint = document.getElementById("uri-hint");

  if (!searchInput || !resultsList) return;

  var searchIndex = null;
  var minScore = 0;
  var currentSort = sortSelect ? sortSelect.value : "popularity";

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
        searchIndex = data;
      })
      .catch(function () {
        searchIndex = [];
      });
  }

  function renderCriticScore(score) {
    var container = document.createElement("span");
    container.className = "popularity-score";
    container.setAttribute("aria-label", "Crítica: " + score.toFixed(1) + " de 10");
    container.setAttribute("title", "Crítica: " + score.toFixed(1) + "/10");

    var num = document.createElement("span");
    num.className = "pop-score-num";
    num.textContent = score.toFixed(1);

    var sep = document.createElement("span");
    sep.className = "pop-score-sep";
    sep.textContent = "/";

    var max = document.createElement("span");
    max.className = "pop-score-max";
    max.textContent = "10";

    var bullets = document.createElement("span");
    bullets.className = "pop-score-bullets";
    bullets.setAttribute("aria-hidden", "true");

    var roundedScore = Math.round(score);
    for (var i = 1; i <= 10; i++) {
      var bullet = document.createElement("span");
      bullet.className = "bullet " + (i <= roundedScore ? "bullet--filled" : "bullet--empty");
      bullet.textContent = "\u25CF";
      bullets.appendChild(bullet);
    }

    container.appendChild(num);
    container.appendChild(sep);
    container.appendChild(max);
    container.appendChild(bullets);

    return container;
  }

  function filterTracks() {
    if (!searchIndex) return [];

    var query = normalizeQuery(searchInput.value.trim());

    var filtered = searchIndex.filter(function (item) {
      var scoreVal = (currentSort === "critic") ? (item.critic_score || 0) : (item.popularity || 0);
      if (scoreVal < minScore) return false;

      if (!query) return true;

      var haystack = normalizeQuery(
        [item.title, item.album_title, item.summary || ""].join(" ")
      );
      return haystack.indexOf(query) !== -1;
    });

    return filtered.sort(function (a, b) {
      if (currentSort === "critic") {
        var scoreDiff = (b.critic_score || 0) - (a.critic_score || 0);
        if (scoreDiff !== 0) return scoreDiff;
      } else {
        var popDiff = (b.popularity || 0) - (a.popularity || 0);
        if (popDiff !== 0) return popDiff;
      }
      return a.title.localeCompare(b.title, "pt-BR");
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

      if (item.spotify_url) {
        var spotLink = document.createElement("a");
        spotLink.href = item.spotify_url;
        spotLink.target = "_blank";
        spotLink.rel = "noopener noreferrer";
        spotLink.className = "spotify-link";
        spotLink.title = "Ouvir no Spotify";
        spotLink.innerHTML = '<svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><path d="M12 2C6.477 2 2 6.477 2 12s4.477 10 10 10 10-4.477 10-10S17.523 2 12 2zm4.586 14.424c-.18.295-.565.387-.86.207-2.377-1.454-5.37-1.783-8.892-.982-.336.076-.67-.135-.746-.472-.076-.336.135-.67.472-.746 3.848-.879 7.144-.504 9.814 1.13.295.18.387.565.207.863zm1.224-2.723c-.226.367-.707.487-1.074.26-2.72-1.672-6.87-2.157-10.08-1.182-.413.125-.847-.107-.972-.52-.125-.413.107-.847.52-.972 3.673-1.114 8.243-.574 11.35 1.34.367.226.487.707.26 1.074zm.106-2.833C14.384 8.627 8.563 8.435 5.21 9.452c-.512.155-1.05-.135-1.206-.647-.156-.512.135-1.05.647-1.206 3.86-1.172 10.28-.95 14.34 1.46.46.273.61.87.337 1.33-.273.46-.87.61-1.33.337z"/></svg>';
        li.appendChild(spotLink);
      }

      if (currentSort === "critic") {
        li.appendChild(renderCriticScore(item.critic_score || 0));
      } else {
        li.appendChild(renderScore(item.popularity || 0));
      }

      resultsList.appendChild(li);
    });
  }

  /* Modal state and handlers */
  function showStatus(message, type) {
    statusContainer.innerHTML = message;
    statusContainer.style.display = "block";
    statusContainer.className = "modal-status modal-status--" + type;
  }

  function showModal() {
    modal.classList.add("active");
    var currentMatches = filterTracks();
    trackCountInput.value = Math.min(20, currentMatches.length);
    trackCountInput.max = currentMatches.length;
    
    statusContainer.innerHTML = "";
    statusContainer.className = "modal-status";
    statusContainer.style.display = "none";
    
    var savedClientId = localStorage.getItem("spotify_client_id") || "";
    clientIdInput.value = savedClientId;
    
    authSection.style.display = "";
    submitModalBtn.style.display = "";
    copyModalBtn.style.display = "";
    trackCountInput.disabled = false;
  }

  function hideModal() {
    modal.classList.remove("active");
  }

  if (uriHint) {
    uriHint.textContent = window.location.origin + window.location.pathname;
  }

  if (openModalBtn && modal) {
    openModalBtn.addEventListener("click", showModal);
    closeModalX.addEventListener("click", hideModal);
    cancelModalBtn.addEventListener("click", hideModal);
    modal.addEventListener("click", function (e) {
      if (e.target === modal) hideModal();
    });
  }

  if (copyModalBtn) {
    copyModalBtn.addEventListener("click", function () {
      var currentMatches = filterTracks();
      var count = parseInt(trackCountInput.value, 10) || 20;
      count = Math.max(1, Math.min(count, currentMatches.length));
      
      var textList = currentMatches.slice(0, count).map(function (item) {
        return "Angra - " + item.title + " (" + item.album_title + ")";
      }).join("\n");
      
      navigator.clipboard.writeText(textList).then(function () {
        showStatus("Lista de " + count + " músicas copiada para a área de transferência!", "success");
      }).catch(function () {
        showStatus("Erro ao copiar músicas.", "error");
      });
    });
  }

  if (submitModalBtn) {
    submitModalBtn.addEventListener("click", function () {
      var clientId = clientIdInput.value.trim();
      if (!clientId) {
        showStatus("Por favor, insira o seu Spotify Client ID.", "error");
        return;
      }
      
      localStorage.setItem("spotify_client_id", clientId);
      
      var currentMatches = filterTracks();
      var count = parseInt(trackCountInput.value, 10) || 20;
      count = Math.max(1, Math.min(count, currentMatches.length));
      
      if (currentMatches.length === 0) {
        showStatus("Nenhuma música na lista para criar playlist.", "error");
        return;
      }
      
      var pendingState = {
        count: count,
        tracks: currentMatches.slice(0, count).map(function (item) {
          return { title: item.title, album: item.album_title };
        }),
        sort: currentSort,
        minScore: minScore,
        query: searchInput.value.trim()
      };
      localStorage.setItem("spotify_pending_playlist", JSON.stringify(pendingState));
      
      var redirectUri = window.location.origin + window.location.pathname;
      var scope = encodeURIComponent("playlist-modify-public playlist-modify-private");
      var url = "https://accounts.spotify.com/authorize" +
                "?client_id=" + encodeURIComponent(clientId) +
                "&response_type=token" +
                "&redirect_uri=" + encodeURIComponent(redirectUri) +
                "&scope=" + scope;
      
      showStatus('<span class="spinner"></span>Redirecionando para o Spotify...', "info");
      window.location.href = url;
    });
  }

  function createSpotifyPlaylist(token, pending) {
    var headers = {
      "Authorization": "Bearer " + token,
      "Content-Type": "application/json"
    };
    
    var userId = null;
    var playlistId = null;
    var trackUris = [];
    var searchPromises = [];
    
    showStatus('<span class="spinner"></span>Obtendo perfil do usuário...', "info");
    
    fetch("https://api.spotify.com/v1/me", { headers: headers })
      .then(function (res) {
        if (!res.ok) throw new Error("Falha ao obter perfil do usuário (token expirado ou inválido).");
        return res.json();
      })
      .then(function (user) {
        userId = user.id;
        showStatus('<span class="spinner"></span>Buscando músicas no Spotify...', "info");
        
        pending.tracks.forEach(function (track) {
          var query = "artist:Angra track:" + track.title;
          var url = "https://api.spotify.com/v1/search?q=" + encodeURIComponent(query) + "&type=track&limit=1";
          
          var p = fetch(url, { headers: headers })
            .then(function (res) {
              if (res.ok) return res.json();
              return null;
            })
            .then(function (searchRes) {
              if (searchRes && searchRes.tracks && searchRes.tracks.items && searchRes.tracks.items.length > 0) {
                trackUris.push(searchRes.tracks.items[0].uri);
              }
            });
          searchPromises.push(p);
        });
        
        return Promise.all(searchPromises);
      })
      .then(function () {
        if (trackUris.length === 0) {
          throw new Error("Nenhuma das músicas pôde ser encontrada no Spotify.");
        }
        
        showStatus('<span class="spinner"></span>Criando playlist no Spotify...', "info");
        
        var filterText = "";
        if (pending.minScore > 0) {
          filterText += " (Nota mín: " + pending.minScore + "+)";
        }
        if (pending.query) {
          filterText += ' (Busca: "' + pending.query + '")';
        }
        var sortName = pending.sort === "critic" ? "Críticos" : "Popularidade";
        var playlistName = "Angra - Top " + pending.count + " (" + sortName + ")";
        var description = "Playlist gerada pelo site Angra Lyrics. Ordenada por: " + sortName + "." + filterText;
        
        return fetch("https://api.spotify.com/v1/users/" + userId + "/playlists", {
          method: "POST",
          headers: headers,
          body: JSON.stringify({
            name: playlistName,
            description: description,
            public: true
          })
        });
      })
      .then(function (res) {
        if (!res.ok) throw new Error("Falha ao criar a playlist.");
        return res.json();
      })
      .then(function (playlist) {
        playlistId = playlist.id;
        showStatus('<span class="spinner"></span>Adicionando músicas à playlist...', "info");
        
        return fetch("https://api.spotify.com/v1/playlists/" + playlistId + "/tracks", {
          method: "POST",
          headers: headers,
          body: JSON.stringify({
            uris: trackUris
          })
        });
      })
      .then(function (res) {
        if (!res.ok) throw new Error("Falha ao adicionar músicas à playlist.");
        
        var playlistUrl = "https://open.spotify.com/playlist/" + playlistId;
        var msg = "<strong>Sucesso!</strong> Playlist criada com " + trackUris.length + " músicas.<br>" +
                  '<a href="' + playlistUrl + '" target="_blank" class="playlist-link">Clique aqui para abrir no Spotify</a>';
        showStatus(msg, "success");
        localStorage.removeItem("spotify_pending_playlist");
      })
      .catch(function (err) {
        showStatus("Erro: " + err.message, "error");
        localStorage.removeItem("spotify_pending_playlist");
      });
  }

  function checkOAuthCallback() {
    var hash = window.location.hash;
    if (!hash) return;
    
    var params = {};
    hash.substring(1).split("&").forEach(function (part) {
      var keyVal = part.split("=");
      if (keyVal.length === 2) {
        params[keyVal[0]] = decodeURIComponent(keyVal[1]);
      }
    });
    
    if (!params.access_token) return;
    
    var pendingStr = localStorage.getItem("spotify_pending_playlist");
    if (!pendingStr) return;
    
    var pending = JSON.parse(pendingStr);
    
    modal.classList.add("active");
    authSection.style.display = "none";
    submitModalBtn.style.display = "none";
    copyModalBtn.style.display = "none";
    trackCountInput.value = pending.count;
    trackCountInput.disabled = true;
    
    showStatus('<span class="spinner"></span>Autenticado! Conectando ao Spotify...', "info");
    
    var token = params.access_token;
    
    if (window.history && window.history.replaceState) {
      window.history.replaceState("", document.title, window.location.pathname + window.location.search);
    } else {
      window.location.hash = "";
    }
    
    createSpotifyPlaylist(token, pending);
  }

  searchInput.addEventListener("input", renderResults);

  if (sortSelect) {
    sortSelect.addEventListener("change", function () {
      currentSort = sortSelect.value;
      renderResults();
    });
  }

  filterButtons.forEach(function (btn) {
    btn.addEventListener("click", function () {
      minScore = parseInt(btn.getAttribute("data-min-score"), 10) || 0;

      filterButtons.forEach(function (b) {
        b.classList.toggle("active", b === btn);
      });

      renderResults();
    });
  });

  loadIndex().then(function () {
    renderResults();
    checkOAuthCallback();
  });
})();
