"""Legal pages: writes tools/pages/privacy-policy.html, terms-of-use.html and
cookie-policy.html partials from the SECTIONS data below, then build_pages.py
turns them into full pages. Run from the site root:
    python3 tools/build_legal.py && python3 tools/build_pages.py

Each page has a sticky table of contents and numbered sections. Lines marked
[CONFIRM] in the notes are facts the company or its legal adviser must check
before launch; the copy is written to the site's actual behaviour (see the
audit notes in each page) and makes no claims beyond it.
"""
import html

COMPANY = 'Faisel Moosa Architects'
ADDRESS = 'Plot 1146, No. 15 Lagos Road, Rhodes Park, Lusaka, Zambia'
EMAIL = 'creativityandflair@gmail.com'
PHONE = '+260 977 824 023'
EFFECTIVE = '4 November 2026'

PAGES = {
    'privacy-policy': {
        'title': 'Privacy Policy',
        'description': f'How {COMPANY} collects, uses, stores and protects personal information submitted through this website, and the rights of data subjects under the Data Protection Act, 2021 of Zambia.',
        'intro': f'{COMPANY} ("we", "us", "our") respects your privacy. This policy explains what personal information we collect through this website, why we collect it, how we keep it and the choices you have. It is written to reflect the Data Protection Act, No. 3 of 2021 of Zambia, which regulates how personal data is collected, processed and stored, and we aim to handle your information in line with it.',
        'sections': [
            ('who-we-are', 'Who we are', [
                f'<p>{COMPANY} is a licensed architectural, planning and development services company based at {ADDRESS}. We are the data controller for personal information collected through this website.</p>',
                f'<p>You can contact us about this policy by email at <a href="mailto:{EMAIL}">{EMAIL}</a>, by telephone on <a href="tel:+260977824023">{PHONE}</a>, or by post at the address above.</p>',
            ]),
            ('what-we-collect', 'Information we collect', [
                '<p>This website collects personal information in one place only: the enquiry form on the Contact page. When you send us an enquiry we receive:</p>',
                '<ul><li>your name;</li><li>your email address;</li><li>your telephone number, if you choose to give it;</li><li>the subject you select and the message you write; and</li><li>the date and time of the enquiry and the IP address of the device it was sent from, which our form handler records with the message to help us identify misuse.</li></ul>',
                '<p>Simply browsing the website does not require you to give us any personal information. The website does not use analytics, advertising or social-media tracking tools, and it does not create an account or profile for you. See our <a href="cookie-policy.html">Cookie Policy</a> for details of the one third-party service we embed.</p>',
            ]),
            ('how-we-use', 'How we use your information', [
                '<p>We use the information from an enquiry to:</p>',
                '<ul><li>read and reply to your enquiry;</li><li>discuss a possible project with you and, if you engage us, carry out that work; and</li><li>keep a record of our correspondence.</li></ul>',
                '<p>The lawful basis for this processing is that you have asked us to respond to you and, where a project follows, that the processing is necessary to perform our agreement with you. We do not use enquiry details for marketing and we do not add you to a mailing list.</p>',
            ]),
            ('how-we-store', 'How we store and protect it', [
                '<p>Your enquiry is sent to us by email and kept in our email system and, where a project follows, in our project records. We take reasonable technical and organisational measures to protect it: the website is served over HTTPS, the form rejects malformed submissions and automated spam, and access to our email and records is limited to the people who need it to respond to you.</p>',
                '<p>We keep enquiry correspondence for as long as needed to deal with your enquiry and any project that follows, and afterwards for the period required by our professional and record-keeping obligations. <!-- [CONFIRM] state the retention period the practice actually applies --></p>',
            ]),
            ('sharing', 'Sharing your information', [
                '<p>We do not sell personal information and we do not share it with third parties for their own purposes. We share it only:</p>',
                '<ul><li>with service providers who help us run the website and our email, who act on our instructions (our web host and email provider); <!-- [CONFIRM] name the hosting and email providers once the live hosting is chosen --></li><li>with consultants and contractors on your project where you have engaged us and the sharing is necessary to carry out the work; and</li><li>where the law requires it or to protect our legal rights.</li></ul>',
                '<p>If any of these providers store information outside Zambia, we take steps to ensure it is protected to a standard comparable to Zambian law, as the Data Protection Act requires for cross-border transfers.</p>',
            ]),
            ('your-rights', 'Your rights', [
                '<p>Under the Data Protection Act, 2021 you have the right to:</p>',
                '<ul><li>ask for access to the personal information we hold about you;</li><li>ask us to correct information that is inaccurate or incomplete;</li><li>ask us to delete information we no longer need;</li><li>object to, or ask us to restrict, processing in certain circumstances;</li><li>withdraw consent where processing is based on consent; and</li><li>lodge a complaint with the Office of the Data Protection Commissioner of Zambia if you believe we have handled your information unlawfully.</li></ul>',
                f'<p>To exercise any of these rights, email <a href="mailto:{EMAIL}">{EMAIL}</a>. We will respond within the time the law allows and may ask you to confirm your identity first.</p>',
            ]),
            ('children', 'Children', [
                '<p>This website is intended for adults and businesses. We do not knowingly collect personal information from anyone under 18. If you believe a child has sent us information, contact us and we will delete it.</p>',
            ]),
            ('changes', 'Changes to this policy', [
                f'<p>We may update this policy from time to time. The date at the top of the page shows when it was last changed, and the current version is always the one published here. This version is effective from {EFFECTIVE}.</p>',
            ]),
        ],
        'related': [('terms-of-use.html', 'Terms of Use'), ('cookie-policy.html', 'Cookie Policy')],
    },
    'terms-of-use': {
        'title': 'Terms of Use',
        'description': f'The terms on which {COMPANY} makes this website available: permitted use, intellectual property, accuracy of content, liability, external links and governing law.',
        'intro': f'These terms govern your use of the {COMPANY} website. By using the website you agree to them. They apply to the website only; any architectural or other professional services we provide are governed by a separate written agreement with the client.',
        'sections': [
            ('using-the-site', 'Using this website', [
                '<p>You may browse the website and use its contact form for lawful purposes, including to learn about our practice and to enquire about our services. You must not use the website in any way that is unlawful, that could damage or interfere with it, or that sends unsolicited or automated messages through the enquiry form.</p>',
                '<p>We may change, suspend or withdraw any part of the website at any time without notice.</p>',
            ]),
            ('intellectual-property', 'Intellectual property', [
                f'<p>The content of this website, including text, drawings, renderings, photographs of our projects, the {COMPANY} name and logo, and the layout of the pages, belongs to {COMPANY} or is used under licence. It is protected by Zambian copyright and trademark law and by international treaties.</p>',
                '<p>You may view the website and print or download extracts for your own personal, non-commercial reference. You may not otherwise copy, reproduce, publish, distribute or create derivative works from any content without our written permission. Architectural designs shown on the website are the intellectual property of the practice and may not be used as the basis for any building work.</p>',
                '<p>Some photographs used to illustrate the website are licensed stock images and remain the property of their respective owners. <!-- [CONFIRM] keep licence records for the stock photography in use --></p>',
            ]),
            ('accuracy', 'Accuracy of content', [
                '<p>We take care to keep the information on the website accurate and current, but it is provided for general information only. Project descriptions, dates and images are illustrative and may be simplified. Nothing on the website is professional advice about a specific site, building or project, and it should not be relied on as such. Advice is given only under a written engagement.</p>',
            ]),
            ('liability', 'Liability', [
                '<p>To the extent permitted by law, we exclude all warranties about the website and its content, and we are not liable for any loss or damage arising from your use of, or inability to use, the website or from reliance on its content. Nothing in these terms limits liability that cannot be limited by law.</p>',
            ]),
            ('external-links', 'External links', [
                '<p>The website contains links to third-party websites and services, including a Google Maps view of our office location and links to our social-media profiles. These are provided for convenience. We do not control those sites and are not responsible for their content, availability or privacy practices. Your use of them is subject to their own terms.</p>',
            ]),
            ('privacy', 'Privacy and cookies', [
                '<p>Personal information you submit through the website is handled as described in our <a href="privacy-policy.html">Privacy Policy</a>. The way the website uses cookies is described in our <a href="cookie-policy.html">Cookie Policy</a>.</p>',
            ]),
            ('governing-law', 'Governing law', [
                '<p>These terms are governed by the laws of the Republic of Zambia, and the courts of Zambia have exclusive jurisdiction over any dispute arising from them or from your use of the website. <!-- [CONFIRM] legal review of jurisdiction clause --></p>',
            ]),
            ('contact', 'Contact', [
                f'<p>Questions about these terms can be sent to <a href="mailto:{EMAIL}">{EMAIL}</a> or to {COMPANY}, {ADDRESS}. These terms are effective from {EFFECTIVE}.</p>',
            ]),
        ],
        'related': [('privacy-policy.html', 'Privacy Policy'), ('cookie-policy.html', 'Cookie Policy')],
    },
    'cookie-policy': {
        'title': 'Cookie Policy',
        'description': f'The cookies and similar technologies used on the {COMPANY} website, what they are for and how to control them.',
        'intro': 'This policy describes the cookies and similar technologies that this website actually uses. We have kept the website deliberately simple: it does not use analytics, advertising or social-media tracking, and it sets no cookies of its own.',
        'sections': [
            ('what-are-cookies', 'What cookies are', [
                '<p>Cookies are small text files that a website stores on your device so that it can remember something about you or your visit. Similar technologies, such as browser local storage, do the same job in a different way. Cookies set by the website you are visiting are called first-party cookies; cookies set by another service embedded in the page are called third-party cookies.</p>',
            ]),
            ('cookies-we-use', 'Cookies this website uses', [
                '<p><strong>First-party cookies: none.</strong> The website does not set cookies or use browser storage. Fonts, scripts and stylesheets are served from our own domain, so viewing the pages sends no request to a third party.</p>',
                '<p><strong>Third-party cookies: Google Maps on the Contact page.</strong> The Contact page embeds an interactive map of our office from Google Maps. When that page loads, your browser requests the map from Google, and Google may set its own cookies and collect information such as your IP address and how you interact with the map. We do not control these cookies. Google describes them in its <a href="https://policies.google.com/technologies/cookies" target="_blank" rel="noopener">cookie policy</a> and <a href="https://policies.google.com/privacy" target="_blank" rel="noopener">privacy policy</a>.</p>',
                '<table class="fma-legal__table"><caption class="visually-hidden">Cookies used on this website</caption><thead><tr><th scope="col">Source</th><th scope="col">Page</th><th scope="col">Purpose</th><th scope="col">Type</th></tr></thead><tbody><tr><td>Google Maps (google.com)</td><td>Contact</td><td>Displays the map of our office; Google may use its cookies for security, preferences and analytics on its own services</td><td>Third-party; set by Google, not by us</td></tr></tbody></table>',
                '<p>No other page on the website loads third-party content. <!-- [CONFIRM] update this policy if analytics (e.g. Google Analytics), a chat widget or embedded video is added later --></p>',
            ]),
            ('managing-cookies', 'How to manage cookies', [
                '<p>Because the website sets no cookies of its own, there is nothing to switch off here. To control the Google cookies from the map you can:</p>',
                '<ul><li>block third-party cookies in your browser settings, which still lets the map display in most browsers;</li><li>clear cookies after your visit; or</li><li>avoid loading the Contact page and use the address, telephone number and email address shown in the footer instead.</li></ul>',
                '<p>Instructions for managing cookies in common browsers are available from the browser makers: <a href="https://support.google.com/chrome/answer/95647" target="_blank" rel="noopener">Chrome</a>, <a href="https://support.apple.com/en-gb/HT201265" target="_blank" rel="noopener">Safari</a>, <a href="https://support.mozilla.org/en-US/kb/enhanced-tracking-protection-firefox-desktop" target="_blank" rel="noopener">Firefox</a> and <a href="https://support.microsoft.com/en-us/microsoft-edge/delete-cookies-in-microsoft-edge-63947406-6e01-6bb0-bd5e-b1feb7aeaa3b" target="_blank" rel="noopener">Edge</a>.</p>',
            ]),
            ('changes', 'Changes to this policy', [
                f'<p>If we add a service that uses cookies, we will update this page and, where the law requires it, ask for your consent before those cookies are set. This version is effective from {EFFECTIVE}.</p>',
            ]),
        ],
        'related': [('privacy-policy.html', 'Privacy Policy'), ('terms-of-use.html', 'Terms of Use')],
    },
}


def esc(s):
    return html.escape(s, quote=True)


def page(slug, p):
    toc = '\n'.join(f'                                <li><a href="#{i}">{esc(t)}</a></li>' for i, t, _ in p['sections'])
    body = ''
    for n, (i, t, paras) in enumerate(p['sections'], 1):
        body += f'''                        <section class="fma-legal__section" id="{i}" aria-labelledby="{i}-title">
                            <h2 id="{i}-title" class="fma-legal__h2"><span class="fma-legal__num" aria-hidden="true">{n:02d}</span>{esc(t)}</h2>
{chr(10).join('                            ' + x for x in paras)}
                        </section>
'''
    related = ' · '.join(f'<a href="{h}">{esc(t)}</a>' for h, t in p['related'])
    return f'''<!-- title: {p['title']} -->
<!-- description: {p['description']} -->
<!-- nav:  -->
<main>
    <!-- Generated by tools/build_legal.py – edit the text there, not here. -->
    <!-- Breadcrumb area start -->
    <div class="breadcrumb__area header__background-color breadcrumb__header-up breadcrumb-space overly overflow-hidden">
        <div class="breadcrumb__background" data-background="./assets/imgs/legal/{slug}.jpg"></div>
        <div class="container">
            <div class="breadcrumb__bg-left"></div>
            <div class="breadcrumb__bg-right"></div>
            <div class="row align-items-center justify-content-between">
                <div class="col-12">
                    <div class="breadcrumb__content text-center">
                        <h1 class="breadcrumb__title mb-15 mb-sm-10 mb-xs-5 color-white title-animation">{esc(p['title'])}</h1>
                        <div class="breadcrumb__menu">
                            <nav aria-label="Breadcrumb">
                                <ul>
                                    <li><span><a href="index.html">Home</a></span></li>
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

    <!-- legal area start -->
    <section class="fma-legal section-space">
        <div class="container">
            <div class="row">
                <div class="col-lg-4 col-xl-3 order-lg-2">
                    <nav class="fma-legal__toc" aria-labelledby="toc-title">
                        <h2 id="toc-title" class="fma-legal__toc-title">On this page</h2>
                        <ol>
{toc}
                        </ol>
                        <p class="fma-legal__related">See also: {related}</p>
                    </nav>
                </div>
                <div class="col-lg-8 col-xl-9 order-lg-1">
                    <div class="fma-legal__content">
                        <p class="fma-legal__meta">Effective {EFFECTIVE}</p>
                        <p class="fma-legal__intro">{p['intro']}</p>
{body}                    </div>
                </div>
            </div>
        </div>
    </section>
    <!-- legal area end -->
</main>
'''


if __name__ == '__main__':
    for slug, p in PAGES.items():
        open(f'tools/pages/{slug}.html', 'w').write(page(slug, p))
        print('wrote partial', slug)
