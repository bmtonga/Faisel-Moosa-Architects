"""Standalone pages (about-us.html, ...) built from a <main> partial in
tools/pages/<name>.html plus index.html's header and footer.

Run from the site root, after any header/footer change on index.html:
    python3 tools/build_pages.py

Each partial starts with two comment lines that set the page title and the
meta description, then the <main> ... </main> markup:
    <!-- title: About Us -->
    <!-- description: ... -->
Links in the shared header/footer are rewritten to point back at the home
page sections, and the matching top-level nav item gets the active class
(the partial's third optional line: <!-- nav: about-us.html -->).
"""
import glob
import html
import os
import re

INDEX = open('index.html').read()


def chrome(active_href):
    body_start = INDEX.index('<body class="body-1">') + len('<body class="body-1">')
    main_start = INDEX.index('<main>')
    top = INDEX[body_start:main_start]
    foot = INDEX[INDEX.index('<footer>'):]
    fix = lambda t: re.sub(r'href="#(about|services|projects(?:-[a-z]+)?|blog)"', r'href="index.html#\1"', t)
    top = fix(top).replace('<li class="active"><a href="index.html">Home</a></li>', '<li><a href="index.html">Home</a></li>')
    if active_href:
        top = top.replace(f'<li><a href="{active_href}">', f'<li class="active"><a href="{active_href}">', 1)
    return top, fix(foot)


def head_for(title, desc):
    h = INDEX[:INDEX.index('<body class="body-1">')]
    h = re.sub(r'<title>.*?</title>', f'<title>{html.escape(title)} – Faisel Moosa Architects</title>', h, count=1)
    h = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{html.escape(desc, quote=True)}">', h, count=1)
    return h


def build():
    for partial in sorted(glob.glob('tools/pages/*.html')):
        name = os.path.basename(partial)
        src = open(partial).read()
        meta = dict(re.findall(r'<!-- (title|description|nav): (.*?) -->', src))
        main = src[src.index('<main>'):src.index('</main>') + len('</main>')]
        top, foot = chrome(meta.get('nav'))
        page = head_for(meta['title'], meta['description']) + '<body class="body-1">' + top + main + '\n\n' + foot
        open(name, 'w').write(page)
        print('wrote', name)


if __name__ == '__main__':
    build()
