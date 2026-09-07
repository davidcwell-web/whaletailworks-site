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
