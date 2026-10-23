# Notes for Claude: Azka Rifky's portfolio

Read this before changing anything. README.md explains the site for Azka;
this file records how we have worked together so far.

## The site

- Live: https://azkarifky1997.github.io/portfolio/
- Repo: https://github.com/Azkarifky1997/portfolio (public)
- Static site built by `build.py` (Python, Markdown + Pillow) into `_site/`.
  GitHub Actions (`.github/workflows/deploy.yml`) builds and publishes on every
  push to `main`.
- Content lives in `content/` (home.md, skills.md, about.md, contact.md,
  work/NN-*.md). The number prefix sets the case study order and the
  "Next case study" links.
- Preview locally: `.venv/bin/python build.py --serve` then http://localhost:8000.
  First time: `python3 -m venv .venv && .venv/bin/pip install -r requirements.txt`.
  Preview mode shows dashed placeholders for missing pictures; the live build never does.

## How Azka likes to work

- Always show a local preview first and only publish (commit + push) when she says so.
- Use her text exactly as written. Don't invent facts, numbers, quotes or names.
  Ask if something seems missing.
- Explain things in plain English, without jargon.
- She often edits on github.com, so `git pull --rebase` before making changes.

## Design rules

- Montserrat (self-hosted in assets/fonts), teal #1F4E5F for text and links,
  ochre #C8962E for decoration only (it fails contrast as text).
- WCAG 2.2 AA: keep heading order, visible focus, alt text on every image.
- Mobile first: check there is no sideways scrolling at 375px.
- Case study photos (JPEG) show small; diagrams (PNG) show wide.
- Home: hero, teal proof band, about me, selected work grid (Rural Loan featured),
  cream "What I do", "How I run research", teal "Let's talk". Gold is for lines only.
- About: intro, "My journey" (layout: journey/chapter/period/stop, chalk line drawn
  by assets/about.js), research map (layout: map, assets/world-land.svg),
  "Projects at a glance" banner (must stay pausable, WCAG 2.2.2), principles, education.
- Work page /work/ from content/projects.md with accessible filters (assets/work.js).
- Job title everywhere: "UX researcher, specialising in inclusive research and service design".
- Bus results: 38% and 23% year on year on two routes, 13% weekends on the third.
  Never "40%".
- No em dashes in site copy.

## Rules for content

- Every image needs alt text. The build stops if a picture has an empty `[ ]`
  description (or an empty `photo_alt:`), which is deliberate.
- File names with spaces are fine. Image URLs include a content fingerprint,
  so re-uploads show straight away.
- Anonymised case studies (member services, rural bus) must stay anonymised:
  no client names, place names, route numbers, operator names or logos, and no
  specific membership levels or processes. Blur identifying details in photos.
  Before publishing changes to those pages, check the wording stays generic.
- Don't add links to GSMA articles unless Azka gives them.
- Her email and phone are on the Contact page by her choice. Never add a home
  address, visa status, or anything about her employer's business situation.
- The repo is public and keeps its history, so don't commit anything private.
