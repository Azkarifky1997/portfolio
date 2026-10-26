"""Build the portfolio site.

Reads the Markdown files in content/ and the pictures in images/, and writes
a finished website into _site/. You should not need to edit this file to add
or change case studies: see README.md.

    python build.py          build the site into _site/
    python build.py --serve  build it, then preview it at http://localhost:8000
"""

import datetime
import hashlib
import html
import re
import shutil
import sys
from pathlib import Path

import markdown
from PIL import Image

ROOT = Path(__file__).parent
CONTENT = ROOT / "content"
IMAGES = ROOT / "images"
ASSETS = ROOT / "assets"
OUT = ROOT / "_site"
CACHE = ROOT / ".cache" / "images"

SITE_URL = "https://azkarifky1997.github.io/portfolio/"
# Where the site lives on GitHub Pages. Used only by the 404 page, which can
# be shown at any address, so it needs full paths rather than relative ones.
BASE_PATH = "/portfolio/"

# Each picture is saved at these widths. Phones download the small one.
IMAGE_WIDTHS = (800, 1600)
FULL_WIDTH = 2400

# True while previewing on your computer: empty image spaces are then shown
# as labelled boxes. They are never shown on the live site.
PREVIEW = "--serve" in sys.argv


# ---------------------------------------------------------------- content


def read_page(path):
    """Split a Markdown file into its settings (front matter) and body text."""
    text = path.read_text(encoding="utf-8")
    meta, body = {}, text
    match = re.match(r"^---\n(.*?)\n---\n?(.*)$", text, re.S)
    if match:
        body = match.group(2)
        current = None
        for line in match.group(1).splitlines():
            if not line.strip():
                continue
            if line.startswith((" ", "\t")) and current is not None:
                key, _, value = line.strip().partition(":")
                meta[current][key.strip()] = value.strip()
            else:
                key, _, value = line.partition(":")
                key, value = key.strip(), value.strip()
                if value:
                    meta[key] = value
                    current = None
                else:
                    meta[key] = {}
                    current = key
    # Settings left blank (like "photo:") come out as empty dicts; treat as empty.
    for key, value in meta.items():
        if value == {}:
            meta[key] = ""
    return meta, body


def load_case_studies():
    studies = []
    for path in sorted((CONTENT / "work").glob("*.md")):
        meta, body = read_page(path)
        meta.setdefault("slug", re.sub(r"^\d+-", "", path.stem))
        meta["file"] = path.name
        meta["body"] = body
        studies.append(meta)
    return studies


# ----------------------------------------------------------------- images


def web_name(name):
    """A web-safe version of a file name, plus a short fingerprint of the picture:
    "Farmer interviews.jpeg" -> "farmer-interviews-3fa9c1". When you replace a
    picture, the fingerprint changes, so browsers fetch the new one straight away."""
    slug = re.sub(r"[^a-z0-9]+", "-", Path(name).stem.lower()).strip("-")
    digest = hashlib.sha1((IMAGES / name).read_bytes()).hexdigest()[:6]
    return f"{slug}-{digest}"


def optimise_images():
    """Make small, fast WebP copies of every picture in images/."""
    CACHE.mkdir(parents=True, exist_ok=True)
    sizes = {}
    for src in sorted(IMAGES.iterdir()):
        if src.suffix.lower() == ".svg":
            # Drawn diagrams: copied as they are (they stay sharp at any size).
            m = re.search(r'viewBox="[\d.]+ [\d.]+ ([\d.]+) ([\d.]+)"', src.read_text(encoding="utf-8"))
            sizes[src.name] = (round(float(m.group(1))), round(float(m.group(2)))) if m else (1600, 900)
            shutil.copyfile(src, CACHE / f"{web_name(src.name)}.svg")
            continue
        if src.suffix.lower() not in (".png", ".jpg", ".jpeg", ".webp"):
            continue
        with Image.open(src) as im:
            im = im.convert("RGB")
            ratio = im.height / im.width
            sizes[src.name] = (im.width, im.height)
            targets = [(w, f"{web_name(src.name)}-{w}.webp") for w in IMAGE_WIDTHS]
            targets.append((FULL_WIDTH, f"{web_name(src.name)}-full.webp"))
            for width, name in targets:
                dest = CACHE / name
                if dest.exists() and dest.stat().st_mtime >= src.stat().st_mtime:
                    continue
                width = min(width, im.width)
                resized = im.resize((width, round(width * ratio)), Image.LANCZOS)
                resized.save(dest, "WEBP", quality=82, method=6)
    shutil.copytree(CACHE, OUT / "images", dirs_exist_ok=True)
    return sizes


def image_tag(name, alt, root, sizes_attr, image_sizes, lazy=True):
    stem = web_name(name)
    if name not in image_sizes:
        sys.exit(f"Missing picture: images/{name} (check the file name)")
    w, h = image_sizes[name]
    loading = ' loading="lazy"' if lazy else ""
    if name.lower().endswith(".svg"):
        return (
            f'<img src="{root}images/{stem}.svg" width="{IMAGE_WIDTHS[0]}" '
            f'height="{round(IMAGE_WIDTHS[0] * h / w)}" alt="{html.escape(alt)}"{loading} decoding="async">'
        )
    small = min(IMAGE_WIDTHS[0], w)
    srcset = ", ".join(
        f"{root}images/{stem}-{width}.webp {min(width, w)}w" for width in IMAGE_WIDTHS
    )
    loading = ' loading="lazy"' if lazy else ""
    return (
        f'<img src="{root}images/{stem}-{IMAGE_WIDTHS[0]}.webp" srcset="{srcset}" '
        f'sizes="{sizes_attr}" width="{small}" height="{round(small * h / w)}" '
        f'alt="{html.escape(alt)}"{loading} decoding="async">'
    )


# --------------------------------------------------------------- markdown

FIGURE_LINE = re.compile(r'^!\[(?P<alt>[^\]]*)\]\((?P<src>[^")]+?)(?:\s+"(?P<caption>[^"]*)")?\)\s*$')


def render_markdown(text, root, image_sizes):
    """Turn Markdown into HTML. A picture on its own line becomes a captioned figure."""

    def figure(match):
        alt, src, caption = match["alt"], match["src"], match["caption"] or ""
        name = Path(src).name
        if name not in image_sizes:
            # Not uploaded yet: a labelled space in the preview, nothing on the live site.
            print(f"Note: images/{name} is not uploaded yet, so it is left out for now.")
            note = placeholder(f"a photo ({name})", f"Upload {name} to images/", "figure-placeholder")
            return f"\n{note}\n" if note else ""
        if not alt.strip():
            sys.exit(
                f"The picture {name} needs alt text: describe it between the [ ] "
                f"in ![ ]({name} ...)"
            )
        img = image_tag(
            name, alt, root, "(min-width: 72rem) 64rem, calc(100vw - 2rem)", image_sizes
        )
        full = (f"{root}images/{web_name(name)}.svg" if name.lower().endswith(".svg")
                else f"{root}images/{web_name(name)}-full.webp")
        w, h = image_sizes[name]
        shape = " figure--portrait" if h > w else ""
        # Photos (JPEGs) are shown smaller than diagrams, which need room for their text.
        if Path(name).suffix.lower() in (".jpg", ".jpeg"):
            shape += " figure--photo"
        label = html.escape(caption.split(".")[0]) if caption else "this image"
        return (
            f'\n<figure class="figure{shape}">{img}<figcaption>{html.escape(caption)} '
            f'<a class="figure__full" href="{full}">View full size'
            f'<span class="visually-hidden">: {label}</span></a></figcaption></figure>\n'
        )

    lines = [FIGURE_LINE.sub(figure, line) for line in text.splitlines()]
    body = markdown.markdown("\n".join(lines), extensions=["tables", "sane_lists"])
    return label_tables(body)


def label_tables(body):
    """Give each table cell its column name, so tables can stack on phones."""

    def fix(table_match):
        table = table_match.group(0)
        headers = [re.sub(r"<[^>]+>", "", h) for h in re.findall(r"<th[^>]*>(.*?)</th>", table, re.S)]

        def fix_row(row_match):
            cells = iter(headers)
            return re.sub(
                r"<td>",
                lambda _: f'<td data-label="{html.escape(next(cells, ""))}">',
                row_match.group(0),
            )

        table = re.sub(r"<tr>.*?</tr>", fix_row, table, flags=re.S)
        return f'<div class="table-wrap">{table}</div>'

    return re.sub(r"<table>.*?</table>", fix, body, flags=re.S)


# -------------------------------------------------------------- templates


def layout(*, title, description, body, root, path, current="", home=None, scripts=""):
    e = html.escape
    page_title = e(title) if path == "" else f"{e(title)} · {e(home['name'])}"
    nav = [("Home", "", "home"), ("Work", "work/", "work"), ("About", "about/", "about")]
    nav_html = "".join(
        f'<li><a href="{root}{href}"' + (' aria-current="page"' if key == current else "") + f">{label}</a></li>"
        for label, href, key in nav
    )
    contact_current = ' aria-current="page"' if current == "contact" else ""
    year = datetime.date.today().year
    return f"""<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{page_title}</title>
<meta name="description" content="{e(description)}">
<link rel="canonical" href="{SITE_URL}{path}">
<meta property="og:type" content="website">
<meta property="og:title" content="{page_title}">
<meta property="og:description" content="{e(description)}">
<meta property="og:url" content="{SITE_URL}{path}">
<meta name="theme-color" content="#1B3A6B">
<link rel="icon" href="{root}assets/favicon.svg" type="image/svg+xml">
<link rel="preload" href="{root}assets/fonts/jakarta-latin-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{root}assets/style.css">
</head>
<body>
<a class="skip-link" href="#main">Skip to content</a>
<header class="site-header">
  <div class="nav-pill">
    <a class="brand" href="{root}"><span class="brand__mark" aria-hidden="true">A</span>{e(home['name'])}</a>
    <button type="button" class="nav-toggle" aria-expanded="false" aria-controls="site-nav" hidden>
      <span class="nav-toggle__bars" aria-hidden="true"></span>Menu
    </button>
    <nav id="site-nav" class="site-nav" aria-label="Main">
      <ul>{nav_html}</ul>
      <a class="nav-contact" href="{root}contact/"{contact_current}>Contact me</a>
    </nav>
  </div>
</header>
<main id="main" tabindex="-1">
{body}
</main>
<footer class="site-footer">
  <div class="site-footer__inner">
    <p>&copy; {year} {e(home['name'])}</p>
    <ul class="site-footer__links">
      <li><a href="mailto:{e(home['email'])}">{e(home['email'])}</a></li>
      <li><a href="{e(home['linkedin'])}">LinkedIn</a></li>
    </ul>
  </div>
</footer>
<script src="{root}assets/site.js" defer></script>
{scripts}
</body>
</html>
"""


def placeholder(label, where, css_class=""):
    """An empty image space. Shown only in the local preview, never on the live site."""
    if not PREVIEW:
        return ""
    return (
        f'<div class="placeholder {css_class}"><p><strong>Space for {label}</strong>'
        f"<br>Add it in <code>{where}</code></p></div>"
    )


# Simple line icons for the skills section. Pick one per skill in content/skills.md.
ICONS = {
    "journey": '<circle cx="5" cy="6" r="2"/><circle cx="19" cy="18" r="2"/><path d="M7 6h8a3 3 0 0 1 0 6H9a3 3 0 0 0 0 6h8"/>',
    "research": '<circle cx="10.5" cy="10.5" r="6"/><path d="m15 15 5 5"/><path d="M8 10.5h5M10.5 8v5"/>',
    "inclusive": '<circle cx="12" cy="4.5" r="2"/><path d="M5 8.5l7 1.5 7-1.5"/><path d="M12 10v4l-3 6M12 14l3 6"/>',
    "wireframe": '<rect x="3" y="4" width="18" height="16" rx="2"/><path d="M3 9h18M9 9v11"/>',
    "systems": '<rect x="3" y="3" width="6" height="6" rx="1"/><rect x="15" y="3" width="6" height="6" rx="1"/><rect x="9" y="15" width="6" height="6" rx="1"/><path d="M6 9v3h12V9M12 12v3"/>',
    "measure": '<path d="M4 20V4"/><path d="M4 20h16"/><path d="M8 16v-4M12 16V8M16 16v-6"/>',
    "workshop": '<circle cx="8" cy="8" r="2.5"/><circle cx="16" cy="8" r="2.5"/><path d="M3.5 19a4.5 4.5 0 0 1 9 0M11.5 19a4.5 4.5 0 0 1 9 0"/>',
    "gem": '<path d="M6 3h12l3 6-9 12L3 9z"/><path d="M3 9h18M9 3l3 6 3-6M12 21 9 9M12 21l3-12"/>',
    "home": '<path d="M3 11 12 4l9 7"/><path d="M5 10v10h14V10"/><path d="M10 20v-5h4v5"/>',
    "coins": '<ellipse cx="9" cy="7" rx="6" ry="3"/><path d="M3 7v4c0 1.7 2.7 3 6 3s6-1.3 6-3V7"/><path d="M9 14v3c0 1.7 2.7 3 6 3s6-1.3 6-3v-4c0-1.6-2.3-2.8-5.3-3"/>',
    "bus": '<rect x="4" y="3" width="16" height="14" rx="2"/><path d="M4 11h16M8 17v3M16 17v3"/><circle cx="8" cy="14" r=".5"/><circle cx="16" cy="14" r=".5"/>',
    "ball": '<circle cx="12" cy="12" r="9"/><path d="m12 7 4 3-1.5 4.5h-5L8 10z"/><path d="M12 3v4M16 10l4.5-1.5M14.5 14.5 17 19M9.5 14.5 7 19M8 10 3.5 8.5"/>',
    "globe": '<circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.7 3.8 5.7 3.8 9s-1.3 6.3-3.8 9c-2.5-2.7-3.8-5.7-3.8-9S9.5 5.7 12 3z"/>',
    "leaf": '<path d="M5 19c0-8 5-14 15-15-1 10-7 15-15 15z"/><path d="M5 19 13 11"/>',
    "pause": '<path d="M9 6v12M15 6v12"/>',
    "play": '<path d="M8 5.5v13l11-6.5z"/>',
    "compass": '<circle cx="12" cy="12" r="9"/><path d="m15.5 8.5-2 5-5 2 2-5z"/>',
    "book": '<path d="M4 5.5A2.5 2.5 0 0 1 6.5 3H20v15H6.5A2.5 2.5 0 0 0 4 20.5z"/><path d="M4 20.5A2.5 2.5 0 0 0 6.5 23H20v-5"/>',
    "chart": '<path d="M4 20V10M10 20V4M16 20v-7M22 20H2"/>',
    "lightbulb": '<path d="M9 18h6M10 21h4"/><path d="M12 3a6 6 0 0 0-3.5 10.9c.6.5 1 1.2 1 2.1h5c0-.9.4-1.6 1-2.1A6 6 0 0 0 12 3z"/>',
    "flower": '<circle cx="12" cy="9" r="2"/><path d="M12 7c0-3 3-4 3-4s1 3-1.5 4.5M12 7c0-3-3-4-3-4S8 6 10.5 7.5M14 9c3 0 4 3 4 3s-3 1-4.5-1.5M10 9c-3 0-4 3-4 3s3 1 4.5-1.5M12 11v10M12 17c-2-2-5-1-5-1M12 15c2-2 5-1 5-1"/>',
    "plane": '<path d="M2 16l20-8-6 13-3-6z"/><path d="M13 15 22 8"/>',
    "bag": '<path d="M5 8h14l-1 13H6z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/>',
    "cap": '<path d="M2 9l10-5 10 5-10 5z"/><path d="M6 11v5c3 2.5 9 2.5 12 0v-5M22 9v6"/>',
    "speech": '<path d="M4 5h16v11H9l-5 4z"/><path d="M8 9h8M8 12h5"/>',
    "sparkle": '<path d="M12 3c.6 4.2 2.8 6.4 7 7-4.2.6-6.4 2.8-7 7-.6-4.2-2.8-6.4-7-7 4.2-.6 6.4-2.8 7-7z"/><path d="M19 15v4M17 17h4"/>',
    "books": '<path d="M4 4h4v16H4zM10 4h4v16h-4z"/><path d="m16 5 3.8-1 3 15.5-3.8 1z"/>',
    "star": '<path d="m12 3 2.7 5.6 6.1.9-4.4 4.3 1 6.1L12 17l-5.4 2.9 1-6.1-4.4-4.3 6.1-.9z"/>',
    "linkedin": '<rect x="3" y="3" width="18" height="18" rx="3"/><path d="M8 10.5V16M8 7.5v.01M12 16v-3.5a2 2 0 0 1 4 0V16M12 10.5V16"/>',
    "email": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3.5 6.5 8.5 6 8.5-6"/>',
}


def icon(name, size=24):
    return (
        f'<svg class="icon" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
        f'stroke="currentColor" stroke-width="1.75" stroke-linecap="round" '
        f'stroke-linejoin="round" aria-hidden="true" focusable="false">{ICONS.get(name, ICONS["journey"])}</svg>'
    )


def load_skills(filename="skills.md"):
    """Read a cards file (skills.md, process.md): each "## Heading" is one card."""
    meta, body = read_page(CONTENT / filename)
    skills = []
    for block in re.split(r"^## ", body, flags=re.M)[1:]:
        lines = block.strip().splitlines()
        title, rest = lines[0].strip(), [l for l in lines[1:] if l.strip()]
        name = "journey"
        if rest and rest[0].startswith("icon:"):
            name = rest.pop(0).split(":", 1)[1].strip()
        skills.append({"title": title, "icon": name, "text": " ".join(rest)})
    return meta, skills


def hero_photo(home, image_sizes):
    """Portrait in front of a large amber shape, with two floating pills."""
    e = html.escape
    if home.get("photo") in image_sizes:
        inner = image_tag(home["photo"], home.get("photo_alt", ""), "", "(min-width: 60rem) 24rem, 80vw",
                          image_sizes, lazy=False)
    else:
        inner = '<span class="hero__initials" aria-hidden="true">AR</span>'
    pills = [p.strip() for p in home.get("pills", "").split("|") if p.strip()]
    pill_html = "".join(f'<span class="hero__pill hero__pill--{i + 1}">{e(p)}</span>' for i, p in enumerate(pills[:2]))
    return (f'<div class="hero__visual"><span class="hero__shape" aria-hidden="true"></span>'
            f'<div class="hero__portrait">{inner}</div>{pill_html}</div>')


def inline_md(text):
    """Small bits of Markdown inside a line, such as **bold** numbers."""
    return re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", html.escape(text))


def heading_md(text):
    """Headings with one *accent* word in italics."""
    return re.sub(r"\*(.+?)\*", r"<em>\1</em>", html.escape(text))


def is_published(slug, studies):
    """A case study exists and is not a draft (drafts only show in the preview)."""
    for s in studies:
        if s["slug"] == slug:
            return PREVIEW or not s.get("draft")
    return False


def project_card(p, root, image_sizes, studies, featured=False, lazy=True, home=False):
    """One project card, shared by the home page and the Work page."""
    e = html.escape
    link = p.get("link", "")
    href = f"{root}work/{link}/" if link and is_published(link, studies) else ""
    if p.get("image") in image_sizes:
        sizes = "(min-width: 60rem) 34rem, 92vw" if featured else "(min-width: 60rem) 22rem, 92vw"
        img = image_tag(p["image"], p.get("image_alt", ""), root, sizes, image_sizes, lazy=lazy)
        if p["image"].lower().endswith((".png", ".svg")):
            img = f'<div class="pcard__diagram">{img}</div>'  # diagrams show whole, not cropped
    else:
        img = f'<div class="pcard__fallback" aria-hidden="true">{icon("leaf", 40)}</div>'
    chips = "".join(f'<li class="chip">{e(c.strip())}</li>' for c in p.get("chips", "").split(",") if c.strip())
    year = f'<span>{e(p["year"])}</span>' if p.get("year") else ""
    if featured and p.get("numbers"):
        rows = []
        for pair in p["numbers"].split(";"):
            num, _, label = (x.strip() for x in pair.partition("|"))
            rows.append(f'<li><strong>{e(num)}</strong> {e(label)}</li>')
        result = f'<ul class="pcard__numbers">{"".join(rows)}</ul>'
    else:
        text = p.get("home_result") if home and p.get("home_result") else p.get("result", "")
        result = f'<p class="pcard__result">{inline_md(text)}</p>' if text else ""
    title = e(p["title"])
    if href:
        action = (f'<p class="pcard__cta"><a href="{href}">Read the case study'
                  f'<span class="visually-hidden">: {title}</span> <span aria-hidden="true">&rarr;</span></a></p>')
    else:
        action = ""
    data = ""
    if not home:
        data = " ".join(
            f'data-{k}="{" ".join(slugify(v) for v in p.get(k, "").split(",") if v.strip())}"'
            for k in ("type", "sector", "region")
        )
    tag = "h3" if home else "h2"
    return f"""
      <li class="pcard{' pcard--featured' if featured else ''}{' pcard--linked' if href else ''}" id="{slugify(p['title'])}" {data}>
        <div class="pcard__image">{img}</div>
        <div class="pcard__body">
          <p class="pcard__meta"><span>{e(p.get('meta', ''))}</span>{year}</p>
          <{tag} class="pcard__title">{title}</{tag}>
          <ul class="chips" aria-label="Methods">{chips}</ul>
          {result}
          {action}
        </div>
      </li>"""


def load_testimonials():
    _, body = read_page(CONTENT / "testimonials.md")
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    items = []
    for block in re.split(r"^## ", body, flags=re.M)[1:]:
        lines = block.strip().splitlines()
        t = {"name": lines[0].strip()}
        for line in lines[1:]:
            k, _, v = line.partition(":")
            if k.strip():
                t[k.strip()] = v.strip()
        if t.get("quote"):
            items.append(t)
    return items


def home_page(home, home_body, studies, image_sizes):
    e = html.escape
    first, _, last = home["name"].partition(" ")
    name = f"{e(first)} {e(last)}".strip()

    band = [w.strip() for w in home.get("skills_band", "").split("|") if w.strip()]
    band_html = '<span class="skills-band__mark" aria-hidden="true">✳</span>'.join(f"<span>{e(w)}</span>" for w in band)

    proof = []
    for number, value in (home.get("proof") or {}).items():
        label, _, link = (p.strip() for p in value.partition("|"))
        num = f'<a href="{e(link)}">{e(number)}</a>' if link else e(number)
        proof.append(f'<li><p class="proof__num">{num}</p><p class="proof__label">{e(label)}</p></li>')

    _, projects = load_projects()
    by_link = {p.get("link"): p for p in projects if p.get("link")}
    chosen = [by_link[s.strip()] for s in home.get("selected", "").split("|") if s.strip() in by_link]
    featured = project_card(chosen[0], "", image_sizes, studies, featured=True, lazy=False, home=True) if chosen else ""
    others = "".join(project_card(p, "", image_sizes, studies, home=True) for p in chosen[1:])

    _, steps = load_skills("process.md")
    step_items = "".join(
        f'<li class="step"><span class="step__num" aria-hidden="true">{i + 1:02d}</span>'
        f'<h3 class="step__title">{e(s["title"])}</h3><p>{e(s["text"])}</p></li>'
        for i, s in enumerate(steps)
    )
    tools = "".join(f'<li class="chip chip--light">{e(t.strip())}</li>' for t in home.get("tools", "").split(",") if t.strip())

    quotes = load_testimonials()
    testimonials = ""
    if quotes:
        slides = "".join(
            f'<figure class="quote"{" hidden" if i else ""}><blockquote><p>{e(q["quote"])}</p></blockquote>'
            f'<figcaption><strong>{e(q["name"])}</strong> · {e(q.get("role", ""))}</figcaption></figure>'
            for i, q in enumerate(quotes)
        )
        controls = ('<button type="button" class="quotes__btn" data-dir="-1" aria-label="Previous testimonial">&larr;</button>'
                    '<button type="button" class="quotes__btn" data-dir="1" aria-label="Next testimonial">&rarr;</button>'
                    ) if len(quotes) > 1 else ""
        testimonials = f"""
<section class="wrap quotes" aria-labelledby="quotes-heading">
  <p class="eyebrow quotes__eyebrow">Testimonials</p>
  <h2 id="quotes-heading">What people <em>say</em></h2>
  <div class="quotes__inner">{controls}<div class="quotes__slides" aria-live="polite">{slides}</div></div>
</section>"""

    email = e(home["email"])
    return f"""
<div class="wrap">
  <section class="hero" aria-labelledby="hero-heading">
    <div class="hero__text">
      <p class="hero__hello">Hello there!</p>
      <h1 id="hero-heading" class="hero__heading">I&rsquo;m <em class="hero__name">{name}</em>,</h1>
      <p class="hero__role">{e(home['role'])}</p>
      <p class="hero__intro">{e(home['intro'])}</p>
      <p class="hero__actions">
        <a class="button" href="work/">See my work<span class="button__arrow" aria-hidden="true">&rarr;</span></a>
        <a class="button button--secondary" href="contact/">Get in touch</a>
      </p>
    </div>
    {hero_photo(home, image_sizes)}
  </section>
</div>
<div class="skills-band"><p class="wrap skills-band__inner">{band_html}</p></div>
<section class="band band--teal on-blue proof" aria-labelledby="proof-heading">
  <div class="wrap">
    <h2 id="proof-heading" class="visually-hidden">Results at a glance</h2>
    <ul class="proof__list">{''.join(proof)}</ul>
    <p class="proof__note">{e(home.get('proof_note', ''))}</p>
  </div>
</section>
<section class="wrap about-short" aria-labelledby="about-heading">
  <h2 id="about-heading" class="eyebrow">About me</h2>
  {markdown.markdown(home_body)}
  <p class="about-short__more"><a href="about/">More about me <span aria-hidden="true">&rarr;</span></a></p>
</section>
<section class="wrap selected" id="work" aria-labelledby="work-heading">
  <div class="selected__head">
    <div><p class="eyebrow">My portfolio</p><h2 id="work-heading">Selected <em>work</em></h2></div>
    <p><a class="selected__all" href="work/">See all work <span aria-hidden="true">&rarr;</span></a></p>
  </div>
  <ul class="pcards pcards--home">{featured}{others}
  </ul>
</section>
<section class="band band--grey process" aria-labelledby="process-heading">
  <div class="wrap">
    <h2 id="process-heading" class="eyebrow">How I run research</h2>
    <ol class="process__steps">{step_items}</ol>
    <div class="tools"><h3 class="tools__title">Tools I use</h3><ul class="chips">{tools}</ul></div>
  </div>
</section>
{testimonials}
<section class="band band--teal on-blue talk" aria-labelledby="talk-heading">
  <div class="wrap talk__inner">
    <div>
      <h2 id="talk-heading">Let&rsquo;s <em>talk</em></h2>
      <p>{e(home.get('talk_text', ''))}</p>
    </div>
    <div class="talk__actions">
      <button type="button" class="talk__copy" data-email="{email}" hidden><span>{email}</span><span class="talk__copy-label">Copy email</span></button>
      <a class="talk__link talk__mail" href="mailto:{email}"><span>{email}</span><span aria-hidden="true">&rarr;</span></a>
      <a class="talk__link" href="{e(home['linkedin'])}"><span>LinkedIn</span><span aria-hidden="true">&rarr;</span></a>
      <p class="visually-hidden" aria-live="polite" data-copy-status></p>
    </div>
  </div>
</section>"""


def case_study_page(study, next_study, image_sizes):
    e = html.escape
    root = "../../"
    snapshot = "".join(
        f"<div><dt>{e(label)}</dt><dd>{e(value)}</dd></div>"
        for label, value in study["snapshot"].items()
    )
    if study.get("hero_image"):
        hero = (
            '<figure class="figure case__hero">'
            + image_tag(study["hero_image"], study.get("hero_alt", ""), root,
                        "(min-width: 72rem) 64rem, calc(100vw - 2rem)", image_sizes, lazy=False)
            + (f"<figcaption>{e(study['hero_caption'])}</figcaption>" if study.get("hero_caption") else "")
            + "</figure>"
        )
    else:
        hero = ""
    body = render_markdown(study["body"], root, image_sizes)
    return f"""
<article class="case">
  <div class="wrap">
    <p class="back-link"><a href="{root}work/">&larr; All work</a></p>
    <header class="case__header">
      <p class="eyebrow">Case study</p>
      <h1>{e(study['title'])}</h1>
      <p class="standfirst">{e(study.get('intro') or study['summary'])}</p>
    </header>
    {hero}
    <section class="snapshot" aria-labelledby="snapshot-heading">
      <h2 id="snapshot-heading" class="section-label">Snapshot</h2>
      <dl>{snapshot}</dl>
    </section>
    <div class="prose">
{body}
    </div>
  </div>
</article>
<nav class="next-case" aria-label="More case studies">
  <div class="wrap">
    <p class="section-label">Next case study</p>
    <a class="next-case__link" href="{root}work/{next_study['slug']}/">{e(next_study['title'])} <span aria-hidden="true">&rarr;</span></a>
    <p class="next-case__summary">{e(next_study['summary'])}</p>
    <p><a href="{root}work/">Back to all work</a></p>
  </div>
</nav>"""


def parse_settings(text):
    settings = {}
    for line in text.splitlines():
        key, _, value = line.partition(":")
        if key.strip():
            settings[key.strip()] = value.strip()
    return settings


def about_section(settings, text, root, image_sizes, index):
    """Build one section of the About page from its settings and Markdown text."""
    e = html.escape
    layout_name = settings.get("layout", "story")
    text = text.replace("{root}", root)
    body = render_markdown(text, root, image_sizes)

    if layout_name == "story":
        photo, name = "", settings.get("photo", "")
        if name and name in image_sizes:
            alt = settings.get("photo_alt", "")
            if not alt:
                sys.exit(
                    f"content/about.md: the photo {name} needs alt text. "
                    "Add a description after photo_alt:"
                )
            photo = image_tag(name, alt, root, "(min-width: 52rem) 24rem, calc(100vw - 2rem)",
                              image_sizes, lazy=index > 0)
        elif name and PREVIEW:
            photo = (f'<p class="hero__photo-note"><strong>Space for a photo</strong><br>'
                     f"Upload <code>{e(name)}</code> to images/</p>")
        side = "left" if settings.get("side") == "left" else "right"
        # Same blob shape and teal outline as the photo on the home page.
        photo_html = (
            f'<div class="story__photo hero__photo"><div class="hero__blob">{photo}</div></div>'
            if photo else ""
        )
        modifier = f" story--photo-{side}" if photo else ""
        if settings.get("width") == "full":
            modifier += " story--full"
        return f'<section class="about-section story{modifier}">{photo_html}<div class="story__text prose">{body}</div></section>'

    if layout_name == "grid":
        body = body.replace("<ol>", '<ol class="principles">', 1)
        return f'<section class="about-section">{body}</section>'

    if layout_name == "projects":
        body = body.replace("<ul>", '<ul class="project-cards">', 1)
        return f'<section class="about-section projects">{body}</section>'

    if layout_name == "cards":
        icons = [i.strip() for i in settings.get("icons", "").split(",") if i.strip()]
        count = [0]

        def card(match):
            name = icons[count[0]] if count[0] < len(icons) else "journey"
            count[0] += 1
            return f'<li><span class="fact-card__icon">{icon(name, 22)}</span><p>{match.group(1)}</p></li>'

        body = re.sub(r"<li>(.*?)</li>", card, body, flags=re.S)
        body = body.replace("<ul>", '<ul class="fact-cards">', 1)
        return f'<section class="about-section">{body}</section>'

    if layout_name == "columns":
        columns = [c for c in re.split(r"(?=<h2)", body) if c.strip()]
        inner = "".join(f'<div class="about-columns__col">{c}</div>' for c in columns)
        return f'<section class="about-section about-columns">{inner}</section>'

    if layout_name == "ticker":
        # A moving banner of project cards. Each bullet: big number | title | one line | optional link
        heading = re.search(r"^## (.+)$", text, re.M)
        cards = []
        for line in re.findall(r"^- (.+)$", text, re.M):
            bits = [b.strip() for b in line.split("|")]
            stat, title, desc, tag, link = (bits + ["", "", "", "", ""])[:5]
            link = link.replace("{root}", root)
            title_html = f'<a href="{e(link)}">{e(title)}</a>' if link else e(title)
            tag_html = f'<p class="ticker-card__tag">{e(tag)}</p>' if tag else ""
            cards.append(
                f'<li class="ticker-card">{tag_html}<p class="ticker-card__stat">{e(stat)}</p>'
                f'<h3 class="ticker-card__title">{title_html}</h3><p class="ticker-card__desc">{e(desc)}</p></li>'
            )
        track = "".join(cards)
        # The second copy makes the loop seamless; it is hidden from screen readers and keyboards.
        copy = re.sub(r'<a href=', '<a tabindex="-1" href=', track)
        title = e(heading.group(1)) if heading else "Projects"
        return (
            f'<section class="ticker" aria-labelledby="ticker-heading">'
            f'<div class="ticker__head"><h2 id="ticker-heading">{title}</h2>'
            f'<button type="button" class="ticker__toggle" aria-label="Pause projects" aria-pressed="false" hidden>'
            f'{icon("pause", 18)}{icon("play", 18)}</button></div>'
            f'<div class="ticker__viewport"><ul class="ticker__track">{track}</ul>'
            f'<ul class="ticker__track ticker__track--copy" aria-hidden="true">{copy}</ul></div></section>'
        )

    if layout_name == "map":
        return research_map(text)

    if layout_name == "education":
        # Each bullet: year | qualification | where
        heading = re.search(r"^## (.+)$", text, re.M)
        rows = []
        for line in re.findall(r"^-(.*)$", text, re.M):
            year, what, where = ([b.strip() for b in line.split("|")] + ["", "", ""])[:3]
            rows.append(
                f'<li class="edu__row"><p class="edu__year">{e(year)}</p>'
                f'<div><p class="edu__what">{e(what)}</p><p class="edu__where">{e(where)}</p></div></li>'
            )
        title = e(heading.group(1)) if heading else "Education"
        return f'<section class="about-section edu"><h2>{title}</h2><ul class="edu__list">{"".join(rows)}</ul></section>'

    if layout_name == "closing":
        # The last paragraph's links become buttons: the first filled, the rest outlined.
        paragraphs = body.rsplit("<p>", 1)
        if len(paragraphs) == 2 and "<a " in paragraphs[1]:
            links = re.findall(r'<a href="([^"]+)">(.*?)</a>', paragraphs[1])
            buttons = "".join(
                (f'<a class="button button--secondary" href="{href}">{label}</a>' if i else
                 f'<a class="button" href="{href}">{label}<span class="button__arrow" aria-hidden="true">&rarr;</span></a>')
                for i, (href, label) in enumerate(links)
            )
            body = paragraphs[0] + f'<p class="closing__actions">{buttons}</p>'
        return f'<section class="about-section closing">{body}</section>'

    return f'<section class="about-section prose">{body}</section>'


# A small hand-drawn star where the journey line ends, with the same chalky texture as the line.
CHALK_STAR = (
    '<svg class="chalk-star" viewBox="0 0 48 48" width="48" height="48" focusable="false">'
    '<defs><filter id="chalk-star" x="-20%" y="-20%" width="140%" height="140%">'
    '<feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="3" seed="4" result="noise"/>'
    '<feDisplacementMap in="SourceGraphic" in2="noise" scale="2.5" xChannelSelector="R" yChannelSelector="G" result="rough"/>'
    '<feColorMatrix in="noise" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  2.6 0 0 0 -0.5" result="grain"/>'
    '<feComposite in="rough" in2="grain" operator="in"/></filter></defs>'
    '<g filter="url(#chalk-star)" fill="none" stroke="#c9ad6b" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round">'
    '<path d="M22 7 L26.6 18.4 L38.8 19.2 L29.4 27 L32.6 39.6 L21.8 32.6 L11 39.8 L14.6 27.2 L5 19.6 L17.4 18.2 Z L22.8 8.8"/>'
    '<path d="M39 6 L42.5 2.5 M41 10.5 L45.5 9.5 M35.5 4 L36 0.5"/>'
    '</g></svg>'
)


MAP_W, MAP_TOP, MAP_BOTTOM = 1000, 84, -58


def map_marker(kind, x, y):
    """Map markers differ by shape as well as colour: in person ●, remote ○, survey ■."""
    if kind == "in person":
        return f'<circle cx="{x:.0f}" cy="{y:.0f}" r="7" class="m-person"/>'
    if kind == "remote":
        return f'<circle cx="{x:.0f}" cy="{y:.0f}" r="6" class="m-remote"/>'
    return f'<rect x="{x - 6:.0f}" y="{y - 6:.0f}" width="12" height="12" class="m-survey"/>'


def research_map(text):
    e = html.escape
    heading = re.search(r"^## (.+)$", text, re.M)
    title = e(heading.group(1)) if heading else "Where my research has taken me"
    land = re.search(r'<path d="([^"]+)"', (ASSETS / "world-land.svg").read_text()).group(1)
    h = MAP_W * (MAP_TOP - MAP_BOTTOM) / 360
    marks, rows, summary = [], [], []
    for line in re.findall(r"^- (.+)$", text, re.M):
        bits = [b.strip() for b in line.split("|")]
        place, kinds, coords, label = bits[:4]
        region = len(bits) > 4 and bits[4] == "region"
        kinds = [k.strip() for k in kinds.split(",") if k.strip()]
        lon, lat = (float(v) for v in coords.split(","))
        x, y = (lon + 180) / 360 * MAP_W, (MAP_TOP - lat) / (MAP_TOP - MAP_BOTTOM) * h
        if region:
            # A general area, deliberately not pinned to any one country.
            marks.append(f'<circle cx="{x - 18:.0f}" cy="{y - 6:.0f}" r="30" class="m-region"/>')
        for i, k in enumerate(kinds):
            marks.append(map_marker(k, x + (i - (len(kinds) - 1) / 2) * 16, y))
        icons = "".join(f'<svg class="map-key" viewBox="0 0 24 24" aria-hidden="true" focusable="false">'
                        f'{map_marker(k, 12, 12)}</svg>' for k in kinds)
        how = " and ".join(kinds)
        rows.append(f'<li><span class="map-list__keys">{icons}</span><span><strong>{e(place)}</strong> '
                    f'<span class="map-list__how">({e(how)})</span><br>{e(label)}</span></li>')
        summary.append(f"{place} ({how})")
    legend = "".join(
        f'<li><svg class="map-key" viewBox="0 0 24 24" aria-hidden="true" focusable="false">{map_marker(k, 12, 12)}</svg>{e(t)}</li>'
        for k, t in [("in person", "In person"), ("remote", "Remote, through local researchers or moderators"),
                     ("survey", "Survey")]
    )
    aria = f"World map of where my research has taken place: {'; '.join(summary)}."
    return (
        f'<section class="about-section research-map" aria-labelledby="map-heading">'
        f'<h2 id="map-heading">{title}</h2>'
        f'<ul class="map-legend" aria-label="Key">{legend}</ul>'
        f'<div class="research-map__inner"><div class="research-map__map">'
        # Framed from Europe to the Pacific, where all the places are.
        f'<svg viewBox="430 45 530 250" role="img" aria-label="{e(aria)}">'
        f'<path d="{land}" class="m-land"/>{"".join(marks)}</svg></div>'
        f'<ul class="map-list">{"".join(rows)}</ul></div></section>'
    )


def journey_stop(settings, text, root, image_sizes, index, is_last):
    """One stop on the About page journey: a year, a round photo or icon, and text."""
    e = html.escape
    side = "left" if index % 2 == 0 else "right"
    name = settings.get("photo", "")
    today_line = settings.get("today", "")
    if today_line:
        # The final "Today" stop: the hand-drawn chalk star instead of a circle.
        media = f'<span class="stop__dot" aria-hidden="true">{CHALK_STAR}</span>'
    else:
        if name and name in image_sizes:
            alt = settings.get("photo_alt", "")
            if not alt:
                sys.exit(f"content/about.md: the photo {name} needs alt text. Add a description after photo_alt:")
            circle = image_tag(name, alt, root, "8rem", image_sizes)
            focus = " stop__circle--top" if settings.get("focus") == "top" else ""
        else:
            circle = icon(settings.get("icon") or "journey", 30)
            focus = " stop__circle--icon"
        media = f'<div class="stop__circle{focus}">{circle}</div>'
    year = f'<p class="stop__year eyebrow">{e(settings["year"])}</p>' if settings.get("year") else ""
    body = render_markdown(text.replace("{root}", root), root, image_sizes)
    # Stop titles sit under the chapter headings (h3), so they are h4.
    body = re.sub(r"<(/?)h3>", r"<\1h4>", body)
    body = body.replace("<ul>", '<ul class="stop__chips">', 1)
    if today_line:
        body += f'<p class="stop__today-line">{e(today_line)}</p>'
    link = ""
    if settings.get("link"):
        title = re.search(r"<h4>(.*?)</h4>", body)
        about = f'<span class="visually-hidden"> about {title.group(1)}</span>' if title else ""
        link = (f'<p class="stop__link"><a href="{root}work/{e(settings["link"])}/">Read the case study'
                f'{about} <span aria-hidden="true">&rarr;</span></a></p>')
    classes = f"stop stop--{side}" + (" stop--last" if is_last else "") + \
        (" stop--featured" if settings.get("highlight") else "") + (" stop--today" if today_line else "")
    return (
        f'<li class="{classes}"><div class="stop__media">{media}</div>'
        f'<div class="stop__text prose">{year}{body}{link}</div></li>'
    )


def journey_section(items, root, image_sizes):
    """The winding "My journey" path: a heading, chapter markers, period labels and stops."""
    e = html.escape
    out, open_list = [], False
    stops_total = sum(1 for s, _ in items if s.get("layout") == "stop")
    n = 0
    heading = ""
    for settings, text in items:
        kind = settings.get("layout")
        if kind == "journey":
            m = re.search(r"^## (.+)$", text, re.M)
            heading = e(m.group(1)) if m else "My journey"
            continue
        if kind == "stop":
            if not open_list:
                out.append('<ol class="journey__list">')
                open_list = True
            out.append(journey_stop(settings, text, root, image_sizes, n, n == stops_total - 1))
            n += 1
            continue
        if open_list:
            out.append("</ol>")
            open_list = False
        label = e(text.strip())
        if kind == "chapter":
            out.append(f'<h3 class="journey__chapter"><span>{label}</span></h3>')
        else:
            out.append(f'<p class="journey__period"><span>{label}</span></p>')
    if open_list:
        out.append("</ol>")
    return (
        f'<section class="journey-band" aria-labelledby="journey">'
        f'<h2 id="journey">{heading or "My journey"}</h2>'
        f'<div class="journey">{"".join(out)}</div></section>'
    )


def about_page(meta, body, image_sizes):
    root = "../"
    parts = re.split(r"^\+\+\+\n(.*?)\n\+\+\+\n", body, flags=re.M | re.S)
    # parts = [text before first section, settings, text, settings, text, ...]
    blocks = [(parse_settings(parts[i]), parts[i + 1]) for i in range(1, len(parts), 2)]
    sections, journey = [], []

    def flush_journey():
        # Consecutive journey, chapter, period and stop sections become one winding path.
        if journey:
            sections.append(journey_section(journey, root, image_sizes))
            journey.clear()

    for settings, text in blocks:
        if settings.get("layout") in ("journey", "chapter", "period", "stop"):
            journey.append((settings, text))
            continue
        flush_journey()
        sections.append(about_section(settings, text, root, image_sizes, len(sections)))
    flush_journey()
    return f"""
<div class="wrap about-page">
{''.join(sections)}
</div>
<script src="{root}assets/about.js" defer></script>"""


FILTER_TYPES = ["Research", "Service design", "Strategy", "Research operations"]


def slugify(text):
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def load_projects():
    """Read content/projects.md: each "## Heading" is one project card."""
    meta, body = read_page(CONTENT / "projects.md")
    body = re.sub(r"<!--.*?-->", "", body, flags=re.S)
    projects = []
    for block in re.split(r"^## ", body, flags=re.M)[1:]:
        lines = block.strip().splitlines()
        p = {"title": lines[0].strip()}
        for line in lines[1:]:
            key, _, value = line.partition(":")
            if key.strip():
                p[key.strip()] = value.strip()
        projects.append(p)
    return meta, projects


def work_index_page(meta, projects, studies, image_sizes):
    e = html.escape
    root = "../"
    cards = "".join(project_card(p, root, image_sizes, studies, lazy=i > 1) for i, p in enumerate(projects))

    def values(key):
        seen = []
        for p in projects:
            for v in p.get(key, "").split(","):
                if v.strip() and v.strip() not in seen:
                    seen.append(v.strip())
        return seen

    groups = []
    for key, label, options in [("type", "Type", FILTER_TYPES), ("sector", "Sector", values("sector")),
                                ("region", "Region", values("region"))]:
        buttons = "".join(
            f'<button type="button" class="filter" aria-pressed="false" data-group="{key}" '
            f'data-value="{slugify(o)}">{e(o)}</button>'
            for o in options
        )
        groups.append(f'<div class="filters__group" role="group" aria-labelledby="filter-{key}">'
                      f'<p class="filters__label" id="filter-{key}">{label}</p>{buttons}</div>')
    return f"""
<div class="wrap work-index">
  <header class="work-index__head">
    <h1>{heading_md(meta.get('title_html', meta['title']))}</h1>
    <p class="standfirst">{e(meta.get('intro', ''))}</p>
  </header>
  <div class="filters" hidden>
    <h2 class="visually-hidden">Filter projects</h2>
    {''.join(groups)}
    <div class="filters__footer">
      <p class="filters__count" aria-live="polite"></p>
      <button type="button" class="filters__clear">Clear filters</button>
    </div>
  </div>
  <ul class="pcards pcards--work">{cards}</ul>
  <p class="projects__empty" hidden>No projects match these filters. Try clearing one.</p>
</div>"""


def styleguide_page():
    """Preview only: the v3 building blocks on one page, for review."""
    chips = "".join(f'<li class="chip">{c}</li>' for c in ["In-language field research", "Affinity mapping", "Journey mapping", "Service blueprint"])
    return f"""
<div class="wrap" style="padding-top:3rem">
  <p class="eyebrow">Design system</p>
  <h1>Building <em>blocks</em></h1>
  <p>Preview-only page showing the v3 tokens and components. It is never published.</p>
  <h2>Selected <em>work</em></h2>
  <h3>Buttons</h3>
  <p style="display:flex;gap:0.75rem;flex-wrap:wrap"><a class="button" href="#">See my work<span class="button__arrow" aria-hidden="true">&rarr;</span></a><a class="button button--secondary" href="#">Get in touch</a></p>
  <h3>Method chips</h3>
  <ul class="chips">{chips}</ul>
  <h3>Colours</h3>
  <ul class="chips">
    <li class="chip" style="background:var(--blue);color:#fff">Blue #1B3A6B</li>
    <li class="chip">Amber #F2A900</li>
    <li class="chip" style="background:var(--white);color:var(--gold-text);border:1px solid var(--line)">Gold text #9A6500</li>
    <li class="chip" style="background:var(--chalk)">Chalk #F3EBD3</li>
    <li class="chip" style="background:var(--grey-bg);border:1px solid var(--line)">Grey #F4F4F2</li>
  </ul>
</div>
<section class="band band--teal on-blue" style="margin-top:3rem">
  <div class="wrap">
    <p class="eyebrow">On a blue band</p>
    <h2 style="color:#fff;margin-top:0">Let's <em>talk</em></h2>
    <p><a class="button button--light" href="#">Get in touch</a></p>
  </div>
</section>"""


def contact_page(meta, body):
    e = html.escape
    phone = ""
    if meta.get("phone"):
        tel = re.sub(r"[^\d+]", "", meta["phone"])
        phone = f'<div><dt>Phone</dt><dd><a href="tel:{tel}">{e(meta["phone"])}</a></dd></div>'
    return f"""
<div class="wrap">
  <div class="prose">
    <h1>{e(meta['title'])}</h1>
    {markdown.markdown(body)}
    <dl class="contact-list">
      <div><dt>Email</dt><dd><a href="mailto:{e(meta['email'])}">{e(meta['email'])}</a></dd></div>
      {phone}
      <div><dt>LinkedIn</dt><dd><a href="{e(meta['linkedin'])}">Azka Rifky on LinkedIn</a></dd></div>
    </dl>
  </div>
</div>"""


def not_found_page():
    return f"""
<div class="wrap">
  <div class="prose">
    <h1>Page not found</h1>
    <p>Sorry, there is nothing at this address. It may have moved.</p>
    <p><a href="{BASE_PATH}">Go to the home page</a></p>
  </div>
</div>"""


# ------------------------------------------------------------------ build


def write(path, text):
    dest = OUT / path / "index.html" if not path.endswith(".html") else OUT / path
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(text, encoding="utf-8")


def build():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir()
    shutil.copytree(ASSETS, OUT / "assets")
    image_sizes = optimise_images()

    home, home_body = read_page(CONTENT / "home.md")
    contact, contact_body = read_page(CONTENT / "contact.md")
    about, about_body = read_page(CONTENT / "about.md")
    home["email"], home["linkedin"] = contact["email"], contact["linkedin"]
    studies = load_case_studies()

    write("", layout(
        title=f"{home['name']}, {home['role']}", description=home["intro"],
        body=home_page(home, home_body, studies, image_sizes), root="", path="", current="home", home=home,
    ))
    for i, study in enumerate(studies):
        next_study = studies[(i + 1) % len(studies)]
        write(f"work/{study['slug']}", layout(
            title=study["title"], description=study["summary"],
            body=case_study_page(study, next_study, image_sizes),
            root="../../", path=f"work/{study['slug']}/", current="work", home=home,
        ))
    projects_meta, projects = load_projects()
    write("work", layout(
        title=projects_meta["title"], description=projects_meta["description"],
        body=work_index_page(projects_meta, projects, studies, image_sizes),
        root="../", path="work/", current="work", home=home,
        scripts='<script src="../assets/work.js" defer></script>',
    ))
    write("about", layout(
        title=about["title"], description=about["description"],
        body=about_page(about, about_body, image_sizes),
        root="../", path="about/", current="about", home=home,
    ))
    if PREVIEW:
        write("styleguide", layout(
            title="Style guide", description="Preview only", body=styleguide_page(),
            root="../", path="styleguide/", home=home,
        ))
    write("contact", layout(
        title=contact["title"], description=contact["description"],
        body=contact_page(contact, contact_body),
        root="../", path="contact/", current="contact", home=home,
    ))
    write("404.html", layout(
        title="Page not found", description="Page not found",
        body=not_found_page(), root=BASE_PATH, path="404.html", home=home,
    ))
    print(f"Built {len(studies)} case studies into {OUT.relative_to(ROOT)}/")


def serve(port=8000):
    import functools
    import http.server

    handler = functools.partial(http.server.SimpleHTTPRequestHandler, directory=str(OUT))
    print(f"Preview: http://localhost:{port}/  (press Ctrl+C to stop)")
    http.server.ThreadingHTTPServer(("127.0.0.1", port), handler).serve_forever()


if __name__ == "__main__":
    build()
    if "--serve" in sys.argv:
        serve()
