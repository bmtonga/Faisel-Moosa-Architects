"""Blog: writes the "Latest Articles" slider on index.html (between the
<!-- latest-article area start/end --> markers, just above the team section) and
generates one blog-<slug>.html page per post, using index.html's header/footer.

Run from the site root, after any header/footer change on index.html:
    python3 tools/build_blog.py
Edit POSTS below to add, remove or rewrite a post. Keep every title to ~30-36
characters and every excerpt to ~120-125 characters so the three cards stay the
same height (the CSS also clamps them to 2 and 3 lines). Each post needs
assets/imgs/blog/<slug>.jpg (1300x634), <slug>-card.jpg (820x400) and
<slug>-thumb.jpg (160x160).
"""
import html
import re

INDEX_FILE = 'index.html'

POSTS = [
    {
        'slug': 'designing-for-lusakas-climate',
        'title': "Designing Homes for Lusaka's Climate",
        'category': 'Architecture Design',
        'date': '14 October, 2026',
        'date_long': 'October 14, 2026',
        'excerpt': 'A house that works with the sun and the rains costs less to run and is more comfortable. Here is how we start every design.',
        'body': [
            ('p', 'Lusaka sits on a plateau with strong sun for most of the year, cool dry winters and a short, intense rainy season. Good design here starts long before materials and finishes are chosen: it starts with where the building sits on its plot and which way its rooms face.'),
            ('p', 'Our first move on any residential project is to orient the main living spaces so they receive soft morning light and are shielded from the hot afternoon sun on the west. Bedrooms are placed where they can be cross-ventilated at night, and service rooms take the harshest exposure.'),
            ('h4', 'Shade is a design element, not an afterthought'),
            ('p', 'Deep roof overhangs, verandas, screens and planted courtyards all do the same job: they keep direct sun off glass and walls so the building stays cool without relying on air conditioning. We size overhangs for the sun angles of each facade, so winter light still reaches inside while high summer sun is cut off.'),
            ('p', 'The rains need the same attention. Generous gutters, well-drained paving and raised floor levels keep water moving away from the house, and covered outdoor spaces mean the garden is still usable when a storm passes through.'),
            ('h4', 'Light without heat'),
            ('p', 'Large openings are welcome when they face the right way. We pair north- and south-facing glazing with narrow, high windows on the east and west, and use light-coloured roofs and walls to reflect heat. The result is a home that is bright all day and noticeably cooler by evening.'),
            ('p', 'If you are planning to build, bring us your plot early. The orientation decisions made in the first sketches are the ones that shape comfort and running costs for the life of the house.'),
        ],
    },
    {
        'slug': 'planning-permission-what-to-expect',
        'title': 'Planning Permission: What to Expect',
        'category': 'Planning & Development',
        'date': '22 September, 2026',
        'date_long': 'September 22, 2026',
        'excerpt': 'Approvals are a normal part of every project. Knowing what the local authority needs, and when, keeps your build on track.',
        'body': [
            ('p', 'Every building in Zambia, from a boundary wall to a shopping mall, needs approval from the relevant local authority before construction starts. The process is not complicated, but it does reward preparation: complete, well-presented drawings move through the system far faster than a partial submission.'),
            ('h4', 'What a submission usually contains'),
            ('p', 'A typical application includes a site plan showing the plot boundaries and setbacks, floor plans, elevations and sections, drainage and sanitation details, and the structural information required for the type of building. The documents must be prepared and signed by registered professionals, which is one of the reasons we are involved from the start rather than only at the drawing stage.'),
            ('p', 'Commercial and multi-storey projects can call for additional submissions, for example fire safety, environmental or traffic considerations, depending on the site and its zoning. We identify these early so that nothing is discovered late in the programme.'),
            ('h4', 'Our role during approval'),
            ('p', 'As the applicant\'s architect we compile the set, lodge it, respond to queries from the planning officers and make any revisions they request. We also keep the client informed about where the application sits, so decisions about contractors and financing can be made with realistic dates in mind.'),
            ('p', 'Once the permit is issued, construction can begin and inspections follow at the key stages of the build. Our project management service carries the same drawings and approvals through to completion, so the building that is handed over is the one that was approved.'),
        ],
    },
    {
        'slug': 'interiors-that-finish-the-story',
        'title': 'Interiors That Finish the Story',
        'category': 'Interior Design',
        'date': '28 August, 2026',
        'date_long': 'August 28, 2026',
        'excerpt': 'Architecture sets the stage; the interior is what people touch every day. How we choose colours, materials and furniture.',
        'body': [
            ('p', 'Interior design completes a project and defines its image. The same shell can read as warm and domestic or crisp and corporate depending on the finishes, lighting and furniture chosen for it, so we treat the interior as a continuation of the architecture rather than a separate exercise.'),
            ('h4', 'Start with how the space is used'),
            ('p', 'A restaurant floor, a family kitchen and a reception area all see different kinds of wear. We begin by asking what each surface has to withstand: foot traffic, spills, sunlight, cleaning regimes. That shortlist of practical demands narrows the material options before any colour board is made.'),
            ('p', 'From there we build a palette of a few durable base materials, typically stone or porcelain floors, timber or veneer for warmth, and painted or plastered walls, and add character through textiles, lighting and a small number of feature finishes.'),
            ('h4', 'Furniture, fixtures and equipment'),
            ('p', 'Selecting FF&E is where budgets are most often lost. We specify items by performance as well as appearance, favour locally available products where the quality is right, and keep a schedule so that every item, its supplier and its lead time is known before orders are placed.'),
            ('p', 'The result is an interior that photographs well on opening day and still looks right years later. If you have a project at the fit-out stage, we are happy to review the brief with you and suggest where to invest and where to save.'),
        ],
    },
]

ARROW = ('<svg width="12" height="12" viewBox="0 0 12 12" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
         '<path d="M1 6H11" stroke="#767676" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>'
         '<path d="M6 1L11 6L6 11" stroke="#767676" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>')
ICON_DATE = ('<svg width="11" height="13" viewBox="0 0 11 13" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
             '<path d="M3.5625 2H6.9375V1.0625C6.9375 0.757812 7.17188 0.5 7.5 0.5C7.80469 0.5 8.0625 0.757812 8.0625 1.0625V2H9C9.82031 2 10.5 2.67969 10.5 3.5V11C10.5 11.8438 9.82031 12.5 9 12.5H1.5C0.65625 12.5 0 11.8438 0 11V3.5C0 2.67969 0.65625 2 1.5 2H2.4375V1.0625C2.4375 0.757812 2.67188 0.5 3 0.5C3.30469 0.5 3.5625 0.757812 3.5625 1.0625V2ZM1.125 11C1.125 11.2109 1.28906 11.375 1.5 11.375H9C9.1875 11.375 9.375 11.2109 9.375 11V5H1.125V11Z" fill="#906E50"/></svg>')
ICON_USER = ('<svg width="12" height="14" viewBox="0 0 12 14" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
             '<path d="M6 7C4.06641 7 2.5 5.43359 2.5 3.5C2.5 1.56641 4.06641 0 6 0C7.93359 0 9.5 1.56641 9.5 3.5C9.5 5.43359 7.93359 7 6 7ZM6 1.3125C4.79297 1.3125 3.8125 2.29297 3.8125 3.5C3.8125 4.70703 4.79297 5.6875 6 5.6875C7.20703 5.6875 8.1875 4.70703 8.1875 3.5C8.1875 2.29297 7.20703 1.3125 6 1.3125ZM0.5 12.8125C0.5 10.3496 2.50586 8.34375 4.96875 8.34375H7.03125C9.49414 8.34375 11.5 10.3496 11.5 12.8125C11.5 13.2695 11.1191 13.625 10.6875 13.625H1.3125C0.880859 13.625 0.5 13.2695 0.5 12.8125ZM1.83984 12.3125H10.1602C9.91797 10.8125 8.60547 9.65625 7.03125 9.65625H4.96875C3.39453 9.65625 2.08203 10.8125 1.83984 12.3125Z" fill="#906E50"/></svg>')

AUTHOR = 'Faisel Moosa Architects'


def esc(s):
    return html.escape(s, quote=True)


# ---------------------------------------------------------------- index section
def index_section():
    slides = []
    for p in POSTS:
        slides.append(f'''                    <div class="swiper-slide">
                        <div class="latest-article__item">
                            <div class="latest-article__media">
                                <a href="blog-{p['slug']}.html"><img src="./assets/imgs/blog/{p['slug']}-card.jpg" alt="{esc(p['title'])}" width="410" height="200"></a>
                                <span class="latest-article__date">{p['date']}</span>
                            </div>
                            <div class="latest-article__content">
                                <ul class="latest-article__meta">
                                    <li><a href="blog-{p['slug']}.html">{esc(p['category'])}</a></li>
                                    <li><a href="blog-{p['slug']}.html"><span>By</span> {AUTHOR}</a></li>
                                </ul>
                                <h6 class="title-animation mb-10"><a href="blog-{p['slug']}.html">{esc(p['title'])}</a></h6>
                                <p class="mb-20">{esc(p['excerpt'])}</p>
                                <a class="read-more" href="blog-{p['slug']}.html">Read More {ARROW}</a>
                            </div>
                        </div>
                    </div>''')
    return f'''    <!-- latest-article area start -->
    <!-- Generated by tools/build_blog.py – edit POSTS there, not here -->
    <section id="blog" class="latest-article section-space__top">
        <div class="container">
            <div class="row">
                <div class="col-12">
                    <div class="section-2__title-wrapper align-items-center mb-55 mb-xs-40">
                        <span class="section-2__subtitle text-center mb-10">Latest Articles</span>
                        <h2 class="section-2__title text-capitalize text-center title-animation">News, Ideas &amp; Resources</h2>
                    </div>
                </div>
            </div>
            <div class="swiper latest-article__slider">
                <div class="swiper-wrapper">
{chr(10).join(slides)}
                </div>
                <div class="latest-article__slider-dot mt-60 mt-xs-40"></div>
            </div>
        </div>
    </section>
    <!-- latest-article area end -->
'''


def update_index():
    s = open(INDEX_FILE).read()
    section = index_section()
    if '<!-- latest-article area start -->' in s:
        s = re.sub(r'    <!-- latest-article area start -->.*?<!-- latest-article area end -->\n', section, s, count=1, flags=re.S)
    else:
        marker = '    <!-- our-team-2 start -->'
        assert marker in s, 'team section marker not found'
        s = s.replace(marker, section + '\n' + marker, 1)
    open(INDEX_FILE, 'w').write(s)
    return s


# ---------------------------------------------------------------- blog pages
def chrome(index_html):
    body_start = index_html.index('<body class="body-1">') + len('<body class="body-1">')
    main_start = index_html.index('<main>')
    top = index_html[body_start:main_start]
    foot = index_html[index_html.index('<footer>'):]
    fix = lambda t: re.sub(r'href="#(about|services|projects(?:-[a-z]+)?|blog)"', r'href="index.html#\1"', t)
    top = fix(top).replace('<li class="active"><a href="index.html">Home</a></li>', '<li><a href="index.html">Home</a></li>')
    top = top.replace('<li class="has-dropdown">\n                                        <a href="index.html#blog">Blog</a>',
                      '<li class="has-dropdown active">\n                                        <a href="index.html#blog">Blog</a>')
    return top, fix(foot)


def head_for(index_html, title, desc):
    h = index_html[:index_html.index('<body class="body-1">')]
    h = re.sub(r'<title>.*?</title>', f'<title>{esc(title)} – Faisel Moosa Architects</title>', h, count=1)
    h = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{esc(desc)}">', h, count=1)
    return h


def sidebar(current):
    cats = sorted({p['category'] for p in POSTS})
    cat_items = '\n'.join(f'                                    <li><a href="index.html#blog">{esc(c)}</a></li>' for c in cats)
    recent = []
    for p in POSTS:
        if p['slug'] == current['slug']:
            continue
        recent.append(f'''                                <div class="sidebar__widget-post">
                                    <a href="blog-{p['slug']}.html" class="sidebar__widget-post__thum">
                                        <img src="./assets/imgs/blog/{p['slug']}-thumb.jpg" alt="" width="80" height="80">
                                    </a>
                                    <div class="sidebar__widget-post__content">
                                        <ul class="sidebar__widget-post__content-meta">
                                            <li>{ICON_DATE} {p['date_long']}</li>
                                        </ul>
                                        <a href="blog-{p['slug']}.html">
                                            <h6 class="sidebar__widget-post__content-title">{esc(p['title'])}</h6>
                                        </a>
                                    </div>
                                </div>''')
    return f'''                <div class="col-xl-4">
                    <div class="sidebar sidebar-rr-sticky">
                        <div class="sidebar__widget">
                            <h4 class="sidebar__widget-title">Categories</h4>
                            <div class="sidebar__widget-category">
                                <ul>
{cat_items}
                                </ul>
                            </div>
                        </div>
                        <div class="sidebar__widget">
                            <h4 class="sidebar__widget-title">Recent Posts</h4>
                            <div class="sidebar-post__wrapper">
{chr(10).join(recent)}
                            </div>
                        </div>
                        <div class="sidebar__widget">
                            <h4 class="sidebar__widget-title">Start a Project</h4>
                            <p class="mb-20">Tell us about your site and your brief and we will come back to you with how we can help.</p>
                            <a href="contact-us.html" class="rr-btn"><span class="btn-wrap"><span class="text-one">Enquire</span><span class="text-two">Enquire</span></span></a>
                        </div>
                    </div>
                </div>'''


def main_for(i):
    p = POSTS[i]
    prev_p = POSTS[i - 1]
    next_p = POSTS[(i + 1) % len(POSTS)]
    body = []
    for tag, text in p['body']:
        body.append(f'                        <{tag}>{esc(text)}</{tag}>')
    return f'''<main>
    <!-- Breadcrumb area start -->
    <div class="breadcrumb__area header__background-color breadcrumb__header-up breadcrumb-space overly overflow-hidden">
        <div class="breadcrumb__background" data-background="./assets/imgs/blog/{p['slug']}.jpg"></div>
        <div class="container">
            <div class="breadcrumb__bg-left"></div>
            <div class="breadcrumb__bg-right"></div>
            <div class="row align-items-center justify-content-between">
                <div class="col-12">
                    <div class="breadcrumb__content text-center">
                        <h2 class="breadcrumb__title mb-15 mb-sm-10 mb-xs-5 color-white title-animation">{esc(p['category'])}</h2>
                        <div class="breadcrumb__menu">
                            <nav>
                                <ul>
                                    <li><span><a href="index.html">Home</a></span></li>
                                    <li><span><a href="index.html#blog">Blog</a></span></li>
                                    <li class="active"><span>{esc(p['title'])}</span></li>
                                </ul>
                            </nav>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- Breadcrumb area end -->

    <!-- blog-details area start -->
    <section class="blog-details section-space">
        <div class="container">
            <div class="row">
                <div class="col-xl-8">
                    <div class="blog-details__content">
                        <div class="blog-details__media">
                            <img src="./assets/imgs/blog/{p['slug']}.jpg" alt="{esc(p['title'])}" width="1300" height="634">
                        </div>
                        <ul class="blog-details__meta">
                            <li><span>{ICON_DATE} {p['date_long']}</span></li>
                            <li><span>{ICON_USER} By {AUTHOR}</span></li>
                        </ul>
                        <h4>{esc(p['title'])}</h4>
{chr(10).join(body)}
                        <div class="blog-details__tag">
                            <div class="blog-details__tag-list__wrapper">
                                <h6>Category :</h6>
                                <ul class="blog-details__tag-list">
                                    <li><a href="index.html#blog">{esc(p['category'])}</a></li>
                                </ul>
                            </div>
                        </div>
                        <div class="blog-details-pagination">
                            <div class="blog-details-pagination__next">
                                <a href="blog-{prev_p['slug']}.html">PREV POST</a>
                                <h6>{esc(prev_p['title'])}</h6>
                            </div>
                            <hr>
                            <div class="blog-details-pagination__prev">
                                <a href="blog-{next_p['slug']}.html">NEXT POST</a>
                                <h6>{esc(next_p['title'])}</h6>
                            </div>
                        </div>
                    </div>
                </div>
{sidebar(p)}
            </div>
        </div>
    </section>
    <!-- blog-details area end -->
</main>

'''


def build():
    index_html = update_index()
    top, foot = chrome(index_html)
    for i, p in enumerate(POSTS):
        page = head_for(index_html, p['title'], p['excerpt']) + '<body class="body-1">' + top + main_for(i) + foot
        open(f"blog-{p['slug']}.html", 'w').write(page)
        print('wrote', f"blog-{p['slug']}.html")


if __name__ == '__main__':
    build()
