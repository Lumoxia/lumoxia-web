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

Rules to keep: do not redraw, recolour, crop or add effects. Apple's badge guidelines (`https://developer.apple.com/app-store/marketing/guidelines/`, read 2026-11-20) say: minimum clear space is one quarter of the badge height, with no photos, typography or graphics inside it; minimum badge height is 40 px onscreen. The site shows every badge 40 px high (the Hebrew file's own viewBox is 42 px high and is scaled to 40) with 10 px of padding on each side. The trademark line is in the footer (`footer.trademarks`).

## Google (shown)

Google's "Get it on Google Play" badge is shown in the game section of every home page, directly after Apple's, linking
to the app's listing (`PLAY_URL` in `scripts/build.py`). Files are in `google-play/<code>.png`, one per language, used
exactly as Google distributes them (PNG, 646 x 250 px).

| Files | Source (fetched 2026-11-21) |
|---|---|
| `google-play/<code>.png` for all 15 site languages | Google Play badges, `https://play.google.com/intl/en_us/badges/` (Partner Marketing Hub). Each file is `https://play.google.com/intl/en_us/badges/static/images/badges/<locale>_badge_web_generic.png`, answered with HTTP 200 and `image/png` |

Locale mapping, site code to Google's file: en to `en`, fr to `fr`, es to `es`, de to `de`, ar to `ar`, zh to `zh-cn`,
it to `it`, hi to `hi`, tl to `fil` (Filipino, Google's code for Tagalog), tr to `tr`, ru to `ru`, he to `iw` (Google's
legacy code for Hebrew), pt to `pt-br` (the site's Portuguese is Brazilian), ja to `ja`, ko to `ko`. Google publishes a
file for every site language, so `english_for` in `PLAYSTORE_BADGE` is empty and any missing file fails the build.
`google-play/en.png` is the English badge that was stored here before it was shown (`google-play.png`) and is
byte-identical to the file Google serves today.

Margins, measured from the alpha channel. Google's PNGs carry transparent margin, and it differs between files:

| Files | Opaque badge in the 646 x 250 canvas | Displayed height | Visible badge |
|---|---|---|---|
| `en`, `ar`, `he` | 564 x 168 px (margin 41 px on every side) | 60 px | 40.3 px |
| the other 12 | 646 x 192 px (margin 29 px above and below, none at the sides) | 53 px | 40.7 px |

The heights are in `PLAYSTORE_BADGE["height"]` and are written as the image's height and width attributes, so the
visible badge is about 40 px high, matching Apple's 40 px badge. `test_play_badge_height` measures every file and fails
if a displayed badge is under 40 px.

Rules to keep: do not redraw, recolour, crop, stretch or add effects. Google's badge guidelines (the page above, read
2026-11-21) say: the badge height is at least 28 px on screen; when shown with other store badges, Google's must be the
same size or larger; clear space is one quarter of the badge height, on a solid or simple background; use the localised
badge for a page in another language; use current artwork from the Partner Marketing Hub. The transparent margins are part
of Google's own files and are not altered; they differ between files (see the table above), and in 12 of the 15 files the
side margin is 0, so the margin alone is not a quarter-height clear space. The separation from the Apple badge comes from
the Apple link's 10 px padding plus the 8 px gap of the row; the Google link adds no padding of its own. The badge is
never cropped or recoloured. Google asks for no extra credit
line; the trademark line is in the footer (`footer.trademarks`).
