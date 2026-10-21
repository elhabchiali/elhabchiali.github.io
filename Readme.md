# Ali El Habchi / Portfolio

Research, engineering and teaching in computer vision and applied AI.

Live site: https://elhabchiali.github.io/

## Editing

The site is buildless at runtime. GitHub Pages serves the committed HTML, CSS,
JavaScript and assets from the repository root. No account, API key, analytics
service or external font dependency is needed.

Shared page templates and editorial content live in `scripts/build_site.py`.
After editing that source, regenerate the public HTML:

```sh
python3 scripts/build_site.py
python3 scripts/check_site.py
node --check lab.js
node scripts/test_filters.js
```

The generator uses Python's standard library. Commit generated HTML alongside
the generator. CSS and JavaScript are edited directly.

For a local preview:

```sh
python3 -m http.server 8000
```

Open http://localhost:8000. Root-relative URLs assume the GitHub user-site root.

## Content

- Home and three detailed work pages
- Research and publication records
- Teaching and an interactive image-filtering lab
- About, career timeline and downloadable CV
- Canonical URLs, sharing metadata, structured profile data and sitemap

Career dates supplied by Ali: Onclusive ended September 2025; ENIAD began
October 2025. The internal move from Onclusive Social to Onclusive occurred in
May 2024. PhD completed in 2025.

Industry pages are professional summaries rather than private source-code or
data releases. Research results are explicitly attributed to their papers.
Illustrations are schematics, not recorded flight data or company dashboards.

## Vision lab

`lab.js` applies 3x3 cross-correlation kernels to 128x128 grayscale input.
It supports synthetic samples, local image uploads, replicated edge padding,
Sobel X, box blur, sharpen and identity. Signed results are clipped to 0-255
for display; the raw response and individual products can be inspected.
Images are processed entirely in the browser.

## Checks

The GitHub workflow regenerates pages, checks for uncommitted generated changes,
validates local links and fragments, and checks JavaScript syntax and numerical filter behavior. Before a
release, also check the homepage and lab on narrow and wide viewports, keyboard
focus, reduced-motion behaviour, and the downloadable CV.
