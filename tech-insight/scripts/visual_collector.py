#!/usr/bin/env python3
"""
visual_collector.py — bulk download primary-source images for a tech-insight report.

Reads a plan JSON describing the images to fetch, downloads each into
assets/<slug>/, and writes/updates assets/<slug>/image_manifest.json with the
original source URL and fetch timestamp.

Plan JSON schema:
{
  "slug": "ai-accelerator-2026",
  "images": [
    {
      "filename": "p1-hero.jpg",
      "source_url": "https://vendor.example.com/press/p1.jpg",
      "license_note": "vendor press kit",
      "caption": "P1 official product photo"
    },
    ...
  ]
}

Usage:
  python visual_collector.py --plan plan.json --assets-root assets/

The script never invents images. If a download fails, it records the failure in
the manifest under "failed" — the linter will then reject the report so the
human writer is forced to find a real primary source.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

try:
    import requests
except ImportError:
    sys.stderr.write("requests is required: pip install requests\n")
    sys.exit(2)


def fetch(url: str, dest: Path, timeout: int = 30) -> tuple[bool, str]:
    headers = {
        "User-Agent": "tech-insight-skill/1.0 (+https://github.com/anthropics/skills)"
    }
    try:
        resp = requests.get(url, headers=headers, timeout=timeout, stream=True)
        resp.raise_for_status()
        dest.parent.mkdir(parents=True, exist_ok=True)
        with open(dest, "wb") as f:
            for chunk in resp.iter_content(chunk_size=64 * 1024):
                if chunk:
                    f.write(chunk)
        return True, f"{dest.stat().st_size} bytes"
    except Exception as e:  # noqa: BLE001
        return False, str(e)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--plan", required=True, help="Path to plan JSON")
    p.add_argument(
        "--assets-root", default="assets", help="Root directory for downloads"
    )
    args = p.parse_args()

    plan_path = Path(args.plan)
    if not plan_path.exists():
        sys.stderr.write(f"plan file not found: {plan_path}\n")
        return 2
    plan = json.loads(plan_path.read_text(encoding="utf-8"))

    slug = plan.get("slug")
    images = plan.get("images") or []
    if not slug or not images:
        sys.stderr.write("plan must contain 'slug' and non-empty 'images'\n")
        return 2

    out_dir = Path(args.assets_root) / slug
    out_dir.mkdir(parents=True, exist_ok=True)
    manifest_path = out_dir / "image_manifest.json"
    manifest: dict = {}
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    manifest.setdefault("entries", {})
    manifest.setdefault("failed", {})

    ok = 0
    failed = 0
    for img in images:
        filename = img["filename"]
        source_url = img["source_url"]
        dest = out_dir / filename
        host = urlparse(source_url).netloc
        success, info = fetch(source_url, dest)
        ts = datetime.now(timezone.utc).isoformat()
        if success:
            manifest["entries"][filename] = {
                "source_url": source_url,
                "source_host": host,
                "license_note": img.get("license_note", ""),
                "caption": img.get("caption", ""),
                "fetched_at": ts,
                "size_info": info,
            }
            manifest["failed"].pop(filename, None)
            ok += 1
            print(f"  OK   {filename}  <- {host}")
        else:
            manifest["failed"][filename] = {
                "source_url": source_url,
                "fetched_at": ts,
                "error": info,
            }
            failed += 1
            print(f"  FAIL {filename}  <- {host}  ({info})")
        time.sleep(0.3)  # be polite

    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(f"\nDone: {ok} ok, {failed} failed. Manifest: {manifest_path}")
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
