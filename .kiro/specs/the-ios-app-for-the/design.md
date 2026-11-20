# Design: App Store link for the iOS app

Implements `requirements.md` (approved with: ribbon "Now on iOS", badge in the game section only, Apple's localised badge per language with English fallback). It follows the pattern the album links already use: a constant and a build method in `scripts/build.py`, one token in the template, assets under `assets/`, a provenance README, and tests in `scripts/test_build.py`.

## Overview

```
scripts/build.py   APPSTORE_URL + APPSTORE_BADGE + Site.appstore() -> {{appstore}} token (home page only)
templates/index.html   ribbon uses game.now; {{appstore}} sits above the Android pill in #game
i18n/strings/*.json    1 new key pair per language, 4 reworded keys
assets/badges/app-store/<code>.svg   one official badge per language (English fallback)
styles.css         .store (badge link) rules, beside the existing .soon rules
scripts/test_build.py  replace the "stored but not shown" test, adapt two others
assets/badges/README.md  provenance of the badge files, Google status
```

Nothing is added to the privacy, support or age templates, the sitemap or the language menu.

## 1. Build script (`scripts/build.py`)

Next to `PATREON_URL`:

```python
APPSTORE_URL = "https://apps.apple.com/us/app/royal-game-of-ur-world-ed/id6829337933"
# Apple's "Download on the App Store" badge, black, one file per language in assets/badges/app-store/.
# A language listed in english_for has no Apple badge and uses en.svg; any other missing file is an error.
APPSTORE_BADGE = {"file": "app-store/{lang}.svg", "english_for": ()}
```

`english_for` is filled in by the badge-fetch task (below) with exactly the languages Apple does not publish. It starts empty so a forgotten or misspelt file fails the build, the same rule as `MUSIC_SERVICES`.

A new method `Site.appstore(code, root)` mirrors `albumlinks`. It resolves the file (same logic as `logo_path`; `logo_path` is generalised to take the descriptor dict, so Apple Music and App Store share it), reads the size with `image_size`, and returns:

```html
<p class="store"><a href="https://apps.apple.com/us/app/royal-game-of-ur-world-ed/id6829337933" target="_blank" rel="noopener" aria-label="Download The Royal Game of Ur on the App Store"><img src="assets/badges/app-store/en.svg" alt="" width="120" height="40" /></a></p>
```

- The accessible name comes from the new string `game.store.link`, with `{app:title}` resolved from the language's `app-terms.json` entry (the same way `{t:...}` strings resolve it), then attribute-escaped. The image has `alt=""` so the link has one name (criterion 3).
- Width and height come from the SVG `viewBox`, so localised badges of different widths do not shift the layout.
- `render_page` adds `"appstore": self.appstore(code, root_prefix(rel)) if page == "index" else ""` to `simple`, and `"appstoreurl"` is not needed because the URL appears only inside this method's output. This keeps criterion 2: the URL exists once, in `build.py`, and in no template or strings file.

## 2. Template (`templates/index.html`, `#game` section)

Three edits:

1. Ribbon: `{{t:game.soon}}` becomes `{{t:game.now}}`.
2. Eyebrow is unchanged in the template (`game.eyebrow`); only its string changes.
3. The `{{appstore}}` token goes after the feature list and before the Android pill:

```html
            </ul>
{{appstore}}
            <div class="soon" role="note">
              <img src="{{root}}assets/mark.svg" alt="" width="40" height="40" />
              <span><strong>{{t:game.soon}}</strong><small>{{t:game.platforms}}</small></span>
            </div>
```

The Contact band template is unchanged; its text changes through `contact.h` and `contact.lead`.

## 3. Strings (all 15 `i18n/strings/*.json`)

| Key | English | Change |
|---|---|---|
| `game.now` | "Now on iOS" | new, ribbon |
| `game.store.link` | "Download {app:title} on the App Store" | new, accessible name of the badge link |
| `game.eyebrow` | "First app, out now on iOS" | reworded |
| `game.platforms` | "to Android" | reworded (was "to iOS and Android") |
| `contact.h` | "{app:title} is on the App Store" | reworded |
| `contact.lead` | "Get it on the App Store. The Android version is coming soon. Follow the work on GitHub." | reworded |
| `game.soon` | "Coming soon" | unchanged, now used only by the Android pill |

`game.now` is a separate key rather than a reuse of `game.soon` because the ribbon and the pill now say different things and translators must see them as two strings. The `contact.lead` sentence about GitHub keeps its existing translation, so translators only add and change the first two sentences. "App Store" stays in Latin script in every language, as the footer attribution does today. Other languages keep the same tags and tokens, use no em or en dashes, and leave `_review` as `unreviewed`. `scripts/check_i18n.py` already enforces key parity, tag and token parity and the dash rule, so it covers the new keys without changes. `i18n/README.md` gets one sentence naming `game.now` and `game.store.link`.

## 4. Badge files (`assets/badges/app-store/`)

- Source: Apple's Marketing Tools "Download on the App Store" badge, black variant (the site is dark, and the stored English badge is already the black one). The Apple Music badges came from `https://toolbox.marketingtools.apple.com/api/v2/badges/...`; the App Store badge comes from the same toolbox, "Download on the App Store" family, one locale per language. The exact URL pattern is confirmed when the files are fetched.
- Locales follow the Apple Music mapping already recorded in `assets/music/README.md` (en-us, fr-fr, es-es, de-de, zh-cn, it-it, tl-ph, tr-tr, ru-ru, he-il, pt-br, ja-jp, ko-kr), plus Apple's Arabic and Hindi badges if Apple publishes them for the App Store. Apple's published set can differ from Apple Music's, so the fetch task records which languages exist and fills `english_for` with those that do not.
- `assets/badges/app-store.svg` (the stored US-UK badge) moves to `assets/badges/app-store/en.svg` with `git mv`, and its README row is updated. Nothing else references the old path, apart from the test being replaced.
- Files are used exactly as Apple distributes them (not redrawn, recoloured or cropped).
- `assets/badges/README.md` is updated: table of files by language with the source URL and fetch date, the badge rules kept (clear space one quarter of the height, minimum 40 px, never altered), and a line saying the Google Play badge is still waiting for a live listing.

If Apple's toolbox cannot be reached or returns a different file than expected for some language, that language uses the English badge and the pull request says so (criterion 4). No badge is drawn.

## 5. Styles (`styles.css`)

Added beside the `.soon` block:

```css
/* App Store badge: Apple's clear space is one quarter of the badge height (10px at 40px high) */
.store { margin: 20px 0 14px; }
.store a { display: inline-flex; align-items: center; justify-content: center; min-width: 44px; min-height: 44px;
  padding: 10px; border-radius: 12px; transition: background 0.15s ease, transform 0.15s ease; }
.store a:hover { background: rgba(232, 198, 106, 0.14); transform: translateY(-2px); }
.store a:focus-visible { outline: 2px solid var(--gold-400); outline-offset: 2px; }
.store img { display: block; height: 40px; width: auto; max-width: 100%; }
```

- These values copy the `.listen a` hover, focus ring and transition, so the badge behaves like the album links. The existing `prefers-reduced-motion` rule is extended with `.store a` so hover movement and transition stop.
- The block sits in the text column of `.product`, which is start-aligned, so it follows the text direction. In right-to-left pages the column is mirrored by the existing `dir` handling; the badge image itself is not flipped because no transform is applied to it.
- On a 320 px viewport, 40 px badge plus 10 px padding on each side is about 140 px wide, far inside the container. `max-width: 100%` is a guard for any wider localised badge.
- The existing 4-pixel-radius ribbon and the `.soon` pill are untouched; only their text changes.

## 6. Tests (`scripts/test_build.py`)

| Test | Change |
|---|---|
| `test_badges_stored_but_not_shown` | Replaced by `test_app_store_badge_shown_and_google_play_not`. For all 15 home pages: exactly one `<a>` with `href` equal to `build.APPSTORE_URL`, with `target="_blank"`, `rel="noopener"`, a non-empty `aria-label` containing "App Store" and the app title, and a child `<img alt="">` whose file exists and is the localised file (or `en.svg` for `english_for` languages). Other pages (privacy, support, age) contain no `apps.apple.com` link. No page references `google-play` or `play.google.com`. `assets/badges/google-play.png` still exists. |
| `test_android_and_store_attribution` | The two `assertIn` lines on the home page change: "to Android" is present, "to iOS and Android" and "It is not in the App Store or on Google Play yet." are absent. Privacy and support keep "for iOS and Android". The Google trademark line check is unchanged. |
| `test_english_text_unchanged` | The home-page branch adds the new visible strings (`game.now`) to `added` and, because five old strings are reworded, maps them back before comparing with the "before" fixture, the same technique `undo_iap_changes` uses for the privacy page (new `undo_store_changes` replaces the new English wording of `game.eyebrow`, `game.platforms`, `contact.h` and `contact.lead` with the old fixture text, and the ribbon text `game.now` with "Coming soon"). The fixtures themselves are not edited: they stay a record of the original site. |
| New: `test_no_coming_soon_for_ios` | For each language, the home page does not contain that language's old `contact.h` and old `game.eyebrow` text (captured as literals in the test from `HEAD` before the change), and `game.now` appears once, as the ribbon text. |
| New: `test_app_store_url_in_one_place` | The listing URL appears in `scripts/build.py` once, and in no file under `templates/` or `i18n/strings/`. |
| `test_english_growth_under_15kb` | Unchanged. The badge file is a separate request, and the HTML grows by well under 1 KB. |
| `test_links_resolve` | Unchanged; it now also covers the badge `src`. |

The new tests are written first and watched failing on the current code (criterion 12), then the implementation makes them pass. `scripts/check_i18n.py` and `build.py --check` run unchanged.

## 7. Verification

- `python3 scripts/build.py`, then `--check`, `python3 scripts/test_build.py`, `python3 scripts/check_i18n.py`, `python3 scripts/test_check.py`.
- Render the home page of English, Arabic, German and Japanese with a headless browser at 1280 px and 320 px and look at the game section: badge visible and sharp, Android pill below it, ribbon text, no horizontal scroll, Arabic mirrored with the badge unflipped. These screenshots check layout only; they do not prove the live App Store link opens, which is not checked beyond the URL string matching the one you supplied.
- The App Store URL is checked once with a plain `curl -sI` for a 200 (or Apple's redirect) response, and the result is reported as it is.

## Alternatives considered

- **Reuse `game.soon` for the ribbon.** Rejected: the ribbon and the pill now carry different messages, and sharing a key would force one translation for both.
- **Put the URL in the strings as `{url:...}` or in the template.** Rejected: criterion 2 and the Patreon precedent require one place in `build.py`.
- **Add the badge as plain template HTML with `{{root}}`.** Rejected: the localised file name and its width and height depend on the language, which the build already knows how to resolve (as for Apple Music).
- **Also show the badge in the Contact band.** Rejected by you (game section only).

## Risks

- Apple may not publish an App Store badge for every one of the 15 languages (Tagalog is the likeliest gap). The English fallback list handles it and the README records it.
- Apple's badge terms are read from its Marketing Resources page when the files are fetched; if they differ from the rules in `assets/badges/README.md` (40 px minimum, one quarter clear space), the README and CSS follow Apple's page.
- Translations of the four reworded strings and two new strings in 14 languages are AI-drafted and unreviewed, like all existing ones.
