"""Smoke test the current game catalog and popup videos.

Set GW_SITE to an HTTP/HTTPS homepage or local file. Requires Playwright and
Microsoft Edge. Checks player wiring, not proof of YouTube decoding/playback.
"""
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

SITE = os.environ.get('GW_SITE', (Path(__file__).resolve().parents[1] / 'index.html').as_uri())
EXPECTED = {
    'xenodex': ['CyElBPor1bs', '8JpWppoVjAU', 'aYksZG8_XV4'],
    'greenwood': ['CvNTH8N5w3M', 'FMc9mh3uJ_U'],
    'reef-currents': ['media/game-catalog/reef-currents-gameplay.mp4'],
    'last-residents': ['media/game-catalog/last-residents-gameplay.mp4'],
}

with sync_playwright() as pw:
    browser = pw.chromium.launch(channel='msedge')
    for width in (1440, 390, 320):
        page = browser.new_page(viewport={'width': width, 'height': 1000}, reduced_motion='reduce')
        errors, youtube = [], []
        page.on('pageerror', lambda e: errors.append(str(e)))
        page.on('request', lambda r: youtube.append(r.url) if 'youtube' in r.url else None)
        page.goto(SITE.split('#')[0] + '#games')
        page.locator('.catalog-row').last.wait_for(state='attached')
        assert page.locator('.catalog-row').count() == 4
        assert page.locator('section#videos').count() == 0
        assert not youtube, 'YouTube contacted before choosing a video'
        assert page.evaluate('document.documentElement.scrollWidth <= innerWidth + 1')
        for game, ids in EXPECTED.items():
            page.locator(f'[data-explore-game="{game}"]').click()
            page.locator('#game-dialog[open]').wait_for()
            assert page.locator('[data-video-slot]').evaluate_all('(es)=>es.map(e=>e.dataset.videoSlot)') == ids
            local = [v for v in ids if v.endswith('.mp4')]
            for video in local:  # gameplay files served by the site itself
                before = len(youtube)
                page.locator(f'[data-game-video="{video}"]').click()
                assert page.locator('#game-dialog iframe').count() == 0
                assert page.locator('#game-dialog video[controls]').count() == 1
                assert page.locator('#game-dialog video[controls]').get_attribute('src') == video
                if not SITE.startswith('file:'):
                    page.wait_for_function("document.querySelector('#game-dialog video[controls]').currentTime > 0.3")
                assert len(youtube) == before, 'A local gameplay file contacted YouTube'
            if not SITE.startswith('file:'):
                for video in ids:
                    if video in local:
                        continue
                    page.locator(f'[data-game-video="{video}"]').click()
                    assert page.locator('#game-dialog iframe').count() == 1
                    assert page.locator('#game-dialog video[controls]').count() == 0
                    assert '/embed/' + video in page.locator('#game-dialog iframe').get_attribute('src')
            else:
                assert page.locator('.game-modal-trailer-link').count() == len(ids) - len(local)
            page.locator('#game-dialog-close').click()
            page.wait_for_function("!document.querySelector('#game-dialog').open && !location.hash.startsWith('#game-')")
            assert page.locator('#game-dialog iframe,#game-dialog video').count() == 0
        page.locator('nav a[href="#videos"]').click()
        assert page.locator('.catalog-row:visible').count() == 4
        page.reload()
        page.locator('.catalog-row').last.wait_for(state='attached')
        assert page.locator('.catalog-row:visible').count() == 4
        assert not errors, str(errors)
        print(f'PASS {width}px: catalog, four popups, five YouTube videos and two gameplay files, cleanup, Videos navigation, reload; zero page errors.')
        page.close()
    browser.close()
print('Player wiring checked. Confirm actual YouTube playback on the live HTTPS site after publication.')
