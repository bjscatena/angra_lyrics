"""Parse setlist.fm stats and compute popularity scores for project tracks."""
from __future__ import annotations

import html
import re
import unicodedata
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
STATS_URL = "https://www.setlist.fm/stats/angra-43d6ff27.html"
BUILD_CONFIG = ROOT / "scripts" / "build_config.yaml"
POPULARITY_PATH = ROOT / "scripts" / "popularity.yaml"

# Spotify streams (millions) for studio-album tracks — Music Metrics Vault, Jun 2026
SPOTIFY_M = {
    "Wuthering Heights": 24.3,
    "Carry On": 23.7,
    "Rebirth": 20.5,
    "Nova Era": 17.5,
    "Heroes of Sand": 11.4,
    "Spread Your Fire": 9.6,
    "The Temple of Hate": 7.7,
    "Nothing to Say": 7.0,
    "Waiting Silence": 5.0,
    "Acid Rain": 4.5,  # estimated from typical ranking
    "Angels Cry": 4.0,
    "Time": 3.8,
    "Angels and Demons": 3.5,
    "Wishing Well": 3.2,
    "Metal Icarus": 3.0,
    "Fireworks": 2.8,
    "Lisbon": 2.5,
    "Carolina IV": 2.3,
    "Late Redemption": 2.0,
    "Millennium Sun": 1.8,
    "Travelers of Time": 1.5,
    "Make Believe": 1.2,
    "Deep Blue": 1.0,
}

# Manual title aliases (project title -> setlist.fm title)
ALIASES = {
    "Z.I.T.O.": "Z.I.T.O.",
    "Salvation: Suicide": "Salvation: Suicide",
    "Deus Le Volt!": "Deus le volt!",
    "Viderunt te Aquae": "Viderunt te Aquae",
    "Tide of Changes – Part I": "Tide of Changes - Part I",
    "Tide of Changes – Part II": "Tide of Changes - Part II",
    "ØMNI – Silence Inside": "ØMNI - Silence Inside",
    "ØMNI – Infinite Nothing": "ØMNI - Infinite Nothing",
    "Vida Seca": "Vida seca",
}


def normalize(title: str) -> str:
    t = html.unescape(title)
    t = unicodedata.normalize("NFKD", t)
    t = "".join(c for c in t if not unicodedata.combining(c))
    t = t.replace("–", "-").replace("—", "-").replace("'", "'")
    t = t.lower()
    t = re.sub(r"[^\w\s]", " ", t)
    t = re.sub(r"\s+", " ", t).strip()
    return t


def fetch_setlist_stats() -> str:
    req = urllib.request.Request(STATS_URL, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return resp.read().decode("utf-8", errors="replace")


def parse_setlist(page_html: str) -> dict[str, int]:
    pattern = re.compile(
        r'class="songName"[^>]*data-stats-sort="([^"]+)"'
        r'.*?<span>([^<]+)</span></a>.*?'
        r'class="songCount" data-stats-sort="(\d+)"',
        re.DOTALL,
    )
    result: dict[str, int] = {}
    for sort_name, link_title, count in pattern.findall(page_html):
        title = html.unescape(sort_name or link_title).strip()
        result[title] = int(count)
    return result


def load_project_tracks() -> list[tuple[str, str, bool]]:
    config = yaml.safe_load(BUILD_CONFIG.read_text(encoding="utf-8"))
    tracks: list[tuple[str, str, bool]] = []
    for album in config["albums"]:
        aid = album["id"]
        album_data = yaml.safe_load((ROOT / "albums" / aid / "album.yaml").read_text(encoding="utf-8"))
        for item in album_data.get("tracklist", []):
            track_data = yaml.safe_load(
                (ROOT / "albums" / aid / "tracks" / item["file"]).read_text(encoding="utf-8")
            )
            tracks.append(
                (
                    track_data["id"],
                    track_data["title"],
                    bool(track_data.get("instrumental", item.get("instrumental", False))),
                )
            )
    return tracks


def match_setlist(title: str, setlist: dict[str, int]) -> int:
    if title in setlist:
        return setlist[title]
    alias = ALIASES.get(title)
    if alias and alias in setlist:
        return setlist[alias]

    norm = normalize(title)
    for sl_title, count in setlist.items():
        if normalize(sl_title) == norm:
            return count

    # partial match for tide of changes etc.
    for sl_title, count in setlist.items():
        if norm in normalize(sl_title) or normalize(sl_title) in norm:
            return count
    return 0


def score_track(title: str, setlist_plays: int, instrumental: bool) -> int:
    """Map setlist.fm plays + Spotify streams to 0–10."""
    spotify = SPOTIFY_M.get(title, 0)

    if instrumental and setlist_plays <= 5:
        return 0 if setlist_plays == 0 else 1

    # Tier 10 — hinos absolutos (top setlist + streaming)
    if setlist_plays >= 380 or spotify >= 22:
        return 10
    if setlist_plays >= 320 or spotify >= 19:
        return 9
    if setlist_plays >= 270 or spotify >= 16:
        return 8
    if setlist_plays >= 220 or spotify >= 13:
        return 7
    if setlist_plays >= 180 or spotify >= 10:
        return 6

    # Tier 5 — staples de show / singles fortes
    if setlist_plays >= 120 or spotify >= 6:
        return 5
    if setlist_plays >= 80 or spotify >= 4:
        return 4

    # Tier 3 — rotação regular ou destaque moderado
    if setlist_plays >= 45 or spotify >= 2.5:
        return 3
    if setlist_plays >= 20 or spotify >= 1.5:
        return 2

    # Tier 1 — raro ao vivo ou faixa de nicho
    if setlist_plays >= 5 or spotify >= 0.8:
        return 1
    if setlist_plays >= 1:
        return 1

    return 0 if instrumental else 1


def album_id_from_track(track_id: str, album_ids: list[str]) -> str:
    for aid in sorted(album_ids, key=len, reverse=True):
        if track_id.startswith(f"{aid}-"):
            return aid
    return track_id


def main() -> None:
    page_html = fetch_setlist_stats()
    setlist = parse_setlist(page_html)
    print(f"Setlist songs parsed: {len(setlist)}")

    tracks = load_project_tracks()
    scores: dict[str, int] = {}
    report: list[str] = []

    for track_id, title, instrumental in tracks:
        plays = match_setlist(title, setlist)
        score = score_track(title, plays, instrumental)
        scores[track_id] = score
        report.append(f"{score} | {plays:4d} plays | {title}")

    print("\n".join(report))
    from collections import Counter

    print("\nDistribution:", Counter(scores.values()))

    # Write yaml
    config = yaml.safe_load(BUILD_CONFIG.read_text(encoding="utf-8"))
    album_titles = {album["id"]: album.get("title", album["id"]) for album in config["albums"]}
    album_ids = list(album_titles.keys())

    lines = [
        "# Popularidade das faixas (0–10).",
        "# Fonte: setlist.fm (apresentações ao vivo, jun/2026) + Spotify (streams).",
        "# 10 = hino absoluto · 0 = intro instrumental raramente destacada",
        "",
        "tracks:",
    ]
    current_album = ""
    for track_id, title, _ in tracks:
        album_id = album_id_from_track(track_id, album_ids)
        if album_id != current_album:
            current_album = album_id
            lines.append("")
            lines.append(f"  # {album_titles.get(album_id, album_id)}")
        lines.append(f"  {track_id}: {scores[track_id]}")

    POPULARITY_PATH.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"\nWrote {POPULARITY_PATH}")


if __name__ == "__main__":
    main()
