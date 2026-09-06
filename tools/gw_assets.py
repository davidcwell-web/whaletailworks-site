"""Refresh the site's Guardians of the Greenwood Way art from the live game.

The scenes are the three the owner picked out on 2026-09-06 (the Old Wyrm's
board, the Emberdeep campfire, the company facing Nocturne). They are
RECAPTURED here rather than copied from those screenshots, which were small
window grabs; capturing from the game gives phone-resolution art and means the
site can never drift from the build. Portraits come from the game's generated
pixel portraits.
"""
import io, json, os, sys
from PIL import Image
from playwright.sync_api import sync_playwright

GAME = 'C:/Users/Cwell/CLAUDE/greenwood'
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'img')
ALL = ['reg', 'elowen', 'barnaby', 'mabs', 'sylvai', 'gruni', 'torvald', 'pip']
close = ("()=>{document.querySelectorAll('dialog[open]').forEach(d=>d.close());"
         "window.GW_CUT&&GW_CUT.isOpen()&&GW_CUT.skip();"
         "GW_TUTOR&&GW_TUTOR.stop&&GW_TUTOR.stop();}")
# the floating chatter is lovely in play and reads as clutter under a caption
HIDE = ("()=>{for(const s of ['#bubbles','#barkBar','#tileTip','#toasts','#tutorCard','#tutorRing'])"
        "for(const e of document.querySelectorAll(s))e.style.display='none';}")
# The page is taller than its content on a phone; clip from the top of the
# carved header to the foot of the board so the art panel has no dead strip.
CLIP = ("()=>{const h=document.querySelector('.topbar'),s=document.querySelector('#stage');"
        "const a=h.getBoundingClientRect(),b=s.getBoundingClientRect();"
        "return {x:0,y:Math.max(0,a.top-6),width:innerWidth,"
        "height:Math.min(innerHeight,b.bottom+8)-Math.max(0,a.top-6)};}")


def save(raw, name, width):
    im = Image.open(io.BytesIO(raw)).convert('RGB')
    im = im.resize((width, int(round(im.height * width / im.width))), Image.LANCZOS)
    p = os.path.join(OUT, name)
    im.save(p, 'JPEG', quality=84, optimize=True, progressive=True)
    print('  %-22s %sx%s  %.0f KB' % (name, im.width, im.height, os.path.getsize(p) / 1024))


with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={'width': 390, 'height': 844},
                    device_scale_factor=3, is_mobile=True, has_touch=True)
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto('file:///' + GAME + '/index.html')
    pg.wait_for_function('window.GW', timeout=25000)
    pg.wait_for_timeout(2500)
    pg.evaluate(close)
    pg.evaluate('GW.setRoster(%s)' % json.dumps(ALL))

    print('boards')
    # m4 — Hazerath's terraces: the gold wyrm, the drakes and the ice read best
    # of any board in the game, which is why it is the hero panel.
    pg.evaluate("GW.startBattle(%s,'m4')" % json.dumps(ALL[:4]))
    pg.wait_for_timeout(2200)
    pg.evaluate(close)
    pg.evaluate(HIDE)
    pg.evaluate('GW.zoomTo(1.25)')
    pg.wait_for_timeout(1500)
    save(pg.screenshot(clip=pg.evaluate(CLIP)), 'gw_shot_wyrm.jpg', 760)

    pg.evaluate("GW.startBattle(%s,'s5')" % json.dumps(ALL[:4]))
    pg.wait_for_timeout(2000)
    pg.evaluate(close)
    pg.evaluate(HIDE)
    pg.evaluate('GW.zoomTo(1.3)')
    pg.wait_for_timeout(1400)
    save(pg.screenshot(clip=pg.evaluate(CLIP)), 'gw_shot_sea.jpg', 600)

    print('campfire (Emberdeep)')
    # openCampfire falls through to the muster when nothing is offerable, which
    # is how the first attempt captured the wrong screen. Give it two talks and
    # a full company, close any muster it left up, then assert it is open.
    pg.evaluate("GW.startBattle(%s,'m3')" % json.dumps(ALL[:4]))
    pg.wait_for_timeout(1600)
    pg.evaluate(close)
    pg.evaluate("()=>{window.GW_MUSTER&&GW_MUSTER.close&&GW_MUSTER.close();}")
    pg.evaluate("()=>{const m=GW.metaObj();m.campPending=2;}")
    pg.evaluate("GW.openFire&&GW.openFire()")
    pg.wait_for_timeout(1800)
    # the once-only "Breaking camp" explainer sits over the whole scene
    pg.evaluate("()=>{try{localStorage.setItem('greenwood.campExplained','1');}catch(e){}"
                "const c=document.querySelector('#campExplain');"
                "if(c){const b=c.querySelector('button');if(b)b.click();c.style.display='none';}}")
    pg.wait_for_timeout(1600)
    assert pg.evaluate("()=>!!(window.GW_CAMP&&GW_CAMP.isOpen&&GW_CAMP.isOpen())"),         'campfire did not open — it fell through to another screen again'
    save(pg.screenshot(), 'gw_shot_camp.jpg', 600)
    pg.evaluate("window.GW_CAMP&&GW_CAMP.close&&GW_CAMP.close()")

    print('cutscene (the company before Nocturne)')
    pg.evaluate("GW.stage('m7_concord')")
    pg.wait_for_timeout(3200)
    for _ in range(60):
        d = pg.evaluate("GW_CUT.debug()")
        if d['line'] is not None and len(d['actors']) >= 4:
            break
        pg.evaluate("GW_CUT.tap()")
        pg.wait_for_timeout(400)
    pg.wait_for_timeout(700)
    save(pg.screenshot(), 'gw_shot_cut.jpg', 600)
    pg.evaluate("GW_CUT.skip()")
    b.close()
assert not errs, errs[:3]

print('portraits')
for k in ALL:
    src = os.path.join(GAME, 'art/newlook/pixel', 'port_%s.png' % k)
    im = Image.open(src).convert('RGBA')
    s = min(im.width, im.height)
    im = im.crop(((im.width - s) // 2, 0, (im.width - s) // 2 + s, s)).resize((96, 96), Image.LANCZOS)
    p = os.path.join(OUT, 'gw_%s.png' % k)
    im.save(p, optimize=True)
print('  8 portraits written')
print('zero page errors')
