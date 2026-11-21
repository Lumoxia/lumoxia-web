# Design: Google Play link beside the App Store link

Implements `requirements.md` (approved by your answers: ribbon and eyebrow say iOS and Android, Google's localised badge per language with English fallback, Contact text updated, badge in the game section only). It extends the App Store work already on `main`: `APPSTORE_URL`, `APPSTORE_BADGE`, `Site.appstore()`, `Site.logo_path()`, the `{{appstore}}` token and the `.store` styles.

## Overview

```
scripts/build.py      PLAY_URL + PLAYSTORE_BADGE + Site.playstore() -> {{playstore}} token (home page only)
scripts/check_i18n.py "playstore" added to the allowed template tokens
templates/index.html  {{playstore}} beside {{appstore}} inside one .store row; "Coming soon" pill removed
i18n/strings/*.json   game.now, game.eyebrow, contact.h, contact.lead reworded; game.play.link added;
                      game.soon and game.platforms removed
assets/badges/google-play/<code>.png   one official badge per language (English fallback)
styles.css            .store becomes a wrapping flex row; .soon rules removed; ribbon wrap guard if needed
scripts/test_build.py positive Google tests replace the "Google not shown" ones
docs                  assets/badges/README.md, README.md, i18n/README.md
```

## 1. Build script (`scripts/build.py`)

Next to `APPSTORE_URL`:

```python
PLAY_URL = "https://play.google.com/store/apps/details?id=art.lumoxia.royalgameofur"
# Google's "Get it on Google Play" badge, one PNG per language in assets/badges/google-play/ (see the README there).
# A language in english_for has no Google badge and uses en.png; any other missing file is an error.
PLAYSTORE_BADGE = {"file": "google-play/{lang}.png", "english_for": ()}
```

`english_for` is filled in by the badge-fetch task with exactly the languages Google does not publish. Probing Google's badge URLs on the design date showed all 15 are available (see section 4), so it is expected to stay empty. It starts empty so a forgotten or misspelt file fails the build.

`Site.playstore(code, root)` mirrors `Site.appstore`. It reuses `logo_path(PLAYSTORE_BADGE, code, "assets/badges")` (no change needed: it already takes a descriptor), reads the size with `image_size` (which already handles PNG from the IHDR header), and returns one anchor:

```html
<a href="https://play.google.com/store/apps/details?id=art.lumoxia.royalgameofur" target="_blank" rel="noopener" aria-label="Get The Royal Game of Ur on Google Play"><img class="play" src="assets/badges/google-play/en.png" alt="" width="646" height="250" /></a>
```

The label comes from `game.play.link` with `{app:title}` resolved as `appstore()` does, then attribute-escaped. The `&` in the URL is not present (one query parameter), but the URL still goes through `html.escape(..., quote=True)`.

The wrapper moves out of the builder and into the template (section 2): `appstore()` now returns the bare anchor (it used to return `<p class="store">...</p>`), and `playstore()` returns the bare anchor. Both tokens exist only in `templates/index.html`, so `render_page` passes `"playstore": self.playstore(...) if page == "index" else ""` beside the existing `appstore` entry. The Play URL appears only inside `playstore()` through `PLAY_URL`, so it exists once in `build.py` (criterion 4). The existing App Store tests that look for `<p class="store">` are adjusted in task 3.

Anchor order in the source is Apple then Google. Because `.store` is a flex row and the page's `dir` flips flex direction, right-to-left pages show Apple on the right, which is the correct reading order (criterion 1).

## 2. Template (`templates/index.html`)

In `#game`, replace

```html
            {{appstore}}
            <div class="soon" role="note">
              <img src="{{root}}assets/mark.svg" alt="" width="40" height="40" />
              <span><strong>{{t:game.soon}}</strong><small>{{t:game.platforms}}</small></span>
            </div>
```

with

```html
            <p class="store">{{appstore}}{{playstore}}</p>
```

The ribbon (`{{t:game.now}}`) and eyebrow (`{{t:game.eyebrow}}`) keep their template lines; only their strings change. The Contact band template is unchanged.

Before deleting the pill, search `templates/`, `scripts/`, `styles.css` and the docs for `game.soon`, `game.platforms` and `.soon`. At design time the only users are the pill itself (`templates/index.html`, `styles.css` `.soon*`), the `OLD_STORE_EN` literals in `scripts/test_build.py` (old wording kept as test data, not as live keys) and `i18n/README.md:42`. If the search finds another user at implementation time, that key stays (criterion 8).

## 3. Strings (all 15 `i18n/strings/*.json`)

| Key | English | Change |
|---|---|---|
| `game.now` | "Now on iOS and Android" | reworded (ribbon) |
| `game.eyebrow` | "First app, out now on iOS and Android" | reworded |
| `game.play.link` | "Get {app:title} on Google Play" | new, accessible name of the Google badge link |
| `contact.h` | "{app:title} is on the App Store and Google Play" | reworded |
| `contact.lead` | "Follow the work on GitHub." | reworded (Android sentence dropped; the existing GitHub sentence translation is kept as is) |
| `game.soon` | "Coming soon" | removed |
| `game.platforms` | "to Android" | removed |

Rules for translations: same tags and tokens as English; "App Store" and "Google Play" stay in Latin script, as in the footer; `{app:title}` kept; no em or en dashes; `_review` stays `unreviewed`; all 15 files keep identical key sets. `contact.lead` is mostly a deletion: in each language remove the Android sentence and leave the GitHub sentence verbatim. Existing translators' phrases for "iOS" in `game.now` and `game.eyebrow` are extended with the Android equivalent (for example German "Jetzt für iOS und Android"), keeping "iOS" and "Android" in Latin script.

`scripts/check_i18n.py` already enforces key parity, tag and token parity and the dash rule. The new build token is a template token, so `"playstore"` is added to the allowed-token set at `scripts/check_i18n.py:18` (criterion 11); `{app:title}` in the new string is already allowed.

## 4. Badge files (`assets/badges/google-play/`)

- Source: Google's "Get it on Google Play" badge download page, `https://play.google.com/intl/en_us/badges/`. Google serves each localised badge as a PNG at `https://play.google.com/intl/en_us/badges/static/images/badges/<locale>_badge_web_generic.png`. Probed on 2026-11-21 (HTTP 200, `image/png`): `en`, `fr`, `es`, `it`, `tr`, `ja`, `ko`, `pt-br`, `zh-cn`, `fil`, `iw`, `ar`, `hi`, `ru`, `de`. Not published under these names (404): `tl`, `he`, `pt-pt`, `en-us`.
- Locale mapping to site codes, recorded in the README: en to `en`, fr to `fr`, es to `es`, de to `de`, ar to `ar`, zh to `zh-cn`, it to `it`, hi to `hi`, tl to `fil` (Filipino, Google's code for Tagalog), tr to `tr`, ru to `ru`, he to `iw` (Google's legacy code for Hebrew), pt to `pt-br` (the site's Portuguese is Brazilian), ja to `ja`, ko to `ko`. The fetch task re-confirms each file is a PNG of the expected badge and records the exact URL and date. If a file differs from this plan, the README records the actual state and `english_for` is set accordingly.
- Files are saved as `assets/badges/google-play/<code>.png`, unmodified (the byte stream Google serves). The stored `assets/badges/google-play.png` moves with `git mv` to `assets/badges/google-play/en.png` after the freshly fetched `en` file is compared with it; if they differ, the fetched file wins and the README says so.
- Visible height. Google's PNGs carry transparent margin (Google's clear space). The fetch task measures, for each file, the pixel size and the bounding box of non-transparent pixels, and records them in the README. Display height is then chosen so that the visible badge is 40 px high, matching Apple's 40 px badge: `display height = 40 * canvas height / visible height`. If every file has the same margin ratio, one CSS height serves all (`.store img.play { height: Npx; width: auto }`); if the ratios differ between languages, the build computes a per-file `height` attribute from the measured ratio instead (kept in a small table in `build.py` next to `PLAYSTORE_BADGE`, with a test that fails if a file is missing from it). The transparent margin is kept, never cropped. It differs between files (in 12 of 15 the side margin is 0), so it is not a uniform clear space; the separation from Apple's badge is the Apple link's 10 px padding plus the 8 px gap, and the Google anchor adds no padding of its own.
- If localised files cannot be fetched (offline, or a changed URL), every language uses the stored English `google-play.png`, `english_for` lists all other languages, and the README and pull request say so. No badge is drawn.
- Google's badge guideline page is read at fetch time and the rules (no alteration, clear space, minimum size) are recorded in the README. If they differ from the rules above, the README and CSS follow Google.

## 5. Styles (`styles.css`)

```css
/* Store badges: Apple's clear space is one quarter of the badge height; Google's PNGs keep their own, varying, margin */
.store { display: flex; flex-wrap: wrap; align-items: center; gap: 4px 8px; margin: 20px 0 14px; }
.store a { ... existing rules, unchanged ... }
.store img.play { display: block; height: Npx; width: auto; max-width: 100%; }   /* N from the measured margin, section 4 */
```

- `.store` was a block holding one link; it becomes a wrapping flex row. `gap` keeps the two badges apart even where wrapped. Start alignment follows the text direction, so Arabic and Hebrew pages are mirrored by `dir` with no extra rule; no transform touches the images.
- The Google anchor reuses `.store a` (44 px minimum touch target, focus ring, lift-only hover, `prefers-reduced-motion` rule already covers `.store a`). Its padding is 0; the PNG margins differ between files and do not by themselves give a quarter-height clear space, so the separation comes from the Apple link's padding and the row gap.
- Remove the `.soon`, `.soon img`, `.soon span`, `.soon strong`, `.soon small` rules and fix the section comment "Coming soon badge and ribbon" to "Ribbon" (the `.ribbon` rule stays).
- At 320 px the two badges (about 120 px and about 135 px wide, plus padding) fit side by side or wrap; `max-width: 100%` guards a wider localised file.
- Ribbon overflow (criterion 7). The ribbon is `position: absolute` over the phone with `padding: 6px 16px`, uppercase, `letter-spacing: 2px`, `font-size: 0.8rem`. "Now on iOS and Android" is the longest English wording yet. The visual check measures `scrollWidth` against `clientWidth` and the ribbon's bounding box against the phone frame for de, ru, tl, he and ar at 320 px. Handling, in order: (a) add `max-width: calc(100% - 8px)` and `white-space: normal` with `text-align: center` and `line-height: 1.25` to `.ribbon`, so a long wording wraps to two lines inside the frame; (b) if a language still overflows (for example a very long single word), shorten that language's `game.now` only (drop the verb: "iOS und Android" for German), leaving `game.eyebrow` in full. The outcome, per language, goes into the pull request. CSS (a) is added only if the check shows it is needed in at least one language; otherwise the CSS is left as is.

## 6. Tests (`scripts/test_build.py`)

Test names are used, not line numbers; the file has changed since the last spec. Written first, watched failing, then the implementation.

| Test | Change |
|---|---|
| `test_app_store_badge_shown_and_google_play_not` | Renamed `test_store_badges_shown`. It keeps the Apple assertions and adds, for every language home page: exactly one `<a>` with `href` equal to `build.PLAY_URL`, `target="_blank"`, `rel="noopener"`, a non-empty `aria-label` containing "Google Play" and the app title, a child `<img alt="">` with a file that exists and ends in `assets/badges/google-play/<code>.png` (or `en.png` for `english_for`); the Apple anchor comes before the Google anchor in the same `.store` element; no `utm_` and no `hl=` in the URL. The "no `google-play` / no `play.google.com`" assertions are removed; the privacy, support, age and Terms pages still carry no `apps.apple.com` link and now also no link to `build.PLAY_URL`. The Terms' Google Play Terms link (`https://play.google.com/about/play-terms/`) is still ignored when counting. |
| `store_links` helper (`test_build.py`) | Extended (or a sibling `play_links`) to parse the Google anchor and its image the same way. |
| `test_android_and_store_attribution` | The home page no longer contains "to Android". It must not contain "coming soon" wording for Android in any language (see next row). Privacy and support keep "for iOS and Android". The Google trademark line check is unchanged. |
| `test_no_coming_soon_for_ios` | Renamed `test_no_coming_soon`. Keeps the per-language old-eyebrow and old-heading checks. Adds: no `class="soon"` element on any page; `game.soon` and `game.platforms` are absent from all 15 strings files; `game.now` appears exactly once, as the ribbon; `game.eyebrow` is present; the old `contact.lead` Android sentence, per language, is absent (the old text of that sentence is captured as literals in the test from `HEAD` before the change, as `OLD_COMING_SOON` already does for the eyebrow and heading). |
| `test_app_store_url_in_one_place` | Extended with `test_play_url_in_one_place`: `build.PLAY_URL` appears once in `scripts/build.py` and in no file under `templates/` or `i18n/strings/`. |
| `test_app_store_badge_resolution` | Sibling `test_play_badge_resolution`: `logo_path(PLAYSTORE_BADGE, "fr", "assets/badges")` gives `google-play/fr.png`; an unknown language raises `build.BuildError`; a language in `english_for` gives `google-play/en.png`; every site language has its file (or is in `english_for`). |
| New: `test_ribbon_and_eyebrow_strings` | The English `game.now` is "Now on iOS and Android" and `game.eyebrow` is "First app, out now on iOS and Android"; in every language both strings mention both platforms ("iOS" and "Android" in Latin script) and `game.now` contains no dash. |
| New: `test_play_badge_height` | For each Google file: PNG, and the visible (opaque) height at the displayed size is at least 40 px, computed from the measured margin table or CSS. Skipped assertion on the margin if the fetch task found the margin identical for all files (then it asserts the single CSS height). |
| `test_english_text_unchanged` and `undo_store_changes` | `OLD_STORE_EN` is updated so each reworded key maps the new English wording back to the original site text: `game.now` to "Coming soon", `game.eyebrow` to "First app, coming soon", `contact.h` to "{app:title} is coming soon", `contact.lead` to "It is not in the App Store or on Google Play yet. Follow the work on GitHub.". The removed keys `game.soon` and `game.platforms` no longer exist in `en.json`, so the helper no longer looks them up: instead the old pill text ("Coming soon" and "to iOS and Android") is removed from the fixture side before comparison (a small helper dropping those two visible items from `before`), and the Google badge label (`game.play.link`) is removed from `after` the same way the App Store label is. `scripts/fixtures/english-before/` is not edited. |
| `test_english_growth_under_15kb` | Unchanged. The HTML grows by well under 1 KB; the badges are separate files. |
| `test_links_resolve` | Unchanged; it now also covers the Google badge `src`. |
| `test_store_styles` | Updated if it asserts the old `.store` rules: it checks `.store` is a wrapping flex row, no hover background, and that no `.soon` rule remains. |
| `scripts/check_i18n.py` run | Must still pass; a unit check in `test_check.py` is added only if that file already tests the token list. |

## 7. Documentation

- `assets/badges/README.md`: the Google section is rewritten from "stored, not shown" to "shown": files in `google-play/<code>.png`, source URL pattern, locale mapping (including `tl` to `fil`, `he` to `iw`, `pt` to `pt-br`, `zh` to `zh-cn`), fetch date, measured margins, rules (no alteration, margin kept as clear space, at least 40 px visible), and `english_for` state. The sentence about "the 'Coming soon, to Android' pill" is removed.
- `README.md` (the `assets/badges/` tree line): both badges are shown.
- `i18n/README.md`: the paragraph about the App Store badge keys names `game.play.link`, drops `game.soon` and `game.platforms`; the "Store attribution" paragraph no longer says the badges are "not shown yet".
- Check with a search that no other doc says Google's badge is stored or unused.

## 8. Verification

- `python3 scripts/build.py`, then `--check`, `python3 scripts/test_build.py`, `python3 scripts/check_i18n.py`, `python3 scripts/test_check.py`.
- Headless browser (the repo-local `.playwright-cli`, or equivalent) at 1280 px and 320 px for English, German, Russian, Tagalog, Hebrew and Arabic home pages: game section shows Apple then Google, both sharp and visually the same height, wrap at 320 px without horizontal scroll, ribbon text inside the phone frame (the criterion 7 measurement), Arabic and Hebrew mirrored with unflipped images, keyboard focus ring visible on the Google link. The screenshots check layout only; they do not prove the live listing opens.
- The Play URL is checked once with `curl -sI`. Google may answer with a redirect or a consent page; the result is reported as it is, and a non-200 is not a reason to change the URL you supplied.

## Alternatives considered

- **Keep the "Coming soon, to Android" pill.** Rejected (default): the app is on Android, and the pill would say the opposite.
- **English badge everywhere.** Rejected by your answer; it is the documented fallback if localised files cannot be fetched.
- **Redraw or crop Google's PNG to match Apple's height.** Rejected: Google forbids alteration; the displayed height is set by CSS and the PNG margin is kept.
- **Two separate `<p class="store">` rows.** Rejected: one wrapping flex row keeps the two badges together on wide screens and stacks them on narrow ones.
- **Put `PLAY_URL` in the strings.** Rejected: one constant in `build.py`, as for `APPSTORE_URL` and `PATREON_URL`.

## Risks

- A Google badge file can have a different margin ratio per language, which would make Apple and Google badges look unequal in some languages; handled by the measured per-file height (section 4).
- Google's `tl` and `he` files exist under `fil` and `iw`; if Google renames them, the build fails loudly (missing file), not silently.
- "Now on iOS and Android" is longer than the old ribbon; handled by the overflow check and fallback (criterion 7).
- The 14 translated strings are AI-drafted and unreviewed, like the existing ones.
