"""Reef Currents joins the line-up, and the studio promise stops being
"no ads, ever" for every game.

Why: the third game is free with occasional ads and a single $1.99 purchase
that removes them. XENODEX and The Greenwood Way keep their own "no ads"
facts (still true). The studio-level line becomes the thing all three share:
no subscriptions, no loot boxes, no accounts — buy once and own it, or one
purchase that removes ads for good.

Also adds the Reef Currents card ("In development" tag, the same one Greenwood
carried before launch) and links its privacy page.
"""
import pathlib, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')
ROOT = pathlib.Path(__file__).resolve().parent.parent
LF = chr(10); CRLF = chr(13) + LF

def patch(name, pairs):
    p = ROOT / name; s = p.read_bytes().decode('utf-8'); nl = CRLF if CRLF in s else LF
    for old, new, label in pairs:
        o, n = old.replace(LF, nl), new.replace(LF, nl)
        c = s.count(o); assert c == 1, 'FAILED (%d matches) in %s: %s' % (c, name, label)
        s = s.replace(o, n); print('  ok: %s' % label)
    p.write_bytes(s.encode('utf-8')); print('WRITTEN', name)

CARD = '''  <div class="game rv">
    <div class="art" style="background:
      radial-gradient(80% 100% at 30% 100%,rgba(34,211,238,.18),transparent),
      linear-gradient(160deg,#07202b,#091120)">
      <img class="gw-shot" src="img/reef_shot_opening.jpg"
           alt="Reef Currents — a sunlit reef with glowing coral and an anemone waiting for water"
           loading="lazy" decoding="async">
    </div>
    <div class="info">
      <span class="tag dev">In development</span>
      <h3>Reef Currents</h3>
      <p class="gw-feat"><strong>Free to play · one $1.99 purchase removes ads forever</strong></p>
      <div class="genre">cozy underwater puzzle · all ages · 30–60 second boards</div>
      <p>Turn the channel stones, guide a fresh current from the inlet to every anemone, then release it and
      watch the reef come alive. No timer, no lives, no move limit. Hints and undo are always free.</p>
      <p class="gw-feat">Thirty hand-set boards across six reef gardens, then an endless reef that keeps
      growing · shells, crabs, kelp and small fish, with a shark, an octopus or a whale's fin passing the edge now
      and then · a journal that fills as you meet them.</p>
      <p class="gw-feat">Classical music rendered for the game — Bach, Pachelbel and an original pavane — and a
      turn sound that climbs a little scale as you play.</p>
      <ul class="gw-facts">
        <li>Plays fully offline</li>
        <li>Occasional ads between boards, never during one</li>
        <li>Non-personalised ads, suitable for children</li>
        <li>One purchase, ever: remove ads for good</li>
      </ul>
      <div class="gw-gallery">
        <img src="img/reef_shot_board.jpg" alt="A five-by-five board of channel stones under water" loading="lazy" decoding="async">
        <img src="img/reef_shot_complete.jpg" alt="A little life returns — the habitat restored card" loading="lazy" decoding="async">
        <img src="img/reef_shot_map.jpg" alt="Your little reef — the map of restored boards" loading="lazy" decoding="async">
      </div>
      <a class="btn ghost" href="reef-currents-privacy.html">Privacy policy</a>
    </div>
  </div>
</section>

<section id="videos">'''

patch('index.html', [
    ('<meta property="og:title" content="Whale Tail Works — games you buy once and own">',
     '<meta property="og:title" content="Whale Tail Works — games worth keeping">',
     'og:title'),
    ('<meta property="og:description" content="Premium games you buy once and own. No ads, no purchases, no account, no internet needed. XENODEX and The Greenwood Way, from a studio in South Carolina.">',
     '<meta property="og:description" content="No subscriptions, no loot boxes, no accounts. Premium games you buy once and own, and free games with one purchase that removes ads for good. XENODEX, The Greenwood Way and Reef Currents, from a studio in South Carolina.">',
     'og:description'),
    ('<p>From alien-hunting strategy to cozy pixel adventures — premium games with no ads, no gacha, no nonsense. Pay once, play forever.</p>',
     '<p>From alien-hunting strategy to cozy pixel adventures to a quiet reef puzzle. No subscriptions, no loot boxes, no accounts. Our premium games are yours the day you buy them; our free games have one purchase, ever, that removes ads for good.</p>',
     'Original Games paragraph'),
    ("    ['> promise: no ads. no gacha. games worth keeping.','']",
     "    ['> reef_currents ..... <span class=\"g\">30 boards set · endless reef growing</span>',''],\n    ['> promise: no subscriptions. no loot boxes. games worth keeping.','']",
     'terminal lines'),
    ("    ['> loading projects…  <span class=\"g\">[██████████] 2 worlds found</span>',''],",
     "    ['> loading projects…  <span class=\"g\">[██████████] 3 worlds found</span>',''],",
     'terminal world count'),
    ('        </svg>Get it on Google Play</a>\n    </div>\n  </div>\n</section>\n\n<section id="videos">',
     '        </svg>Get it on Google Play</a>\n    </div>\n  </div>\n' + CARD,
     'Reef Currents card after Greenwood'),
])

patch('privacy.html', [
    ('<p>Our games are premium, offline-first titles. They do not contain advertising SDKs, do not require\naccounts, and do not transmit gameplay data to us. Game saves are stored locally on your device.\nWhere a game has its own privacy policy, it is linked from that game\'s store listing.</p>\n<ul>\n<li><a href="greenwood-privacy.html">The Greenwood Way</a></li>',
     '<p>Our premium games are offline-first titles that contain no advertising SDKs, require no accounts, and\ntransmit no gameplay data to us. Our free games show non-personalised advertisements between puzzles through\nGoogle AdMob and offer one purchase that removes them; they still require no accounts and send us nothing.\nGame saves are stored locally on your device. Each game\'s own policy is linked from its store listing and below.</p>\n<ul>\n<li><a href="greenwood-privacy.html">The Greenwood Way</a></li>\n<li><a href="reef-currents-privacy.html">Reef Currents</a></li>',
     'Our games paragraph + Reef link'),
])
