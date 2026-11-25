#!/usr/bin/env python3
"""Entry point for the news-image-20261124 submission.

The page is a finished image: entry.png sits next to this file in the repo.
This script only copies that committed image into the output directory.
It never re-renders anything — the pixels submitted are the pixels built.
"""
import hashlib
import os
import shutil
import sys
from pathlib import Path

BYTE_LIMIT = 1_048_576


def sha256_of(path):
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    here = Path(__file__).resolve().parent
    src = here / "entry.png"
    if not src.is_file():
        print("error: entry.png is missing from %s" % here, file=sys.stderr)
        return 1
    size = src.stat().st_size
    if size > BYTE_LIMIT:
        print("error: entry.png is %d bytes, over the %d byte limit"
              % (size, BYTE_LIMIT), file=sys.stderr)
        return 1
    if len(sys.argv) > 1:
        dest_dir = Path(sys.argv[1])
    else:
        dest_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output")
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / "entry.png"
    shutil.copyfile(src, dest)
    copied = dest.stat().st_size
    if copied != size:
        print("error: copied %d bytes, expected %d" % (copied, size),
              file=sys.stderr)
        return 1
    if sha256_of(dest) != sha256_of(src):
        print("error: copied file hash differs from entry.png",
              file=sys.stderr)
        return 1
    print("Wrote %s (%d bytes)" % (dest, size))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
