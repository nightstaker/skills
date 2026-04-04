#!/usr/bin/env python3
"""
Slide ID Manager — lock, unlock, and verify slide IDs for incremental updates.

Usage:
    # List all slides with their IDs
    python scripts/slide_id_manager.py list input.pptx

    # Lock specific slide IDs
    python scripts/slide_id_manager.py lock input.pptx --ids 256,258,271 --manifest .slide_locks.json

    # Lock by position (slide number)
    python scripts/slide_id_manager.py lock input.pptx --positions 2,3,7 --manifest .slide_locks.json

    # Unlock specific IDs
    python scripts/slide_id_manager.py unlock --ids 256 --manifest .slide_locks.json

    # Check if a slide is locked
    python scripts/slide_id_manager.py check --id 256 --manifest .slide_locks.json

    # Verify locked slides survived a round-trip (compares original vs output)
    python scripts/slide_id_manager.py verify --original input.pptx --output output.pptx --manifest .slide_locks.json

    # Show current manifest
    python scripts/slide_id_manager.py show --manifest .slide_locks.json
"""

import argparse
import hashlib
import json
import sys
import zipfile
from datetime import date
from pathlib import Path

try:
    from lxml import etree
except ImportError:
    print("ERROR: Missing lxml. Run: pip install lxml", file=sys.stderr)
    sys.exit(1)

NS_P = "http://schemas.openxmlformats.org/presentationml/2006/main"
NS_R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
NS_REL = "http://schemas.openxmlformats.org/package/2006/relationships"


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _get_slide_entries(pptx_path: str) -> list[dict]:
    """Return ordered list of {position, id, rid, slide_file, title}."""
    pptx_path = Path(pptx_path)
    entries = []

    with zipfile.ZipFile(pptx_path, "r") as zf:
        with zf.open("ppt/presentation.xml") as f:
            prs = etree.fromstring(f.read())

        try:
            with zf.open("ppt/_rels/presentation.xml.rels") as f:
                rels_tree = etree.fromstring(f.read())
        except KeyError:
            return entries

        rid_to_target = {}
        for rel in rels_tree.iter("{%s}Relationship" % NS_REL):
            rel_type = rel.get("Type", "")
            if "slide" in rel_type and "slideLayout" not in rel_type and "slideMaster" not in rel_type:
                rid_to_target[rel.get("Id")] = rel.get("Target", "")

        sld_id_lst = prs.find("{%s}sldIdLst" % NS_P)
        if sld_id_lst is None:
            return entries

        for pos, sld_id_elem in enumerate(sld_id_lst, start=1):
            sid = sld_id_elem.get("id")
            rid = sld_id_elem.get("{%s}id" % NS_R)
            target = rid_to_target.get(rid, "")
            if target.startswith("../"):
                slide_file = "ppt/" + target[3:]
            elif not target.startswith("ppt/"):
                slide_file = "ppt/slides/" + Path(target).name
            else:
                slide_file = target

            # Try to get slide title
            title = ""
            try:
                with zf.open(slide_file) as f:
                    slide_xml = etree.fromstring(f.read())
                for ph in slide_xml.iter("{%s}ph" % NS_P):
                    if ph.get("type") in ("title", "ctrTitle"):
                        sp = ph.getparent()
                        while sp is not None and sp.tag != "{%s}sp" % NS_P:
                            sp = sp.getparent()
                        if sp is not None:
                            for t in sp.iter("{http://schemas.openxmlformats.org/drawingml/2006/main}t"):
                                title += t.text or ""
                        break
            except Exception:
                pass

            entries.append({
                "position": pos,
                "id": int(sid) if sid else None,
                "rid": rid,
                "slide_file": slide_file,
                "title": title.strip()[:60],
            })

    return entries


def _hash_slide(pptx_path: str, slide_file: str) -> str:
    """SHA-256 hash of a slide's XML content."""
    with zipfile.ZipFile(pptx_path, "r") as zf:
        try:
            with zf.open(slide_file) as f:
                return hashlib.sha256(f.read()).hexdigest()
        except KeyError:
            return ""


# ---------------------------------------------------------------------------
# Manifest I/O
# ---------------------------------------------------------------------------

def _load_manifest(manifest_path: str) -> dict:
    p = Path(manifest_path)
    if p.exists():
        return json.loads(p.read_text(encoding="utf-8"))
    return {"locked": []}


def _save_manifest(manifest: dict, manifest_path: str):
    Path(manifest_path).write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_list(pptx_path: str, manifest_path: str = None):
    """List all slides with IDs and lock status."""
    entries = _get_slide_entries(pptx_path)

    locked_ids = set()
    if manifest_path:
        manifest = _load_manifest(manifest_path)
        locked_ids = {e["id"] for e in manifest.get("locked", [])}

    print(f"{'Pos':>4}  {'ID':>6}  {'Lock':5}  Title")
    print("-" * 65)
    for e in entries:
        lock_marker = "🔒   " if e["id"] in locked_ids else "     "
        title = e["title"] or "(no title)"
        print(f"{e['position']:>4}  {e['id'] or '?':>6}  {lock_marker}  {title}")

    print(f"\nTotal: {len(entries)} slides")
    if locked_ids:
        print(f"Locked: {len(locked_ids)} slides")


def cmd_lock(pptx_path: str, ids: list[int] = None, positions: list[int] = None,
             manifest_path: str = ".slide_locks.json"):
    """Lock slides by ID or position."""
    entries = _get_slide_entries(pptx_path)
    pos_to_entry = {e["position"]: e for e in entries}
    id_to_entry  = {e["id"]: e for e in entries if e["id"]}

    targets = []
    if ids:
        for sid in ids:
            if sid in id_to_entry:
                targets.append(id_to_entry[sid])
            else:
                print(f"WARNING: Slide ID {sid} not found in {pptx_path}", file=sys.stderr)

    if positions:
        for pos in positions:
            if pos in pos_to_entry:
                targets.append(pos_to_entry[pos])
            else:
                print(f"WARNING: Position {pos} not found in {pptx_path}", file=sys.stderr)

    if not targets:
        print("No slides to lock.", file=sys.stderr)
        sys.exit(1)

    manifest = _load_manifest(manifest_path)
    existing_locked_ids = {e["id"] for e in manifest.get("locked", [])}

    added = 0
    for e in targets:
        if e["id"] in existing_locked_ids:
            print(f"  Already locked: slide {e['position']} (ID {e['id']}) — {e['title']}")
            continue
        content_hash = _hash_slide(pptx_path, e["slide_file"])
        manifest.setdefault("locked", []).append({
            "id": e["id"],
            "position": e["position"],
            "title": e["title"],
            "slide_file": e["slide_file"],
            "locked_at": str(date.today()),
            "source_file": str(pptx_path),
            "content_hash": content_hash,
        })
        added += 1
        print(f"  Locked: slide {e['position']} (ID {e['id']}) — {e['title']}")

    _save_manifest(manifest, manifest_path)
    print(f"\n{added} slide(s) locked. Manifest saved to: {manifest_path}")


def cmd_unlock(ids: list[int], manifest_path: str):
    """Remove locks for specified slide IDs."""
    manifest = _load_manifest(manifest_path)
    ids_set = set(ids)
    before = len(manifest.get("locked", []))
    manifest["locked"] = [e for e in manifest.get("locked", []) if e["id"] not in ids_set]
    removed = before - len(manifest["locked"])
    _save_manifest(manifest, manifest_path)
    print(f"Unlocked {removed} slide(s). Manifest updated: {manifest_path}")


def cmd_check(slide_id: int, manifest_path: str):
    """Check if a specific slide ID is locked."""
    manifest = _load_manifest(manifest_path)
    locked = {e["id"] for e in manifest.get("locked", [])}
    if slide_id in locked:
        entry = next(e for e in manifest["locked"] if e["id"] == slide_id)
        print(f"LOCKED — slide ID {slide_id}: \"{entry['title']}\" (locked {entry['locked_at']})")
        sys.exit(0)  # exit 0 = locked
    else:
        print(f"NOT LOCKED — slide ID {slide_id}")
        sys.exit(1)  # exit 1 = not locked (callers can use this in shell logic)


def cmd_verify(original_pptx: str, output_pptx: str, manifest_path: str):
    """
    Verify that all locked slides in the manifest are present and unchanged in the output file.
    """
    manifest = _load_manifest(manifest_path)
    locked = manifest.get("locked", [])

    if not locked:
        print("No locked slides in manifest. Nothing to verify.")
        return

    # Get slide IDs in output file
    output_entries = _get_slide_entries(output_pptx)
    output_id_to_entry = {e["id"]: e for e in output_entries}

    errors = []
    warnings = []

    for lock in locked:
        sid = lock["id"]
        title = lock.get("title", "")
        stored_hash = lock.get("content_hash", "")

        if sid not in output_id_to_entry:
            errors.append(f"MISSING: Slide ID {sid} (\"{title}\") not found in output file")
            continue

        out_entry = output_id_to_entry[sid]
        current_hash = _hash_slide(output_pptx, out_entry["slide_file"])

        if stored_hash and current_hash != stored_hash:
            errors.append(
                f"MODIFIED: Slide ID {sid} (\"{title}\") content changed\n"
                f"  Original hash: {stored_hash[:16]}...\n"
                f"  Current hash:  {current_hash[:16]}..."
            )
        else:
            print(f"  ✓  Slide ID {sid} ({title[:40]})")

    print()
    if errors:
        print(f"❌ Verification FAILED — {len(errors)} issue(s):")
        for e in errors:
            print(f"  {e}")
        sys.exit(1)
    else:
        print(f"✅ All {len(locked)} locked slides verified successfully.")


def cmd_show(manifest_path: str):
    """Show the current manifest contents."""
    manifest = _load_manifest(manifest_path)
    locked = manifest.get("locked", [])
    if not locked:
        print(f"No locked slides in {manifest_path}")
        return

    print(f"Locked slides in: {manifest_path}\n")
    print(f"{'ID':>6}  {'Pos':>4}  {'Locked':10}  Title")
    print("-" * 60)
    for e in sorted(locked, key=lambda x: x.get("position", 0)):
        print(f"{e['id']:>6}  {e.get('position', '?'):>4}  {e.get('locked_at', ''):10}  {e.get('title', '')}")
    print(f"\nTotal: {len(locked)} locked slides")


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(description="Manage slide ID locks for incremental PPT updates")
    sub = parser.add_subparsers(dest="command", required=True)

    # list
    p_list = sub.add_parser("list", help="List all slides with IDs")
    p_list.add_argument("pptx", help="PPTX file path")
    p_list.add_argument("--manifest", help="Show lock status from this manifest file")

    # lock
    p_lock = sub.add_parser("lock", help="Lock slides to prevent modification")
    p_lock.add_argument("pptx", help="PPTX file path")
    p_lock.add_argument("--ids", help="Comma-separated slide IDs to lock (e.g. 256,258)")
    p_lock.add_argument("--positions", help="Comma-separated slide positions to lock (e.g. 2,3,7)")
    p_lock.add_argument("--manifest", default=".slide_locks.json", help="Manifest file path")

    # unlock
    p_unlock = sub.add_parser("unlock", help="Remove lock from slide IDs")
    p_unlock.add_argument("--ids", required=True, help="Comma-separated slide IDs to unlock")
    p_unlock.add_argument("--manifest", default=".slide_locks.json", help="Manifest file path")

    # check
    p_check = sub.add_parser("check", help="Check if a slide ID is locked (exit 0=locked, 1=not locked)")
    p_check.add_argument("--id", required=True, type=int, help="Slide ID to check")
    p_check.add_argument("--manifest", default=".slide_locks.json", help="Manifest file path")

    # verify
    p_verify = sub.add_parser("verify", help="Verify locked slides survived a round-trip")
    p_verify.add_argument("--original", required=True, help="Original PPTX path")
    p_verify.add_argument("--output", required=True, help="Output PPTX path")
    p_verify.add_argument("--manifest", default=".slide_locks.json", help="Manifest file path")

    # show
    p_show = sub.add_parser("show", help="Show manifest contents")
    p_show.add_argument("--manifest", default=".slide_locks.json", help="Manifest file path")

    args = parser.parse_args()

    if args.command == "list":
        cmd_list(args.pptx, args.manifest)

    elif args.command == "lock":
        ids = [int(x) for x in args.ids.split(",")] if args.ids else None
        positions = [int(x) for x in args.positions.split(",")] if args.positions else None
        if not ids and not positions:
            print("ERROR: Provide --ids or --positions", file=sys.stderr)
            sys.exit(1)
        cmd_lock(args.pptx, ids=ids, positions=positions, manifest_path=args.manifest)

    elif args.command == "unlock":
        ids = [int(x) for x in args.ids.split(",")]
        cmd_unlock(ids, manifest_path=args.manifest)

    elif args.command == "check":
        cmd_check(args.id, manifest_path=args.manifest)

    elif args.command == "verify":
        cmd_verify(args.original, args.output, manifest_path=args.manifest)

    elif args.command == "show":
        cmd_show(manifest_path=args.manifest)


if __name__ == "__main__":
    main()
