#!/usr/bin/env python3
"""Compress the JPEGs in your images/ folder for faster loading (better Core Web Vitals).

Usage:   python3 optimize-images.py images
Needs:   pip install pillow

- Resizes anything wider than 1600px (selfie.jpg, the hero background, is allowed 1920px)
- Re-saves as optimised progressive JPEG at quality 78 and strips EXIF/GPS metadata
- Keeps your originals in a sibling folder called <folder>_original
- Only replaces a file if the new version is actually smaller
"""
import shutil
import sys
from pathlib import Path

from PIL import Image, ImageOps

QUALITY = 78
DEFAULT_MAX_WIDTH = 1600
MAX_WIDTH = {"selfie.jpg": 1920}
SKIP = {"og-image.jpg"}  # already optimised, must stay 1200x630


def main() -> None:
    folder = Path(sys.argv[1] if len(sys.argv) > 1 else "images")
    if not folder.is_dir():
        sys.exit(f"Folder not found: {folder}")
    backup = folder.with_name(folder.name + "_original")
    backup.mkdir(exist_ok=True)

    before_total = after_total = 0
    for path in sorted(folder.glob("*.jp*g")):
        if path.name in SKIP:
            continue
        before = path.stat().st_size
        if not (backup / path.name).exists():
            shutil.copy2(path, backup / path.name)
        with Image.open(backup / path.name) as im:
            im = ImageOps.exif_transpose(im).convert("RGB")
            limit = MAX_WIDTH.get(path.name, DEFAULT_MAX_WIDTH)
            if im.width > limit:
                im = im.resize((limit, round(im.height * limit / im.width)), Image.LANCZOS)
            tmp = path.with_suffix(".tmp.jpg")
            im.save(tmp, "JPEG", quality=QUALITY, optimize=True, progressive=True)
        if tmp.stat().st_size < before:
            tmp.replace(path)
        else:
            tmp.unlink()
        after = path.stat().st_size
        before_total += before
        after_total += after
        print(f"{path.name:<16} {before/1024:8.0f} KB -> {after/1024:8.0f} KB")

    if before_total:
        saved = 100 * (1 - after_total / before_total)
        print(f"\nTotal {before_total/1024/1024:.1f} MB -> {after_total/1024/1024:.1f} MB ({saved:.0f}% smaller)")
    else:
        print("No JPEGs found.")


if __name__ == "__main__":
    main()
