# Website update handoff — 2026-09-07
Local changes prepared by Codex; NOT published. Git HTTPS access failed with SEC_E_NO_CREDENTIALS in restricted session; GitHub Pages API returned 404.

- index.html: XENODEX $2.99 USD and Greenwood $3.99 USD, sourced from each game store/LISTING.md.
- Five click-to-play youtube-nocookie video cards; IDs discovered in public channel RSS: CyElBPor1bs, CvNTH8N5w3M, 8JpWppoVjAU, aYksZG8_XV4, FMc9mh3uJ_U.
- Channel link; honest email launch CTA; generic eBay homepage links replaced by email enquiries until actual seller URL is supplied.
- privacy.html: describes user-initiated YouTube embeds and Google Fonts.
- Reduced-motion CSS and focus outlines added. No installed game files changed.
- Tests: 390px and 1440px, five cards, no iframe before click, correct iframe after click, zero page errors, no horizontal overflow. Player network mocked for interaction test; actual playback must be checked on HTTPS after deployment (file previews are not reliable YouTube hosts).
- Preserve the Search Console meta verification and CNAME.

Publish from normal Windows user: review git diff, commit these three files, then push current branch to origin. Check repository Settings > Pages and verify live HTTPS player playback. Do not assume local edits are live.

Remaining: actual eBay storefront URL, confirmed public Play Store listing URLs, verify real playback and final navigation on deployed site. Consider individual game pages and a short development-news section.

## Approved motion preview applied
User approved preview. Applied index.html and media/ assets: shorter aligned video headings, Greenwood video thumbnails, five-second muted local gameplay loop with pause and reduced-motion handling, original whale rendered with periodic tail-only deformation. No source art replaced. Desktop/phone checks passed; player request mocked for interaction tests. Local muted playback/pause and reduced-motion verified. Publish index.html, privacy.html, media/ and this handoff. Live deployment still pending normal-user Git credentials; do not claim it is published. Use HTTP/HTTPS for embed review, not file URLs (YouTube error 153).

## PUBLISHED — 2026-09-07 (Claude)

Committed and pushed to origin/main; GitHub Pages served the new markup and all
three media files (HTTP 200) within minutes. CNAME (whaletailworks.net) and the
Search Console verification meta are untouched.

Verified on the LIVE HTTPS site at 1440 and 390, desktop and mobile:

| | |
|---|---|
| prices | XENODEX $2.99, Greenwood $3.99 — both matched against each game's store/LISTING.md, and the retired $0.99 is gone |
| video cards | five present; NO request to youtube.com before a click; a youtube-nocookie embed after one |
| playback | all five embeds played on HTTPS. Zero failed YouTube responses across 112 requests |
| video IDs | all five resolve through YouTube's oembed API and all five are on the Whale Tail Works LLC channel |
| gameplay loop | muted, looping, playsinline; the toggle pauses and relabels |
| whale | the img is replaced by a canvas that repaints (proved by screenshot diff — the canvas is tainted under file://, so getImageData cannot be used) |
| layout | no horizontal overflow at either width; every image loads; no failed requests; zero page errors |

Two of the five are vertical Shorts, so they letterbox inside the 16:9 cards.
That is correct, not a fault — but if it ever looks wrong, the fix is a 9:16
card variant, not a change to the embed.

One defect fixed before publishing: the storefront links had become mailto: but
kept target="_blank", which leaves a stray blank tab when the browser hands off
to the mail client. target is now conditional on an http(s) URL, so it resumes
working by itself once the real seller URL replaces the placeholder.

`tools/sitecheck_media.py` runs all of the above; it takes GW_SITE so the same
script proves a local file and the deployed site.

### Still open
- The real eBay storefront URL (one constant, `EBAY_STORE_URL` in index.html).
- Public Play listing URLs once the games are live.
- The Greenwood store page exists only in English and Japanese; es/pt/de/fr are
  written for the game but not for the site.
- Suggested next: individual game pages, and a short development-news section.
