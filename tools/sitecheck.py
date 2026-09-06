"""Render the site on desktop and phone: no broken images, no failed requests,
no horizontal overflow, no page errors, and the Greenwood copy is current."""
import sys
from playwright.sync_api import sync_playwright
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
URL = 'file:///C:/Users/Cwell/CLAUDE/whaletailworks-site/index.html'
SHOT = ('C:/Users/Cwell/AppData/Local/Temp/claude/C--Users-Cwell/'
        '038247ee-bc53-4509-973e-fea9921a4358/scratchpad/site_%s.png')
fails = 0


def ck(name, ok, info=''):
    global fails
    print(('  OK   ' if ok else '  FAIL ') + name + ('' if ok else '  ' + str(info)[:200]))
    if not ok:
        fails += 1


with sync_playwright() as pw:
    b = pw.chromium.launch()
    for label, vp, dsf in [('desktop', {'width': 1440, 'height': 960}, 2),
                           ('phone', {'width': 390, 'height': 844}, 3)]:
        pg = b.new_page(viewport=vp, device_scale_factor=dsf)
        errs, bad = [], []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('response', lambda r: bad.append(r.url.split('/')[-1]) if r.status >= 400 else None)
        pg.goto(URL)
        pg.wait_for_timeout(1800)
        pg.evaluate("()=>document.querySelector('#games').scrollIntoView()")
        pg.wait_for_timeout(1600)
        # force the lazy images to load, or this check passes vacuously on
        # anything still below the fold
        pg.evaluate("()=>[...document.images].forEach(i=>{i.loading='eager';i.src=i.src;})")
        pg.wait_for_timeout(2500)
        broken = pg.evaluate("()=>[...document.images]"
                             ".filter(i=>!i.complete||i.naturalWidth===0)"
                             ".map(i=>i.getAttribute('src'))")
        ck('%s: every image loaded' % label, not broken, broken[:5])
        ck('%s: no failed requests' % label, not bad, bad[:5])
        ck('%s: no horizontal overflow' % label,
           pg.evaluate("()=>document.documentElement.scrollWidth<=window.innerWidth+1"),
           pg.evaluate("()=>document.documentElement.scrollWidth+' vs '+window.innerWidth"))
        ck('%s: zero page errors' % label, not errs, errs[:2])
        chips = pg.evaluate("()=>[...document.querySelectorAll('.gw-facts li')].map(e=>e.innerText)")
        ck('%s: four honesty chips render' % label, len(chips) == 4, chips)
        txt = pg.evaluate("()=>document.body.innerText")
        ck('%s: says 21 missions, not 15' % label,
           '21-mission' in txt and '15-mission' not in txt)
        pg.evaluate("()=>{const t=document.getElementById('termBody');t&&t.scrollIntoView();}")
        pg.wait_for_timeout(6000)      # the terminal types its lines in
        term = pg.evaluate("()=>{const t=document.getElementById('termBody');return t?t.innerText:'';}")
        ck('%s: ticker says 21/21 missions' % label, '21/21 missions' in term, term[:160])
        pg.locator('.game').last.screenshot(path=SHOT % label)
        pg.close()
    b.close()
print('\nRESULT:', 'ALL PASS' if not fails else '%d FAIL' % fails)
sys.exit(1 if fails else 0)
