"""The Greenwood Way is on Google Play — say so, and link to it.

Verified live 2026-09-10: net.whaletailworks.greenwood returns HTTP 200,
developer "Whale Tail Works", $3.99, Everyone 10+. The page still called it
"In Development" and offered an email link to ask about launch.

Both games are now published, so the site stops promising and starts selling.
"""
import pathlib
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
ROOT = pathlib.Path(__file__).resolve().parent.parent
STORE = 'https://play.google.com/store/apps/details?id=net.whaletailworks.greenwood'
LF = chr(10)
CRLF = chr(13) + LF

p = ROOT / 'index.html'
s = p.read_bytes().decode('utf-8')
nl = CRLF if CRLF in s else LF


def sub(old, new, label):
    global s
    o, n = old.replace(LF, nl), new.replace(LF, nl)
    c = s.count(o)
    assert c == 1, 'FAILED (%d matches): %s' % (c, label)
    s = s.replace(o, n)
    print('  ok: %s' % label)


sub('      <span class="tag dev">In Development</span>' + LF + '      <h3>The Greenwood Way</h3>',
    '      <span class="tag live">Out now on Google Play</span>' + LF + '      <h3>The Greenwood Way</h3>',
    'status tag: In Development -> Out now')

# the email CTA becomes a store button, matching XENODEX's
sub('      <a class="btn ghost" href="mailto:contact@whaletailworks.net?subject=Greenwood%20launch">Ask About Launch</a>',
    '      <a class="btn primary" href="%s" target="_blank" rel="noopener">' % STORE + LF +
    '        <svg width="17" height="17" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true">' + LF +
    '          <path d="M3 2.5v19c0 .6.6 1 1.1.7l13.2-8.7c.5-.3.5-1.1 0-1.4L4.1 1.8C3.6 1.5 3 1.9 3 2.5z"/>' + LF +
    '        </svg>Get it on Google Play</a>',
    'CTA: email enquiry -> store button')

# both games are out; the site description should not imply otherwise
sub('<meta name="description" content="Whale Tail Works LLC — an independent game studio and curated online storefront. Home of XENODEX and The Greenwood Way.">',
    '<meta name="description" content="Whale Tail Works LLC — an independent game studio and curated online storefront. XENODEX and The Greenwood Way, both out now on Google Play.">',
    'meta description mentions both are out')

p.write_bytes(s.encode('utf-8'))
print(LF + 'WRITTEN')
