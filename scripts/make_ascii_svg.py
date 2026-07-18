#!/usr/bin/env python3
"""
make_ascii_svg.py

Converts a prepped grayscale image (see prep_photo.py) into a monochrome,
self-typing ASCII-art SVG.

Each pixel's brightness picks a glyph from a density ramp (sparse for
bright, dense for dark). Each row wipes in left-to-right with a small
block "cursor" riding the edge, staggered top to bottom. Prints once and
freezes -- no looping.

Usage:
    python scripts/make_ascii_svg.py [source-prepped.png]

Output: ascii-portrait.svg  (feel free to rename the OUT_PATH below --
the README just needs to point at whatever you call it)
"""

import os
import sys

from PIL import Image

SRC_DEFAULT = os.path.join(os.path.dirname(__file__), "..", "source-prepped.png")
OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "ascii-portrait.svg")

# bright (sparse) -> dark (dense). Leading space clears background to nothing.
RAMP = " .`:-=+*cs#%@"

COLS = 100                # character grid width
CHAR_W = 6.2               # px per character cell (monospace-ish)
CHAR_H = 11                 # px per row (line height)
CHAR_ASPECT = CHAR_W / CHAR_H   # terminal chars are taller than wide; corrects the grid so the portrait isn't stretched

FILL_COLOR = "#c9d1d9"     # single light-gray fill -- monochrome by design
CURSOR_COLOR = "#39d353"

ROW_STAGGER = 0.05         # seconds between each row starting to type
CHAR_DUR = 0.012           # seconds per character revealed within a row


def load_grid(path):
    img = Image.open(path).convert("L")  # grayscale
    w, h = img.size
    rows = max(1, round((h / w) * COLS * CHAR_ASPECT))
    small = img.resize((COLS, rows), Image.LANCZOS)
    pixels = small.load()

    grid = []
    for y in range(rows):
        row = []
        for x in range(COLS):
            brightness = pixels[x, y]  # 0 = black, 255 = white
            idx = int((255 - brightness) / 255 * (len(RAMP) - 1))
            row.append(RAMP[idx])
        grid.append("".join(row))
    return grid


def esc(ch):
    return {"&": "&amp;", "<": "&lt;", ">": "&gt;"}.get(ch, ch)


def build_svg(grid):
    width = COLS * CHAR_W + 20
    height = len(grid) * CHAR_H + 20

    parts = []
    parts.append(
        f'<svg viewBox="0 0 {width:.0f} {height:.0f}" width="{width:.0f}" height="{height:.0f}" '
        f'xmlns="http://www.w3.org/2000/svg" font-family="\'Courier New\', ui-monospace, '
        f'SFMono-Regular, monospace" font-size="{CHAR_H - 1}">'
    )
    parts.append(f'<rect x="0" y="0" width="{width:.0f}" height="{height:.0f}" fill="#0d1117"/>')

    clip_id_n = 0
    for row_i, row_text in enumerate(grid):
        trimmed = row_text.rstrip()
        if not trimmed:
            continue

        row_len = len(trimmed)
        y = 14 + row_i * CHAR_H
        row_begin = row_i * ROW_STAGGER
        row_dur = max(0.08, row_len * CHAR_DUR)
        clip_id = f"clip{clip_id_n}"
        clip_id_n += 1

        clip_width_full = row_len * CHAR_W

        # A clipPath rect that wipes from 0 -> full width, revealing the
        # text underneath left-to-right. fill="freeze" keeps the final
        # (fully revealed) frame after the animation ends.
        parts.append(f'<clipPath id="{clip_id}">')
        parts.append(
            f'  <rect x="10" y="{y - CHAR_H + 3:.1f}" width="0" height="{CHAR_H}">'
            f'<animate attributeName="width" from="0" to="{clip_width_full:.1f}" '
            f'begin="{row_begin:.3f}s" dur="{row_dur:.3f}s" fill="freeze"/>'
            f'</rect>'
        )
        parts.append("</clipPath>")

        escaped = "".join(esc(c) for c in trimmed)
        parts.append(
            f'<text x="10" y="{y:.1f}" fill="{FILL_COLOR}" clip-path="url(#{clip_id})" '
            f'xml:space="preserve">{escaped}</text>'
        )

        # small block cursor riding the wipe edge, then fading out once done
        cursor_x_start = 10
        cursor_x_end = 10 + clip_width_full
        parts.append(
            f'<rect x="{cursor_x_start}" y="{y - CHAR_H + 3:.1f}" width="{CHAR_W:.1f}" height="{CHAR_H}" '
            f'fill="{CURSOR_COLOR}">'
            f'<animate attributeName="x" from="{cursor_x_start}" to="{cursor_x_end:.1f}" '
            f'begin="{row_begin:.3f}s" dur="{row_dur:.3f}s" fill="freeze"/>'
            f'<animate attributeName="opacity" from="1" to="0" '
            f'begin="{row_begin + row_dur:.3f}s" dur="0.15s" fill="freeze"/>'
            f'</rect>'
        )

    parts.append("</svg>")
    return "\n".join(parts)


def main():
    src = sys.argv[1] if len(sys.argv) > 1 else SRC_DEFAULT
    if not os.path.exists(src):
        raise SystemExit(
            f"Source image not found: {src}\n"
            "Run prep_photo.py first (python scripts/prep_photo.py your-photo.jpg)."
        )
    grid = load_grid(src)
    svg = build_svg(grid)
    with open(OUT_PATH, "w") as f:
        f.write(svg)
    print(f"Wrote {OUT_PATH} ({len(grid)} rows x {COLS} cols, {len(svg)} bytes)")


if __name__ == "__main__":
    main()
