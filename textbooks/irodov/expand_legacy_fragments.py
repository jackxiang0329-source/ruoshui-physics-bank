#!/usr/bin/env python3
"""Restore untracked legacy TeX fragments for older regression entrypoints.

The repository tracks 40 compact section files. Historical QA still imports
the 164 original split fragments by filename. This deterministic compatibility
step reconstructs them from exact embedded bytes (and verifies Git blob SHA1).
It must not commit the transient files. No network or external packages.
"""
from pathlib import Path
import hashlib
import re

ROOT = Path(__file__).resolve().parent
CHAPTERS = ROOT / "chapters"
START = re.compile(
    r"(?ms)^% === BEGIN "
    r"(\d{2}-[a-z0-9-]+-\d{3}-\d{3}\.tex) "
    r"blob ([0-9a-f]{40}) ===\n"
    r"(.*?)"
    r"^% === END \1 ===(?:\n|$)"
)


def git_blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest()


def main() -> None:
    sections = sorted(
        p for p in CHAPTERS.glob("*.tex")
        if re.fullmatch(r"\d{2}-[a-z0-9-]+\.tex", p.name)
    )
    if len(sections) != 40:
        raise RuntimeError(f"Expected 40 compact sections, found {len(sections)}")
    seen: dict[str, bytes] = {}
    for section in sections:
        source = section.read_text(encoding="utf-8")
        blocks = list(START.finditer(source))
        if not blocks:
            raise RuntimeError(f"No recoverable fragments in {section}")
        for match in blocks:
            name, expected_sha, raw = match.groups()
            if name in seen:
                raise RuntimeError(f"Duplicate old source fragment: {name}")
            data = raw.encode("utf-8")
            if git_blob_sha(data) != expected_sha and data.endswith(b"\n"):
                # A no-final-newline source had one separator newline added.
                data = data[:-1]
            if git_blob_sha(data) != expected_sha:
                raise RuntimeError(f"Git blob hash mismatch for {name}")
            seen[name] = data
    if len(seen) != 164:
        raise RuntimeError(f"Expected 164 legacy fragments, found {len(seen)}")
    for name, data in seen.items():
        destination = CHAPTERS / name
        if destination.exists():
            if destination.read_bytes() != data:
                raise RuntimeError(f"Conflicting transient fragment: {name}")
        else:
            destination.write_bytes(data)
    print("PASS: 164 historical TeX views restored exactly from 40 tracked section files.")
    print("These 164 compatibility fragments are untracked and must not be committed.")


if __name__ == "__main__":
    main()
