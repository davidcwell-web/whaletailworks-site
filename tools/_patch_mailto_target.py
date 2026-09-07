"""The storefront links became mailto: but kept target="_blank".

A mailto opened in a new tab hands off to the mail client and leaves a stray
blank tab behind in most browsers. Only a real http(s) storefront should open in
a new tab, so the attribute is now conditional — and it will start working again
by itself on the day the real eBay URL replaces the placeholder.
"""
import pathlib
import sys

sys.stdout.reconfigure(encoding='utf-8', errors='replace')
p = pathlib.Path(__file__).resolve().parent.parent / 'index.html'
s = p.read_bytes().decode('utf-8')
NL = chr(13) + chr(10) if chr(13) + chr(10) in s else chr(10)

OLD = NL.join([
    "  document.querySelectorAll('[data-ebay]').forEach(a=>{",
    "    a.href=EBAY_STORE_URL;a.target='_blank';a.rel='noopener';",
    "  });",
])
NEW = NL.join([
    "  /* A mailto: must NOT open in a new tab — the browser hands off to the",
    "     mail client and leaves a stray blank tab behind. Only a real http(s)",
    "     storefront gets target=_blank, so this starts working again on its own",
    "     the day the placeholder is replaced with the seller URL. */",
    "  const external=/^https?:/i.test(EBAY_STORE_URL);",
    "  document.querySelectorAll('[data-ebay]').forEach(a=>{",
    "    a.href=EBAY_STORE_URL;",
    "    if(external){a.target='_blank';a.rel='noopener';}",
    "    else{a.removeAttribute('target');a.removeAttribute('rel');}",
    "  });",
])

n = s.count(OLD)
assert n == 1, 'anchor matched %d times' % n
p.write_bytes(s.replace(OLD, NEW).encode('utf-8'))
print('mailto no longer opens a stray blank tab')
