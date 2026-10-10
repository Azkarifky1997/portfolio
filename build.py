"""Build the portfolio site.

Reads the Markdown files in content/ and the pictures in images/, and writes
a finished website into _site/. You should not need to edit this file to add
or change case studies: see README.md.

    python build.py          build the site into _site/
    python build.py --serve  build it, then preview it at http://localhost:8000
"""

import datetime
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


def optimise_images():
    """Make small, fast WebP copies of every picture in images/."""
    CACHE.mkdir(parents=True, exist_ok=True)
    sizes = {}
    for src in sorted(IMAGES.iterdir()):
        if src.suffix.lower() not in (".png", ".jpg", ".jpeg", ".webp"):
            continue
        with Image.open(src) as im:
            im = im.convert("RGB")
            ratio = im.height / im.width
            sizes[src.name] = (im.width, im.height)
            targets = [(w, f"{src.stem}-{w}.webp") for w in IMAGE_WIDTHS]
            targets.append((FULL_WIDTH, f"{src.stem}-full.webp"))
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
    stem = Path(name).stem
    if name not in image_sizes:
        sys.exit(f"Missing picture: images/{name} (check the file name)")
    w, h = image_sizes[name]
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

FIGURE_LINE = re.compile(r'^!\[(?P<alt>[^\]]*)\]\((?P<src>\S+?)(?:\s+"(?P<caption>[^"]*)")?\)\s*$')


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
        full = f"{root}images/{Path(name).stem}-full.webp"
        label = html.escape(caption.split(".")[0]) if caption else "this image"
        return (
            f'\n<figure class="figure">{img}<figcaption>{html.escape(caption)} '
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


def layout(*, title, description, body, root, path, current="", home=None):
    e = html.escape
    page_title = e(title) if path == "" else f"{e(title)} · {e(home['name'])}"
    nav = [
        ("Work", "", "work"),
        ("Skills", "#skills", "skills"),
        ("About", "about/", "about"),
        ("Contact", "contact/", "contact"),
    ]
    nav_html = "".join(
        f'<li><a href="{root}{href}"'
        + (' aria-current="page"' if key == current else "")
        + f">{label}</a></li>"
        for label, href, key in nav
    )
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
<meta name="theme-color" content="#ffffff">
<link rel="icon" href="{root}assets/favicon.svg" type="image/svg+xml">
<link rel="preload" href="{root}assets/fonts/montserrat-latin-normal.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="{root}assets/style.css">
</head>
<body>
<a class="skip-link" href="#main">Skip to main content</a>
<header class="site-header">
  <div class="site-header__inner">
    <a class="site-name" href="{root}">{e(home['name'])}</a>
    <nav aria-label="Main">
      <ul class="site-nav">{nav_html}</ul>
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
    "linkedin": '<rect x="3" y="3" width="18" height="18" rx="3"/><path d="M8 10.5V16M8 7.5v.01M12 16v-3.5a2 2 0 0 1 4 0V16M12 10.5V16"/>',
    "email": '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3.5 6.5 8.5 6 8.5-6"/>',
}


def icon(name, size=24):
    return (
        f'<svg class="icon" width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" '
        f'stroke="currentColor" stroke-width="1.75" stroke-linecap="round" '
        f'stroke-linejoin="round" aria-hidden="true" focusable="false">{ICONS.get(name, ICONS["journey"])}</svg>'
    )


def load_skills():
    """Read content/skills.md: each "## Heading" is one skill card."""
    meta, body = read_page(CONTENT / "skills.md")
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
    if home.get("photo"):
        inner = image_tag(home["photo"], home.get("photo_alt", ""), "", "(min-width: 48rem) 26rem, 18rem",
                          image_sizes, lazy=False)
    elif PREVIEW:
        inner = ('<p class="hero__photo-note"><strong>Space for your photo</strong><br>'
                 "Add it in <code>content/home.md</code> (photo:)</p>")
    else:
        inner = '<span class="hero__initials" aria-hidden="true">AR</span>'
    return f'<div class="hero__photo"><div class="hero__blob">{inner}</div></div>'


def home_page(home, home_body, studies, image_sizes):
    e = html.escape
    cards = []
    for i, s in enumerate(studies):
        if s.get("thumbnail") in image_sizes:
            thumb = image_tag(
                s["thumbnail"], "", "", "(min-width: 48rem) 24rem, 85vw", image_sizes, lazy=True,
            )
        else:
            # Card picture not uploaded yet: a plain panel with a leaf mark.
            thumb = f'<div class="card__image-fallback">{icon("leaf", 40)}</div>'
        cards.append(f"""
      <li class="card">
        <div class="card__image">{thumb}</div>
        <div class="card__body">
          <h3 class="card__title"><a href="work/{s['slug']}/">{e(s['title'])}</a></h3>
          <p class="card__summary">{e(s['summary'])}</p>
          <dl class="card__meta">
            <div><dt>Role</dt><dd>{e(s['card_role'])}</dd></div>
            <div><dt>Result</dt><dd>{e(s['card_result'])}</dd></div>
          </dl>
          <p class="card__cta" aria-hidden="true">Read the case study <span>&rarr;</span></p>
        </div>
      </li>""")

    first, _, last = home["name"].partition(" ")
    facts = "".join(
        f"<div><dt>{e(k)}</dt><dd>{e(v)}</dd></div>" for k, v in (home.get("facts") or {}).items()
    )
    skills_meta, skills = load_skills()
    skill_cards = "".join(
        f'<li class="skill"><span class="skill__icon">{icon(s["icon"])}</span>'
        f'<h3 class="skill__title">{e(s["title"])}</h3><p>{e(s["text"])}</p></li>'
        for s in skills
    )
    tools = "".join(
        f"<li>{e(t.strip())}</li>" for t in skills_meta.get("tools", "").split(",") if t.strip()
    )
    tools_html = (
        f'<div class="tools"><h3 class="tools__title">Tools I use</h3><ul class="tools__list">{tools}</ul></div>'
        if tools else ""
    )
    return f"""
<div class="wrap">
  <section class="hero">
    <div class="hero__text">
      <h1 class="hero__heading"><span class="hero__hi">Hi,</span> I&rsquo;m <span class="hero__name">{e(first)}</span>{(" " + e(last)) if last else ""}</h1>
      <p class="hero__role">{e(home['role'])}</p>
      <p class="hero__intro">{e(home['intro'])}</p>
      <p class="hero__actions">
        <a class="button" href="contact/">Get in touch</a>
        <a class="button button--secondary" href="#work">See my work</a>
      </p>
      <ul class="hero__social">
        <li><a href="{e(home['linkedin'])}">{icon("linkedin")}<span class="visually-hidden">LinkedIn</span></a></li>
        <li><a href="mailto:{e(home['email'])}">{icon("email")}<span class="visually-hidden">Email {e(home['email'])}</span></a></li>
      </ul>
    </div>
    {hero_photo(home, image_sizes)}
  </section>
</div>
<section class="intro-about" aria-labelledby="about-heading">
  <div class="wrap intro-about__inner">
    <div class="intro-about__text">
      <h2 id="about-heading" class="section-label">About me</h2>
      {markdown.markdown(home_body)}
      <p class="intro-about__more"><a href="about/">More about me <span aria-hidden="true">&rarr;</span></a></p>
    </div>
    <dl class="facts">{facts}</dl>
  </div>
</section>
<div class="wrap">
  <section class="skills" id="skills" aria-labelledby="skills-heading">
    <h2 id="skills-heading" class="section-label">{e(skills_meta.get('title', 'Skills'))}</h2>
    <ul class="skills__grid">{skill_cards}</ul>
    {tools_html}
  </section>
  <section class="work" id="work" aria-labelledby="work-heading">
    <div class="work__header">
      <h2 id="work-heading" class="section-label">Selected work</h2>
      <div class="carousel__buttons" hidden>
        <button type="button" class="carousel__btn" data-dir="-1" aria-controls="cards" aria-label="Previous case study">&larr;</button>
        <button type="button" class="carousel__btn" data-dir="1" aria-controls="cards" aria-label="Next case study">&rarr;</button>
      </div>
    </div>
    <ul class="carousel" id="cards">{''.join(cards)}
    </ul>
  </section>
</div>
<script src="assets/carousel.js" defer></script>"""


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
    <p class="back-link"><a href="{root}">&larr; All work</a></p>
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
    <p><a href="{root}">Back to all work</a></p>
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

    if layout_name == "closing":
        # The last paragraph's links become buttons: the first filled, the rest outlined.
        paragraphs = body.rsplit("<p>", 1)
        if len(paragraphs) == 2 and "<a " in paragraphs[1]:
            links = re.findall(r'<a href="([^"]+)">(.*?)</a>', paragraphs[1])
            buttons = "".join(
                f'<a class="button{" button--secondary" if i else ""}" href="{href}">{label}</a>'
                for i, (href, label) in enumerate(links)
            )
            body = paragraphs[0] + f'<p class="closing__actions">{buttons}</p>'
        return f'<section class="about-section closing">{body}</section>'

    return f'<section class="about-section prose">{body}</section>'


def about_page(meta, body, image_sizes):
    root = "../"
    parts = re.split(r"^\+\+\+\n(.*?)\n\+\+\+\n", body, flags=re.M | re.S)
    # parts = [text before first section, settings, text, settings, text, ...]
    sections = []
    for i in range(1, len(parts), 2):
        sections.append(about_section(parse_settings(parts[i]), parts[i + 1], root, image_sizes, len(sections)))
    return f"""
<div class="wrap about-page">
{''.join(sections)}
</div>"""


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
        body=home_page(home, home_body, studies, image_sizes), root="", path="", current="work", home=home,
    ))
    for i, study in enumerate(studies):
        next_study = studies[(i + 1) % len(studies)]
        write(f"work/{study['slug']}", layout(
            title=study["title"], description=study["summary"],
            body=case_study_page(study, next_study, image_sizes),
            root="../../", path=f"work/{study['slug']}/", current="work", home=home,
        ))
    write("about", layout(
        title=about["title"], description=about["description"],
        body=about_page(about, about_body, image_sizes),
        root="../", path="about/", current="about", home=home,
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
