"""Add the studio's social accounts, and the card metadata the site never had.

Sharing whaletailworks.net produced a bare link with no title, description or
image, because the page carried no Open Graph or Twitter card tags at all. Now
that the studio is posting on X and YouTube, every share is a missed impression.

  - og:* and twitter:card metadata, pointing at the new 1200x630 social card
  - twitter:site so shared links are attributed to @whaletailworks
  - a Follow column in the footer with X and YouTube (YouTube moves out of
    Navigate, where it did not belong)
"""
import pathlib
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
ROOT = pathlib.Path(__file__).resolve().parent.parent
LF = chr(10)
CRLF = chr(13) + LF

X_URL = 'https://x.com/whaletailworks'
YT_URL = 'https://www.youtube.com/channel/UCmSlGVq_usKin321b86frdg'


def edit(rel, pairs):
    p = ROOT / rel
    s = p.read_bytes().decode('utf-8')
    nl = CRLF if CRLF in s else LF
    for old, new, label in pairs:
        o, n = old.replace(LF, nl), new.replace(LF, nl)
        c = s.count(o)
        assert c == 1, 'FAILED %s: %d matches for %s' % (rel, c, label)
        s = s.replace(o, n)
        print('  ok: %-40s %s' % (label, rel))
    p.write_bytes(s.encode('utf-8'))


DESC = ('Premium games you buy once and own. No ads, no purchases, no account, '
        'no internet needed. XENODEX and The Greenwood Way, from a studio in South Carolina.')

META = LF.join([
    '<meta name="description" content="Whale Tail Works LLC — an independent game studio and curated online storefront. Home of XENODEX and The Greenwood Way.">',
    '',
    '<!-- Social cards. Without these a shared link is a bare URL with no preview. -->',
    '<meta property="og:type" content="website">',
    '<meta property="og:site_name" content="Whale Tail Works LLC">',
    '<meta property="og:url" content="https://whaletailworks.net/">',
    '<meta property="og:title" content="Whale Tail Works — games you buy once and own">',
    '<meta property="og:description" content="%s">' % DESC,
    '<meta property="og:image" content="https://whaletailworks.net/img/social_card.jpg">',
    '<meta property="og:image:width" content="1200">',
    '<meta property="og:image:height" content="630">',
    '<meta property="og:image:alt" content="Whale Tail Works — XENODEX and The Greenwood Way">',
    '<!-- twitter:title/description/image inherit from og:* above. -->',
    '<meta name="twitter:card" content="summary_large_image">',
    '<meta name="twitter:site" content="@whaletailworks">',
    '<meta name="twitter:creator" content="@whaletailworks">',
])

FOOT_OLD = LF.join([
    '      <a href="privacy.html">Privacy Policy</a>',
    '      <a href="%s" target="_blank" rel="noopener">YouTube channel</a>' % YT_URL,
    '    </div>',
    '    <div>',
    '      <h5>Contact</h5>',
])
FOOT_NEW = LF.join([
    '      <a href="privacy.html">Privacy Policy</a>',
    '    </div>',
    '    <div>',
    '      <h5>Follow</h5>',
    '      <a href="%s" target="_blank" rel="noopener">X · @whaletailworks</a>' % X_URL,
    '      <a href="%s" target="_blank" rel="noopener">YouTube channel</a>' % YT_URL,
    '    </div>',
    '    <div>',
    '      <h5>Contact</h5>',
])

edit('index.html', [
    ('<meta name="description" content="Whale Tail Works LLC — an independent game studio and curated online storefront. Home of XENODEX and The Greenwood Way.">',
     META, 'open graph + twitter card metadata'),
    (FOOT_OLD, FOOT_NEW, 'Follow column with X and YouTube'),
])
print(LF + 'WRITTEN')
