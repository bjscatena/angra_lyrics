#!/usr/bin/env python3
"""Validate album and track YAML content before build."""

from __future__ import annotations

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
ALBUMS_DIR = ROOT / "albums"
POPULARITY_PATH = ROOT / "scripts" / "popularity.yaml"

ALBUM_REQUIRED = ("id", "title", "type", "release", "tracklist", "history", "assets")
TRACK_REQUIRED = ("id", "album_id", "track_number", "title", "language", "research", "metadata")
TRACK_VOCAL_REQUIRED = ("lyrics",)
DATE_PATTERN = re.compile(r"^\d{4}-\d{2}-\d{2}$")


class ValidationError(Exception):
    def __init__(self, rule: str, message: str) -> None:
        self.rule = rule
        super().__init__(message)


def load_yaml(path: Path) -> dict:
    with path.open(encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    if not isinstance(data, dict):
        raise ValidationError("R01", f"{path}: YAML root must be a mapping")
    return data


def require_fields(data: dict, fields: tuple[str, ...], context: str) -> None:
    for field in fields:
        if field not in data or data[field] in (None, ""):
            raise ValidationError("R01", f"{context}: missing required field '{field}'")


def validate_date(value: str, context: str) -> None:
    if not isinstance(value, str) or not DATE_PATTERN.match(value):
        raise ValidationError("R08", f"{context}: invalid date '{value}' (expected YYYY-MM-DD)")
    try:
        datetime.strptime(value, "%Y-%m-%d")
    except ValueError as exc:
        raise ValidationError("R08", f"{context}: invalid date '{value}'") from exc


def validate_album(album_dir: Path) -> list[str]:
    album_path = album_dir / "album.yaml"
    if not album_path.exists():
        return []

    errors: list[str] = []
    slug = album_dir.name
    ctx = f"albums/{slug}/album.yaml"

    try:
        album = load_yaml(album_path)
        require_fields(album, ALBUM_REQUIRED, ctx)

        if album.get("id") != slug:
            raise ValidationError("R04", f"{ctx}: id '{album.get('id')}' does not match folder '{slug}'")

        release = album.get("release", {})
        if not isinstance(release, dict):
            raise ValidationError("R01", f"{ctx}: release must be a mapping")
        if "date" not in release:
            raise ValidationError("R01", f"{ctx}: missing required field 'release.date'")
        validate_date(release["date"], ctx)

        history = album.get("history", {})
        if not isinstance(history, dict) or not history.get("summary"):
            raise ValidationError("R01", f"{ctx}: missing required field 'history.summary'")

        assets = album.get("assets", {})
        if not isinstance(assets, dict) or not assets.get("cover"):
            raise ValidationError("R07", f"{ctx}: missing assets.cover")
        cover_path = album_dir / assets["cover"]
        if not cover_path.exists():
            raise ValidationError("R07", f"{ctx}: cover file not found at '{assets['cover']}'")

        tracklist = album.get("tracklist", [])
        if not isinstance(tracklist, list) or not tracklist:
            raise ValidationError("R01", f"{ctx}: tracklist must be a non-empty list")

        seen_numbers: set[int] = set()
        for entry in tracklist:
            if not isinstance(entry, dict):
                raise ValidationError("R01", f"{ctx}: tracklist entries must be mappings")
            number = entry.get("number")
            file_name = entry.get("file")
            if number is None or not file_name:
                raise ValidationError("R01", f"{ctx}: tracklist entry missing number or file")

            if number in seen_numbers:
                raise ValidationError("R05", f"{ctx}: duplicate track_number {number}")
            seen_numbers.add(number)

            track_path = album_dir / "tracks" / file_name
            if not track_path.exists():
                raise ValidationError("R02", f"{ctx}: tracklist references missing file 'tracks/{file_name}'")

            track_errors = validate_track(track_path, slug, entry)
            errors.extend(track_errors)

    except ValidationError as exc:
        errors.append(f"[{exc.rule}] {exc}")

    return errors


def validate_track(track_path: Path, album_slug: str, tracklist_entry: dict) -> list[str]:
    ctx = f"albums/{album_slug}/tracks/{track_path.name}"
    errors: list[str] = []

    try:
        track = load_yaml(track_path)
        require_fields(track, TRACK_REQUIRED, ctx)

        if track.get("album_id") != album_slug:
            raise ValidationError(
                "R04",
                f"{ctx}: album_id '{track.get('album_id')}' does not match folder '{album_slug}'",
            )

        number = track.get("track_number")
        expected = tracklist_entry.get("number")
        if number != expected:
            raise ValidationError(
                "R05",
                f"{ctx}: track_number {number} does not match tracklist number {expected}",
            )

        is_instrumental = bool(track.get("instrumental") or tracklist_entry.get("instrumental"))
        has_lyrics = "lyrics" in track and track["lyrics"] not in (None, [])

        if is_instrumental and has_lyrics:
            raise ValidationError("R06", f"{ctx}: instrumental track must not have lyrics block")

        if not is_instrumental:
            require_fields(track, TRACK_VOCAL_REQUIRED, ctx)
            lyrics = track.get("lyrics", [])
            if not isinstance(lyrics, list) or not lyrics:
                raise ValidationError("R03", f"{ctx}: vocal track must have non-empty lyrics")

            for section in lyrics:
                if not isinstance(section, dict):
                    raise ValidationError("R03", f"{ctx}: lyrics sections must be mappings")
                lines = section.get("lines", [])
                if not lines:
                    raise ValidationError("R03", f"{ctx}: lyrics section '{section.get('section')}' has no lines")
                for line in lines:
                    if not isinstance(line, dict):
                        raise ValidationError("R03", f"{ctx}: lyric lines must be mappings")
                    original = line.get("original", "")
                    translation = line.get("translation", "")
                    if not str(original).strip():
                        raise ValidationError("R03", f"{ctx}: lyric line missing original text")
                    if not str(translation).strip():
                        raise ValidationError("R03", f"{ctx}: lyric line missing translation")

        research = track.get("research", {})
        if not isinstance(research, dict):
            raise ValidationError("R01", f"{ctx}: research must be a mapping")
        if not research.get("summary"):
            raise ValidationError("R01", f"{ctx}: missing required field 'research.summary'")
        if not research.get("context"):
            raise ValidationError("R01", f"{ctx}: missing required field 'research.context'")

    except ValidationError as exc:
        errors.append(f"[{exc.rule}] {exc}")

    return errors


def collect_track_ids() -> set[str]:
    ids: set[str] = set()
    if not ALBUMS_DIR.exists():
        return ids

    for album_dir in sorted(p for p in ALBUMS_DIR.iterdir() if p.is_dir()):
        album_path = album_dir / "album.yaml"
        if not album_path.exists():
            continue

        album = load_yaml(album_path)
        for entry in album.get("tracklist", []):
            file_name = entry.get("file")
            if not file_name:
                continue
            track_path = album_dir / "tracks" / file_name
            if not track_path.exists():
                continue
            track = load_yaml(track_path)
            track_id = track.get("id")
            if track_id:
                ids.add(str(track_id))

    return ids


def validate_popularity() -> list[str]:
    if not POPULARITY_PATH.exists():
        return [f"[R09] {POPULARITY_PATH.relative_to(ROOT)}: popularity file not found"]

    data = load_yaml(POPULARITY_PATH)
    tracks = data.get("tracks", {})
    if not isinstance(tracks, dict):
        return ["[R09] scripts/popularity.yaml: tracks must be a mapping"]

    errors: list[str] = []
    expected_ids = collect_track_ids()
    defined_ids = set(tracks.keys())

    missing = sorted(expected_ids - defined_ids)
    for track_id in missing:
        errors.append(f"[R09] scripts/popularity.yaml: missing popularity for track '{track_id}'")

    extra = sorted(defined_ids - expected_ids)
    for track_id in extra:
        errors.append(f"[R09] scripts/popularity.yaml: unknown track id '{track_id}'")

    for track_id, value in tracks.items():
        try:
            score = int(value)
        except (TypeError, ValueError):
            errors.append(f"[R09] scripts/popularity.yaml: invalid popularity for '{track_id}'")
            continue
        if score < 0 or score > 10:
            errors.append(
                f"[R09] scripts/popularity.yaml: popularity for '{track_id}' must be 0–10 (got {score})"
            )

    return errors


def validate_all() -> list[str]:
    if not ALBUMS_DIR.exists():
        return []

    errors: list[str] = []
    album_dirs = sorted(p for p in ALBUMS_DIR.iterdir() if p.is_dir())

    validated_any = False
    for album_dir in album_dirs:
        if (album_dir / "album.yaml").exists():
            validated_any = True
            errors.extend(validate_album(album_dir))

    if not validated_any:
        print("No album.yaml files found — nothing to validate (OK for Phase 0).")
    else:
        errors.extend(validate_popularity())

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate Angra Lyrics YAML content")
    parser.parse_args()

    errors = validate_all()
    if errors:
        print(f"Validation failed with {len(errors)} error(s):\n")
        for err in errors:
            print(f"  {err}")
        return 1

    print("Validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
