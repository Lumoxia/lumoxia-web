# Store badges

## Apple (shown)

Apple's "Download on the App Store" badge is shown in the game section of every home page, linking to the app's listing
(`APPSTORE_URL` in `scripts/build.py`). Files are in `app-store/<code>.svg`, one per language, used exactly as Apple
distributes them.

| Files | Source (fetched 2026-11-20) |
|---|---|
| `app-store/<code>.svg` for en, fr, es, de, zh, it, tl, tr, ru, he, pt, ja, ko | Apple Marketing Tools, `https://toolbox.marketingtools.apple.com/api/v2/badges/download-on-the-app-store/black/<locale>/download`, file `black.svg`. Locales: en-us, fr-fr, es-es, de-de, zh-cn, it-it, tl-ph, tr-tr, ru-ru, he-il, pt-br, ja-jp, ko-kr |

Apple publishes no badge for Arabic (`ar-sa`) or Hindi (`hi-in`): the toolbox answers 404. Those two pages use
`app-store/en.svg`; the exceptions are listed in `english_for` in `APPSTORE_BADGE` in `scripts/build.py`, and any other
missing file fails the build. `app-store/en.svg` is the US-UK badge that was stored here before it was shown, and is
byte-identical to the toolbox file.

Rules to keep: do not redraw, recolour, crop or add effects. Keep Apple's clear space (one quarter of the badge height)
on every side; the page gives the badge 10 px of padding at 40 px high. Apple's minimum height is 40 px. These rules
were carried over from this file's earlier version and were not re-read on Apple's page when the localised files were
fetched. The trademark line is in the footer (`footer.trademarks`).

## Google (stored, not shown)

`google-play.png` is Google's "Get it on Google Play" badge, English, from
[Google Play badges](https://play.google.com/intl/en_us/badges/) (Google distributes it as PNG). It is not shown on any
page, because the Android app has no live listing, and Google only allows its badge to link to one. When it does, add
the badge next to the Apple one in the game section (build it the same way as `Site.appstore`), replace the "Coming
soon, to Android" pill, and use the localised badge for each page's language when Google offers one. Same rules: no
redrawing, recolouring or cropping, the badge's own transparent margin kept as clear space, at least 40 px of visible
height.
