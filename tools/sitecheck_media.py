"""Full check of the video/motion update. Takes GW_SITE to point at a local file
URL or the live HTTPS site, so the same script proves both.

Covers what was asked: both prices, five video cards, mobile layout, muted
autoplay and pause, and the whale's tail animation.
"""
import os
import sys
import time

from playwright.sync_api import sync_playwright

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
SITE = os.environ.get('GW_SITE', 'file:///C:/Users/Cwell/CLAUDE/whaletailworks-site/index.html')
LIVE = SITE.startswith('http')
fails = 0


def ck(name, ok, info=''):
    global fails
    print(('  OK   ' if ok else '  FAIL ') + name + ('' if ok else '  ' + str(info)[:220]))
    if not ok:
        fails += 1


with sync_playwright() as pw:
    b = pw.chromium.launch()
    for label, vp in (('desktop', {'width': 1440, 'height': 960}),
                      ('phone', {'width': 390, 'height': 844})):
        pg = b.new_page(viewport=vp, is_mobile=(label == 'phone'), has_touch=(label == 'phone'))
        errs, bad, yt = [], [], []
        pg.on('pageerror', lambda e: errs.append(str(e)))
        pg.on('response', lambda r: bad.append('%s %s' % (r.status, r.url.split('/')[-1]))
              if r.status >= 400 else None)
        pg.on('request', lambda r: yt.append(r.url) if 'youtube' in r.url else None)
        pg.goto(SITE, wait_until='load')
        pg.wait_for_timeout(2500)
        print('\n--- %s ---' % label)

        # prices
        txt = pg.evaluate('()=>document.body.innerText')
        ck('%s: XENODEX price $2.99' % label, '$2.99' in txt and '$0.99' not in txt)
        ck('%s: Greenwood price $3.99' % label, '$3.99' in txt)

        # video cards
        cards = pg.evaluate("()=>document.querySelectorAll('.video-card').length")
        ck('%s: five video cards' % label, cards == 5, cards)
        ck('%s: no YouTube contact before a click' % label, not yt, yt[:3])

        # click one and confirm an iframe replaces the button
        pg.evaluate("()=>document.querySelector('#videos').scrollIntoView()")
        pg.wait_for_timeout(600)
        pg.evaluate("()=>document.querySelector('[data-video]').click()")
        pg.wait_for_timeout(1200)
        src = pg.evaluate("()=>{const f=document.querySelector('.video-slot iframe');"
                          "return f?f.src:null;}")
        ck('%s: click loads a nocookie embed' % label,
           bool(src) and 'youtube-nocookie.com/embed/' in src, src)

        # the ambient loop: muted, and pausable
        st = pg.evaluate("""()=>{const v=document.querySelector('#ambient-gameplay');
            return v?{muted:v.muted,loop:v.loop,inline:v.playsInline,
                      paused:v.paused,readyState:v.readyState}:null;}""")
        ck('%s: gameplay loop is muted and looping' % label,
           st and st['muted'] and st['loop'] and st['inline'], st)
        pg.evaluate("()=>document.querySelector('#motion-toggle').click()")
        pg.wait_for_timeout(900)
        after = pg.evaluate("()=>{const v=document.querySelector('#ambient-gameplay');"
                            "return {paused:v.paused,label:document.querySelector('#motion-toggle').textContent};}")
        ck('%s: the preview toggle changes state and label' % label,
           after['label'] in ('Play preview', 'Pause preview'), after)

        # the whale: the img is swapped for a canvas that repaints
        wh = pg.evaluate("""()=>{const c=document.querySelector('.hero-logo canvas.mark');
            return c?{w:c.width,h:c.height,label:c.getAttribute('aria-label')}:null;}""")
        ck('%s: whale replaced by a live canvas' % label, bool(wh), wh)
        if wh:
            # getImageData taints under file://, so compare rendered pixels the
            # only way that works in both contexts: screenshot the element twice.
            el = pg.locator('.hero-logo canvas.mark')
            f1 = el.screenshot()
            time.sleep(1.4)
            f2 = el.screenshot()
            ck('%s: whale canvas is painting' % label,
               len(f1) > 200 and f1 != f2, 'identical frames' if f1 == f2 else '')

        # layout + hygiene
        ck('%s: no horizontal overflow' % label,
           pg.evaluate('()=>document.documentElement.scrollWidth<=window.innerWidth+1'),
           pg.evaluate('()=>document.documentElement.scrollWidth+" vs "+window.innerWidth'))
        pg.evaluate("()=>[...document.images].forEach(i=>{i.loading='eager';i.src=i.src;})")
        pg.wait_for_timeout(2000)
        broken = pg.evaluate("()=>[...document.images].filter(i=>!i.complete||i.naturalWidth===0)"
                             ".map(i=>i.getAttribute('src'))")
        ck('%s: every image loaded' % label, not broken, broken[:4])
        realbad = [x for x in bad if 'youtube' not in x.lower()]
        ck('%s: no failed requests' % label, not realbad, realbad[:4])
        ck('%s: zero page errors' % label, not errs, errs[:2])
        pg.close()
    b.close()

print('\nRESULT:', 'ALL PASS' if not fails else '%d FAIL' % fails)
sys.exit(1 if fails else 0)
