"""Generate project-<slug>.html pages from index.html's header/footer and the
photos under assets/imgs/portfolio/<slug>/.  Run from the site root:
    python3 tools/build_projects.py
Edit PROJECTS below to add a project or change its title, category, type or year.
"""
import os, re, glob, html

INDEX = open('index.html').read()

PROJECTS = [
    # slug, title, filter-classes, category label, type/description (from company profile), year
    ('arcades-shopping-mall',   'Arcades Shopping Mall',        'Commercial · Refurbishment', 'Refurbished shopping mall',           '2025'),
    ('cargo88-hotel',           'Cargo88 Hotel',                'Commercial',                 'Hotel',                               '2023'),
    ('east-park-mall-phase-6',  'East Park Mall – Phase 6',     'Commercial',                 'Various stores and piazza',           '2019–2025'),
    ('east-park-mall-piazza',   'East Park Mall Piazza',        'Commercial',                 'Open event and social space',         '2019'),
    ('tafika',                  'Tafika',                       'Commercial',                 'Restaurant and bar',                  '2024'),
    ('gardenview-properties',   'Gardenview Properties',        'Commercial',                 'Office block',                        '2017'),
    ('office-park',             'Office Park',                  'Commercial',                 'Office park',                         'Ongoing'),
    ('multipurpose-building',   'Multipurpose Building',        'Commercial',                 '4 storey multipurpose building',      '2023'),
    ('bonanza',                 'Bonanza',                      'Residential',                '4, 3 and 2 bedroom houses',           '2022'),
    ('four-bedroom-house-2024', 'Four Bedroom House (2024)',    'Residential',                '4 bedroom house',                     '2024'),
    ('four-bedroom-house-2021', 'Four Bedroom House (2021)',    'Residential',                '4 bedroom house',                     '2021'),
    ('private-gate-entry',      'Private Gate Entry',           'Residential',                'Private community security house',    '2023'),
    ('gambrel-house',           'Gambrel House',                'Residential',                'Gambrel-roof inspired country cottage','2010'),
]

# ---- shared chrome from index.html, with anchors rewritten for sub-pages ----
def chrome():
    body_start = INDEX.index('<body class="body-1">') + len('<body class="body-1">')
    main_start = INDEX.index('<main>')
    top = INDEX[body_start:main_start]
    foot = INDEX[INDEX.index('<footer>'):]
    for part in ('top', 'foot'):
        pass
    fix = lambda t: (t.replace('href="#about"', 'href="index.html#about"')
                       .replace('href="#services"', 'href="index.html#services"')
                       .replace('href="#projects"', 'href="index.html#projects"'))
    top = fix(top).replace('<li class="active"><a href="index.html">Home</a></li>', '<li><a href="index.html">Home</a></li>') \
                  .replace('<li><a href="index.html#projects">Projects</a></li>', '<li class="active"><a href="index.html#projects">Projects</a></li>')
    foot = fix(foot)
    return top, foot

HEAD = INDEX[:INDEX.index('<body class="body-1">')]

def head_for(title, desc):
    h = HEAD
    h = re.sub(r'<title>.*?</title>', f'<title>{html.escape(title)} – Faisel Moosa Architects</title>', h, 1)
    h = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{html.escape(desc, quote=True)}">', h, 1)
    h = h.replace('<link rel="stylesheet" href="assets/css/project-portfolio.css">',
                  '<link rel="stylesheet" href="assets/css/project-portfolio.css">\n    <link rel="stylesheet" href="assets/css/project-page.css">')
    return h

CHECK = ('<svg width="19" height="13" viewBox="0 0 19 13" fill="none" xmlns="http://www.w3.org/2000/svg">'
         '<path d="M18.1094 0.640625C18.6172 1.10938 18.6172 1.92969 18.1094 2.39844L8.10938 12.3984C7.64062 12.9062 6.82031 12.9062 6.35156 12.3984L1.35156 7.39844C0.84375 6.92969 0.84375 6.10938 1.35156 5.64062C1.82031 5.13281 2.64062 5.13281 3.10938 5.64062L7.21094 9.74219L16.3516 0.640625C16.8203 0.132812 17.6406 0.132812 18.1094 0.640625Z" fill="#906E50"/></svg>')

def main_for(i):
    slug, title, cat, desc, year = PROJECTS[i]
    imgs = sorted(f for f in glob.glob(f'assets/imgs/portfolio/{slug}/*.jpg') if not f.endswith('cover.jpg'))
    from PIL import Image
    hero = max(imgs, key=lambda f: (Image.open(f).size[0] >= Image.open(f).size[1], Image.open(f).size[0]))
    # cover index (which numbered file matches the cover) is unknown here; show all numbered images in the gallery
    t = html.escape(title); d = html.escape(desc)
    related = [p for p in PROJECTS if p[0] != slug and p[2].split(' ·')[0] == cat.split(' ·')[0]][:3]
    if len(related) < 3:
        related += [p for p in PROJECTS if p[0] != slug and p not in related][:3-len(related)]
    gallery = '\n'.join(
        f'                    <a href="./{f}" class="project-page__gallery-item popup-image" aria-label="View photo {n} of {t}">'
        f'<img src="./{f}" alt="{t} – photo {n}" loading="lazy"></a>'
        for n, f in enumerate(imgs, 1))
    rel = '\n'.join(f'''                <div class="col-md-6 col-lg-4">
                    <a href="project-{p[0]}.html" class="related-project__media project-page__related">
                        <img src="./assets/imgs/portfolio/{p[0]}/cover.jpg" alt="{html.escape(p[1])}">
                        <span class="project-page__related-caption"><strong>{html.escape(p[1])}</strong><span>{html.escape(p[3])} · {html.escape(p[4])}</span></span>
                    </a>
                </div>''' for p in related)
    prev_p = PROJECTS[i-1]; next_p = PROJECTS[(i+1) % len(PROJECTS)]
    return f'''<main>
    <!-- Breadcrumb area start  -->
    <div class="breadcrumb__area header__background-color breadcrumb__header-up breadcrumb-space overly overflow-hidden">
        <div class="breadcrumb__background" data-background="./assets/imgs/portfolio/{slug}/cover.jpg"></div>
        <div class="container">
            <div class="breadcrumb__bg-left"></div>
            <div class="breadcrumb__bg-right"></div>
            <div class="row align-items-center justify-content-between">
                <div class="col-12">
                    <div class="breadcrumb__content text-center">
                        <h2 class="breadcrumb__title mb-15 mb-sm-10 mb-xs-5 color-white title-animation">{t}</h2>
                        <div class="breadcrumb__menu">
                            <nav>
                                <ul>
                                    <li><span><a href="index.html">Home</a></span></li>
                                    <li><span><a href="index.html#projects">Projects</a></span></li>
                                    <li class="active"><span>{t}</span></li>
                                </ul>
                            </nav>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- Breadcrumb area end  -->

    <!-- project details start -->
    <section class="protfolio-details section-space__top">
        <div class="container">
            <div class="protfolio-details__content">
                <div class="protfolio-details__media">
                    <img src="./{hero}" alt="{t} – {d.lower()} by Faisel Moosa Architects">
                    <div class="protfolio-details__info">
                        <span class="protfolio-details__info-date"><i class="fa-regular fa-calendar-days"></i>{html.escape(year)}</span>
                        <div class="protfolio-details__info-list">
                            <div class="protfolio-details__info-list__item">Project: <span class="ml-20">{d}</span></div>
                            <div class="protfolio-details__info-list__item">Category: <span>{html.escape(cat)}</span></div>
                        </div>
                    </div>
                </div>

                <h4>Project Details</h4>
                <p>{t} is a {d.lower()} designed by Faisel Moosa Architects. Project type: {html.escape(cat.replace(' ·', ','))}. Year: {html.escape(year)}.</p>
                <ul class="mb-30">
                    <li>{CHECK} Architecture design by Faisel Moosa Architects, Lusaka</li>
                    <li>{CHECK} {len(imgs)} project photo{'s' if len(imgs) != 1 else ''} in the gallery below – click any image to view it full size</li>
                </ul>

                <h4>Gallery</h4>
                <div class="project-page__gallery mb-40">
{gallery}
                </div>

                <div class="project-page__nav">
                    <a href="project-{prev_p[0]}.html" class="rr-btn rr-btn-white"><span class="btn-wrap"><span class="text-one"><i class="fa-regular fa-arrow-left"></i> {html.escape(prev_p[1])}</span><span class="text-two"><i class="fa-regular fa-arrow-left"></i> {html.escape(prev_p[1])}</span></span></a>
                    <a href="index.html#projects" class="rr-btn"><span class="btn-wrap"><span class="text-one">All Projects</span><span class="text-two">All Projects</span></span></a>
                    <a href="project-{next_p[0]}.html" class="rr-btn rr-btn-white"><span class="btn-wrap"><span class="text-one">{html.escape(next_p[1])} <i class="fa-regular fa-arrow-right"></i></span><span class="text-two">{html.escape(next_p[1])} <i class="fa-regular fa-arrow-right"></i></span></span></a>
                </div>
            </div>
        </div>
    </section>
    <!-- project details end -->

    <section class="related-project section-space">
        <div class="container">
            <h2 class="text-center mb-60">Related Projects</h2>
            <div class="row mb-minus-30">
{rel}
            </div>
        </div>
    </section>
</main>

'''

if __name__ == '__main__':
    top, foot = chrome()
    for i, p in enumerate(PROJECTS):
        slug, title, cat, desc, year = p
        page = head_for(title, f'{title} – {desc}, {year}. {cat} project by Faisel Moosa Architects, Lusaka, Zambia.') \
             + '<body class="body-1">' + top + main_for(i) + foot
        open(f'project-{slug}.html', 'w').write(page)
    print('wrote', len(PROJECTS), 'pages')
    # link the home-page cards to the new pages
    s = INDEX
    for slug, title, *_ in PROJECTS:
        block = re.search(r'<article class="project-portfolio__item [^"]*">(?:(?!</article>).)*?/' + re.escape(slug) + r'/cover\.jpg(?:(?!</article>).)*?</article>', s, re.S).group(0)
        s = s.replace(block, block.replace('href="protfolio-details.html"', f'href="project-{slug}.html"'))
    open('index.html', 'w').write(s)
    print('index links to protfolio-details left:', s.count('protfolio-details.html'))
