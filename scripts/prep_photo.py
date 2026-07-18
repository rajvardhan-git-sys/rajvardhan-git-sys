#!/usr/bin/env python3
"""
prep_photo.py

Turns a normal photo into a clean, high-contrast grayscale image that
converts well to ASCII. A flatly-lit face converts to a dark, unreadable
blob without this step.

1. Remove the background (rembg) so only the subject remains.
2. Boost local contrast with CLAHE (contrast-limited adaptive histogram
   equalization) -- this is what gives a flat face real highlights/shadows.
3. Composite onto pure white so the background maps to the blank end of
   the ASCII ramp (white -> space character).

Run this once per photo (not part of the daily automation -- only the
portrait libraries below need it):

    python scripts/prep_photo.py source-photo.jpg

Output: source-prepped.png
"""

import sys
import os

import numpy as np
import cv2
from PIL import Image
from rembg import remove

OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "source-prepped.png")


def remove_background(path):
    with open(path, "rb") as f:
        input_bytes = f.read()
    output_bytes = remove(input_bytes)  # returns RGBA PNG bytes, subject isolated
    from io import BytesIO
    return Image.open(BytesIO(output_bytes)).convert("RGBA")


def boost_contrast(rgba_img):
    """Apply CLAHE on the luminance channel only, so colors don't posterize."""
    rgb = np.array(rgba_img.convert("RGB"))
    lab = cv2.cvtColor(rgb, cv2.COLOR_RGB2LAB)
    l_channel, a_channel, b_channel = cv2.split(lab)

    clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(8, 8))
    l_boosted = clahe.apply(l_channel)

    lab_boosted = cv2.merge((l_boosted, a_channel, b_channel))
    rgb_boosted = cv2.cvtColor(lab_boosted, cv2.COLOR_LAB2RGB)

    boosted = Image.fromarray(rgb_boosted).convert("RGBA")
    boosted.putalpha(rgba_img.getchannel("A"))  # keep original transparency mask
    return boosted


def composite_on_white(rgba_img):
    white_bg = Image.new("RGBA", rgba_img.size, (255, 255, 255, 255))
    composited = Image.alpha_composite(white_bg, rgba_img)
    return composited.convert("L")  # grayscale


def main():
    if len(sys.argv) < 2:
        raise SystemExit("Usage: python scripts/prep_photo.py <source-photo.jpg>")
    src = sys.argv[1]
    if not os.path.exists(src):
        raise SystemExit(f"File not found: {src}")

    print("Removing background...")
    no_bg = remove_background(src)

    print("Boosting local contrast (CLAHE)...")
    boosted = boost_contrast(no_bg)

    print("Compositing onto white...")
    final = composite_on_white(boosted)

    final.save(OUT_PATH)
    print(f"Wrote {OUT_PATH} ({final.size[0]}x{final.size[1]})")
    print("Next: python scripts/make_ascii_svg.py")


if __name__ == "__main__":
    main()
