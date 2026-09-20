# Game catalog and popups

The homepage keeps its existing hero, navigation, backgrounds, stars, whale and
alien letter animation. The catalog follows that hero; About the Studio follows
the catalog. Explore game opens an accessible native dialog on the same page.

## Adding or updating a game

Edit `media/game-catalog/games-data.js`. Add one object to the array with:

- Unique `id` using lowercase letters, digits and hyphens; `title`, `genre`,
  `summary`, `accent`, `price`, `priceNote`.
- `status`: `available` or `coming-soon`. Only `available` games with a `store`
  URL receive a Google Play purchase link.
- `cover`, `coverAlt`, optional `containCover: true` for artwork with lettering.
- `paragraphs` and `features`: arrays of plain text.
- `screenshots`: array of `{src, caption}`. Use real gameplay captures.
- `privacy`: relative privacy-page URL.
- Optional `videos: [{id, title, poster, short}]` using YouTube video IDs.
  Set `short: true` for a vertical 9:16 Short. Trailers use 16:9.
- Optional `preview: {src, poster}` for a local muted gameplay loop.
- Optional `heroes: [{src, name}]` for a character gallery.

Rows, popups and availability counts are generated from this one array. No build
step is needed. When changing these files, update their cache version in the
three `index.html` links. Keep the small `noscript` fallback in `index.html`
accurate too.

Game details support direct links such as `#game-greenwood`. Close, Escape,
backdrop click and browser Back dismiss the popup. Focus and page position return
to the opener. Filters are temporary presentation state and reset on reload;
the catalog writes no cookies or local storage.

YouTube is contacted only after Play is clicked. Closing the popup destroys its
player. File previews use a YouTube link to avoid error 153. Check actual embedded
playback on the deployed HTTPS site.

## Artwork and font source records

- `greenwood-cover.webp`: size/format conversion of the previously approved
  Greenwood store refresh `play_feature_1024x500.png`, based on the selected
  carved emerald banner. Existing source records remain in the Greenwood project.
- `reef-cover.webp`: size/format conversion of the Reef Currents store refresh
  `source/feature-master.png`, generated with OpenAI ImageGen on 2026-09-13.
  Existing prompts and provenance remain in the Reef Currents store-media records.
- XENODEX artwork, all gameplay captures, whale and other site images use the
  existing website assets. No new generated or purchased artwork was introduced.
- `last-residents-cover.webp` and `img/lr_shot_*.jpg`: size/format conversions of
  the room paintings and the arrival painting from *The Last Residents* (generated
  with OpenAI image generation during that project; prompts and provenance stay in
  the game project). Added 2026-09-20 for the coming-soon card. No video yet.
- `outfit.ttf`: previously bundled Outfit font. Retain `OFL-Outfit.txt` with it.
  Original copyright and the SIL Open Font License are included there.

This pass does not alter game builds, store prices, privacy policies, the
Google Search Console verification tag, CNAME or ad verification records.


## Gameplay inside Explore — 2026-09-13

All five previously listed YouTube videos now live with their own game: three
for XENODEX and two for Greenwood. The standalone Watch the Games section is
removed. The original Videos navigation link targets `#videos`, a catalog
anchor which selects With videos. Explore then opens at that game's videos.
Normal Explore opens at the introduction; Watch gameplay jumps to the videos.
Reef Currents has no published video yet, so it has no empty video section.

Only one YouTube iframe runs at a time. Starting another restores the earlier
poster. Closing the popup destroys all players and disconnects its preview
observer. The existing five-second XENODEX loop stays muted, plays only when
visible, pauses with the page hidden and respects reduced motion and Save-Data.
A visible Play/Pause control remains available; YouTube always requires a click.

The two `xenodex-*-short.jpg` posters are the previously approved portrait
stills from the XENODEX video refresh. They show the actual corresponding Shorts
and replace unrelated landscape posters inside the vertical players.

Verification: `python tools/sitecheck_media.py` checks the current catalog and
popup video wiring. Set `GW_SITE` for HTTP/HTTPS testing. It does not claim actual
YouTube playback merely because an iframe loaded.
