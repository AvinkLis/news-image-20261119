#!/usr/bin/env python3
"""Entry program for the make.fun bounty news-image-20261119.

The picture itself (entry.png, kept beside this file) is the entry: a
front page summing up the world news of Thursday 19 November 2026.
This program's whole job is to deliver that picture to the output
directory — /output inside the grader's container, or the directory in
MAKEFUN_OUTPUT_DIR when run elsewhere. It uses only the standard
library, touches no network, and writes exactly the same bytes on
every run.
"""

import os
import shutil
import struct
from pathlib import Path

HERE = Path(__file__).resolve().parent
PICTURE = HERE / "entry.png"

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
BYTE_LIMIT = 1024 * 1024  # the competition gate: at most 1 MiB
SIDE_LIMIT = 1024  # ... and at most 1024 by 1024 pixels


def main() -> None:
    blob = PICTURE.read_bytes()
    if not blob.startswith(PNG_MAGIC):
        raise SystemExit("entry.png is not a PNG file")
    if len(blob) > BYTE_LIMIT:
        raise SystemExit("entry.png is larger than the 1 MiB gate limit")
    width, height = struct.unpack(">II", blob[16:24])  # the IHDR fields
    if width > SIDE_LIMIT or height > SIDE_LIMIT:
        raise SystemExit("entry.png is larger than the 1024x1024 gate limit")
    target_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    target_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(PICTURE, target_dir / "entry.png")


if __name__ == "__main__":
    main()
