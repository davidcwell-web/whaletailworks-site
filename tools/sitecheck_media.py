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
    'reef-currents': [],
    'last-residents': [],
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
            if ids and not SITE.startswith('file:'):
                for video in ids:
                    page.locator(f'[data-game-video="{video}"]').click()
                    assert page.locator('#game-dialog iframe').count() == 1
                    assert '/embed/' + video in page.locator('#game-dialog iframe').get_attribute('src')
            elif ids:
                assert page.locator('.game-modal-trailer-link').count() == len(ids)
            page.locator('#game-dialog-close').click()
            page.wait_for_function("!document.querySelector('#game-dialog').open && !location.hash.startsWith('#game-')")
            assert page.locator('#game-dialog iframe,#game-dialog video').count() == 0
        page.locator('nav a[href="#videos"]').click()
        assert page.locator('.catalog-row:visible').count() == 2
        page.reload()
        page.locator('.catalog-row').last.wait_for(state='attached')
        assert page.locator('.catalog-row:visible').count() == 2
        assert not errors, str(errors)
        print(f'PASS {width}px: catalog, three popups, five videos, cleanup, Videos navigation, reload; zero page errors.')
        page.close()
    browser.close()
print('Player wiring checked. Confirm actual YouTube playback on the live HTTPS site after publication.')
