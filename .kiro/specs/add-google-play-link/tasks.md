# Tasks: Google Play link beside the App Store link

Work on branch `feature/google-play-link` (a git worktree outside the main checkout), rebase often, and open a pull request at the end. Commit sources and generated pages together. All commands run from the repo root. Requirement numbers refer to the acceptance criteria in `requirements.md`; section numbers refer to `design.md`.

- [x] 1. Baseline
  - Run `python3 scripts/build.py --check`, `python3 scripts/test_build.py`, `python3 scripts/check_i18n.py` and `python3 scripts/test_check.py` and confirm all pass before any change.
  - Save, for all 15 languages, the current text of `game.now`, `game.eyebrow`, `contact.h`, `contact.lead`, `game.soon` and `game.platforms` (read from `i18n/strings/*.json` at `HEAD`); task 3 uses the old `contact.lead` Android sentence as literals.
  - Search `templates/`, `scripts/`, `styles.css` and the docs for `game.soon`, `game.platforms` and `.soon` to confirm the pill is the only live user (design section 2).
  - Check the listing: `curl -sI "https://play.google.com/store/apps/details?id=art.lumoxia.royalgameofur"` and note the status line for the pull request.
  - _Requirements: 8, 15_

- [x] 2. Fetch Google's badges and measure them
  - From `https://play.google.com/intl/en_us/badges/static/images/badges/<locale>_badge_web_generic.png` download one PNG per language with the mapping in design section 4 (en, fr, es, de, ar, zh-cn, it, hi, fil for tl, tr, ru, iw for he, pt-br, ja, ko). Save unmodified as `assets/badges/google-play/<code>.png`.
  - Compare the fetched `en` file with the stored `assets/badges/google-play.png`, then `git mv` the stored file to `assets/badges/google-play/en.png` (the fetched file replaces it if they differ).
  - Record any language for which Google serves no file; these become `english_for` in task 5. If localised files cannot be fetched at all, use the stored English badge for every language and note it for the pull request. Draw nothing.
  - For each file measure the pixel size and the bounding box of the non-transparent pixels (for example with Python and a PNG reader or `sips`); decide the displayed height that makes the visible badge 40 px high, matching Apple's badge (design section 4). Note whether the margin ratio is the same in every file.
  - Read Google's badge guidelines from the badge page and note the rules (no alteration, clear space, minimum size).
  - _Requirements: 2, 3; design section 4_

- [x] 3. Write the failing tests first (`scripts/test_build.py`)
  - Rewrite `test_app_store_badge_shown_and_google_play_not` into `test_store_badges_shown` and extend the `store_links` helper: Apple anchor once and before the Google anchor; Google anchor once with `href == build.PLAY_URL`, `target="_blank"`, `rel="noopener"`, `aria-label` containing "Google Play" and the app title, child `<img alt="">` with a file ending in `assets/badges/google-play/<code>.png` (or `en.png` for `english_for`) that exists; no `utm_` or `hl=` in the URL; other pages carry neither store link (ignore the Terms' Play Terms link).
  - Update `test_android_and_store_attribution`: the home page no longer contains "to Android"; privacy and support keep "for iOS and Android"; the Google trademark line check stays.
  - Rename and extend `test_no_coming_soon_for_ios` to `test_no_coming_soon`: no `class="soon"` on any page, `game.soon` and `game.platforms` absent from all 15 strings files, `game.now` once as the ribbon, and the old Android sentence of `contact.lead` absent per language (literals from task 1).
  - Add `test_play_url_in_one_place`, `test_play_badge_resolution` (resolves per language, missing file raises `build.BuildError`, `english_for` gives `en.png`, every site language has its file), `test_ribbon_and_eyebrow_strings` (English wording exact; every language names both platforms in Latin script; no dashes) and `test_play_badge_height` (visible height at the displayed size is at least 40 px, from task 2's measurements).
  - Update `OLD_STORE_EN`, `undo_store_changes` and `test_english_text_unchanged` as in design section 6: map the new English wording of `game.now`, `game.eyebrow`, `contact.h`, `contact.lead` back to the original site text, drop the old pill text from the fixture side, and drop the `game.play.link` label from the page side. Do not edit `scripts/fixtures/english-before/`.
  - Update `test_store_styles` for the wrapping flex `.store` and no `.soon` rules.
  - Run the tests and confirm the new and updated ones fail for the right reasons on the current code.
  - _Requirements: 15; design section 6_

- [x] 4. English strings
  - In `i18n/strings/en.json`: reword `game.now` ("Now on iOS and Android"), `game.eyebrow` ("First app, out now on iOS and Android"), `contact.h` ("{app:title} is on the App Store and Google Play") and `contact.lead` ("Follow the work on GitHub."); add `game.play.link` ("Get {app:title} on Google Play"); delete `game.soon` and `game.platforms` if task 1 found no other user.
  - _Requirements: 6, 8, 9; design section 3_

- [x] 5. Build script and i18n checker
  - `scripts/build.py`: add `PLAY_URL` and `PLAYSTORE_BADGE` (with `english_for` from task 2) next to `APPSTORE_URL`; make `Site.appstore()` return the bare anchor; add `Site.playstore()` (accessible name from `game.play.link`, size from `image_size`, displayed height from task 2); add `"playstore"` to `simple` in `render_page` for the home page only.
  - `scripts/check_i18n.py`: add `"playstore"` to the allowed template tokens.
  - _Requirements: 3, 4, 5, 11; design section 1_

- [x] 6. Template and styles
  - `templates/index.html`: replace `{{appstore}}` and the "Coming soon" pill with `<p class="store">{{appstore}}{{playstore}}</p>`.
  - `styles.css`: make `.store` a wrapping flex row, add the Google image rule with the height from task 2, delete the `.soon*` rules and fix the section comment.
  - Run `python3 scripts/build.py`.
  - _Requirements: 1, 2, 5, 8, 12; design sections 2 and 5_

- [x] 7. Translate into the other 14 languages
  - In `ar`, `de`, `es`, `fr`, `he`, `hi`, `it`, `ja`, `ko`, `pt`, `ru`, `tl`, `tr`, `zh`: extend `game.now` and `game.eyebrow` to name iOS and Android, add `game.play.link`, reword `contact.h` to name the App Store and Google Play, cut the Android sentence from `contact.lead` (keep the GitHub sentence verbatim), and delete `game.soon` and `game.platforms`. Keep "App Store", "Google Play", "iOS" and "Android" in Latin script, keep `{app:title}` and existing tags and tokens, use no em or en dashes, keep Portuguese in pt-BR, and leave `_review` as `unreviewed`. Keep the key sets of all 15 files identical.
  - Run `python3 scripts/build.py`, then `python3 scripts/check_i18n.py`.
  - _Requirements: 6, 9, 10; design section 3_

- [x] 8. Make the tests pass
  - Run `python3 scripts/build.py --check`, `python3 scripts/test_build.py`, `python3 scripts/check_i18n.py` and `python3 scripts/test_check.py`. Fix failures in code, not by loosening tests. Confirm `test_english_growth_under_15kb` still passes.
  - _Requirements: 15_

- [x] 9. Visual check and ribbon overflow
  - Serve the repo root with `python3 -m http.server 8000 --bind 127.0.0.1`. Screenshot the `#game` and `#contact` sections of the English, German, Russian, Tagalog, Hebrew and Arabic home pages at 1280 px and 320 px.
  - Measure at 320 px for each of those languages: document `scrollWidth` against `clientWidth`, and the ribbon's bounding box against the phone frame. If any ribbon overflows, apply the design section 5 fallback: first wrapping (`max-width`, `white-space: normal`), then, only if still needed, a shorter `game.now` for that language, and re-run task 8. Record the result per language.
  - Confirm: Apple then Google badges, equal visible height, wrap at 320 px with no horizontal scroll, Arabic and Hebrew mirrored with unflipped images, focus ring visible on the Google link. State what the screenshots do and do not show. Stop the server when done.
  - _Requirements: 1, 2, 5, 7, 12_

- [x] 10. Documentation
  - `assets/badges/README.md`: rewrite the Google section (shown; files; URL pattern; locale mapping; fetch date; measured margins; guideline rules read in task 2; `english_for` state) and remove the pill sentence. `README.md` (the `assets/badges/` line) and `i18n/README.md` (the badge-keys paragraph and the "Store attribution" paragraph) updated as in design section 7. Search for any other doc that says Google's badge is stored or unused.
  - _Requirements: 3, 16; design section 7_

- [x] 11. Commit and pull request
  - Commit spec, sources, badge files and regenerated pages with a clean history. Push the branch by name and open a pull request with the description written to a file. It lists: the listing HTTP status from task 1, any language on the English badge fallback, ribbon overflow results per language and what was changed, that translations are AI-drafted and unreviewed, and the test commands run with their results.
  - Wait for review, address comments, rebase if needed. Do not merge; a human merges.
  - _Requirements: 15_
