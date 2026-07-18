#!/usr/bin/env python3

"""
render_heatmap_svg.py

Reads data/contributions.json (written by fetch_contributions.py) and draws
the classic 53-week x 7-day GitHub calendar as a self-contained animated SVG.

Reveal animation: boxes slide down + fade in, one diagonal at a time
(week_index + weekday_index -> same delay), then freeze. No looping.

Output: contrib-heatmap.svg
"""

import os
import json
from datetime import datetime, timedelta

DATA_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "contributions.json")
OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "contrib-heatmap.svg")

# none -> brightest. Level 5 is a bonus "neon" tier we add on top of
# GitHub's real 0-4 levels, reserved for your very best days, purely for flair.
PALETTE = ["#161b22", "#0e4429", "#006d32", "#26a641", "#39d353", "#69f0a0"]

CELL = 11          # box size in px
GAP = 3             # gap between boxes
RADIUS = 2           # corner radius
LEFT_PAD = 28        # room for weekday labels (Mon/Wed/Fri)
TOP_PAD = 20          # room for month labels
STAGGER = 0.012      # seconds of delay added per diagonal step
DUR = 0.35           # seconds each box takes to animate in

WEEKDAY_LABELS = {1: "Mon", 3: "Wed", 5: "Fri"}
MONTH_ABBR = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
              "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def load_data():
    with open(DATA_PATH) as f:
        return json.load(f)


def to_grid(days):
    """Map each day to (week_col, weekday_row) using GitHub's Sunday-start grid."""
    parsed = [dict(d, dt=datetime.strptime(d["date"], "%Y-%m-%d")) for d in days]
    start = min(d["dt"] for d in parsed)
    anchor_sunday = start - timedelta(days=(start.weekday() + 1) % 7)

    cells = []
    max_week = 0
    for d in parsed:
        weekday_row = (d["dt"].weekday() + 1) % 7  # Sunday = 0
        week_col = (d["dt"] - anchor_sunday).days // 7
        max_week = max(max_week, week_col)
        cells.append({**d, "col": week_col, "row": weekday_row})
    return cells, max_week + 1


def boost_top_days(cells):
    """Promote a handful of the very best days from level 4 to level 5."""
    nonzero_counts = sorted((c["count"] for c in cells if c["count"] > 0), reverse=True)
    if len(nonzero_counts) < 10:
        return cells
    threshold = nonzero_counts[max(0, len(nonzero_counts) // 20)]  # top ~5%
    for c in cells:
        if c["level"] >= 4 and c["count"] >= threshold:
            c["level"] = 5
    return cells


def month_labels(cells):
    """Return [(week_col, 'Jan'), ...] for the first week each month appears in."""
    seen = {}
    for c in cells:
        month = c["dt"].month
        if month not in seen or c["col"] < seen[month]:
            seen[month] = c["col"]
    return sorted(((col, MONTH_ABBR[m - 1]) for m, col in seen.items()), key=lambda x: x[0])


def esc(text):
    return (
        str(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def build_svg(data):
    cells, n_weeks = to_grid(data["days"])
    cells = boost_top_days(cells)

    grid_w = n_weeks * (CELL + GAP) - GAP
    grid_h = 7 * (CELL + GAP) - GAP
    width = LEFT_PAD + grid_w + 20
    legend_h = 26
    footer_h = 26
    height = TOP_PAD + grid_h + legend_h + footer_h + 16

    parts = []
    parts.append(
        f'<svg viewBox="0 0 {width} {height}" width="{width}" height="{height}" '
        f'xmlns="http://www.w3.org/2000/svg" font-family="\'Courier New\', ui-monospace, '
        f'SFMono-Regular, monospace">'
    )

    parts.append(f"""
  <style>
    .bg {{ fill: #0d1117; }}
    .lbl {{ fill: #7d8590; font-size: 10px; }}
    .footer {{ fill: #c9d1d9; font-size: 11px; }}
    .box {{
      opacity: 0;
      transform: translate(0px, -6px);
      animation-name: reveal;
      animation-duration: {DUR}s;
      animation-timing-function: ease-out;
      animation-fill-mode: forwards;
    }}
    @keyframes reveal {{
      0%   {{ opacity: 0; transform: translate(0px, -6px); }}
      100% {{ opacity: 1; transform: translate(0px, 0px); }}
    }}
  </style>
""")

    parts.append(f'<rect class="bg" x="0" y="0" width="{width}" height="{height}" rx="6"/>')

    # Month labels
    for col, label in month_labels(cells):
        x = LEFT_PAD + col * (CELL + GAP)
        parts.append(f'<text class="lbl" x="{x}" y="{TOP_PAD - 7}">{label}</text>')

    # Weekday labels
    for row, label in WEEKDAY_LABELS.items():
        y = TOP_PAD + row * (CELL + GAP) + CELL - 2
        parts.append(f'<text class="lbl" x="0" y="{y}">{label}</text>')

    # Day boxes, diagonal stagger by (col + row)
    for c in cells:
        x = LEFT_PAD + c["col"] * (CELL + GAP)
        y = TOP_PAD + c["row"] * (CELL + GAP)
        color = PALETTE[min(c["level"], len(PALETTE) - 1)]
        delay = (c["col"] + c["row"]) * STAGGER
        title = f'{c["count"]} contribution{"s" if c["count"] != 1 else ""} on {c["date"]}'
        parts.append(
            f'<rect class="box" x="{x}" y="{y}" width="{CELL}" height="{CELL}" '
            f'rx="{RADIUS}" ry="{RADIUS}" fill="{color}" '
            f'style="animation-delay:{delay:.3f}s"><title>{esc(title)}</title></rect>'
        )

    # Legend: Less [boxes] More
    legend_y = TOP_PAD + grid_h + 20
    lx = LEFT_PAD
    parts.append(f'<text class="lbl" x="{lx}" y="{legend_y + 8}">Less</text>')
    lx += 32
    for color in PALETTE:
        parts.append(
            f'<rect x="{lx}" y="{legend_y}" width="{CELL - 1}" height="{CELL - 1}" '
            f'rx="{RADIUS}" fill="{color}"/>'
        )
        lx += CELL + 2
    parts.append(f'<text class="lbl" x="{lx + 4}" y="{legend_y + 8}">More</text>')

    # Footer stats
    footer_y = legend_y + 26
    total = data["total_contributions"]
    streak = data["current_streak"]
    longest = data["longest_streak"]
    footer_text = (
        f'{total:,} contributions in the last year '
        f'\u00b7 current streak {streak}d \u00b7 longest streak {longest}d'
    )
    parts.append(f'<text class="footer" x="{LEFT_PAD}" y="{footer_y}">{esc(footer_text)}</text>')

    parts.append("</svg>")
    return "\n".join(parts)


def main():
    data = load_data()
    svg = build_svg(data)
    with open(OUT_PATH, "w") as f:
        f.write(svg)
    print(f"Wrote {OUT_PATH} ({len(svg)} bytes)")


if __name__ == "__main__":
    main()
