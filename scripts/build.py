#!/usr/bin/env python3
"""Build static site from album YAML content."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

import yaml
from jinja2 import Environment, FileSystemLoader, select_autoescape

ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = ROOT / "scripts"
STATIC_DIR = SCRIPTS_DIR / "static"
ALBUMS_DIR = ROOT / "albums"
TEMPLATES_DIR = SCRIPTS_DIR / "templates"
CONFIG_PATH = SCRIPTS_DIR / "build_config.yaml"
POPULARITY_PATH = SCRIPTS_DIR / "popularity.yaml"


def load_config() -> dict:
    with CONFIG_PATH.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def load_popularity() -> dict[str, int]:
    data = load_yaml(POPULARITY_PATH) or {}
    tracks = data.get("tracks", {})
    result: dict[str, int] = {}
    for track_id, value in tracks.items():
        score = int(value)
        result[str(track_id)] = max(0, min(10, score))
    return result


def load_yaml(path: Path) -> dict | None:
    if not path.exists():
        return None
    with path.open(encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def normalize_base_path(path: str) -> str:
    path = (path or "").strip().rstrip("/")
    if path and not path.startswith("/"):
        path = f"/{path}"
    return path


def parse_score(score_str: str) -> float | None:
    if not score_str:
        return None
    score_str = score_str.strip()
    if score_str.endswith("%"):
        try:
            return float(score_str[:-1]) / 100.0 * 10.0
        except ValueError:
            return None
    if "/" in score_str:
        try:
            parts = score_str.split("/")
            if len(parts) == 2:
                numerator = float(parts[0])
                denominator = float(parts[1])
                if denominator != 0:
                    return numerator / denominator * 10.0
        except ValueError:
            return None
    try:
        return float(score_str)
    except ValueError:
        return None


def calculate_critic_score(ratings: list[dict]) -> float | None:
    if not ratings:
        return None
    scores = []
    for r in ratings:
        score_val = parse_score(r.get("score", ""))
        if score_val is not None:
            scores.append(score_val)
    if not scores:
        return None
    return round(sum(scores) / len(scores), 2)


def asset_prefix_for(depth: int) -> str:
    """Relative prefix for assets and internal links (works locally and on GitHub Pages)."""
    return "../" * depth if depth > 0 else ""


def absolute_url(site_url: str, base_path: str, rel_path: str) -> str:
    rel = rel_path.lstrip("/")

    if site_url:
        return f"{site_url.rstrip('/')}/{rel}"

    if base_path:
        return f"{base_path.rstrip('/')}/{rel}"

    return rel_path


def track_page_name(track_file: str) -> str:
    return Path(track_file).stem + ".html"


def run_validation() -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPTS_DIR / "validate.py")],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(result.stdout)
        print(result.stderr, file=sys.stderr)
        raise SystemExit(1)


def copy_static_assets(output_dir: Path) -> None:
    if not STATIC_DIR.exists():
        return

    for src in STATIC_DIR.rglob("*"):
        if not src.is_file():
            continue
        rel = src.relative_to(STATIC_DIR)
        dest = output_dir / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dest)


def copy_assets(album_dir: Path, album_id: str, output_dir: Path) -> str | None:
    album = load_yaml(album_dir / "album.yaml")
    if not album:
        return None

    assets = album.get("assets", {})
    cover_rel = assets.get("cover")
    cover_url = None

    if cover_rel:
        cover_src = album_dir / cover_rel
        if cover_src.exists():
            dest_dir = output_dir / "assets" / "covers"
            dest_dir.mkdir(parents=True, exist_ok=True)
            dest_name = f"{album_id}{cover_src.suffix.lower()}"
            shutil.copy2(cover_src, dest_dir / dest_name)
            cover_url = f"assets/covers/{dest_name}"

    return cover_url


def build_search_index(albums_data: list[dict]) -> list[dict]:
    index: list[dict] = []
    for album in albums_data:
        album_id = album["id"]
        for track in album.get("tracks", []):
            page_name = track.get("page_name") or track.get("url", "")
            index.append(
                {
                    "album_id": album_id,
                    "album_title": album.get("title", album_id),
                    "track_number": track.get("number"),
                    "title": track.get("title", ""),
                    "url": f"albums/{album_id}/{page_name}",
                    "summary": (track.get("research") or {}).get("summary", ""),
                    "popularity": track.get("popularity", 0),
                    "critic_score": track.get("critic_score", 0),
                }
            )
    return index


def asset_version_for_build() -> str:
    """Cache-bust token derived from static assets and popularity data."""
    candidates = [
        POPULARITY_PATH,
        STATIC_DIR / "css" / "style.css",
        STATIC_DIR / "js" / "main.js",
        STATIC_DIR / "js" / "popular.js",
        STATIC_DIR / "js" / "popularity.js",
    ]
    latest = 0.0
    for path in candidates:
        if path.exists():
            latest = max(latest, path.stat().st_mtime)
    return str(int(latest)) if latest else "1"


def render(env: Environment, template_name: str, asset_prefix: str, **context) -> str:
    template = env.get_template(template_name)
    return template.render(asset_prefix=asset_prefix, **context)


def build_site(skip_validate: bool = False) -> None:
    if not skip_validate:
        run_validation()

    config = load_config()
    output_dir = ROOT / config.get("output_dir", "site")
    site_title = config.get("site_title", "Angra Lyrics")
    site_description = config.get("site_description", "")
    base_path = normalize_base_path(config.get("base_path", ""))
    site_url = (config.get("site_url") or "").strip()

    env = Environment(
        loader=FileSystemLoader(str(TEMPLATES_DIR)),
        autoescape=select_autoescape(["html", "xml"]),
    )
    env.globals["site_title"] = site_title
    env.globals["site_description"] = site_description
    asset_version = asset_version_for_build()
    render_context = {"asset_version": asset_version}

    output_dir.mkdir(parents=True, exist_ok=True)
    copy_static_assets(output_dir)

    popularity_map = load_popularity()
    albums_output: list[dict] = []
    album_prefix = asset_prefix_for(2)

    for album_meta in config.get("albums", []):
        album_id = album_meta["id"]
        album_dir = ALBUMS_DIR / album_id
        album_data = load_yaml(album_dir / "album.yaml")

        album_entry: dict = {
            "id": album_id,
            "title": album_meta.get("title", album_id),
            "year": album_meta.get("year"),
            "has_content": album_data is not None,
            "url": f"albums/{album_id}/index.html",
            "cover_url": None,
            "tracks": [],
            "critic_score": None,
        }

        if album_data:
            album_entry["title"] = album_data.get("title", album_entry["title"])
            album_entry["release"] = album_data.get("release", {})
            album_entry["lineup"] = album_data.get("lineup", [])
            album_entry["history"] = album_data.get("history", {})
            album_entry["assets"] = album_data.get("assets", {})
            album_entry["ratings"] = album_data.get("ratings", [])
            album_entry["critic_score"] = calculate_critic_score(album_entry["ratings"])

            cover_url = copy_assets(album_dir, album_id, output_dir)
            album_entry["cover_url"] = cover_url

            album_out = output_dir / "albums" / album_id
            album_out.mkdir(parents=True, exist_ok=True)

            tracks: list[dict] = []
            for item in album_data.get("tracklist", []):
                track_file = item.get("file", "")
                track_path = album_dir / "tracks" / track_file
                track_data = load_yaml(track_path) or {}
                page_name = track_page_name(track_file)

                track_id = track_data.get("id") or f"{album_id}-{Path(track_file).stem}"
                track_ratings = track_data.get("ratings", [])
                track_entry = {
                    **track_data,
                    "number": item.get("number"),
                    "duration": track_data.get("duration") or item.get("duration"),
                    "instrumental": track_data.get("instrumental", item.get("instrumental", False)),
                    "url": page_name,
                    "page_name": page_name,
                    "popularity": popularity_map.get(track_id, 0),
                    "critic_score": calculate_critic_score(track_ratings),
                }
                tracks.append(track_entry)

            album_page_path = f"albums/{album_id}/index.html"
            album_og_image = (
                absolute_url(site_url, base_path, cover_url) if cover_url else None
            )

            for i, track in enumerate(tracks):
                track_page_path = f"albums/{album_id}/{track['page_name']}"
                track_html = render(
                    env,
                    "track.html",
                    asset_prefix=album_prefix,
                    album=album_entry,
                    track=track,
                    prev_track=tracks[i - 1] if i > 0 else None,
                    next_track=tracks[i + 1] if i + 1 < len(tracks) else None,
                    page_url=absolute_url(site_url, base_path, track_page_path),
                    og_image_url=album_og_image,
                    **render_context,
                )
                (album_out / track["page_name"]).write_text(track_html, encoding="utf-8")

            album_entry["tracks"] = tracks

            album_html = render(
                env,
                "album.html",
                asset_prefix=album_prefix,
                album=album_entry,
                page_url=absolute_url(site_url, base_path, album_page_path),
                og_image_url=album_og_image,
                **render_context,
            )
            (album_out / "index.html").write_text(album_html, encoding="utf-8")

        albums_output.append(album_entry)

    index_prefix = asset_prefix_for(0)
    index_html = render(
        env,
        "index.html",
        asset_prefix=index_prefix,
        albums=albums_output,
        page_url=absolute_url(site_url, base_path, "index.html"),
        **render_context,
    )
    (output_dir / "index.html").write_text(index_html, encoding="utf-8")

    popular_html = render(
        env,
        "popular.html",
        asset_prefix=index_prefix,
        page_url=absolute_url(site_url, base_path, "popular.html"),
        **render_context,
    )
    (output_dir / "popular.html").write_text(popular_html, encoding="utf-8")

    # Filter albums that have content and sort them by critic_score descending
    albums_by_rating = sorted(
        [a for a in albums_output if a.get("has_content") and a.get("critic_score") is not None],
        key=lambda x: x["critic_score"],
        reverse=True,
    )
    # Add pending albums at the end
    pending_albums = [a for a in albums_output if not a.get("has_content") or a.get("critic_score") is None]
    albums_sorted = albums_by_rating + pending_albums

    critics_html = render(
        env,
        "critics.html",
        asset_prefix=index_prefix,
        albums=albums_sorted,
        page_url=absolute_url(site_url, base_path, "critics.html"),
        **render_context,
    )
    (output_dir / "critics.html").write_text(critics_html, encoding="utf-8")

    search_index = build_search_index([a for a in albums_output if a.get("tracks")])
    (output_dir / "search-index.json").write_text(
        json.dumps(search_index, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(f"Site built at {output_dir.relative_to(ROOT)}/")
    print(f"  Albums: {len(albums_output)}")
    print(f"  With content: {sum(1 for a in albums_output if a.get('has_content'))}")
    if base_path:
        print(f"  Base path: {base_path}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build Angra Lyrics static site")
    parser.add_argument("--skip-validate", action="store_true", help="Skip validation step")
    args = parser.parse_args()

    build_site(skip_validate=args.skip_validate)
    return 0


if __name__ == "__main__":
    sys.exit(main())
