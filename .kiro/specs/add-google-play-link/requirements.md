# Requirements: Google Play link beside the App Store link

## Goal

*The Royal Game of Ur (World Edition)* is now live on Google Play as well as the App Store. Show Google's official "Get it on Google Play" badge beside Apple's badge in the game section, say on the page that the app is on iOS and Android, and drop every "Android coming soon" message.

The listing is `https://play.google.com/store/apps/details?id=art.lumoxia.royalgameofur`.

Use the existing pipeline: edit `templates/`, `i18n/strings/*.json`, `styles.css` and `scripts/`, run `python3 scripts/build.py`, and commit sources and generated pages together. The site stays static and dependency-free: no script, tracker or embed is added. This follows the App Store change (PR 24, spec `the-ios-app-for-the`).

## Where Android is "coming soon" or missing today

| Place | Today (English) |
|---|---|
| Ribbon on the phone screenshot (`game.now`) | "Now on iOS" |
| Eyebrow over the game title (`game.eyebrow`) | "First app, out now on iOS" |
| Pill under the badge (`game.soon` and `game.platforms`) | "Coming soon, to Android" |
| Contact band heading (`contact.h`) | "{app:title} is on the App Store" |
| Contact band lead (`contact.lead`) | "The Android version is coming soon. Follow the work on GitHub." |

`assets/badges/google-play.png` (English, 646 x 250 px) is stored but unused. `assets/badges/README.md` says the Google badge may only link to a live listing; that is now true.

## Acceptance criteria

1. **Google Play badge in the game section.** The `#game` section of the home page of every language shows Google's official "Get it on Google Play" badge, linking to the listing URL above, directly after Apple's App Store badge. The two badges sit in one `.store` row that wraps onto two lines when the container is too narrow. Order is Apple first, then Google, in every language including right-to-left ones (so on Arabic and Hebrew pages the row reads from the right, as the page does).
2. **Badge is unaltered and sized to match Apple's.** The badge file is used exactly as Google distributes it: not redrawn, recoloured, cropped or given effects. The PNG's own transparent margin is kept as clear space. The visible badge (the opaque part) is at least 40 px high on screen and visually matches the height of Apple's badge beside it; the build measures or the README records the margin so the displayed height is chosen on purpose, not guessed.
3. **Localised badge.** Each language page uses Google's own localised badge for that language. The locale mapping covers all 15 site languages (en, fr, es, de, ar, zh, it, hi, tl, tr, ru, he, pt, ja, ko). Languages for which Google publishes no file use the English badge, through an `english_for` tuple in the badge descriptor, the same pattern as `APPSTORE_BADGE`. The source page, the URL pattern, the locale mapping and the fetch date are recorded in `assets/badges/README.md`. If localised files cannot be fetched at implementation time, every language uses the stored English `google-play.png` and the pull request and README say so; no badge is drawn.
4. **One place for the URL.** The listing URL is defined once, as a constant in `scripts/build.py` next to `APPSTORE_URL`, and reaches the template through the build. No template or strings file contains it.
5. **Safe, clear link.** The link opens in a new tab with `rel="noopener"`. Its accessible name is a new string, `game.play.link` ("Get {app:title} on Google Play"), translated in all 15 languages, naming the app and the store. The badge image has `alt=""` so the link has one name. The URL is plain: no `utm` parameters and no `hl` language parameter. Touch target at least 44 px by 44 px, visible gold keyboard focus ring, hover state the same as Apple's (lift only, nothing painted into the clear space). The image is never mirrored or translated by CSS.
6. **Ribbon and eyebrow say iOS and Android.** In English, ribbon `game.now` becomes "Now on iOS and Android" and eyebrow `game.eyebrow` becomes "First app, out now on iOS and Android", with the same meaning in the other 14 languages.
7. **Ribbon does not overflow.** The ribbon is uppercase with letter spacing and sits over the phone screenshot. At a 320 px wide viewport, in the longest languages (de, ru, tl, and the right-to-left he and ar), the ribbon text stays inside the phone frame's column and the page has no horizontal scroll. This is checked in a browser, not assumed. If a ribbon overflows, the design's fallback applies: allow the ribbon text to wrap onto two lines (`white-space: normal`, bounded `max-width`), and only if that still does not fit, shorten that language's `game.now` wording (for example to "iOS and Android" with the verb dropped). The result is recorded in the pull request.
8. **"Coming soon, to Android" pill removed.** The pill is deleted from `templates/index.html`, with its `.soon` CSS rules, and the keys `game.soon` and `game.platforms` are deleted from all 15 strings files, provided nothing else uses them (checked with a search of `templates/`, `scripts/` and `styles.css`). If something does use one, that key stays and the pull request says why.
9. **Contact band.** English: heading `contact.h` is "{app:title} is on the App Store and Google Play"; lead `contact.lead` becomes "Follow the work on GitHub." (the sentence "The Android version is coming soon." is dropped, the GitHub sentence keeps its existing translation). The same in all 15 languages. The GitHub and Patreon buttons, their spacing and copy are unchanged. The Contact band and the legal pages get text changes only, no badge.
10. **Translations.** Every changed or new string exists in all 15 `i18n/strings/*.json` files with the same tags and tokens as English, no em or en dashes, and `_review` left as `unreviewed`. "App Store", "Google Play" and the app title are not translated (the title comes from `{app:title}`). Tone stays plain and direct, in the solo-studio voice. All 15 files have exactly the same keys.
11. **i18n check knows the new token.** The new build token (for example `{{playstore}}`) is added to the list of allowed template tokens in `scripts/check_i18n.py`, so the checker keeps passing and still rejects unknown tokens.
12. **Layout.** On a 320 px viewport the two badges wrap if needed, stay inside the container, align with the text column (start-aligned, mirrored on Arabic and Hebrew), and the page has no horizontal scroll. The English home page grows by less than 15 KB over `scripts/fixtures/english-before/`, as `test_english_growth_under_15kb` requires.
13. **Trademark line.** `footer.trademarks` already credits Google's Play marks and is left unchanged. Google's badge guidelines require no further credit on the page; the README records the guideline page read.
14. **Unchanged.** The hero, mission, music, founder and footer layout; the Privacy, Support, Age Suitability and Terms pages and their wording (including "for iOS and Android"); the sitemap; and the home page only (no badge on other pages) are untouched.
15. **Checks and tests first.** `python3 scripts/build.py --check`, `python3 scripts/test_build.py`, `python3 scripts/check_i18n.py` and `python3 scripts/test_check.py` pass. Tests are written first and fail on the current code. They cover: a Google Play link and badge on every language's home page, exactly one, with the exact URL and the required attributes; the Apple link still present once and before the Google link; no "coming soon" Android wording and no `game.soon` pill on any page in any language; the Play URL appears once in `scripts/build.py` and in no template or strings file; the localised badge file resolves per language (and a missing file raises `build.BuildError`, a language in `english_for` resolves to English); the new ribbon and eyebrow strings are present, with the ribbon once; the Contact copy changed. The old tests that assert Google Play is not shown are rewritten into these positive tests, not deleted.
16. **Docs.** `assets/badges/README.md` (Google section rewritten: shown, files, locale mapping, source, fetch date, rules), `README.md` (the `assets/badges/` line, which says Google's badge is "stored until the Android listing exists") and `i18n/README.md` (the sentence about the badge keys and the "Store attribution" paragraph that says the badges are "not shown yet") are updated.

## Out of scope

- Badges in the Contact band, the hero, or the privacy, support, age and Terms pages.
- Country or language parameters in the Play URL (`hl`, `gl`), `utm` tracking, or a smart-banner meta tag.
- Structured data (`SoftwareApplication`) and Open Graph changes.
- Changing the Android wording in the legal pages (the app's policies cover both platforms).
- Editing `scripts/fixtures/english-before/`: it stays a record of the original site.

## Decisions (answered by you, recorded in `.spec-state.json`)

1. Ribbon "Now on iOS and Android" and eyebrow "First app, out now on iOS and Android" in all 15 languages, with an explicit overflow check and fallback (criteria 6 and 7).
2. Google's official localised badge PNGs per language, English fallback via `english_for`, provenance in the README; stored English badge if localised files cannot be fetched (criteria 2 and 3).
3. Contact heading "{app:title} is on the App Store and Google Play" and lead without the Android sentence (criterion 9).
4. Badge only in the game section, Apple then Google in one wrapping `.store` row; Contact band and legal pages get text changes only (criterion 1).

## Defaults I chose that you may overrule

- The "Coming soon, to Android" pill is removed rather than kept (criterion 8).
- Plain URL, no `utm` or `hl` (criterion 5).
- `game.play.link` as the translated accessible name, image `alt=""` (criterion 5).
- Home page only, generated pages rebuilt and committed (criterion 14).
