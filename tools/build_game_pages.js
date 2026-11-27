#!/usr/bin/env node
// Builds one static page per game from media/game-catalog/games-data.js, plus sitemap.xml.
//
//   node tools/build_game_pages.js          write <game-id>/index.html for every available game, and sitemap.xml
//   node tools/build_game_pages.js --check  exit 1 if any generated file is out of date (run before a push)
//
// Why: the homepage catalog is built by script, so crawlers that do not run JavaScript (and the AI answer
// crawlers) see almost nothing about each game. These pages carry the same facts as the popups in plain HTML,
// with a canonical URL, social cards and JSON-LD. games-data.js stays the single source: edit a game there,
// then rerun this script. Never hand-edit a generated page; the next run overwrites it.
'use strict';
const fs = require('fs');
const path = require('path');

const ROOT = path.join(__dirname, '..');
const SITE = 'https://whaletailworks.net';
const CHECK = process.argv.includes('--check');

global.window = {};
require(path.join(ROOT, 'media', 'game-catalog', 'games-data.js'));
const games = window.WTW_GAME_CATALOG.filter((g) => g.status === 'available');

// ---- image sizes (PNG, JPEG, WebP), so every <img> gets width and height and the layout does not shift ----
function imageSize(rel) {
  const file = path.join(ROOT, rel);
  if (!fs.existsSync(file)) throw new Error('missing image: ' + rel);
  const b = fs.readFileSync(file);
  if (b.readUInt32BE(0) === 0x89504e47) return { w: b.readUInt32BE(16), h: b.readUInt32BE(20) };
  if (b.toString('ascii', 0, 4) === 'RIFF' && b.toString('ascii', 8, 12) === 'WEBP') {
    const kind = b.toString('ascii', 12, 16);
    if (kind === 'VP8X') return { w: 1 + b.readUIntLE(24, 3), h: 1 + b.readUIntLE(27, 3) };
    if (kind === 'VP8L') { const n = b.readUInt32LE(21); return { w: (n & 0x3fff) + 1, h: ((n >> 14) & 0x3fff) + 1 }; }
    if (kind === 'VP8 ') return { w: b.readUInt16LE(26) & 0x3fff, h: b.readUInt16LE(28) & 0x3fff };
  }
  if (b[0] === 0xff && b[1] === 0xd8) {
    let i = 2;
    while (i < b.length) {
      if (b[i] !== 0xff) { i++; continue; }
      const m = b[i + 1];
      if (m >= 0xc0 && m <= 0xcf && m !== 0xc4 && m !== 0xc8 && m !== 0xcc) return { h: b.readUInt16BE(i + 5), w: b.readUInt16BE(i + 7) };
      i += 2 + b.readUInt16BE(i + 2);
    }
  }
  throw new Error('cannot read size: ' + rel);
}

const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
const abs = (rel) => SITE + '/' + rel.replace(/^\/+/, '');
const up = (rel) => '../' + rel; // pages live one folder down
const priceNumber = (p) => (/free/i.test(p) ? '0' : (String(p).match(/[\d.]+/) || ['0'])[0]);
const firstSentence = (s) => (s.match(/^.*?[.!?](\s|$)/) || [s])[0].trim();

function description(g) {
  // Summary + platforms + price, kept near 155 characters. Built only from fields in games-data.js.
  // Each store gets its own price, because they can differ (Reef Currents: free on Play, $0.99 on iOS).
  const play = /free/i.test(g.price) ? 'Free on Google Play' : `${g.price} on Google Play`;
  const apple = g.ios === 'available' ? (g.appStorePrice || `${g.price} on the App Store`) : '';
  const where = apple ? (apple.startsWith(g.price + ' ') ? `${g.price} on Google Play and the App Store` : `${play}, ${apple}`) : play;
  let d = `${g.summary} ${g.genre} for Android${apple ? ' and iOS' : ''}. ${where}.`;
  if (d.length > 160) d = `${g.summary} ${where}.`;
  return d;
}

function jsonLd(g) {
  const offers = [{
    '@type': 'Offer', price: priceNumber(g.price), priceCurrency: 'USD',
    availability: 'https://schema.org/InStock', url: g.store, category: 'Google Play',
  }];
  if (g.ios === 'available' && g.appStore) {
    offers.push({
      '@type': 'Offer', price: priceNumber(g.appStorePrice || g.price), priceCurrency: 'USD',
      availability: 'https://schema.org/InStock', url: g.appStore, category: 'App Store',
    });
  }
  const multi = (g.features || []).concat(g.paragraphs || []).some((t) => /co-op|versus|multiplayer|two to four players/i.test(t));
  const game = {
    '@type': ['VideoGame', 'MobileApplication'],
    '@id': `${SITE}/${g.id}/#game`,
    name: g.title,
    url: `${SITE}/${g.id}/`,
    description: g.summary,
    genre: g.genre,
    image: abs(g.cover),
    applicationCategory: 'GameApplication',
    operatingSystem: g.ios === 'available' ? 'Android, iOS' : 'Android',
    gamePlatform: g.ios === 'available' ? ['Android', 'iOS'] : ['Android'],
    playMode: multi ? ['SinglePlayer', 'MultiPlayer', 'CoOp'] : 'SinglePlayer',
    publisher: { '@id': `${SITE}/#org` },
    author: { '@id': `${SITE}/#org` },
    offers,
  };
  if (g.screenshots?.length) game.screenshot = g.screenshots.map((s) => abs(s.src));
  const yt = (g.videos || []).find((v) => v.id);
  if (yt) game.trailer = { '@type': 'VideoObject', name: `${g.title} - ${yt.title}`, embedUrl: `https://www.youtube-nocookie.com/embed/${yt.id}`, url: `https://www.youtube.com/watch?v=${yt.id}`, thumbnailUrl: abs(yt.poster) };
  const page = {
    '@type': 'WebPage', '@id': `${SITE}/${g.id}/#webpage`, url: `${SITE}/${g.id}/`, name: g.title,
    isPartOf: { '@id': `${SITE}/#website` }, about: { '@id': `${SITE}/${g.id}/#game` },
    breadcrumb: { '@id': `${SITE}/${g.id}/#breadcrumb` },
  };
  const crumbs = {
    '@type': 'BreadcrumbList', '@id': `${SITE}/${g.id}/#breadcrumb`,
    itemListElement: [
      { '@type': 'ListItem', position: 1, name: 'Whale Tail Works', item: `${SITE}/` },
      { '@type': 'ListItem', position: 2, name: 'Games', item: `${SITE}/#games` },
      { '@type': 'ListItem', position: 3, name: g.title, item: `${SITE}/${g.id}/` },
    ],
  };
  return JSON.stringify({ '@context': 'https://schema.org', '@graph': [game, page, crumbs] }, null, 2).replace(/</g, '\\u003c');
}

function img(rel, alt, cls, lazy) {
  const s = imageSize(rel);
  return `<img${cls ? ` class="${cls}"` : ''} src="${esc(up(rel))}" alt="${esc(alt)}" width="${s.w}" height="${s.h}"${lazy ? ' loading="lazy" decoding="async"' : ''}>`;
}

function videoBlock(v, g) {
  if (v.id) {
    const poster = v.poster ? img(v.poster, `${g.title} - ${v.title}`, '', true) : '';
    return `<figure class="video"><a href="https://www.youtube.com/watch?v=${esc(v.id)}" rel="noopener">${poster}<span class="play">Watch on YouTube</span></a><figcaption>${esc(v.title)}</figcaption></figure>`;
  }
  const size = v.poster ? imageSize(v.poster) : null;
  return `<figure class="video"><video controls preload="none" playsinline${v.poster ? ` poster="${esc(up(v.poster))}" width="${size.w}" height="${size.h}"` : ''}><source src="${esc(up(v.src))}" type="video/mp4"></video><figcaption>${esc(v.title)}</figcaption></figure>`;
}

function page(g) {
  const desc = description(g);
  const title = `${g.title} - ${g.genre} for Android${g.ios === 'available' ? ' and iOS' : ''} | Whale Tail Works`;
  const buttons = [`<a class="store" href="${esc(g.store)}" rel="noopener">Get it on Google Play <span>${esc(g.price)}</span></a>`];
  if (g.ios === 'available' && g.appStore) buttons.push(`<a class="store" href="${esc(g.appStore)}" rel="noopener">Download on the App Store <span>${esc((g.appStorePrice || g.price).replace(/ on the App Store$/, ''))}</span></a>`);
  else if (g.ios === 'coming-soon') buttons.push('<span class="soon">iOS: coming soon</span>');
  const facts = [
    ['Genre', g.genre],
    ['Platforms', g.ios === 'available' ? 'Android (Google Play), iOS (App Store)' : 'Android (Google Play)' + (g.ios === 'coming-soon' ? '; iOS coming soon' : '')],
    ['Price', `${g.price} on Google Play${g.ios === 'available' && g.appStorePrice ? '; ' + g.appStorePrice : ''}`],
    ['Purchase', g.priceNote],
    ['Developer', 'Whale Tail Works LLC, a one-person studio in South Carolina'],
  ];
  const heroes = g.heroes?.length ? `<section><h2>The heroes</h2><ul class="heroes">${g.heroes.map((h) => `<li>${img(h.src, h.name, '', true)}<span>${esc(h.name)}</span></li>`).join('')}</ul></section>` : '';
  const shots = g.screenshots?.length ? `<section><h2>Screenshots</h2><div class="shots">${g.screenshots.map((s) => `<figure>${img(s.src, `${g.title}: ${s.caption}`, '', true)}<figcaption>${esc(s.caption)}</figcaption></figure>`).join('')}</div></section>` : '';
  const vids = g.videos?.length ? `<section><h2>Videos</h2><div class="videos">${g.videos.map((v) => videoBlock(v, g)).join('')}</div></section>` : '';
  const others = games.filter((o) => o.id !== g.id).map((o) => `<li><a href="../${o.id}/">${esc(o.title)}</a> <span>${esc(o.genre)}</span></li>`).join('');
  return `<!DOCTYPE html>
<!-- GENERATED by tools/build_game_pages.js from media/game-catalog/games-data.js. Do not edit by hand. -->
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(title)}</title>
<meta name="description" content="${esc(desc)}">
<link rel="canonical" href="${SITE}/${g.id}/">
<meta property="og:type" content="website">
<meta property="og:site_name" content="Whale Tail Works LLC">
<meta property="og:url" content="${SITE}/${g.id}/">
<meta property="og:title" content="${esc(g.title)}">
<meta property="og:description" content="${esc(desc)}">
<meta property="og:image" content="${abs(g.cover)}">
<meta property="og:image:alt" content="${esc(g.coverAlt || g.title)}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:site" content="@whaletailworks">
<link rel="icon" type="image/png" href="../favicon.png">
<link rel="stylesheet" href="../media/game-pages.css">
<script type="application/ld+json">
${jsonLd(g)}
</script>
</head>
<body style="--accent:${esc(g.accent)}">
<header class="top"><a href="../">Whale Tail Works</a><nav><a href="../#games">All games</a><a href="../#studio">Studio</a></nav></header>
<main>
<nav class="crumbs" aria-label="Breadcrumb"><a href="../">Home</a> / <a href="../#games">Games</a> / <span aria-current="page">${esc(g.title)}</span></nav>
<section class="hero">
<div class="cover${g.containCover ? ' contain' : ''}">${img(g.cover, g.coverAlt || g.title, '', false)}</div>
<div class="intro">
<p class="genre">${esc(g.genre)}</p>
<h1>${esc(g.title)}</h1>
<p class="summary">${esc(g.summary)}</p>
<div class="buttons">${buttons.join('')}</div>
<p class="note">${esc(g.priceNote)}. Prices in USD; local store prices may vary.</p>
</div>
</section>
<section><h2>About the game</h2>${(g.paragraphs || []).map((p) => `<p>${esc(p)}</p>`).join('')}</section>
<section><h2>What you get</h2><ul class="features">${(g.features || []).map((f) => `<li>${esc(f)}</li>`).join('')}</ul></section>
<section><h2>Facts</h2><dl class="facts">${facts.map(([k, v]) => `<dt>${esc(k)}</dt><dd>${esc(v)}</dd>`).join('')}</dl></section>
${heroes}
${shots}
${vids}
<section><h2>More from Whale Tail Works</h2><ul class="more">${others}</ul></section>
</main>
<footer><p><a href="../${esc(g.privacy)}">${esc(g.title)} privacy policy</a> · <a href="mailto:support@whaletailworks.net">support@whaletailworks.net</a> · <a href="../">whaletailworks.net</a></p><p>© Whale Tail Works LLC</p></footer>
</body>
</html>
`;
}

function sitemap() {
  const pages = ['', ...games.map((g) => g.id + '/')];
  // Privacy pages of released games only: a page for an unreleased game (EMBERKIT) stays reachable but unlisted.
  const released = new Set(games.map((g) => g.privacy));
  const htmls = fs.readdirSync(ROOT).filter((f) => f.endsWith('.html') && f !== 'index.html' && f !== 'xenodex' &&
    (released.has(f) || f === 'privacy.html' || f === 'wickhold-delete-data.html' || (f === 'reef-currents-ios-privacy.html' && released.has('reef-currents-privacy.html'))));
  if (fs.existsSync(path.join(ROOT, 'xenodex', 'privacy.html'))) htmls.push('xenodex/privacy.html');
  const urls = pages.concat(htmls.sort()).map((p) => `  <url><loc>${SITE}/${p}</loc></url>`).join('\n');
  return `<?xml version="1.0" encoding="UTF-8"?>\n<!-- GENERATED by tools/build_game_pages.js. Rerun it after adding a page. -->\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n${urls}\n</urlset>\n`;
}

const outputs = games.map((g) => [path.join(ROOT, g.id, 'index.html'), page(g)]);
outputs.push([path.join(ROOT, 'sitemap.xml'), sitemap()]);
let stale = 0;
for (const [file, body] of outputs) {
  const rel = path.relative(ROOT, file);
  const current = fs.existsSync(file) ? fs.readFileSync(file, 'utf8') : null;
  // Git on Windows may check files out with CRLF; compare without line endings so --check stays honest.
  if (current !== null && current.replace(/\r\n/g, '\n') === body) { console.log('unchanged  ' + rel); continue; }
  if (CHECK) { console.log('OUT OF DATE  ' + rel); stale++; continue; }
  fs.mkdirSync(path.dirname(file), { recursive: true });
  fs.writeFileSync(file, body);
  console.log('wrote      ' + rel);
}
if (CHECK && stale) { console.log(`${stale} generated file(s) out of date: run node tools/build_game_pages.js`); process.exit(1); }
