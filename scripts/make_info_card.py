#!/usr/bin/env python3
"""
make_info_card.py

Hand-authors a small neofetch-style SVG panel: a title bar, then colored
key/value rows. Each row fades + slides in on a short stagger so it looks
like it's printing next to the ASCII portrait, then freezes (no looping).

Set STATIC=1 to emit a frozen, non-animated frame (handy for local
Quick Look / image-viewer previews where SMIL/CSS animation won't play).

>>> EDIT THE CONFIG BELOW WITH YOUR OWN INFO <<<

Output: info-card.svg
"""

import os

OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "info-card.svg")
STATIC = os.environ.get("STATIC") == "1"

# ---------------------------------------------------------------------------
# EDIT ME: this is the content of the card. Keep it to the story numbers
# can't tell -- the heatmap above already covers your GitHub stats.
# ---------------------------------------------------------------------------
CONFIG = {
    "user_at_host": "you@github",
    "rows": [
        ("Now", "Building things I'd want to use"),
        ("Prev", "Add your last role / focus here"),
        ("Stack", "Python \u00b7 TypeScript \u00b7 React \u00b7 PostgreSQL"),
        ("Highlights", "Add 1-2 things you're proud of"),
    ],
}

# Colors (roughly matches a common neofetch color scheme)
BG = "#0d1117"
BORDER = "#30363d"
TITLE_BAR = "#161b22"
KEY_COLOR = "#39d353"     # bright green, like a neofetch label
VAL_COLOR = "#c9d1d9"
DIM_COLOR = "#7d8590"
PROMPT_COLOR = "#69f0a0"

WIDTH = 490
ROW_H = 34
TITLE_H = 32
PAD_X = 20
STAGGER = 0.18   # seconds between each row's fade-in
DUR = 0.45


def esc(text):
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def build_svg():
    rows = CONFIG["rows"]
    height = TITLE_H + len(rows) * ROW_H + 18

    parts = []
    parts.append(
        f'<svg viewBox="0 0 {WIDTH} {height}" width="{WIDTH}" height="{height}" '
        f'xmlns="http://www.w3.org/2000/svg" font-family="\'Courier New\', ui-monospace, '
        f'SFMono-Regular, monospace">'
    )

    if not STATIC:
        parts.append(f"""
  <style>
    .row {{
      opacity: 0;
      transform: translateX(-8px);
      animation-name: type-in;
      animation-duration: {DUR}s;
      animation-timing-function: ease-out;
      animation-fill-mode: forwards;
    }}
    @keyframes type-in {{
      0%   {{ opacity: 0; transform: translateX(-8px); }}
      100% {{ opacity: 1; transform: translateX(0px); }}
    }}
  </style>
""")

    # Card background + border
    parts.append(
        f'<rect x="0.5" y="0.5" width="{WIDTH - 1}" height="{height - 1}" rx="8" '
        f'fill="{BG}" stroke="{BORDER}"/>'
    )

    # Title bar
    parts.append(f'<rect x="0.5" y="0.5" width="{WIDTH - 1}" height="{TITLE_H}" rx="8" fill="{TITLE_BAR}"/>')
    parts.append(f'<rect x="0.5" y="{TITLE_H - 8}" width="{WIDTH - 1}" height="8" fill="{TITLE_BAR}"/>')
    # traffic-light dots
    for i, dot_color in enumerate(["#ff5f56", "#ffbd2e", "#27c93f"]):
        parts.append(f'<circle cx="{18 + i * 16}" cy="{TITLE_H / 2}" r="5" fill="{dot_color}"/>')
    parts.append(
        f'<text x="{WIDTH / 2}" y="{TITLE_H / 2 + 4}" text-anchor="middle" '
        f'fill="{DIM_COLOR}" font-size="12">{esc(CONFIG["user_at_host"])}</text>'
    )

    # prompt line
    prompt_y = TITLE_H + 24
    parts.append(
        f'<text x="{PAD_X}" y="{prompt_y}" font-size="13">'
        f'<tspan fill="{PROMPT_COLOR}">$</tspan> '
        f'<tspan fill="{VAL_COLOR}">neofetch</tspan></text>'
    )

    key_w = max(len(k) for k, _ in rows) * 8 + 12

    for i, (key, value) in enumerate(rows):
        y = TITLE_H + 24 + (i + 1) * ROW_H
        row_attrs = "" if STATIC else f' class="row" style="animation-delay:{i * STAGGER:.2f}s"'
        parts.append(f'<g{row_attrs}>')
        parts.append(
            f'<text x="{PAD_X}" y="{y}" font-size="13" font-weight="bold" fill="{KEY_COLOR}">{esc(key)}</text>'
        )
        parts.append(
            f'<text x="{PAD_X + key_w}" y="{y}" font-size="13" fill="{VAL_COLOR}">{esc(value)}</text>'
        )
        parts.append("</g>")

    parts.append("</svg>")
    return "\n".join(parts)


def main():
    svg = build_svg()
    with open(OUT_PATH, "w") as f:
        f.write(svg)
    mode = "static" if STATIC else "animated"
    print(f"Wrote {OUT_PATH} ({mode}, {len(svg)} bytes)")


if __name__ == "__main__":
    main()
