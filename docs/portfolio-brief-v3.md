# Portfolio restructure brief v3 (for Claude Code)

**Repo:** `azkarifky1997/portfolio` (static site, markdown content files with `+++ layout +++` blocks, published on GitHub Pages at https://azkarifky1997.github.io/portfolio/)
**Owner:** Azka Rifky
**Date:** 26 October 2026
**Replaces:** Brief v2. Where v2 and this brief disagree, follow this brief.

This brief changes the portfolio's look, page structure and case studies. The wireframes that go with it are in `docs/wireframes/` (see section 0). Read this whole file and look at the wireframes before you change anything.

---

## 0. Files that come with this brief

Put these in the repo under `docs/` (not published as pages):

| File | What it is | How to use it |
|---|---|---|
| `docs/portfolio-brief-v3.md` | This brief | The source of truth |
| `docs/wireframes/home.png` (or `.pdf`) | Homepage wireframe | Layout reference |
| `docs/wireframes/case-study.png` | Case study template, filled with Rural Loan | Layout reference for every case study |
| `docs/wireframes/about.png` | About page wireframe | Layout reference |
| `docs/wireframes/source/*.dc.html` | The wireframes' HTML source | Exact colours, sizes, spacing and the chalk-line SVG path. These files will not render on their own; read them, don't publish them |
| `docs/Azka_Projects_Master_Record.md` | Every confirmed fact about each project | Check facts here. Section 14 is private: never publish anything from it |

Orange "note" boxes in the wireframes are instructions to you, not content. Grey dashed boxes are image placeholders.

---

## 1. Ground rules (apply everywhere)

1. **Voice:** UK spelling, plain warm English, first person, varied sentence length. **No em dashes** anywhere in visible text. No filler or buzzwords.
2. **Facts:** use only facts in this brief, the master record, or already on the site. **Never invent** numbers, quotes, testimonials, dates or outcomes. Where this brief says `[GAP]`, leave the sentence out (do not publish a placeholder) unless the brief says otherwise.
3. **Anonymise clients** from the agency years (2023 to 2026): say "a county council", "a UK membership organisation", "a global professional body", "a UK city destination", "a cultural institution in the Middle East". Never use the names in section 14 of the master record. These partners may be named: GSMA, MiBank, Kamapim, Field Buzz, YUX Design, Dialog Axiata, Agrithmics, Principality Building Society, WE Cymru (Wellbeing Economy Cymru).
4. **The agency** is "a research-led design and digital agency" and is in the **past tense** (Azka left on 20 October 2026).
5. **Title everywhere:** "UX researcher, specialising in inclusive research and service design". Short form: "UX researcher".
6. **Credit honestly:** say who did what. Results from partnerships "belong to the teams and partners I worked with".
7. **Images:** every image has alt text. Recreated diagrams are captioned "Recreated from memory" or "Recreated and anonymised". No children's faces. No home address.
8. **Never on the site:** availability, CV download, visa or sponsorship, date of birth, school name, star ratings, skill percentages.

---

## 2. Design system

### 2.1 Colour tokens (define once as CSS custom properties)

| Token | Value | Use |
|---|---|---|
| `--blue` | `#1B3A6B` | Nav bar, primary buttons, dark bands, headings accents on numbers |
| `--blue-dark` | `#12284C` | Link hover, pressed states |
| `--amber` | `#F2A900` | Chips, highlight shapes, numbers and accent words **on blue only**, lines, bubbles |
| `--gold-text` | `#9A6500` | Italic accent words **on white or light grey** (passes 4.5:1) |
| `--chalk` | `#F3EBD3` | Chalk line and chalk text on the blue About band |
| `--ink` | `#1C1C1C` | Body text |
| `--muted` | `#555555` | Meta text (dates, sectors) on white |
| `--grey-bg` | `#F4F4F2` | Light section bands, cards |
| `--line` | `#D8D8D4` | Card borders |
| `--white` | `#FFFFFF` | Page background |

**Contrast rules:** amber (`#F2A900`) is never used for text on white or light grey. On blue it passes (about 5.7:1). Body text on white is `--ink`. Check every new pairing reaches 4.5:1 for normal text and 3:1 for large text (24px+, or 19px+ bold) and for UI parts.

### 2.2 Type

- Font: **Plus Jakarta Sans** from Google Fonts, weights 400, 500, 600, 700, 800 and italic 500, 600, 700. Fallback `system-ui, sans-serif`.
- Body: 16px minimum (17px in case studies), regular 400, line height 1.6.
- Headings: h1 48 to 56px, h2 36 to 40px, h3 18 to 21px, all weight 700. Scale down on phones with `clamp()`.
- **Accent word:** each main heading has one word or short phrase in *italic, weight 600*: `--gold-text` on white, `--amber` on blue. Examples: "Selected *work*", "About *me*", "Let's *talk*".
- **Section label (eyebrow):** 15px, weight 500, ink colour, with a short amber dash before it (14px × 3px).

### 2.3 Components

- **Nav bar:** a rounded pill (full radius) in `--blue`, inset from the page edges, 60px tall. Left: amber circle with "A", then "Azka Rifky" in white. Right: Home, Work, About in white (current page in amber with underline), then a white pill button "Contact me" with ink text. On phones it collapses to a menu button (a real `<button>` with `aria-expanded`).
- **Primary button:** blue pill, white bold text, amber 2px border, ending in an amber circle with an arrow. **Secondary button:** white pill with a 2px ink border. Both at least 48px tall.
- **Method chips:** amber pill, ink text, 13px, weight 600. Used on cards and in case study headers to show methods. Chips are text, not links, unless stated.
- **Cards:** white, 1px `--line` border, 10 to 16px radius. Featured card has a 4px amber top border.
- **Bands:** full-width blue bands for proof numbers, case study headers, impact numbers and the contact block; light grey bands for "How I run research" and the research map.
- **Skills band** (homepage): a static amber strip with a 10px blue bottom edge: "User research ✳ Service design ✳ Inclusive design ✳ Test and learn". **It must not scroll or animate.** The ✳ marks are `aria-hidden`.

### 2.4 Accessibility (WCAG 2.2 AA, required)

- Contrast as in 2.1. Never convey meaning by colour alone (map pins use different **shapes**).
- Every interactive thing is a real `<a href>` or `<button>`. Visible focus ring on everything (for example a 3px amber outline with offset on blue, blue outline on white). Targets at least 44 × 44px.
- A "Skip to content" link first in the page. One `h1` per page, headings in order, `header`, `nav`, `main`, `footer` landmarks.
- Alt text on every meaningful image; decorative shapes, the chalk line, icons and ✳ marks are `aria-hidden="true"` or `alt=""`.
- Respect `prefers-reduced-motion`: no auto-moving content for those users.
- Works at 320px wide and at 200% zoom with no horizontal scrolling.
- Copy-email button announces "Email copied" through a polite live region.

---

## 3. Site map

- **Home** (`/`)
- **Work** (`/work/`): new page listing every project
- **About** (`/about/`)
- **Contact** (`/contact/`): keep as is, restyled
- **Case studies** (`/work/<slug>/`): five, all on the new template
  1. `rural-loan` (featured)
  2. `rural-bus`
  3. `wellbeing-wales` (**new**)
  4. `membership-journeys`
  5. `tea-sri-lanka`

Keep existing case study URLs working (redirect if you rename any).

---

## 4. Homepage (see `home.png`)

In this order:

1. **Nav bar** (2.3).
2. **Hero**, two columns (stack on phones):
   - Small outlined tag: "Hello there!"
   - h1: "I'm *Azka Rifky*," (accent on the name, with an amber underline)
   - Large line (36px, bold, not a heading): "UX researcher, specialising in inclusive research and service design"
   - Intro (keep current): "I've always been a creative person in a very analytical world. Today I use both to help people understand people, from vanilla farmers in Papua New Guinea to ultra-wealthy property buyers in Saudi Arabia."
   - Buttons: "See my work" (primary, to Work page) and "Get in touch" (secondary, to Contact).
   - Right: the existing portrait (`1684752387570.jpeg`) cut out or masked, in front of a large amber rounded shape; two floating pills over it: "UX researcher" (blue) and "Service designer" (amber). Alt text: "Portrait of Azka Rifky".
3. **Skills band** (2.3).
4. **Proof strip** (blue band, amber numbers, white labels):
   - **355** first-time loans for farmers in Papua New Guinea
   - **Up to 38%** more bus passengers year on year, from test-and-learn studies
   - **654** students surveyed in 5 countries
   - **750** Wales residents in a nationally representative survey
   - Under it: "Results belong to the teams and partners I worked with."
5. **About me** (short): label "About me", then "I'm a UX researcher with over five years' experience in Sri Lanka and the UK. I plan and run research in the field and remotely, and turn it into services teams can actually build, with inclusive design at the core." Link: "More about me →".
6. **Selected work:** label "My portfolio", h2 "Selected *work*", link "See all work →".
   - **Featured card** (Rural Loan): image left, text right. Meta "Financial inclusion · Papua New Guinea" and "2021". Title "A first loan for farmers with no ID, bank account or credit history". Chips: In-language field research, Affinity mapping, Journey mapping, Service blueprint, Wireframes. Numbers: **355** loans to 330 farmers; **35%** of borrowers were women; **99%** first-time access to a loan. Link "Read the case study →".
   - **Three cards** below (image, meta and year, title, 3 chips, one-line result, link):
     - Rural bus: "Public transport", 2025, "Testing and learning our way to more bus passengers", chips Field research, Surveys, Test and learn; "Passengers rose on all three routes, by **up to 38%** year on year".
     - Wales: "Public policy · Wales", 2024, "Is Wales ready for a wellbeing economy?", chips National survey, Community dialogues, Thematic analysis; "**750** residents surveyed, **6** community dialogues".
     - Member services: "Membership", no year (`[GAP]`), "Bringing member services into one place", chips Process mapping, Service blueprints, Member portal; "One place for members to manage their learning, qualifications and CPD. Live in phases."
   - The tea case study appears on the Work page, not here.
7. **How I run research** (grey band, keep current four steps and text): 01 Start with the decision; 02 Go to where people are; 03 Find the pattern; 04 Make it land. Below: "Tools I use" as white chips or small logo tiles (Figma, Miro, Maze, Qualtrics, Power BI, Notion, Otter.ai). **No percentages.**
8. **Testimonials:** label "Testimonials", h2 "What people *say*", a simple carousel with previous and next buttons and real, attributed quotes. **Azka has no quotes yet: build the component but hide the section until `content/testimonials.md` has at least one entry.** No star ratings.
9. **Let's talk** (blue band): h2 "Let's *talk*", the current line, then a **Copy email** button (copies `azkarifky@yahoo.com`) and a LinkedIn link (`https://www.linkedin.com/in/azka-rifky-279b18106/`).
10. **Footer:** "© 2026 Azka Rifky", email, LinkedIn.

Remove from the homepage: the six "What I do" cards, the long About text and the auto-carousel (that stays on About).

---

## 5. Work page (new)

- h1 "My *work*", one line: "Research and service design across finance, transport, public policy, membership and agriculture."
- Filters (real buttons with `aria-pressed`), with a live count ("Showing 9 projects", announced politely): **Type** (Research, Service design, Strategy, Research operations), **Sector**, **Region**.
- Cards in a grid, same card style as the homepage. Projects with a case study link to it; others have no link.

| Project (card title) | Meta | Year | Chips | One-line result | Link |
|---|---|---|---|---|---|
| A first loan for farmers with no ID, bank account or credit history | Financial inclusion · Papua New Guinea | 2021 | In-language field research, Journey mapping, Service blueprint | 355 loans to 330 farmers, 35% women | rural-loan |
| Testing and learning our way to more bus passengers | Public transport · England | 2025 | Field research, Surveys, Test and learn | Passengers up on all three routes, by up to 38% | rural-bus |
| Is Wales ready for a wellbeing economy? | Public policy · Wales | 2024 | National survey, Community dialogues, Thematic analysis | 750 residents surveyed, 6 dialogues | wellbeing-wales |
| Bringing member services into one place | Membership · UK | (omit) | Process mapping, Service blueprints, Member portal | One place for learning, qualifications and CPD; live in phases | membership-journeys |
| Tea, weather and trust in rural Sri Lanka | Agriculture · Sri Lanka | 2020 | Interviews in Sinhala, Ride-alongs, Journey maps | Research report, journey maps and recommendations | tea-sri-lanka |
| Members' needs across five countries | Professional body · UK, India, Singapore, Malaysia, China | 2023 | Longitudinal surveys, Choice grids, Need states | Around 200 members per wave; a need-state tool the client uses to plan services | none |
| What future members want | Education · UK, India, Singapore, Saudi Arabia, China | 2024 | Interviews, Survey, LLM-assisted analysis | 654 students surveyed in 5 countries | none |
| How people feel about AI | Technology · UK | (omit) | Survey, Readiness tool | Around 3,000 people; a tool to measure readiness to adopt AI | none |
| Ultra-luxury property buyers in Saudi Arabia | Property · Saudi Arabia | (omit) | Mixed methods, Moderator management, Personas | Led to a framework agreement | none |
| Understanding a city's visitors | Tourism · UK | (omit) | Survey, Segmentation, Insight portal | Over 1,000 respondents; a customer intelligence portal | none |
| Digital experience for a global professional body | Professional body · Global | 2023 | Expert review, Content mapping, Navigation strategy | A navigation strategy built around members' needs | none |
| Brand research for a cultural institution | Culture · Middle East | Ongoing | In-country research, Value proposition | Ongoing | none |
| Building a research practice | Research operations · UK | 2023 to 2026 | Research standards, Insight repository, Coaching | Standards, consent and GDPR processes, a Notion repository, AI training | none |

Do not give the Saudi or AI projects a respondent number other than the ones above.

---

## 6. About page (see `about.png`)

1. **Header** (centred): label "My journey", h1 "About *me*", one line: "An accountant who became a researcher: I help people understand people." Remove the old longer intro.
2. **Journey band** (full-width `--blue` band). A **chalk line** winds down the page between eight stops. Build it to these rules:
   - Use the SVG in `docs/wireframes/source/About.dc.html` as the starting point: a 1000px-wide layout where the line runs **down one side, turns along the empty gap between two stops, then runs down the other side**, with rounded corners. The line must **never cross text**. Text blocks sit beside each bubble, vertically centred on it.
   - Chalk look: `--chalk` stroke about 7px, round caps, an SVG `feTurbulence` + `feDisplacementMap` filter for grainy edges, plus a thin dashed blue overlay for texture. The SVG is `aria-hidden`. Optional: the line draws in on scroll, **only** when `prefers-reduced-motion` is not set.
   - **Bubbles:** 96px circles with a chalk border. A **photo** where one exists, otherwise the **year** in bold on amber.
   - **Chapter pills** sit on the line: "Sri Lanka" at the start, "United Kingdom" between stops 5 and 6. Dashed chalk outline, chalk text.
   - Ends with an amber ✦ and "Today: still curious, still asking 'why?'"
   - **Below 900px wide:** replace the winding line with one straight chalk line down the left, bubbles on it, text to the right.
   - Markup is an ordered list (`<ol>`), one `<li>` per stop, so it reads as a timeline without the visuals.

   The eight stops (label in amber caps, title, text):

   | # | Bubble | Label | Title | Text |
   |---|---|---|---|---|
   | 1 | 2017 | Growing up | Studying in Sri Lanka | Cambridge O and A Levels, then a First Class BSc in Applied Accounting, finishing top of my batch. |
   | 2 | 2016–17 | First job | Finance internship, MAS Legato | The accountancy services arm of MAS, one of Sri Lanka's largest apparel manufacturers. |
   | 3 | 2018–19 | My first step into research | Junior Analyst, Uzabase | Financial research and reports on industry trends, competitors and markets. |
   | 4 | Photo of Azka's jewellery if supplied, otherwise 2017–21 | 2017 to 2021, alongside | My own jewellery brand | Designing and selling jewellery, and running a small business alongside my full-time jobs. |
   | 5 | Photo: `Farmer interviews.jpeg` | 2019 to 2021 | Innovation Quotient: discovering design thinking | Business designer, then team lead, on fintech, insurance, mobile and agriculture projects. Chips linking to the tea and Rural Loan case studies, plus "Bank app research" (no link). |
   | 6 | Photo: `Graduation MA.jpeg` | October 2021 | A new country, and an MA with Distinction | A big change. MA Design Innovation at the University of South Wales, focused on inclusive design. |
   | 7 | 2021–23 | Alongside the MA | Pandora, Cardiff: top seller | The store's top seller for 2022. Every interaction shapes how people feel about a brand. |
   | 8 | Photo: `bus-card.jpg` | 2023 to 2026 | A research-led design agency | Product Marketing Consultant to Lead CX Research Consultant. Chips: Member services, Rural buses, Wellbeing economy in Wales, Member need states, Future members, AI attitudes, Saudi property buyers, City visitors portal, Research practice. Chips for projects with case studies link to them. |

   Photo alt texts: stop 5 "Interviewing a tea farmer on his veranda in Sri Lanka"; stop 6 "Azka at her MA graduation"; stop 8 "A rural bus at a stop"; stop 4 "Jewellery designed by Azka".

3. **Research map** (grey band): label "Research map", h2 "Where my research has *taken me*". A simple flat world map, centred, with pins. Pins are buttons; each opens a speech bubble on **hover, keyboard focus or tap**, closes on Esc or tapping elsewhere. Under the map, a legend and a visually hidden list with the same content for screen readers.
   - Pin shapes: **filled circle** = in person; **outlined circle** = remote, through local researchers or moderators; **amber diamond** = survey.

   | Pin | Shape | Bubble text | Link |
   |---|---|---|---|
   | United Kingdom | Filled circle | In person and survey. Wales, rural England, a city destination, membership bodies, member need states. | Bus, Wales, member services |
   | Sri Lanka | Filled circle | In person. Tea farmers, bank app research, co-design workshops. | Tea |
   | Papua New Guinea | Outlined circle | Remote, through two local field researchers. Rural Loan: 54 farmers in 8 villages. | Rural Loan |
   | Saudi Arabia | Outlined circle | Remote, through moderators, and survey. Property buyers; future members survey. | none |
   | Middle East (general marker, never on Oman) | Filled circle | In person. Research for a cultural institution. | none |
   | India | Diamond | Survey. Future members; member need states. | none |
   | China | Diamond | Survey. Future members; member need states. | none |
   | Singapore | Diamond | Survey. Future members; member need states. | none |
   | Malaysia | Diamond | Survey. Member need states. | none |

4. **Projects at a glance:** keep the existing auto-scrolling carousel and its pause button. It must pause on hover and on keyboard focus, and stay still under reduced motion. Restyle cards to the new look.
5. **What I always do**, **Education**, **Let's talk:** keep the content, restyle only.

---

## 7. Case study template (see `case-study.png`)

Every case study uses these sections, in this order. Section headings are descriptive and each has one accent word.

1. **Header band** (blue): "← All work" link; label "Case study · <sector> · <year>"; h1 with the project name in italic amber, for example "*Rural Loan:* a first loan for farmers with no ID, bank account or credit history"; a one-line summary; method chips. **Image on the right if there is one** (in a circle with an amber shape behind); **if not, the text runs full width.**
2. **Sticky contents bar** on desktop (About, Challenge, Process, Insights, Solution, Impact, Reflection). Not sticky on phones.
3. **Snapshot strip:** My role · Team · Timeline · Partners or client.
4. **About the project:** text left, image right if available, otherwise full-width text.
5. **The challenge:** short text, then the **research question** in a blue callout, then **hypotheses** as small cards if there were any (each with a "Confirmed" or "Disproved" chip).
6. **Research process** (grey band): a row of **design thinking stage cards** with arrows between them. Use only the stages that really happened, from: Empathise, Define, Ideate, Prototype, Test, Deliver. Each card lists its methods as chips. Use "Test" only where testing or evaluation actually happened; otherwise end with "Deliver". Below: **method highlights**, one card per key method, each with a real artefact image and two or three sentences.
7. **Key insights:** icon cards (simple line icons, `aria-hidden`), a short title and one or two sentences each, with numbers where they exist.
8. **The solution:** if there was one, a "We heard → So we designed" table plus the key design images. **If there was no solution, skip this section and give more insight cards instead.**
9. **Impact** (blue band): big amber numbers with labels, then an attribution line.
10. **Reflection:** three cards, "What I'd do *differently*".
11. **Next case study** link, and a **Sources** line where published sources exist.

Target reading time about five minutes. Keep paragraphs short.

---

## 8. Case study content

### 8.1 Rural Loan, Papua New Guinea (`rural-loan`)

- **Header:** "Case study · Financial inclusion · 2021". h1 "*Rural Loan:* a first loan for farmers with no ID, bank account or credit history". Summary: "How in-language field research shaped a loan, its rules and the tool bank staff used in the village." Chips: Design thinking, In-language field research, Mixed-method interviews, Affinity mapping, Journey mapping, Service blueprint, Wireframes. Image: `rural-loan-kyc.png`.
- **Snapshot:** My role: Co-lead, human-centred design partner (Innovation Quotient). Team: me and one colleague, with two local field researchers. Timeline: early 2021, research and design. Partners: GSMA AgriTech (funded by the Australian Government), MiBank, Kamapim, Field Buzz, YUX Design, a credit risk specialist.
- **About the project** (h2 "A loan built around *farmers*, not paperwork"): keep the current "challenge" text about GSMA AgriTech bringing together the lender, the buyer (about 3,000 farmers) and the agritech company to build a minimum viable credit product.
- **The challenge** (h2 "Banks need an *identity* farmers didn't have"): farmers had no ID, bank account, financial history or collateral; some had no birth certificate; loan sharks were often the only option; a trip to the bank could take hours; over 800 languages.
  - Research question callout: "How could we offer a loan that works for vanilla farmers in Papua New Guinea?" `[Azka may replace with a "How might we" version]`
  - Hypothesis 1: "Field agents, not farmers, will use the app." Chip: Confirmed. Hypothesis 2: "Loans of 2 to 3 months will suit farmers." Chip: Disproved, farmers needed 6 months or more.
- **Research process** (h2 "*Design thinking*, run remotely through local researchers"):
  - Empathise: Desk research, Stakeholder interviews, App demo, Field interviews, Gamified voting
  - Define: Affinity mapping, Journey mapping, Key insights
  - Ideate: Service flows, Partner workshops
  - Prototype: Service blueprint, Wireframes, Functional specifications
  - Deliver: MVP agreed by the consortium, Launched by MiBank
  - Highlights: (1) "Interviews in farmers' own languages": we recruited and trained two bilingual field researchers; 54 farmers in 8 villages and 6 field agents; sessions under an hour, with a closed-question section to count patterns. (2) "Research that works with low literacy": researchers drew grids and farmers voted by marking them with fruit peel. (3) "Mapping a farmer's financial year": `rural-loan-farmers-year.png`. (4) "The whole service, not just a screen": `rural-loan-blueprint.png`.
- **Key insights** (h2 "What we heard from *farmers*"): No one lives on vanilla alone (every farmer relied on other income, such as cocoa); Credit was new (only 7% had taken a formal loan); Few smartphones (48% had a mobile phone, only 2% a smartphone); Carrying cash is dangerous; Longer loans needed (6 months or more, not 2 to 3); Women often had no money of their own (and usually hid what they had at home). Keep `rural-loan-insights.png`.
- **Solution** (h2 "From insight to *design decision*"): table: No ID, but a trusted trading relationship → identity from the buyer's trading records; Few smartphones, agents have them → an assisted model, agents apply alongside farmers in the village; Loans needed to expand → three loan sizes tied to vine count (300, 500 and 1,000 kina, about £69 to £230); Credit is unfamiliar → mandatory financial literacy training. Then `rural-loan-kyc.png` and `rural-loan-wireframes.png` with the existing captions and alt text. Keep the existing trade-off notes.
- **Impact:** 355 loans over a 2.5-year pilot · 330 farmers · 35% of borrowers were women · 99% first-time access to a loan. Attribution: "GSMA's 2023 evaluation. These results belong to the whole partnership, and the pilot ran after my phase of the work." Keep the farmer quote, attributed to GSMA's evaluation.
- **Reflection:** Test the rules, not just the screens; Design for who's missing; Make insights survive delivery. Use the existing reflection text, shortened.
- **Sources:** the two GSMA articles already listed.

### 8.2 Rural bus test-and-learn (`rural-bus`)

**Keep the client's data private.** This page shows the process and a headline result only. Do not publish per-route figures, survey response counts, comment counts, campaign recall percentages or any other numbers from the client's reports. Remove "up to around 40%" and "adjusting for other causes" everywhere on the site.

- **Header:** "Case study · Public transport · 2025". h1 "Testing and learning our way to more *bus passengers*". Summary: "Three short test-and-learn studies on three rural bus routes, each with its own reason to travel." Chips: Field research, Roundtables, Surveys, Thematic analysis, Campaign design, Test and learn. Image: `bus-card.jpg`.
- **Snapshot:** My role: Co-led all three studies with the agency's CEO, as the programme's lead researcher, from fieldwork to evaluation. A designer created the campaign materials. Client: a rural county council in England. Timeline: 2025; each route ran a series of two-week sprints, then a six-month evaluation.
- **Challenge:** keep the current text (many routes and operators; a county-wide plan would be slow and expensive). Research question callout: "What would get more people on each rural route, without new buses or timetables?"
- **Research process:**
  - Empathise: Rode the routes, Conversations at stops and on buses, Roundtables at local lunch clubs, Surveys
  - Define: Thematic analysis of passengers' comments, A proposition for each route
  - Ideate: Campaign concepts with each operator
  - Prototype: Route campaigns, QR codes on posters
  - Test: Six-month evaluation, Year-on-year ticket data, Campaign recall surveys
  - Highlights: the test-and-learn cycle (`bus-cycle.png`); three routes, three propositions (`bus-routes.png`, with the table of routes A, B and C: who uses each one and the proposition tested); "riding the routes" (why on-bus conversations found things a desk survey would miss).
- **Key insights** (no figures):
  - Community beats online: campaigns were remembered far better where local community groups helped spread the word than where they ran online only.
  - People want to know when the bus is coming: reliable times and live tracking mattered more to passengers than anything else.
  - One route was really a connection: passengers used it to reach trains and other buses, so its proposition changed to joined-up journeys.
- **Solution:** "Quick, cheap and doable" recommendations (keep `bus-recommendations.png`): live bus times in Google Maps, QR codes at stops linking to bus times, and targeted route campaigns. Three recommendation reports, one per route.
- **Impact:** one headline only: "Passenger numbers rose year on year on all three routes, by **up to 38%**." Redraw `bus-result.png` to show just that line. Attribution: "Measured from ticket data, comparing the same month a year apart. Results belong to the council, the operators and the team."
- **Reflection:** Small tests beat big plans. Go where the users are. Fit the recommendation to the client's capacity. What I'd do differently: bigger evaluation samples (incentives helped), a comparison route from the start, and pushing harder for the digital change.

### 8.3 Is Wales ready for a wellbeing economy? (`wellbeing-wales`, new)

Client WE Cymru is public and may be named.

- **Header:** "Case study · Public policy · 2024". h1 "*Is Wales ready* for a wellbeing economy?" Summary: "A nationally representative survey and community dialogues across Wales, to find out whether people, not just activists, are ready for a different kind of economy." Chips: National survey, Choice grids, Roundtables, One-to-one interviews, Filmed dialogues, Thematic analysis, AI-assisted analysis, Persona stories. Image: `[GAP: Azka to supply a photo from the dialogues, with no children's faces]`, otherwise full-width header.
- **Snapshot:** My role: I designed and analysed the national survey, and designed the community dialogues, reviewing them with the agency's CEO. I co-led the roundtables with the CEO and ran the one-to-one interviews in rural Wales myself, with a filmmaker. I analysed the written responses by hand and with AI, and shaped the persona stories. Client: Wellbeing Economy Cymru (WE Cymru). Timeline: fieldwork October to November 2024; interim findings April 2025.
- **About the project:** WE Cymru is the Wales hub of the global Wellbeing Economy Alliance. It wanted a neutral answer to a simple question: is the population at large, not a passionate minority, ready for a transition to an economy that serves people and place?
- **Challenge:** reaching everyone, not just the people who already care. Research question callout: "Is Wales ready for a transition to a wellbeing economy, and what would it need to get there?"
- **Research process:**
  - Empathise: Nationally representative survey of 750 residents, Choice-grid questions, Six community dialogue events (roundtables and one-to-one interviews), 20 people filmed (10 hours of video)
  - Define: Thematic analysis of 2,000 written responses (by hand and with AI, checked against the raw data), Awareness segments
  - Ideate: Six persona stories of people and place (draft)
  - Deliver: Interim findings, A pilot proposal for the Vale of Glamorgan
  - Highlights: (1) "Choice grids": people pinned themselves on a grid to show which statement they were closest to, then added a note saying why, giving numbers and reasons in one question. (2) "Going to where people are": roundtables in communities, and one-to-one interviews in rural Wales, filmed with a filmmaker. (3) "Including the youngest voice": one dialogue included a seven-year-old, with a parent alongside; consent from both the child and the parent, including for recording. (4) "Three kinds of awareness": "I've heard of it", "I'm familiar with it", "I believe in it".
**Keep the focus on the process, not the findings.** The numbers on this page describe the research (how many people, which methods), not the results. Do not publish percentages or detailed findings from the client's reports.

- **Key insights** (no solution section; three short cards, no figures):
  - Awareness isn't even: how much people knew about a wellbeing economy varied with age and education.
  - People could see what it might change: given space to answer in their own words, they talked about everyday services such as healthcare, housing and education.
  - Place matters: different communities had different reasons for wanting change, so one national message wouldn't fit everywhere.
- **Impact** (blue band): **750** residents in a nationally representative survey · **2,000** written responses · **6** community dialogues · **20** people filmed. Then: "The research fed into WE Cymru's first Wellbeing Economy Cymru conference (November 2024), was shared at Davos by the agency's CEO, and became the evidence for a pilot proposal in the Vale of Glamorgan." Attribution: "Results belong to WE Cymru and the team."
- **Reflection:** `[GAP: Azka to approve]`. Suggested, for Azka to confirm or rewrite before publishing:
  1. "Pick the method for the person": a survey reached the whole country, but the dialogues reached people a survey would miss.
  2. "Plan for the youngest and oldest voices from the start."
  3. "Agree what happens next": the persona stories stayed at draft stage, so next time I'd agree up front how the findings will be used.
  **Do not publish this page until Azka confirms the reflection and the image.** Build it, but leave it unlinked (no nav, Work page or homepage link) until then, or put it behind a `draft: true` flag if the site supports one.
- **Sources:** WE Cymru, "Is Wales Ready? For a transition to a wellbeing economy", interim extract, April 2025.

### 8.4 Bringing member services into one place (`membership-journeys`)

**Rewrite this case study.** The story is now about joining up scattered platforms into one service with a member portal, not only about automating eligibility. Keep the URL.

- **Header:** "Case study · Membership". h1 "Bringing member services into *one place*". Summary: "Joining up a website, a member area, a learning platform and a qualifications shop, so members can see where they are and what comes next." Chips: Workshops, Interviews, Process mapping, Personas, Service blueprints, Member portal, Wireframes, Functional specifications, Usability testing. Image: a new recreated, anonymised blueprint or portal image.
- **Snapshot:** My role: Service and UX design lead. Client: a UK membership organisation. Timeline: `[GAP]`, omit.
- **About the project** (h2 "Four places to go, *one member*"): The organisation's services were spread across several places: a public website, a separate logged-in member area, a separate learning platform for studies, and a separate place to buy qualifications. It wanted to bring them together into one space, so members weren't confused moving between platforms.
- **Challenge** (h2 "Members didn't know *what came next*"): members weren't sure how to progress as a member, how to qualify, how to buy qualifications or how to keep learning. A lot of guidance happened by hand, with members having to contact staff. Staff were also checking eligibility by hand, even though most of the information was already in the CRM. Research question callout: "How might we give members one place to see where they are, what comes next and how to get there?"
- **Research process:**
  - Empathise: Workshops and interviews with every department, Conversations with staff and members
  - Define: Process mapping for the business and the member, Manual versus digital, Business rules, Personas (member types, staff who are also members, staff who process cases)
  - Ideate: Future-state journeys, Client review groups
  - Prototype: Service blueprints, Member portal wireframes, Functional specifications
  - Test: Usability testing, User acceptance testing
  - Highlights: (1) "Mapping both sides": we mapped every process from the business side and the member's side, to see which steps were manual and which could be digital. (2) "One portal": wireframes of the member portal (recreated, anonymised).
- **Key insights:** Services were scattered, so members had to work out which platform to use; members couldn't see their own progress; guidance relied on staff; staff checked eligibility by hand despite the data being in the CRM; some work was repeated across departments. Do not add research numbers (`[GAP]`).
- **Solution** (h2 "From scattered platforms to *one service*"): We heard → So we designed:
  - Services spread across several platforms → one joined-up site with a single member portal
  - Members unsure how to progress → a portal where members track their CPD, qualifications and studies in one place, personalised to them
  - Guidance given by hand → routine guidance and eligibility checks built into the service, with staff kept for unusual cases
  - Members lapsing → renewal and lapse reminders
  - No clear view of how the service performs → the portal lets the organisation track its KPIs
  - Too much for one release → phased delivery, with automated exemptions fully designed for a later phase
  - Keep "How our thinking changed" as a short callout.
- **Impact:** "Now live in phases." No numbers.
- **Reflection:** keep the current reflection (journeys take the shape of the business; keep bringing the conversation back to the member), as three short cards, adding: "One place is only better if it's simpler. Joining platforms together meant designing the paths between them, not just moving pages."

### 8.5 Tea, weather and trust (`tea-sri-lanka`)

- **Header:** "Case study · Agriculture · Sri Lanka · 2020". h1 "*Tea, weather* and trust in rural Sri Lanka". Keep the current intro question. Chips: Interviews in Sinhala, Ride-alongs, Stakeholder interviews, Affinity mapping, Journey mapping. Image: `Farmer interviews.jpeg`.
- **Snapshot:** keep current. My role: User research partner (Innovation Quotient), team of three.
- **Challenge:** keep current. Research question callout: "Could the trusted relationship between tea factories and farmers carry weather-index insurance, and would farmers take it up?"
- **Research process:** Empathise: Interviews in Sinhala, Ride-alongs with leaf collectors, Factory staff interviews. Define: Synthesis wall, Journey maps across the year. Deliver: Research report, Recommendations. Highlights use the three real photos with their existing alt text. Do not quote a number of farmers interviewed (`[GAP]`).
- **Key insights:** keep the current five, as icon cards. Keep the GSMA farmer quote.
- **No solution section.** "What happened next" becomes the Impact band, as text, credited to the whole programme.
- **Reflection:** keep current four points, as cards.

---

## 9. Site-wide fixes

- Bus figures: everywhere, only "up to 38%" (passengers rose on all three routes, by up to 38% year on year). No per-route figures anywhere, including the About carousel (use "Up to 38%").
- Wales: "750 Wales residents in a nationally representative survey". **Remove "aged 7 to over 90" and "~700" everywhere.** Remove Davos years; say "shared at Davos by the agency's CEO".
- About page: the agency in the past tense.
- The need-states project: "around 200 members per wave in the UK, India, Singapore, Malaysia and China", Azka worked on waves 3 and 4 and the longitudinal analysis across all four.

---

## 10. Gaps (do not fill)

Member services research numbers and year; Saudi respondent numbers; AI study key finding; number of tea farmers interviewed; Wales image and reflection; jewellery photo; testimonials.

---

## 11. How to work

1. Make a new branch, `restructure-v3`.
2. Work in this order and **stop after each step to show Azka a preview**: (a) design tokens, nav, footer, buttons, chips; (b) homepage; (c) case study template, using Rural Loan; (d) the other case studies; (e) Work page; (f) About page with the chalk journey and map.
3. After each step, check: no em dashes in visible text; contrast; keyboard-only use; 320px width; reduced motion; every image has alt text.
4. Do not merge to the published branch until Azka says so.
5. Finish with a short list of anything you couldn't do or had to guess.
