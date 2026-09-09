"""XENODEX is on Google Play — say so, and link to it.

Verified live 2026-09-09: net.whaletailworks.xenodex returns HTTP 200, developer
"Whale Tail Works", $2.99, Everyone 10+. The site still said "Launching on
Google Play" with a dead "Available Soon" button pointing at "#".

This is the studio's first published game, so the page should send people to it
rather than describe it as forthcoming.
"""
import pathlib
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
ROOT = pathlib.Path(__file__).resolve().parent.parent
STORE = 'https://play.google.com/store/apps/details?id=net.whaletailworks.xenodex'
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


sub('<span class="tag live">Launching on Google Play</span>',
    '<span class="tag live">Out now on Google Play</span>',
    'status tag: launching -> out now')

sub('      <a class="btn primary" href="#" id="playLink">',
    '      <a class="btn primary" href="%s" id="playLink" target="_blank" rel="noopener">' % STORE,
    'play button now points at the live listing')

sub('        </svg>Available Soon on Google Play</a>',
    '        </svg>Get it on Google Play</a>',
    'button label')

# the meta description still describes both as forthcoming
sub('<meta property="og:title" content="Whale Tail Works — games you buy once and own">',
    '<meta property="og:title" content="Whale Tail Works — games you buy once and own">',
    'og:title unchanged (still accurate)')

p.write_bytes(s.encode('utf-8'))
print(LF + 'WRITTEN')
