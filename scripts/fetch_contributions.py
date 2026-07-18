#!/usr/bin/env python3
"""
fetch_contributions.py

Scrapes the *public* HTML fragment GitHub serves at:
    https://github.com/users/<username>/contributions
(the same fragment your profile page loads to draw the calendar).

No GraphQL API, no personal access token required.

Writes data/contributions.json with:
  - the raw day-by-day calendar (date, level 0-4, count)
  - derived stats: total, current streak, longest streak, best day,
    monthly totals

Usage:
    python scripts/fetch_contributions.py [github-username]

If no username is given, falls back to the GITHUB_USERNAME env var.
"""

import os
import re
import sys
import json
from datetime import datetime, timezone

import requests
from bs4 import BeautifulSoup

CONTRIB_URL = "https://github.com/users/{username}/contributions"
OUT_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "contributions.json")

HEADERS = {
    # A normal browser UA avoids being served a stripped-down response.
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
    )
}

TOOLTIP_RE = re.compile(r"^(No|\d[\d,]*)\s+contributions?\s+on", re.IGNORECASE)


def get_username():
    if len(sys.argv) > 1:
        return sys.argv[1]
    env_user = os.environ.get("GITHUB_USERNAME")
    if env_user:
        return env_user
    raise SystemExit(
        "No username given. Usage: python scripts/fetch_contributions.py <username>\n"
        "(or set the GITHUB_USERNAME environment variable)"
    )


def parse_count(tooltip_text):
    """'5 contributions on July 13th.' -> 5   /   'No contributions on ...' -> 0"""
    if not tooltip_text:
        return 0
    m = TOOLTIP_RE.match(tooltip_text.strip())
    if not m:
        return 0
    raw = m.group(1)
    if raw.lower() == "no":
        return 0
    return int(raw.replace(",", ""))


def fetch_calendar(username):
    url = CONTRIB_URL.format(username=username)
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    soup = BeautifulSoup(resp.text, "html.parser")

    day_cells = soup.select("td.ContributionCalendar-day[data-date]")
    if not day_cells:
        raise RuntimeError(
            f"No contribution cells found for '{username}'. "
            "GitHub may have changed its markup, or the username is wrong/private."
        )

    # tool-tip elements carry the exact contribution count and are linked
    # to a day cell via the `for` attribute -> that cell's `id`.
    tooltip_by_id = {}
    for tip in soup.select("tool-tip[for]"):
        tooltip_by_id[tip.get("for")] = tip.get_text(strip=True)

    days = []
    for td in day_cells:
        date_str = td["data-date"]
        level = int(td.get("data-level", 0))
        tooltip_text = tooltip_by_id.get(td.get("id"))
        count = parse_count(tooltip_text)
        days.append({"date": date_str, "level": level, "count": count})

    days.sort(key=lambda d: d["date"])
    return days


def compute_stats(days):
    total = sum(d["count"] for d in days)

    # Current streak: walk backwards from the most recent day. If the very
    # last day (usually "today") has 0 contributions yet, skip it rather
    # than zeroing the streak, since today isn't over yet.
    current_streak = 0
    idx = len(days) - 1
    if idx >= 0 and days[idx]["count"] == 0:
        idx -= 1
    while idx >= 0 and days[idx]["count"] > 0:
        current_streak += 1
        idx -= 1

    # Longest streak: max run of consecutive days with count > 0.
    longest_streak = 0
    run = 0
    for d in days:
        if d["count"] > 0:
            run += 1
            longest_streak = max(longest_streak, run)
        else:
            run = 0

    best_day = max(days, key=lambda d: d["count"]) if days else None

    monthly_totals = {}
    for d in days:
        month_key = d["date"][:7]  # YYYY-MM
        monthly_totals[month_key] = monthly_totals.get(month_key, 0) + d["count"]

    return {
        "total_contributions": total,
        "current_streak": current_streak,
        "longest_streak": longest_streak,
        "best_day": best_day,
        "monthly_totals": monthly_totals,
    }


def main():
    username = get_username()
    days = fetch_calendar(username)
    stats = compute_stats(days)

    payload = {
        "username": username,
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        **stats,
        "days": days,
    }

    os.makedirs(os.path.dirname(OUT_PATH), exist_ok=True)
    with open(OUT_PATH, "w") as f:
        json.dump(payload, f, indent=2)

    print(
        f"Wrote {OUT_PATH}: {stats['total_contributions']} contributions, "
        f"current streak {stats['current_streak']}, "
        f"longest streak {stats['longest_streak']}"
    )


if __name__ == "__main__":
    main()
