# Faisel Moosa Architects – website

Static site for Faisel Moosa Architects, Lusaka. Built on the Artima HTML template
(home variant 4) with the template's demo pages, variants and unused assets removed.

## Pages

| File | Purpose |
| --- | --- |
| `index.html` | Home: hero, About, Services, counters, Work Process, Projects grid, Founder, footer. Nav links are in-page anchors (`#about`, `#services`, `#projects`). |
| `contact-us.html` | Contact details, enquiry form (posts to `mail.php`), map. |
| `project-<slug>.html` | One page per project (13). **Generated** – do not edit by hand; see Tools. |
| `mail.php` | Form mailer. Requires a PHP host; recipient is set near the bottom of the file. |

## Folders

```
assets/
  css/
    main.css              Artima theme (compiled; do not edit the vendor sections)
    project-portfolio.css Projects grid on the home page
    project-page.css      Project detail pages
    fma-theme.css         Site-wide overrides (hover timings, contact labels, …) – loaded last on every page
    vendor/, plugins/     Third-party CSS
  js/
    main.js               Artima behaviour (sliders, animations, counters)
    project-portfolio.js  Isotope grid + filters for the Projects section
    vendor/, plugins/     Third-party JS
  imgs/
    portfolio/<slug>/     Project photos: cover.jpg (610 px, grid) + 01.jpg… (≤1600 px, lightbox)
    portfolio/*.jpg|png   Home-page images (about, services, process-*, founder)
    logo/fma-*.png        Brand marks; imgs/fma-favicon.png
    home/, contact-us/, experience/   Icons and shapes used by the home and contact pages
  fonts/                  Font Awesome Pro webfonts
  scss/                   Artima's Sass source (not built; kept for a future main.css trim)
tools/
  build_projects.py       Regenerates all project-*.html pages and relinks the home-page cards
```

## Conventions

- File names: lower-case kebab-case (`project-east-park-mall-piazza.html`).
- CSS classes: BEM, `block__element` (`project-portfolio__card`, `project-page__gallery-item`),
  matching the template's own style. Our blocks are prefixed `project-portfolio`, `project-page`
  and (in `fma-theme.css`) the template's block names they refine.
- Every page shares the same header, offcanvas and footer markup, copied from `index.html`;
  the generator does this for project pages. Change the header or footer in `index.html`,
  then re-run the generator and re-apply to `contact-us.html`.
- HTML sections are wrapped in `<!-- name start -->` / `<!-- name end -->` comments.
- Each CSS/JS file we added starts with a comment saying what it is for and where it is used.
- Template oddities kept as-is: the class `protfolio-details` (Artima's spelling, defined in
  `main.css`) is used on project pages.

## Tools

Regenerate the project pages after changing the `PROJECTS` list (title, category, type, year)
or adding photos under `assets/imgs/portfolio/<slug>/`:

```
python3 tools/build_projects.py
```

## Content sources

Copy, project list, years and contact details come from the 2026 company profile.
Photos are interim quality; replace files in place (same paths) when final images arrive.
