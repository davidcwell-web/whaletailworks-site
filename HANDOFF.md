## Current handoff — 2026-09-13: owner asks Claude to finish publication

Publication remains authorized; Codex stopped uploading and handed completion
to Claude. The latest shared record is
`../AI-HANDOFFS/whaletailworks-site/2026-09-13-1903-claude-finish-publication.md`.

Preserve newer commits 47656b4 (Reef privacy ad wording) and f573807 (catalog ad
wording), plus the four final uncommitted files. The full current payload is now
14 files, including reef-currents-privacy.html. Do not restore older review copies.
Do not blindly push the older unpublished 57e1800 with personal attribution.
Last remote verified: 082ed8d, README only; recheck remote state before publishing.

Prefer Claude's normal authenticated Git environment. Preserve all local work,
apply the final snapshot on current remote history with the studio/private Git
identity, push normally without force, then verify the live site and five videos.
The new homepage was not live at the last check. Earlier broad tests passed;
actual new live playback and final deployment verification remain outstanding.
The previous wait for Codex browser-upload permission is superseded by this
handoff. Privacy settings were already verified; see the shared record for details.

---

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


## Catalog and popup update — 2026-09-13 (Codex)

Implemented option 3 from the approved mockups. Games now appears directly below
the original animated hero; About the Studio follows Games. Explore game opens a
native popup with details, screenshots, pricing and available trailers.

Original navigation, hero markup, inline styles/scripts, whale, UFO letter theft,
backgrounds and stars are preserved. Prices remain XENODEX $2.99, Greenwood $3.99,
and Reef Currents coming soon, free with an optional $1.99 purchase.

Game entries and popup content are maintained in `media/game-catalog/games-data.js`.
See `media/game-catalog/README.md` for adding games and source/license records.
250 browser checks passed at desktop and phone widths, with zero page errors;
original stars and UFO letter theft were observed. Popup trailer requests and
cleanup were tested with a mocked YouTube response; verify playback on HTTPS
after publication. This pass has NOT committed, pushed or deployed the update.

Shared handoff: `AI-HANDOFFS/whaletailworks-site/LATEST.md` under the shared CLAUDE
directory. Original-file backups and verification evidence are in the Codex task's
`outputs/website-games-catalog/` directory.


## Approved website release — 2026-09-13 (Codex)

The owner approved publication of the catalog and popups above. The three-game
catalog is directly below the existing animated introduction; About the Studio
follows it. Explore game stays on this page and opens a native dialog.

Maintain game content in `media/game-catalog/games-data.js`; instructions and
artwork/font source records are in `media/game-catalog/README.md`. The page meta
description now mentions the upcoming Reef Currents alongside the two available
games. The existing top layout, navigation, whale, alien letter animation,
backgrounds, starfield, CNAME and Search Console verification are retained.

Publication includes only `index.html`, `HANDOFF.md` and `media/game-catalog/`.
Private Business Hub and shared AI handoff files are local-only documentation.
The former implementation note saying "not deployed" describes the earlier
pre-publication state; the deployment result will be appended below after the
live HTTPS checks finish.


### Gameplay consolidation requested during release

All five Watch the Games videos now appear inside their matching Explore game
popup. XENODEX has its trailer, Hull Run and Base Defense; Greenwood has its
trailer and Battles. Videos in the unchanged top navigation selects the catalog
With videos view. No separate Watch the Games section remains. Player controls,
portrait Shorts, lazy YouTube loading and the existing muted XENODEX loop are
maintained inside the popups. See the catalog README for maintenance.


### Current release status — 2026-09-13

The owner authorized publication, including moving Watch the Games into the
Explore popups. All source files are installed locally and the catalog payload
is committed. Publication is still pending: this Codex process cannot access a
working GitHub credential. Git push failed; the CLI reports an invalid sign-in,
and GitHub in Edge is signed out. The live homepage was checked and still serves
the earlier layout. Do not describe this update as publicly deployed yet.

Resume from the website repository in a normally signed-in shell with
`git push origin main`. Do not force-push or recreate the approved changes.
If Windows TLS credentials fail in the agent shell, per-command
`git -c http.sslBackend=openssl push origin main` avoids that TLS backend issue;
it still requires valid GitHub authentication. No global Git settings changed.

Validation: 327 catalog and popup browser assertions passed at widths 1440,
1024, 390 and 320, with zero page errors. After final poster and preview lifecycle
adjustments, all popup images loaded, the three Shorts had portrait posters,
muted preview time advanced, YouTube selection paused it, manual restart worked
and scrolling it out of view paused it again. The maintained checker
`tools/sitecheck_media.py` also passed against the installed source at 1440,
390 and 320. Set `GW_SITE` to the deployed HTTPS homepage to repeat its checks.
These tests prove player wiring and cleanup; actual YouTube playback on the new
deployed page remains a post-publication check.

The existing site, three studio privacy pages, app-ads.txt and the separate
XENODEX GitHub Pages privacy URL returned HTTP 200. The alternate whaletail.works
domain returned a TLS handshake error from this environment; investigate that
alias separately without changing the working main-domain configuration.

The private Business Hub and shared Claude handoff now distinguish local-ready
from published, describe the video arrays and link to this release. They are
not part of the public repository. Public release files are index.html,
HANDOFF.md, media/game-catalog/ and the updated tools/sitecheck_media.py.

Earlier open-item notes about missing Google Play links are superseded: XENODEX
and Greenwood now have live store links. Reef Currents remains coming soon.
The existing eBay storefront placeholder and additional website translations
remain separate follow-ups.


## Newer status — GitHub identity choice pending, 2026-09-13

The owner signed into GitHub in Edge successfully, then asked to hide their real
name from GitHub. No public commit or upload was made by Codex. The repository
and live site still have the previous public revision, f7ae1e2. Publishing is
held pending the owner's privacy choice; browser authentication is now available.

An explicit choice is pending: use Whale Tail Works LLC for the display name and
this website's future commit author, with GitHub's private commit email; or plan
cleanup of existing identity exposure first; or keep the settings unchanged.
No account settings or public history have been changed. Username and old
commits remain identifying even with a studio display name and private email.
The checked homepage and three local privacy-page sources have no personal-name
match; GitHub's repository/commit metadata is the visible exposure found.

Do NOT push the existing unpublished 57e1800 as-is if the owner wants private
future attribution: it was authored using the repository's existing personal
Git identity. Preserve a local backup and correct only our unpublished commit,
or publish the reviewed files through the signed-in browser after fixing the
web commit identity. Do not rewrite published history or rename the account
without resolving the broader scope and linked GitHub Pages policy URLs.

Source is installed and fully tested. Four files have final uncommitted updates:
HANDOFF.md, media/game-catalog/README.md, media/game-catalog/games-catalog.js and
tools/sitecheck_media.py. Include them in the final publication. The earlier
statement that all final changes were committed referred to the first payload;
57e1800 is followed by these tested finishing changes.


## Current status — privacy verified, browser upload permission pending

The owner completed the basic privacy settings and explicitly reauthorized
publication. Verified in the signed-in Edge browser: display name Whale Tail
Works LLC; profile activity private; email private; blocking pushes that expose
personal email enabled. Verified private commit address in GitHub settings.
Website-local Git identity now uses the studio name and that private address;
global Git identity and old public history were not changed.

Publication started via GitHub's browser UI. Commit
082ed8d1d17814bb6dad09847e701a80a80c0d43 creates only a small README in
media/game-catalog. GitHub's public API confirms its author is Whale Tail Works
LLC and the email is a GitHub noreply address. The new homepage is NOT live yet.

The ten-file catalog upload is blocked by the Edge extension's missing Allow
access to file URLs permission. The tool's official troubleshooting requires
the user to enable it manually in Edge Extensions > ChatGPT > Details. Browser
security policy also blocks the agent from opening edge://extensions; do not
work around that restriction. A user question is pending asking when enabled.

Resume after the user enables it: use the existing GitHub upload form for
media/game-catalog to upload all ten local catalog files. Upload the maintained
checker into tools, then index.html at the root, and verify the live HTTPS site.
After live verification, update/upload the final HANDOFF.md. Every file is
prepared and tested; do not reconstruct the site. Do not upload the private Hub.

Because browser commits are now ahead of the old public revision, do not push
the old unpublished local commit 57e1800. It retains the old personal author.
After all browser uploads, preserve the complete local work on a local backup
branch, verify identical remote file content, then align main with the published
remote without force-pushing or changing published history. This is still
unfinished; the local repository currently has four final modified files.
