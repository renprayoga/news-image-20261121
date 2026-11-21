#!/usr/bin/env python3
"""Entry point for news-image-20261121: "The World in One Image".

Copies the pre-rendered entry.png (produced by render.py in this
same directory) byte for byte into the output directory as entry.png.

Standard library only. No network, no clock, no randomness, no
re-rendering: whatever the grader runs, the bytes it writes are the
bytes that were verified here, so two runs always agree.
"""

import hashlib
import os
import shutil
import sys
from pathlib import Path

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    repo_root = Path(__file__).resolve().parent
    source = repo_root / "entry.png"
    if not source.is_file():
        print(f"missing {source}", file=sys.stderr)
        return 1
    with open(source, "rb") as handle:
        head = handle.read(len(PNG_MAGIC))
    if head != PNG_MAGIC:
        print("entry.png is not a PNG file", file=sys.stderr)
        return 1

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    dest = out_dir / "entry.png"
    shutil.copyfile(source, dest)

    if sha256_of(dest) != sha256_of(source):
        print("copy mismatch: destination differs from source",
              file=sys.stderr)
        return 1
    print(f"wrote {dest} ({dest.stat().st_size} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
