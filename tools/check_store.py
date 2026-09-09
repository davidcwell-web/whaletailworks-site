"""Is either game actually on Google Play, and what does the listing say?

The console's wording proved misleading once (a "Published" row that referred to
the store listing, not the app), so this reads the public store page instead.
404 = not published. 200 = live.
"""
import re
import sys

from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', errors='replace')

APPS = [
    ('XENODEX (LLC)', 'net.whaletailworks.xenodex'),
    ('The Greenwood Way', 'net.whaletailworks.greenwood'),
    ('XENODEX (personal, retired)', 'com.davidcwell.xenodex'),
]
PAT = {
    'developer': r'Whale Tail Works[^\n]{0,40}',
    'price': r'\$\d+\.\d\d',
    'rating': r'(?:Everyone 10\+|Everyone|Teen|Rated for \d+\+)',
    'downloads': r'[\d.,]+[KMB]?\+?\s+Downloads',
    'updated': r'Updated on[^\n]{0,30}',
}

with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={'width': 1280, 'height': 1000})
    for name, pkg in APPS:
        url = 'https://play.google.com/store/apps/details?id=' + pkg
        try:
            r = pg.goto(url, wait_until='domcontentloaded', timeout=40000)
            pg.wait_for_timeout(2500)
            code = r.status if r else 0
        except Exception as e:
            print('%-28s ERROR %s' % (name, str(e)[:60]))
            continue
        print('%-28s HTTP %s  %s' % (name, code, 'LIVE' if code == 200 else 'not published'))
        if code == 200:
            txt = pg.evaluate('()=>document.body.innerText')
            print('    title      %s' % pg.title()[:70])
            for k, rx in PAT.items():
                m = re.search(rx, txt)
                print('    %-10s %s' % (k, m.group(0).strip() if m else '—'))
            print('    url        %s' % url)
        print()
    b.close()
