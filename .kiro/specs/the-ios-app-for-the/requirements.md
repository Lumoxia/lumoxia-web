# Requirements: App Store link for the iOS app

## Goal

*The Royal Game of Ur (World Edition)* is now live on the App Store. Update the Lumoxia website so every visitor can reach the listing, and so the page no longer says the app is "coming soon" on iOS. The Android version is still unreleased, so Android keeps a "Coming soon" message.

The listing is `https://apps.apple.com/us/app/royal-game-of-ur-world-ed/id6829337933`.

Use the existing pipeline: edit `templates/`, `i18n/strings/*.json`, `styles.css` and `scripts/`, run `python3 scripts/build.py`, and commit sources and generated pages together. The site stays static and dependency-free: no script, tracker or embed is added.

## Where "coming soon" appears today

All four are in the home page template and its strings, so they appear on every language build.

| Place | Today (English) |
|---|---|
| Ribbon on the phone screenshot (`game.soon`) | "Coming soon" |
| Eyebrow over the game title (`game.eyebrow`) | "First app, coming soon" |
| Pill under the feature list (`game.soon` and `game.platforms`) | "Coming soon, to iOS and Android" |
| Contact band heading and lead (`contact.h`, `contact.lead`) | "{app:title} is coming soon" and "It is not in the App Store or on Google Play yet. Follow the work on GitHub." |

`assets/badges/app-store.svg` (Apple's black "Download on the App Store" badge) and `assets/badges/google-play.png` are already stored but unused. `assets/badges/README.md` says the badges may only link to a live listing, and that is now true for Apple only.

## Acceptance criteria

1. **App Store badge in the game section.** The `#game` section of the home page of every language shows Apple's official "Download on the App Store" badge, linking to the listing URL above. The badge is unaltered (not redrawn, recoloured, cropped or given effects), keeps Apple's clear space of one quarter of its height, and is shown at least 40 px high. It sits where the "Coming soon" pill sits today, above the Android notice.
2. **One place for the URL.** The listing URL is defined once in `scripts/build.py`, next to `PATREON_URL`, and reaches the templates through a token. No template or strings file contains the URL.
3. **Safe, clear link.** The link opens in a new tab with `rel="noopener"`. Its accessible name is translated in all 15 languages and names the app and the store (for example "Download {app:title} on the App Store"). The badge image has empty `alt` text, so the link has one name, not two. The badge is never translated or mirrored in right-to-left pages. The touch target is at least 44 px by 44 px, with a visible gold keyboard focus ring and a hover state consistent with the existing links.
4. **Localised badge where Apple offers one.** Each language page uses Apple's own badge for that language when Apple publishes one, following the rule already in `assets/badges/README.md`. Languages without an Apple badge use the stored English one (the same fallback pattern as the Apple Music badges, which list the exceptions in `english_for`). Each file's source page and fetch date are recorded in `assets/badges/README.md`. If a localised badge cannot be obtained, that language uses the English badge and the pull request says so; no badge is drawn.
5. **iOS is no longer "coming soon".** The three game-section messages change as follows in English, and the same meaning in the other 14 languages:
   - Ribbon: "Now on iOS" (replaces "Coming soon").
   - Eyebrow: "First app, out now on iOS" (replaces "First app, coming soon").
   - Pill: strong text "Coming soon", small text "to Android" (replaces "to iOS and Android"). The mark and layout of the pill are unchanged.
6. **Android stays "coming soon", with no Google Play link.** Nothing on the site links to Google Play or shows the Google Play badge. `assets/badges/google-play.png` stays stored and unused, and `assets/badges/README.md` says Apple's badge is now shown and Google's is still waiting for a live listing.
7. **Contact band.** The heading and lead no longer say the app is coming soon or that it is not in the App Store. English: heading "{app:title} is on the App Store" and lead "Get it on the App Store. The Android version is coming soon. Follow the work on GitHub." The GitHub and Patreon buttons, their spacing and their copy are unchanged.
8. **Translations.** Every changed or new string exists in all 15 `i18n/strings/*.json` files with the same tags and tokens as English, no em or en dashes, and `_review` left as `unreviewed`. "App Store" and the app title are not translated (the title comes from `{app:title}`). Tone stays plain and direct, in the solo-studio voice.
9. **Layout.** On a 320 px viewport the badge, the Android pill and the text stay inside the container and centred or aligned as the pill is today, with no horizontal scroll. Arabic and Hebrew mirror correctly. The English home page grows by less than 15 KB over `scripts/fixtures/english-before/`, as the existing test requires.
10. **Trademark line.** `footer.trademarks` already credits Apple's App Store service mark and Google's Play marks, and is left unchanged. Apple's badge guidelines require no further credit.
11. **Unchanged.** The hero, mission, music, founder and footer layout, the Privacy, Support and Age Suitability pages, and their "for iOS and Android" wording (the app's policies still cover both platforms) are untouched. The sitemap needs no change.
12. **Checks.** `python3 scripts/build.py --check`, `python3 scripts/test_build.py` and `python3 scripts/check_i18n.py` pass. The test `test_badges_stored_but_not_shown` is replaced by tests that: the App Store badge and exact listing URL are present once on every language's home page; no page links to Google Play or references `google-play.png`; no page still contains the old "coming soon" iOS wording in any language; and the old "not in the App Store" contact copy is gone. These tests fail on the current code and pass after the change.

## Out of scope

- A Google Play link or badge, until the Android app is published.
- App Store smart-banner meta tags, structured data (`SoftwareApplication`) and Open Graph changes.
- Country-specific listing URLs: the single `/us/` URL is used for every language, as given. Apple redirects visitors to their own storefront.
- Changing the support, privacy or age-suitability pages, or the Android wording in them.

## Decisions I made that you may overrule

- **Ribbon kept, reworded** to "Now on iOS" rather than removed, so the phone screenshot keeps its accent and the page says plainly which platform is live.
- **Badge in the game section only**, not also in the hero or the Contact band, to keep one clear call to action. The Contact band links to the same listing through the text change only.
- **Localised badges** are included (criterion 4). If you would rather ship the English badge everywhere now and localise later, criterion 4 becomes a single sentence and the task list gets shorter.
