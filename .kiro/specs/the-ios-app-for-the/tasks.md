# Tasks: App Store link for the iOS app

Work on a new branch from `main` in the main repo (for example `feature/app-store-link`), rebase often, and open a pull request at the end. Commit sources and generated pages together. All commands run from the repo root. Requirement numbers refer to the acceptance criteria in `requirements.md`; section numbers refer to `design.md`.

- [ ] 1. Baseline and branch
  - Create the branch. Run `python3 scripts/build.py --check`, `python3 scripts/test_build.py`, `python3 scripts/check_i18n.py` and `python3 scripts/test_check.py` and confirm all pass before any change.
  - Save the current English and translated text of `game.eyebrow`, `game.platforms`, `contact.h` and `contact.lead` for all 15 languages (read from `i18n/strings/*.json` at `HEAD`); task 3 uses them as literals.
  - Check the listing: `curl -sI https://apps.apple.com/us/app/royal-game-of-ur-world-ed/id6829337933` and note the status line for the pull request.
  - _Requirements: 12_

- [ ] 2. Fetch Apple's App Store badges
  - From Apple's Marketing Tools (the same toolbox used for the Apple Music badges, "Download on the App Store" family, black variant), download one badge per language using the locale mapping in `assets/music/README.md`, plus Arabic and Hindi if Apple publishes them.
  - `git mv assets/badges/app-store.svg assets/badges/app-store/en.svg`, then save the others as `assets/badges/app-store/<code>.svg`, unmodified.
  - Record which languages Apple does not publish; these become `english_for` in task 5. If a file cannot be fetched, that language uses the English badge and this is noted for the pull request. Draw nothing.
  - Read Apple's badge rules from the same page and confirm: clear space one quarter of the height, minimum 40 px. If they differ, note it for tasks 6 and 9.
  - _Requirements: 1, 4; design section 4_

- [ ] 3. Write the failing tests first (`scripts/test_build.py`)
  - Replace `test_badges_stored_but_not_shown` with `test_app_store_badge_shown_and_google_play_not`: on each of the 15 home pages exactly one link to `build.APPSTORE_URL` with `target="_blank"`, `rel="noopener"`, a non-empty `aria-label` containing "App Store", and an `<img alt="">` whose file exists (the localised file, or `en.svg` for `english_for` languages); no `apps.apple.com` link on the privacy, support and age pages; no page mentions `google-play` or `play.google.com`; `assets/badges/google-play.png` still exists.
  - Update `test_android_and_store_attribution`: the home page contains "to Android", and does not contain "to iOS and Android" or "It is not in the App Store or on Google Play yet."; privacy and support still say "for iOS and Android"; the Google trademark line check is unchanged.
  - Add `test_no_coming_soon_for_ios`: for each language, the home page no longer contains the old `contact.h` and `game.eyebrow` text saved in task 1, and shows `game.now` exactly once, as the ribbon.
  - Add `test_app_store_url_in_one_place`: the URL appears once in `scripts/build.py` and nowhere under `templates/` or `i18n/strings/`.
  - Add a unit test for the badge builder: a missing file raises `build.BuildError`, and a language in `english_for` resolves to `en.svg`.
  - Adapt `test_english_text_unchanged` with a new `undo_store_changes` (model it on `undo_iap_changes`): add `game.now` to `added`, and map the new English wording of `game.eyebrow`, `game.platforms`, `contact.h`, `contact.lead` and the ribbon text back to the old fixture text before comparing. Do not edit `scripts/fixtures/english-before/`.
  - Run the tests and confirm the new and updated ones fail for the right reasons on the current code.
  - _Requirements: 12; design section 6_

- [ ] 4. English strings
  - In `i18n/strings/en.json` add `game.now` ("Now on iOS") and `game.store.link` ("Download {app:title} on the App Store"), and reword `game.eyebrow`, `game.platforms`, `contact.h` and `contact.lead` exactly as in design section 3.
  - Leave `game.soon` unchanged.
  - _Requirements: 5, 7; design section 3_

- [ ] 5. Build script
  - In `scripts/build.py` add `APPSTORE_URL` and `APPSTORE_BADGE` next to `PATREON_URL`, with `english_for` set from task 2.
  - Generalise `logo_path` to take a descriptor dict (Apple Music keeps working) and add `Site.appstore(code, root)` returning the `<p class="store">` link block from design section 1, with the accessible name resolved from `game.store.link` and the language's `{app:title}` and then attribute-escaped, and width and height read with `image_size`.
  - Add `"appstore"` to `simple` in `render_page` for the home page only (empty string for other pages).
  - _Requirements: 1, 2, 3, 4; design section 1_

- [ ] 6. Template and styles
  - `templates/index.html`: ribbon uses `{{t:game.now}}`; add the `{{appstore}}` line after the feature list and before the Android pill.
  - `styles.css`: add the `.store` rules from design section 5 beside the `.soon` block, and extend the `prefers-reduced-motion` rule with `.store a`. If Apple's rules read in task 2 differ (minimum size or clear space), follow Apple.
  - Run `python3 scripts/build.py`.
  - _Requirements: 1, 3, 5, 9; design sections 2 and 5_

- [ ] 7. Translate into the other 14 languages
  - Add `game.now` and `game.store.link` and reword `game.eyebrow`, `game.platforms`, `contact.h` and `contact.lead` in `ar`, `de`, `es`, `fr`, `he`, `hi`, `it`, `ja`, `ko`, `pt`, `ru`, `tl`, `tr`, `zh`. Keep "App Store" in Latin script, keep `{app:title}` and the existing tags and tokens, use no em or en dashes, keep the existing translation of the GitHub sentence in `contact.lead`, and leave `_review` as `unreviewed`.
  - Use each language's existing "Coming soon" wording from `game.soon` for the Android pill context, and keep the Portuguese in pt-BR.
  - Run `python3 scripts/build.py`, then `python3 scripts/check_i18n.py`.
  - _Requirements: 8; design section 3_

- [ ] 8. Make the tests pass
  - Run `python3 scripts/build.py --check`, `python3 scripts/test_build.py`, `python3 scripts/check_i18n.py` and `python3 scripts/test_check.py`. Fix failures in code, not by loosening tests. Confirm `test_english_growth_under_15kb` still passes.
  - _Requirements: 12_

- [ ] 9. Documentation
  - `assets/badges/README.md`: replace the intro and table so Apple's badges are shown and listed per language with source URL and fetch date, record the badge rules read in task 2, and say the Google Play badge is stored but unused until Android has a live listing. Update the old "To show them" paragraph for the new state.
  - `i18n/README.md`: one sentence naming `game.now` and `game.store.link` in the strings section.
  - Check that no other doc still says the badges are "not shown on any page".
  - _Requirements: 4, 6; design sections 3 and 4_

- [ ] 10. Visual check
  - Serve the repo root with `python3 -m http.server 8000 --bind 127.0.0.1` and screenshot the `#game` and `#contact` sections of the English, Arabic, German and Japanese home pages at 1280 px and 320 px with a headless browser.
  - Confirm: badge visible and sharp, Android pill under it, ribbon reads "Now on iOS" (or the language's wording), no horizontal scroll at 320 px, Arabic mirrored with the badge unflipped, keyboard focus ring visible on the badge. State what the screenshots do and do not show; they do not prove the live link opens.
  - Stop the server when done.
  - _Requirements: 3, 9_

- [ ] 11. Pull request
  - Commit the spec, sources, badge files and regenerated pages with rebase-clean history, push the branch by name, and open a pull request with the description written to a file. The description lists: the listing HTTP status from task 1, which languages use the English badge fallback, any badge that could not be fetched, that translations are AI-drafted and unreviewed, and the test commands run with their results.
  - Wait for review, address comments, rebase if needed. Do not merge; a human merges.
  - _Requirements: 12_
