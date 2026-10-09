# Azka Rifky – portfolio

My portfolio website: https://azkarifky1997.github.io/portfolio/

Everything you write lives in the `content` folder as plain Markdown files.
Pictures live in the `images` folder. When you save a change to GitHub, the
site rebuilds and goes live by itself, usually within two minutes.

## What is where

| Folder or file | What it is |
| --- | --- |
| `content/home.md` | Your name, role line, intro, photo, the "About me" text and the three quick facts on the home page |
| `content/skills.md` | The "What I do" skill cards and the "Tools I use" list on the home page |
| `content/about.md` | The About page (and its photo) |
| `content/contact.md` | Your email, phone and LinkedIn link |
| `content/work/` | One file per case study. The number at the start sets the order. |
| `images/` | Original PNG or JPG pictures. The site makes small, fast copies automatically. |
| `assets/style.css` | Colours, fonts and layout. You rarely need to touch this. |
| `build.py` | The script that turns the files into a website. No need to edit it. |

## Edit a case study (the easiest way, in your browser)

1. Go to your repository on github.com and open `content/work/`.
2. Click the case study file, then the pencil icon (Edit).
3. Change the text. Markdown basics:
   - `## Heading` makes a section heading, `### Heading` a smaller one
   - `**bold**` makes **bold** text
   - Start a line with `- ` for a bullet, or `1. ` for a numbered list
   - Leave an empty line between paragraphs
4. Click **Commit changes**. The site updates in a minute or two. You can watch
   progress in the **Actions** tab (a green tick means it is live).

## The settings at the top of each case study

Each case study file starts with a block between two `---` lines. This
controls the home page card and the snapshot box:

```
---
title: Rural Loan, Papua New Guinea
slug: rural-loan                      ← the web address: /work/rural-loan/
summary: One line shown on the card and under the title
card_role: Short role shown on the home page card
card_result: Headline result shown on the home page card
thumbnail: rural-loan-kyc.png         ← picture on the home page card
hero_image: workshop.jpg              ← optional large picture at the top of the page
hero_alt: Describe the picture       ← alt text for that picture
hero_caption: Optional caption
snapshot:
  My role: ...                        ← each indented line is one row
  Client: ...                            in the snapshot box, in this order
  Methods: ...
  Result: ...
---
```

Keep the indented snapshot lines indented with two spaces.

## Add a picture with a caption

1. Upload the PNG or JPG into the `images` folder (on GitHub: open `images`,
   then **Add file → Upload files**). Use a short name with no spaces, such as
   `bus-timetable.png`.
2. In the case study, put this on its own line, with an empty line above and below:

```
![Alt text: describe what the picture shows for someone who cannot see it.](bus-timetable.png "Caption shown under the picture. Recreated and anonymised.")
```

- The part in `[ ]` is the **alt text**, read out by screen readers. Describe
  what the picture actually shows, including any words in it.
- The part in quotes is the **caption** everyone sees.

## Add a new case study

1. In `content/work/`, open an existing case study and copy all of its text.
2. Create a new file (**Add file → Create new file**) named with the next
   number, for example `content/work/04-new-project.md`.
3. Paste, then change the settings block (give it a new `slug`) and the text.
4. Upload its pictures to `images/` and commit. A new card appears on the
   home page automatically, and the "Next case study" links update themselves.

To change the order of case studies, change the numbers at the start of the
file names. To remove one, delete its file.

## Edit your skills

Open `content/skills.md`. Each `## Heading` is one card: the heading, then an
`icon:` line, then one or two sentences. Add, remove or reorder cards freely.
The icons you can choose are listed at the top of the file. Edit the tools by
changing the comma-separated `tools:` line.

## Add your photo, or a lead image on a case study

There are three places waiting for a picture:

- **Home page photo (in the ochre shape at the top):** in `content/home.md`, change `photo:` to `photo: azka.jpg`. A photo with you in the centre works best, as the edges get rounded off.
- **About page photo:** in `content/about.md`, change `photo:` to `photo: azka.jpg`
- **Top of each case study:** in its file, fill in `hero_image:`, `hero_alt:` and
  (optionally) `hero_caption:`

Upload the picture to `images/` first. Photos of you work best roughly square.

Until you add them, the live site shows a circle with your initials instead of
a photo, and simply leaves out the case study lead image. In the preview on
your computer, each empty space shows as a dashed box telling you which file
to edit, so you can see where pictures will go.

You can also add more pictures anywhere inside a case study, using the
picture line described above.

## Preview changes on your computer first (optional)

You only need this if you edit files on your computer instead of on GitHub.
Open Terminal, then:

```bash
cd ~/Documents/Portfolio/portfolio
```

The first time only, set up the tools:

```bash
/opt/homebrew/bin/python3 -m venv .venv && .venv/bin/pip install -r requirements.txt
```

Then, each time you want a preview:

```bash
.venv/bin/python build.py --serve
```

Open http://localhost:8000 in your browser. Press Ctrl+C in Terminal to stop.
Run the command again to see further edits.

To publish changes made on your computer, use GitHub Desktop or:

```bash
git add -A && git commit -m "Update case study" && git push
```

## Good habits

- Write alt text for every picture, and keep "Recreated" notes in captions.
- Keep client names out of anonymised case studies.
- Don't add your home address: the site is public.
