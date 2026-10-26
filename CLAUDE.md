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

## Design rules (brief v3: docs/portfolio-brief-v3.md)

- Plus Jakarta Sans (self-hosted in assets/fonts). Tokens in assets/style.css:
  blue #1B3A6B, amber #F2A900 (text on blue only), gold text #9A6500 (accent words
  on white), chalk #F3EBD3, grey #F4F4F2. One italic accent word per main heading:
  write it as *word* in headings.
- WCAG 2.2 AA: heading order, visible focus, alt text, 44px targets, 320px with no
  sideways scroll, reduced motion respected. The project banner must stay pausable.
- Case studies are content/work/NN-slug.md, written as +++ sections
  (about, challenge, process, insights, thinking, solution, impact, reflection, sources).
  draft: true shows a case study in the preview only (Wales is a draft until Azka
  approves its reflection and image).
- Project cards on Home and Work come from content/projects.md. Testimonials appear
  only when content/testimonials.md has a real quote.
- About page: intro, chalk journey (layout: chapter / stop / today, line drawn by
  assets/about.js), research map with pin bubbles, banner, principles, education.
- Private facts (client names etc.) live outside the repo in ../private-docs/.
  Never copy them into the repo.

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
- Testimonials (content/testimonials.md) are copied word for word from what Azka
  sends, typos and all. Never shorten, correct or anonymise them.
- The repo is public and keeps its history, so don't commit anything private.
