#!/usr/bin/env python3

from __future__ import annotations

import argparse
import csv
import json
import struct
import sys
from collections import Counter
from io import StringIO
from pathlib import Path
from urllib.parse import quote


DEFAULT_REPOSITORY = "ArcticMunkee/Remote3-TV-Logo-Project"
DEFAULT_BRANCH = "main"
LOGO_DIRS = ("tv-logos", "misc")
MANIFEST_FILENAMES = ("logos.json", "logos.csv", "countries.json")
PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"


def display_name(slug: str) -> str:
    return " ".join(part.capitalize() for part in slug.split("-"))


def url_for_path(base_url: str, relative_path: str) -> str:
    return f"{base_url}/{'/'.join(quote(part) for part in relative_path.split('/'))}"


def read_png_size(path: Path) -> tuple[int, int]:
    with path.open("rb") as file:
        header = file.read(24)

    if len(header) < 24 or not header.startswith(PNG_SIGNATURE) or header[12:16] != b"IHDR":
        raise ValueError(f"Not a valid PNG file: {path}")

    return struct.unpack(">II", header[16:24])


def iter_logo_paths(root: Path) -> list[Path]:
    paths: list[Path] = []

    for directory_name in LOGO_DIRS:
        directory = root / directory_name
        if not directory.exists():
            continue

        paths.extend(path for path in directory.rglob("*.png") if path.is_file())

    return sorted(paths, key=lambda path: path.relative_to(root).as_posix())


def build_logo_entry(root: Path, path: Path, repository: str, branch: str) -> dict[str, object]:
    relative_path = path.relative_to(root).as_posix()
    parts = relative_path.split("/")
    top_level = parts[0]
    file_name = path.name
    stem = path.stem
    width, height = read_png_size(path)
    raw_base_url = f"https://raw.githubusercontent.com/{repository}/{branch}"
    github_base_url = f"https://github.com/{repository}/blob/{branch}"

    entry: dict[str, object] = {
        "path": relative_path,
        "file_name": file_name,
        "name": stem,
        "section": top_level,
        "size_bytes": path.stat().st_size,
        "width": width,
        "height": height,
        "raw_url": url_for_path(raw_base_url, relative_path),
        "github_url": url_for_path(github_base_url, relative_path),
    }

    if top_level == "tv-logos":
        country_or_region = parts[1] if len(parts) > 2 else ""
        entry.update(
            {
                "type": "tv-logo",
                "country_or_region": country_or_region,
                "country_or_region_name": display_name(country_or_region),
                "misc_category": "",
            }
        )
    else:
        misc_category = parts[1] if len(parts) > 2 else ""
        entry.update(
            {
                "type": "misc",
                "country_or_region": "",
                "country_or_region_name": "",
                "misc_category": misc_category,
            }
        )

    return entry


def build_country_manifest(logos: list[dict[str, object]], repository: str, branch: str) -> dict[str, object]:
    tv_counts = Counter(
        str(logo["country_or_region"])
        for logo in logos
        if logo["type"] == "tv-logo" and logo["country_or_region"]
    )
    misc_counts = Counter(
        str(logo["misc_category"])
        for logo in logos
        if logo["type"] == "misc" and logo["misc_category"]
    )
    github_base_url = f"https://github.com/{repository}/tree/{branch}"

    countries = [
        {
            "slug": slug,
            "name": display_name(slug),
            "path": f"tv-logos/{slug}",
            "count": tv_counts[slug],
            "github_url": url_for_path(github_base_url, f"tv-logos/{slug}"),
        }
        for slug in sorted(tv_counts)
    ]
    misc_categories = [
        {
            "slug": slug,
            "name": display_name(slug),
            "path": f"misc/{slug}",
            "count": misc_counts[slug],
            "github_url": url_for_path(github_base_url, f"misc/{slug}"),
        }
        for slug in sorted(misc_counts)
    ]

    return {
        "schema_version": 1,
        "repository": repository,
        "branch": branch,
        "total_tv_logos": sum(1 for logo in logos if logo["type"] == "tv-logo"),
        "total_misc_logos": sum(1 for logo in logos if logo["type"] == "misc"),
        "total_countries_or_regions": len(countries),
        "total_misc_categories": len(misc_categories),
        "countries_or_regions": countries,
        "misc_categories": misc_categories,
    }


def build_csv(logos: list[dict[str, object]]) -> str:
    fields = [
        "path",
        "file_name",
        "name",
        "type",
        "section",
        "country_or_region",
        "country_or_region_name",
        "misc_category",
        "width",
        "height",
        "size_bytes",
        "raw_url",
        "github_url",
    ]
    buffer = StringIO()
    writer = csv.DictWriter(buffer, fieldnames=fields, extrasaction="ignore", lineterminator="\n")
    writer.writeheader()
    writer.writerows(logos)
    return buffer.getvalue()


def build_manifests(root: Path, repository: str, branch: str) -> dict[str, str]:
    logo_paths = iter_logo_paths(root)
    logos = [build_logo_entry(root, path, repository, branch) for path in logo_paths]
    logo_manifest = {
        "schema_version": 1,
        "repository": repository,
        "branch": branch,
        "total_logos": len(logos),
        "logos": logos,
    }
    country_manifest = build_country_manifest(logos, repository, branch)

    return {
        "logos.json": json.dumps(logo_manifest, indent=2, ensure_ascii=True) + "\n",
        "logos.csv": build_csv(logos),
        "countries.json": json.dumps(country_manifest, indent=2, ensure_ascii=True) + "\n",
    }


def write_manifests(root: Path, output_dir: Path, repository: str, branch: str) -> None:
    manifests = build_manifests(root, repository, branch)
    output_dir.mkdir(parents=True, exist_ok=True)

    for file_name, content in manifests.items():
        (output_dir / file_name).write_text(content, encoding="utf-8")

    print(f"Wrote {len(manifests)} manifest files to {output_dir}")


def check_manifests(root: Path, output_dir: Path, repository: str, branch: str) -> int:
    manifests = build_manifests(root, repository, branch)
    outdated: list[str] = []

    for file_name, expected_content in manifests.items():
        manifest_path = output_dir / file_name

        if not manifest_path.exists():
            outdated.append(file_name)
            continue

        actual_content = manifest_path.read_text(encoding="utf-8")
        if actual_content != expected_content:
            outdated.append(file_name)

    if not outdated:
        print("Manifest files are up to date.")
        return 0

    print("Manifest files are missing or outdated:")
    for file_name in outdated:
        print(f"- {file_name}")
    print()
    print("Run this command locally and commit the updated files:")
    print("python3 scripts/generate_manifest.py")
    return 1


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate manifest files for TV logo assets.")
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="Repository root. Defaults to current directory.")
    parser.add_argument("--output-dir", type=Path, default=None, help="Manifest output directory. Defaults to root.")
    parser.add_argument("--repository", default=DEFAULT_REPOSITORY, help="GitHub repository in owner/name form.")
    parser.add_argument("--branch", default=DEFAULT_BRANCH, help="Branch used for generated GitHub and raw URLs.")
    parser.add_argument("--check", action="store_true", help="Fail if committed manifest files are missing or outdated.")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = args.root.resolve()
    output_dir = args.output_dir.resolve() if args.output_dir else root

    if args.check:
        return check_manifests(root, output_dir, args.repository, args.branch)

    write_manifests(root, output_dir, args.repository, args.branch)
    return 0


if __name__ == "__main__":
    sys.exit(main())
