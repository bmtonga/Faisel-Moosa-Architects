"""Service pages: generates service-<slug>.html for each entry in SERVICES,
using index.html's header/footer and the Artima service-details layout.

Run from the site root, after any header/footer change on index.html:
    python3 tools/build_services.py
Edit SERVICES below to change a page's copy. Images live in assets/imgs/services/
(<slug>-hero.jpg 1600x600, <slug>-lead.jpg 1700x860, <slug>-1.jpg and -2.jpg 820x820,
<slug>-3.jpg 600x520); see the IMAGES map in prepare_images() to regenerate them.
"""
import html
import re

INDEX_FILE = 'index.html'
PHONE = '+260 977 824 023'
PHONE_HREF = 'tel:+260977824023'

SERVICES = [
    {
        'slug': 'architecture-design',
        'title': 'Architecture Design',
        'short': 'Concept to detailed design for new buildings and extensions.',
        'lead_title': 'Buildings Designed Around the People Who Use Them',
        'lead': 'Design does not follow a rigid formula or a cookie-cutter process. We question everything during the process and look for innovative ways to steer away from the norm, working directly with the client in collaborative efforts to meet their needs and achieve their goals. The result is a building that answers its brief, suits its site and Lusaka\'s climate, and can be built within the budget set for it.',
        'features': [
            ('Residential', 'Private houses, housing developments and gate houses, from a single plot to a multi-unit scheme.'),
            ('Commercial', 'Hotels, shopping malls, office blocks and multipurpose buildings, designed for the way they will trade and be maintained.'),
        ],
        'section2_title': 'From First Sketch to Detailed Design',
        'section2': [
            'Every commission starts with a conversation about what the client wants to achieve, followed by a site visit. Early sketches test how the building sits on the plot, which way its rooms face and how it is approached, before any detail is drawn.',
            'As the design develops we bring the engineers and other consultants in, so that structure, services and cost are resolved together with the architecture rather than after it.',
        ],
        'list': ['Brief development and site analysis', 'Concept and sketch design options', 'Developed design with 3D views for client review', 'Detailed design ready for production information'],
        'section3_title': 'What You Receive',
        'section3': 'A complete, coordinated set of architectural drawings and visualisations that describe the building clearly to you, to the planning authority and to the contractor who will price and build it.',
        'points': [
            ('Clear decisions, recorded', 'Each stage ends with a review meeting and a signed-off set of drawings, so the project moves forward on agreed ground.'),
            ('One practice, start to finish', 'The same team carries the design through production information and on to site, so nothing is lost between stages.'),
        ],
        'alts': ['Four bedroom house designed by Faisel Moosa Architects', 'Multipurpose building by Faisel Moosa Architects', 'Bonanza housing development', 'Gambrel House country cottage'],
    },
    {
        'slug': 'interior-design',
        'title': 'Interior Design',
        'short': 'Interiors that complete the project and define its image.',
        'lead_title': 'Interiors That Complete the Project',
        'lead': 'Interior design completes the project and goes a long way in defining the image or identifying the structure. Our entire design team collaborates with the client in defining that image and how to achieve it, in the selection of colours, materials, textures and furniture, fixtures and equipment (FF&E).',
        'features': [
            ('Homes', 'Kitchens, bathrooms, living spaces and bedrooms planned around how a family actually lives.'),
            ('Hospitality & retail', 'Restaurants, bars, hotels and shops where the interior is part of the business, designed for durability as well as atmosphere.'),
        ],
        'section2_title': 'Materials, Light and Furniture Chosen Together',
        'section2': [
            'We begin with how each space is used and what its surfaces have to withstand, then build a palette of durable base materials and add character through lighting, textiles and a small number of feature finishes.',
            'Furniture, fixtures and equipment are specified by performance as well as appearance, with locally available products preferred where the quality is right, and recorded in a schedule so every item, supplier and lead time is known before orders are placed.',
        ],
        'list': ['Space planning and layouts', 'Colour, material and finish selection', 'Lighting design', 'FF&E specification and schedules'],
        'section3_title': 'What You Receive',
        'section3': 'Interior layouts, finishes schedules, lighting layouts and FF&E schedules, coordinated with the architectural drawings so the fit-out can be priced and installed without surprises.',
        'points': [
            ('Designed with the architecture', 'Because the same practice designs the building, interior and shell are resolved together rather than in competition.'),
            ('Budgets held', 'Specifications are chosen with the cost plan in view, so the opening-day interior is the one that was approved.'),
        ],
        'alts': ['Open-plan interior with timber ceiling and a steel staircase', 'Tafika restaurant and bar interior', 'Cargo88 Hotel interior', 'Tafika interior detail'],
    },
    {
        'slug': 'planning-development',
        'title': 'Planning & Development',
        'short': 'Licensed planning and development services, including planning permission.',
        'lead_title': 'Approvals Handled, Development Advised',
        'lead': 'As a licensed professional architectural, planning and development services company, we prepare and manage planning permission applications and advise individuals, builders, investors and developers on what a site can accommodate. Early, well-prepared submissions keep a project on schedule.',
        'features': [
            ('Planning applications', 'Site plans, drawings and supporting documents compiled, lodged and followed through with the local authority.'),
            ('Development advice', 'Site appraisals, massing studies and feasibility layouts that show what a plot can support before money is committed.'),
        ],
        'section2_title': 'What the Process Involves',
        'section2': [
            'A typical application includes a site plan showing boundaries and setbacks, floor plans, elevations and sections, drainage and sanitation details and the structural information required for the type of building, prepared and signed by registered professionals.',
            'Commercial and multi-storey projects can call for additional submissions depending on the site and its zoning. We identify these early, respond to queries from the planning officers and make any revisions they request.',
        ],
        'list': ['Site appraisal and zoning check', 'Feasibility layouts and massing', 'Planning submission drawings and documents', 'Liaison with the local authority through to approval'],
        'section3_title': 'What You Receive',
        'section3': 'An approved application and a clear record of the conditions attached to it, so construction can begin on a known basis and the building handed over is the one that was approved.',
        'points': [
            ('Realistic programmes', 'We keep you informed of where the application sits, so decisions about contractors and financing are made with realistic dates in mind.'),
            ('Carried through to site', 'The same approved drawings are managed through construction by our project management service.'),
        ],
        'alts': ['Office park development by Faisel Moosa Architects', 'East Park Mall Phase 6', 'Gardenview Properties office block', 'Aerial view of a waterside resort development'],
    },
    {
        'slug': 'project-management',
        'title': 'Project Management',
        'short': 'Representing the owner during construction, from site visits to handover.',
        'lead_title': 'Your Representative on Site',
        'lead': 'During the construction period we make ourselves available to the contractor to answer any questions and address any concerns they may have. We are involved throughout construction to represent the owner: conducting site observation visits, monitoring progress, preparing any required change orders, reviewing construction drawings and managing planning permission applications.',
        'features': [
            ('Site observation', 'Regular visits to check that the work follows the drawings and specification, with written reports after each one.'),
            ('Progress and change', 'Programme and cost monitored against the contract; change orders prepared, priced and agreed before work proceeds.'),
        ],
        'section2_title': 'From Contractor Appointment to Handover',
        'section2': [
            'We help the client assemble tender documents, compare the contractors\' prices and appoint the contractor on a clear contract. Once on site, queries are answered promptly so the programme is not held up waiting for decisions.',
            'As the building nears completion we inspect the work, list the items to be corrected and certify completion only when they are done, then hand over the as-built drawings and operating information.',
        ],
        'list': ['Tender documents and contractor appointment', 'Site observation visits and reports', 'Programme, cost and change-order control', 'Inspections, defects lists and handover'],
        'section3_title': 'What You Receive',
        'section3': 'A building delivered as designed, a documented record of decisions made on site, and a single point of contact who answers for the project throughout construction.',
        'points': [
            ('The owner\'s interests first', 'We are appointed by you, not the contractor, and our reports and certificates reflect that.'),
            ('Continuity from the drawing board', 'The architects who designed the building are the ones checking it on site.'),
        ],
        'alts': ['Two engineers reviewing drawings on an earthworks site, seen from above', 'Arcades Shopping Mall refurbishment', 'East Park Mall Piazza', 'Construction site inspection'],
    },
]

ICON_CHECK = ('<svg width="18" height="18" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
              '<path d="M15 7.36V8.004C14.9991 9.5135 14.5103 10.9823 13.6065 12.1913C12.7027 13.4003 11.4323 14.2847 9.98475 14.7127C8.5372 15.1407 6.99008 15.0893 5.57413 14.5662C4.15818 14.0431 2.94926 13.0763 2.12767 11.8099C1.30609 10.5436 0.915854 9.04565 1.01517 7.53942C1.11449 6.0332 1.69804 4.59943 2.6788 3.45196C3.65955 2.30448 4.98495 1.50477 6.45733 1.17211C7.92971 0.839444 9.47018 0.991643 10.849 1.60601" stroke="#906E50" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>'
              '<path d="M15.0004 2.40381L8.00039 9.41081L5.90039 7.31081" stroke="#906E50" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></svg>')
ICON_PHONE = ('<svg width="22" height="22" viewBox="0 0 16 16" fill="none" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">'
              '<path d="M9.67161 3.67583C10.3263 3.80331 10.9279 4.12286 11.3995 4.59359C11.8712 5.06432 12.1913 5.66481 12.319 6.3182M9.67161 1C11.0317 1.15081 12.3 1.75871 13.2683 2.72391C14.2365 3.6891 14.8472 4.95421 15 6.31151M14.3298 11.6498V13.6567C14.3305 13.843 14.2923 14.0274 14.2175 14.1981C14.1427 14.3688 14.033 14.522 13.8955 14.648C13.758 14.7739 13.5956 14.8698 13.4187 14.9295C13.2419 14.9892 13.0546 15.0113 12.8686 14.9946C10.8062 14.7709 8.8251 14.0675 7.08449 12.9409C5.46509 11.9138 4.09211 10.5434 3.06307 8.92713C1.93035 7.18196 1.22544 5.19502 1.00544 3.12728C0.988691 2.94229 1.01072 2.75585 1.07012 2.57982C1.12952 2.4038 1.22499 2.24204 1.35046 2.10486C1.47592 1.96768 1.62863 1.85808 1.79886 1.78303C1.96909 1.70798 2.15312 1.66913 2.33921 1.66896H4.34993C4.6752 1.66576 4.99053 1.78072 5.23716 1.99242C5.48379 2.20411 5.64488 2.49809 5.6904 2.81956C5.77527 3.4618 5.93266 4.0924 6.15957 4.69933C6.24974 4.93876 6.26926 5.19898 6.2158 5.44915C6.16235 5.69932 6.03816 5.92895 5.85796 6.11083L5.00676 6.9604C5.96088 8.63517 7.35021 10.0218 9.02818 10.9741L9.87939 10.1246C10.0616 9.94471 10.2917 9.82076 10.5423 9.76741C10.793 9.71405 11.0537 9.73353 11.2936 9.82354C11.9017 10.05 12.5335 10.2071 13.177 10.2918C13.5025 10.3376 13.7999 10.5013 14.0124 10.7517C14.225 11.0021 14.3379 11.3217 14.3298 11.6498Z" stroke="#ffffff" stroke-linecap="round" stroke-linejoin="round"/></svg>')


def esc(s):
    return html.escape(s, quote=True)


def chrome(index_html):
    body_start = index_html.index('<body class="body-1">') + len('<body class="body-1">')
    main_start = index_html.index('<main>')
    top = index_html[body_start:main_start]
    foot = index_html[index_html.index('<footer>'):]
    fix = lambda t: re.sub(r'href="#(about|services|projects(?:-[a-z]+)?|blog)"', r'href="index.html#\1"', t)
    top = fix(top).replace('<li class="active"><a href="index.html">Home</a></li>', '<li><a href="index.html">Home</a></li>')
    top = top.replace('<li class="has-dropdown">\n                                        <a href="index.html#services">Services</a>',
                      '<li class="has-dropdown active">\n                                        <a href="index.html#services">Services</a>')
    return top, fix(foot)


def head_for(index_html, title, desc):
    h = index_html[:index_html.index('<body class="body-1">')]
    h = re.sub(r'<title>.*?</title>', f'<title>{esc(title)} – Faisel Moosa Architects</title>', h, count=1)
    h = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{esc(desc)}">', h, count=1)
    return h


def sidebar(current):
    links = '\n'.join(
        f'                                <a href="service-{s["slug"]}.html"{" class=\"active\"" if s["slug"] == current["slug"] else ""}'
        f'{" aria-current=\"page\"" if s["slug"] == current["slug"] else ""}>{esc(s["title"])}<i class="fa-regular fa-angle-right"></i></a>'
        for s in SERVICES)
    return f'''                <div class="col-xl-4">
                    <div class="sidebar sidebar-rr-sticky">
                        <div class="sidebar__widget has--service">
                            <h2 class="visually-hidden">Our services</h2>
                            <div class="sidebar__widget-service">
{links}
                            </div>
                        </div>
                        <div class="sidebar__widget widget__contact">
                            <div class="sidebar__widget-contact overflow-hidden">
                                <div class="sidebar__widget-contact__thumb">
                                    <img src="./assets/imgs/services/sidebar-contact.jpg" alt="" width="410" height="310" loading="lazy">
                                    <div class="sidebar__widget-contact__content">
                                        <div class="sidebar__widget-contact__icon">{ICON_PHONE}</div>
                                        <span>Talk to us about your project</span>
                                        <a href="{PHONE_HREF}">{PHONE}</a>
                                        <p class="mb-0">Plot 1146, No. 15 Lagos Road, Rhodes Park, Lusaka. Monday to Friday.</p>
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="sidebar__widget">
                            <h3 class="sidebar__widget-title">Start a Project</h3>
                            <p class="mb-20">Tell us about your site and your brief and we will come back to you with how we can help.</p>
                            <a href="contact-us.html" class="rr-btn"><span class="btn-wrap"><span class="text-one">Enquire</span><span class="text-two">Enquire</span></span></a>
                        </div>
                    </div>
                </div>'''


def main_for(s):
    sl = s['slug']
    feats = '\n'.join(f'''                            <div class="col-lg-6">
                                <div class="service-details__information-item">
                                    <h3 class="h6">{ICON_CHECK} {esc(t)}</h3>
                                    <p>{esc(d)}</p>
                                </div>
                            </div>''' for t, d in s['features'])
    items = '\n'.join(f'                            <li>{esc(x)}</li>' for x in s['list'])
    points = '\n'.join(f'''                                <h3 class="h6 mb-15">{esc(t)}</h3>
                                <p>{esc(d)}</p>''' for t, d in s['points'])
    sec2 = '\n'.join(f'                        <p>{esc(p)}</p>' for p in s['section2'])
    a = s['alts']
    return f'''<main>
    <!-- Breadcrumb area start -->
    <div class="breadcrumb__area header__background-color breadcrumb__header-up breadcrumb-space overly overflow-hidden">
        <div class="breadcrumb__background" data-background="./assets/imgs/services/{sl}-hero.jpg"></div>
        <div class="container">
            <div class="breadcrumb__bg-left"></div>
            <div class="breadcrumb__bg-right"></div>
            <div class="row align-items-center justify-content-between">
                <div class="col-12">
                    <div class="breadcrumb__content text-center">
                        <h1 class="breadcrumb__title mb-15 mb-sm-10 mb-xs-5 color-white title-animation">{esc(s['title'])}</h1>
                        <div class="breadcrumb__menu">
                            <nav aria-label="Breadcrumb">
                                <ul>
                                    <li><span><a href="index.html">Home</a></span></li>
                                    <li><span><a href="index.html#services">Services</a></span></li>
                                    <li class="active"><span>{esc(s['title'])}</span></li>
                                </ul>
                            </nav>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <!-- Breadcrumb area end -->

    <!-- service-details area start -->
    <section class="service-details section-space">
        <div class="container">
            <div class="row">
                <div class="col-xl-8">
                    <div class="service-details__content">
                        <div class="service-details__media">
                            <img src="./assets/imgs/services/{sl}-lead.jpg" alt="{esc(a[0])}" width="850" height="430">
                        </div>
                        <h2 class="h4 title-animation">{esc(s['lead_title'])}</h2>
                        <p class="mb-45">{esc(s['lead'])}</p>
                        <div class="row">
{feats}
                        </div>
                        <div class="row mt-10">
                            <div class="col-lg-6">
                                <div class="service-details__media">
                                    <img src="./assets/imgs/services/{sl}-1.jpg" alt="{esc(a[1])}" width="410" height="410" loading="lazy">
                                </div>
                            </div>
                            <div class="col-lg-6">
                                <div class="service-details__media">
                                    <img src="./assets/imgs/services/{sl}-2.jpg" alt="{esc(a[2])}" width="410" height="410" loading="lazy">
                                </div>
                            </div>
                        </div>
                        <h2 class="h4 title-animation">{esc(s['section2_title'])}</h2>
{sec2}
                        <ul>
{items}
                        </ul>
                        <h2 class="h4 title-animation">{esc(s['section3_title'])}</h2>
                        <p>{esc(s['section3'])}</p>
                        <div class="row mt-80 align-items-center">
                            <div class="col-lg-7">
{points}
                            </div>
                            <div class="col-lg-5">
                                <div class="service-details__media">
                                    <img src="./assets/imgs/services/{sl}-3.jpg" alt="{esc(a[3])}" width="300" height="260" loading="lazy">
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
{sidebar(s)}
            </div>
        </div>
    </section>
    <!-- service-details area end -->

    <!-- cta area start -->
    <section class="fma-cta section-space header__background-color" aria-labelledby="cta-title">
        <div class="container">
            <div class="row align-items-center">
                <div class="col-lg-8">
                    <span class="section-2__subtitle mb-10 text-white">Start A Project</span>
                    <h2 id="cta-title" class="section-2__title text-white mb-20 mb-lg-0">Tell us about your site and your brief.</h2>
                </div>
                <div class="col-lg-4 text-lg-end">
                    <a href="contact-us.html" class="rr-btn">
                        <span class="btn-wrap">
                            <span class="text-one">Enquire</span>
                            <span class="text-two">Enquire</span>
                        </span>
                    </a>
                </div>
            </div>
        </div>
    </section>
    <!-- cta area end -->
</main>

'''


def build():
    index_html = open(INDEX_FILE).read()
    top, foot = chrome(index_html)
    for s in SERVICES:
        page = head_for(index_html, s['title'], s['short'] + ' Faisel Moosa Architects, Lusaka.') + '<body class="body-1">' + top + main_for(s) + foot
        open(f"service-{s['slug']}.html", 'w').write(page)
        print('wrote', f"service-{s['slug']}.html")


if __name__ == '__main__':
    build()
