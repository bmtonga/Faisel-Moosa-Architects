# Faisel Moosa Architects – website

Static site for Faisel Moosa Architects, Lusaka. Built on the Artima HTML template
(home variant 4) with the template's demo pages, variants and unused assets removed.

## Pages

| File | Purpose |
| --- | --- |
| `index.html` | Home: hero, About, Services, counters, Work Process, Projects grid, Founder, footer. Nav links are in-page anchors (`#about`, `#services`, `#projects`). |
| `contact-us.html` | Contact details, enquiry form (posts to `mail.php`), map. |
| `project-<slug>.html` | One page per project (13). **Generated** – do not edit by hand; see Tools. |
| `mail.php` | Contact form handler (PHP 8.2, PHPMailer over SMTP). All settings come from environment variables – see **Contact form** below. |

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
src/
  Env.php                 Reads settings from the environment (falls back to a local .env file)
  ContactMailer.php       Builds and sends the enquiry email with PHPMailer
vendor/                   Composer dependencies (not committed – run `composer install`)
tools/
  build_projects.py       Regenerates all project-*.html pages and relinks the home-page cards
composer.json / .lock     PHP dependencies (phpmailer/phpmailer)
.env.example              Mail settings template; copy to .env locally (never commit .env)
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

## Contact form

`contact-us.html` posts to `mail.php`, which validates the fields, drops honeypot
submissions, and sends the enquiry by SMTP with PHPMailer. **The PHP code is the same
everywhere; only the mail settings differ**, and they are read from environment
variables (`MAIL_HOST`, `MAIL_PORT`, `MAIL_ENCRYPTION`, `MAIL_USERNAME`,
`MAIL_PASSWORD`, `MAIL_FROM_ADDRESS`, `MAIL_FROM_NAME`, `MAIL_TO_ADDRESS`,
`MAIL_SUBJECT_PREFIX`). Real environment variables always take priority; a `.env`
file in the site root is only a fallback for local development.

### Run locally (PHP 8.2+, Composer, Mailpit)

```
composer install                 # installs PHPMailer into vendor/
copy .env.example .env           # Windows   (cp on macOS/Linux) – defaults point at Mailpit
mailpit                          # SMTP on :1025, inbox UI on http://localhost:8025
php -S localhost:8000            # from the site root, then open http://localhost:8000/contact-us.html
```

Submit the form; the email appears in Mailpit instead of a real inbox. Nothing is
sent externally. (Mailpit: https://mailpit.axllent.org – a single binary, or
`winget install axllent.mailpit` / `brew install mailpit`.)

### Deploy

Upload the site **including `vendor/`** (or run `composer install --no-dev` on the
server), do **not** upload `.env`, and set the `MAIL_*` variables in the host's
environment-variable settings (cPanel/Hostinger "Environment variables", Apache
`SetEnv`, a Docker `env_file`, …). A Gmail/Google Workspace example is in
`.env.example`: host `smtp.gmail.com`, port 587, `tls`, and an App Password – never
the account password. `MAIL_FROM_ADDRESS` must be a sender the SMTP host allows;
the visitor's address goes in Reply-To.

Responses are plain text with HTTP status codes (200 sent, 422 validation,
405 wrong method, 500 mail failure); `assets/js/vendor/ajax-form.js` shows the
text under the form. Set `MAIL_DEBUG=1` locally to log the SMTP transcript.

## Content sources

Copy, project list, years and contact details come from the 2026 company profile.
Photos are interim quality; replace files in place (same paths) when final images arrive.
