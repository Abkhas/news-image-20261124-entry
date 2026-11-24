#!/usr/bin/env python3
"""Entrypoint for the n24 news-image entry (Tuesday 24 November 2026).

The page is already drawn and committed as entry.png beside this file.
All this program does is copy that file into the grader's output
folder. It draws nothing, reaches for no network and uses no random
numbers, so both grader runs write byte-identical files.
"""

import os
import shutil
import sys
from pathlib import Path

BYTE_LIMIT = 1_048_576


def main() -> int:
    here = Path(__file__).resolve().parent
    src = here / "entry.png"
    if not src.is_file():
        print("error: entry.png is missing from %s" % here,
              file=sys.stderr)
        return 1

    size = src.stat().st_size
    if size > BYTE_LIMIT:
        print("error: entry.png is %d bytes, over the %d byte limit"
              % (size, BYTE_LIMIT), file=sys.stderr)
        return 1

    dest_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR") or "out")
    dest_dir.mkdir(parents=True, exist_ok=True)
    dest = dest_dir / "entry.png"
    shutil.copyfile(src, dest)
    copied = dest.stat().st_size
    if copied != size:
        print("error: copied %d bytes, expected %d" % (copied, size),
              file=sys.stderr)
        return 1
    print("Wrote %s (%d bytes)" % (dest, size))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
