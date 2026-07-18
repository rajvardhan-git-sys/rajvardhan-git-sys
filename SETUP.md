# Setup guide

All 8 files in this bundle are tested and working (I ran the full pipeline
against real GitHub data before handing this to you). Here's how to get it
live on your profile.

## 1. Create your profile repo

GitHub renders a special README on your profile page if you create a repo
with the *exact same name as your username*.

```bash
gh repo create YOUR_USERNAME --public --clone
cd YOUR_USERNAME
```

Copy all the files from this bundle into that folder, preserving the
structure:

```
YOUR_USERNAME/
├── README.md
├── scripts/
│   ├── requirements.txt
│   ├── requirements-ci.txt
│   ├── prep_photo.py
│   ├── make_ascii_svg.py
│   ├── make_info_card.py
│   ├── fetch_contributions.py
│   └── render_heatmap_svg.py
├── data/
│   └── .gitkeep
└── .github/workflows/update-profile-art.yml
```

## 2. Personalize the info card

Open `scripts/make_info_card.py` and edit the `CONFIG` dict near the top —
that's your role, previous focus, stack, and highlights. This is the only
file with placeholder text you need to fill in by hand (I didn't have your
bio, so I left it as clearly-marked placeholders).

## 3. Generate your ASCII portrait (one-time, local only)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r scripts/requirements.txt
python scripts/prep_photo.py your-photo.jpg      # writes source-prepped.png
python scripts/make_ascii_svg.py                  # writes ascii-portrait.svg
```

Look at `source-prepped.png` before converting — if the background-removal
step (`rembg`) missed something or the contrast looks off, that's the file
to fix (crop tighter, better lighting, etc.) rather than fighting the ASCII
step itself.

## 4. Generate the info card + heatmap once, to test locally

```bash
python scripts/make_info_card.py
python scripts/fetch_contributions.py YOUR_USERNAME
python scripts/render_heatmap_svg.py
```

Open the three `.svg` files in a browser tab (not an image viewer — some
image viewers don't run SVG animations) to see them play.

## 5. Push everything

```bash
git add .
git commit -m "Set up animated profile README"
git push
```

## 6. Turn on the daily auto-refresh

The workflow in `.github/workflows/update-profile-art.yml` re-scrapes your
contributions and re-renders the heatmap every day at ~06:17 UTC, and
commits the result back. It does **not** touch your portrait or info card —
those only change when you re-run their scripts by hand.

Go to your repo's **Actions** tab and click **"Run workflow"** once by hand
(`workflow_dispatch`) to confirm it commits a fresh SVG before you trust the
cron.

## Notes / things worth knowing

- **No token needed.** `fetch_contributions.py` scrapes the public HTML
  GitHub already serves at `github.com/users/<you>/contributions` — the
  same fragment your profile page loads. No GraphQL API, no PAT, so
  there's no secret to manage in Actions.
- **Why the animation survives GitHub's sanitizer:** GitHub strips
  `<script>` and inline `style=` from README *HTML*, but an SVG referenced
  via `<img src="...">` is loaded as its own standalone document by the
  browser — completely outside README sanitization. That's why the CSS
  keyframes / SMIL `<animate>` tags inside the SVGs actually play.
- **Only `<br>` controls vertical spacing** in the README; `margin`/`padding`
  in inline styles get stripped. Use `<h3>` instead of `<h1>`/`<h2>` if you
  don't want GitHub's full-width divider line under a heading.
- Keep the `<img>` widths adding up (`370 + 490 = 860` to match the heatmap)
  so the two blocks line up visually.
