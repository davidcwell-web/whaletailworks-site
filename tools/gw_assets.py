"""Refresh the site's Guardians of the Greenwood Way art from the live game.

Board shots are captured on a desktop viewport, cropped to the stage and written
as 900px progressive JPEGs; portraits come straight from the game's generated
pixel portraits at 96px. Re-run after any art pass so the site never shows a
build the game has moved past.
"""
import io, json, os, sys
from PIL import Image
from playwright.sync_api import sync_playwright

GAME = 'C:/Users/Cwell/CLAUDE/greenwood'
OUT  = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'img')
ALL  = ['reg', 'elowen', 'barnaby', 'mabs', 'sylvai', 'gruni', 'torvald', 'pip']
BOARDS = [('wild', 'w1', 1.35), ('sea', 's5', 1.30), ('peaks', 'm6', 1.30)]
close = ("()=>{document.querySelectorAll('dialog[open]').forEach(d=>d.close());"
         "window.GW_CUT&&GW_CUT.isOpen()&&GW_CUT.skip();"
         "GW_TUTOR&&GW_TUTOR.stop&&GW_TUTOR.stop();}")


def jpeg(img, name, w=900, ratio=900 / 617):
    """Centre-crop to the site's aspect, resize, save progressive JPEG."""
    tw, th = img.width, int(round(img.width / ratio))
    if th > img.height:
        th = img.height
        tw = int(round(th * ratio))
    left, top = (img.width - tw) // 2, (img.height - th) // 2
    img = img.crop((left, top, left + tw, top + th))
    img = img.resize((w, int(round(w / ratio))), Image.LANCZOS).convert('RGB')
    p = os.path.join(OUT, name)
    img.save(p, 'JPEG', quality=82, optimize=True, progressive=True)
    print('  %-22s %sx%s  %.0f KB' % (name, img.width, img.height, os.path.getsize(p) / 1024))


print('board shots')
with sync_playwright() as pw:
    b = pw.chromium.launch()
    pg = b.new_page(viewport={'width': 1440, 'height': 980}, device_scale_factor=2)
    errs = []
    pg.on('pageerror', lambda e: errs.append(str(e)))
    pg.goto('file:///' + GAME + '/index.html')
    pg.wait_for_function('window.GW', timeout=25000)
    pg.wait_for_timeout(2500)
    pg.evaluate(close)
    pg.evaluate('GW.setRoster(%s)' % json.dumps(ALL))
    for name, mk, z in BOARDS:
        pg.evaluate("GW.startBattle(%s,'%s')" % (json.dumps(ALL[:4]), mk))
        pg.wait_for_timeout(1800)
        pg.evaluate(close)
        pg.evaluate('GW.zoomTo(%s)' % z)
        pg.wait_for_timeout(1400)
        shot = pg.locator('#stage').screenshot()
        jpeg(Image.open(io.BytesIO(shot)), 'gw_shot_%s.jpg' % name)
    b.close()
assert not errs, errs[:3]

print('portraits')
for k in ALL:
    src = os.path.join(GAME, 'art/newlook/pixel', 'port_%s.png' % k)
    im = Image.open(src).convert('RGBA')
    s = min(im.width, im.height)
    im = im.crop(((im.width - s) // 2, 0, (im.width - s) // 2 + s, s))
    im = im.resize((96, 96), Image.LANCZOS)
    p = os.path.join(OUT, 'gw_%s.png' % k)
    im.save(p, optimize=True)
    print('  gw_%s.png  %.0f KB' % (k, os.path.getsize(p) / 1024))
print('zero page errors')
