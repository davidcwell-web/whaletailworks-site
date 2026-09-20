"""The Last Residents joins the catalog as a coming-soon title.

Why: the studio's next game is far enough along to announce. The card stays
deliberately vague (no chapter names, no spirit rules, no ending) and shows
five room paintings from the game. No video yet.
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

ENTRY = """  },
  {
    id: 'last-residents', title: 'The Last Residents', genre: 'Mystery adventure', status: 'coming-soon',
    accent: '#9fc0dc', price: 'Coming soon',
    priceNote: 'One-time purchase · No ads',
    summary: 'You came to pick up your girlfriend. The lights are on. Nobody answers.',
    cover: 'media/game-catalog/last-residents-cover.webp',
    coverAlt: 'The Last Residents — a house on a hill above a lit town, rain at every window',
    paragraphs: [
      'A house that remembers. Every room holds something that happened in it, and something that is still waiting. Walk in, look closely, and work out what each room wants before it lets you go further.',
      'Point-and-click puzzles that use the whole house: old tapes and older wiring, a phone that only finds a signal in certain places, notes nobody meant you to read, and a few things that move when you are not looking.',
      'Painted rooms, a storm that never quite stops, and a story that starts with an ordinary evening and ends somewhere else entirely.'
    ],
    features: [
      'Planned as a premium game: buy once, own it. No ads, no in-app purchases.',
      'Plays fully offline.',
      'Puzzles with no timers and no lives. Every mistake has a way back.',
      'A spooky mystery for teens and up. Quiet more often than loud.'
    ],
    screenshots: [
      {src:'img/lr_shot_kitchen.jpg',caption:'The kitchen, after dark'},
      {src:'img/lr_shot_hall.jpg',caption:'The stair hall'},
      {src:'img/lr_shot_lounge.jpg',caption:'The sitting room'},
      {src:'img/lr_shot_study.jpg',caption:'A study nobody uses'},
      {src:'img/lr_shot_garage.jpg',caption:'The garage'}
    ],
    privacy: 'last-residents-privacy.html'
  }
];"""

patch('media/game-catalog/games-data.js', [
    ("    privacy: 'reef-currents-privacy.html'\n  }\n];", "    privacy: 'reef-currents-privacy.html'\n" + ENTRY, 'catalog entry'),
])

patch('index.html', [
    ('media/game-catalog/games-catalog.css?v=20260913-videos', 'media/game-catalog/games-catalog.css?v=20260920-lr', 'css cache version'),
    ('media/game-catalog/games-data.js?v=20260913-videos', 'media/game-catalog/games-data.js?v=20260920-lr', 'data cache version'),
    ('media/game-catalog/games-catalog.js?v=20260913-videos', 'media/game-catalog/games-catalog.js?v=20260920-lr', 'js cache version'),
    ('<li>Reef Currents — coming soon, free with an optional $1.99 upgrade.</li></ul>',
     '<li>Reef Currents — coming soon, free with an optional $1.99 upgrade.</li><li>The Last Residents — coming soon, a mystery adventure in a house that remembers.</li></ul>',
     'noscript list'),
    ('<meta name="description" content="Explore XENODEX and The Greenwood Way, out now on Google Play, plus Reef Currents, an upcoming cozy underwater puzzle. Original games from Whale Tail Works LLC.">',
     '<meta name="description" content="Explore XENODEX and The Greenwood Way, out now on Google Play, plus Reef Currents, an upcoming cozy underwater puzzle, and The Last Residents, a mystery adventure in a house that remembers. Original games from Whale Tail Works LLC.">',
     'meta description'),
    ("    ['> loading projects…  <span class=\"g\">[██████████] 3 worlds found</span>',''],",
     "    ['> loading projects…  <span class=\"g\">[██████████] 4 worlds found</span>',''],",
     'terminal world count'),
    ("    ['> reef_currents ..... <span class=\"g\">30 boards set · endless reef growing</span>',''],",
     "    ['> reef_currents ..... <span class=\"g\">30 boards set · endless reef growing</span>',''],\n    ['> last_residents .... <span class=\"g\">lights on · nobody answers</span>',''],",
     'terminal last residents line'),
])

patch('tools/sitecheck_media.py', [
    ("    'reef-currents': [],\n", "    'reef-currents': [],\n    'last-residents': [],\n", 'sitecheck expected games'),
])

patch('media/game-catalog/README.md', [
    ('- `outfit.ttf`: previously bundled Outfit font.',
     '- `last-residents-cover.webp` and `img/lr_shot_*.jpg`: size/format conversions of\n  the room paintings and the arrival painting from *The Last Residents* (generated\n  with OpenAI image generation during that project; prompts and provenance stay in\n  the game project). Added 2026-09-20 for the coming-soon card. No video yet.\n- `outfit.ttf`: previously bundled Outfit font.',
     'README artwork record'),
])
print('DONE')
