"""Cache-busting: stamps ?v=<version> on the site's own CSS/JS links so browsers
and the GitHub Pages CDN pick up new styles immediately after a deploy.
Run from the site root after changing any file in assets/css or assets/js,
then re-run the page generators:
    python3 tools/bump_assets.py
"""
import datetime
import glob
import re

ASSETS = ['assets/css/main.css', 'assets/css/project-portfolio.css', 'assets/css/project-page.css',
          'assets/css/fma-theme.css', 'assets/js/main.js', 'assets/js/project-portfolio.js', 'assets/js/fma-site.js']
VERSION = datetime.datetime.now().strftime('%Y%m%d%H%M')

for f in ['index.html', 'contact-us.html'] + glob.glob('tools/pages/*.html') + ['tools/build_projects.py']:
    s = open(f).read()
    for a in ASSETS:
        s = re.sub(re.escape(a) + r'(\?v=\d+)?(?=["\'])', f'{a}?v={VERSION}', s)
    open(f, 'w').write(s)
print('assets stamped with v=' + VERSION)
