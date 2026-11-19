#!/usr/bin/env python3
"""
Deliver the entry image.

The picture itself (entry.png, drawn by make_image.py) sits next to this
file.  This program checks that it really is a PNG inside the bounty
limits -- at most 1 MiB on disk and at most 1024 px on a side -- and then
copies it into the output directory named by the MAKEFUN_OUTPUT_DIR
environment variable (default: /output).

Standard library only.
"""

import os
import shutil
import struct
import sys
from pathlib import Path

PNG_SIGNATURE = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1_048_576          # 1 MiB
MAX_SIDE = 1024                # px, either dimension


def png_dimensions(blob):
    """(width, height) read straight out of the IHDR chunk."""
    if len(blob) < 24:
        raise ValueError("file too short to hold a PNG header")
    if blob[:8] != PNG_SIGNATURE:
        raise ValueError("missing the PNG magic bytes")
    if blob[12:16] != b"IHDR":
        raise ValueError("first chunk is not IHDR")
    return struct.unpack(">II", blob[16:24])


def check_image(path):
    blob = path.read_bytes()
    if len(blob) > MAX_BYTES:
        raise ValueError(f"{path.name} is {len(blob)} bytes, over the "
                         f"{MAX_BYTES}-byte limit")
    width, height = png_dimensions(blob)
    if width > MAX_SIDE or height > MAX_SIDE:
        raise ValueError(f"{path.name} is {width}x{height}, over the "
                         f"{MAX_SIDE}px limit")
    return width, height, len(blob)


def main():
    here = Path(__file__).resolve().parent
    source = here / "entry.png"
    if not source.is_file():
        print(f"error: {source} not found", file=sys.stderr)
        return 1
    try:
        width, height, nbytes = check_image(source)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    target = out_dir / source.name
    shutil.copyfile(source, target)
    print(f"copied {source.name} ({width}x{height}, {nbytes} bytes) "
          f"-> {target}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
