# Tasks: Age Suitability page for The Royal Game of Ur

Implements `requirements.md` and `design.md`. Work in `/Users/giorsi/Development/kiro/lumoxia-web`. Tests are written before the code they cover (tasks 2 and 3 before 4 to 8). Commit the sources and the regenerated pages together. Do not edit generated pages by hand.

- [x] 1. Branch
  - From an up-to-date `main`, create the branch `feature/age-suitability-page` in the main repo checkout (the checkout currently holds untracked spec folders only; do not touch them). Add this spec folder `.kiro/specs/investigate-what-an-apple-store/` to the first commit.
  - Run `python3 scripts/build.py --check`, `python3 scripts/check_i18n.py` and `python3 scripts/test_build.py` and confirm all three pass before any change (baseline).

- [x] 2. Write the failing tests first (`scripts/test_build.py`)
  - Add `"age": "age.html"` to the test file's `PAGES` so the existing all-pages loops cover the new page (requirement 2.2, 2.5).
  - Add `test_age_page_states_the_content_facts`: for each of the 15 languages, the generated page contains the rendered `age.content.l1` to `l6`, `age.buy.p1`, `age.privacy.p`, `age.region.p`, `age.changes.p`; the contact link is `mailto:rgur-support@lumoxia.art?subject=` plus the URL-encoded `age.subject`; for languages other than English each of those strings differs from the English text (requirements 1.3 to 1.7, design Tests 2).
  - Add `test_age_page_does_not_state_a_rating`: no age page contains `4+`, `9+`, `13+`, `16+` or `18+` (decision D1).
  - Add `test_age_page_is_linked`: in every language the Privacy, Support, landing and Age pages each have a footer link whose `href` ends in `royal-game-of-ur/age-suitability/` and none of them has it in the top navigation (requirement 3.1, decision D2).
  - Add `test_sitemap_has_the_age_pages`: `sitemap.xml` has 15 `<loc>` entries for the age page, each with 15 language alternates plus `x-default` (requirement 2.4).
  - Update `test_english_text_unchanged` so that, for the Privacy, Support and landing pages, it removes the `footer.age` text and its preceding `·` separator before comparing with `scripts/fixtures/english-before/` (same technique as the Patreon footer link). Do not change the fixtures.
  - Run `python3 scripts/test_build.py` and confirm the new tests fail for the right reason (page missing), not because of a typo in the test.

- [x] 3. Register the page in the generator (`scripts/build.py`)
  - Add `"age": ("age.html", "royal-game-of-ur/age-suitability/")` to `PAGES`. Check that `render_page`'s `albumlinks` guard (`page == "index"`) and the other per-page code need no change; the address, `alternates`, `langmenu` and `sitemap` loops already use `PAGES`.

- [x] 4. English strings (`i18n/strings/en.json`)
  - Add the keys and English text exactly as in the design's strings table: `meta.age.title`, `meta.age.description`, `footer.age`, `age.h1`, `age.meta`, `age.short`, `age.content.h`, `age.content.p`, `age.content.l1` to `age.content.l6`, `age.buy.h`, `age.buy.p1`, `age.buy.p2`, `age.privacy.h`, `age.privacy.p`, `age.region.h`, `age.region.p`, `age.changes.h`, `age.changes.p`, `age.contact.h`, `age.contact.p`, `age.subject`.
  - Place the `meta.age.*` keys after `meta.support.*`, `footer.age` after `footer.privacy`, and the `age.*` keys after `support.*`, matching the file's existing grouping. No em or en dashes.

- [x] 5. Template (`templates/age.html`) and footer links
  - Create `templates/age.html` from `templates/support.html` with the body order in the design (h1, meta, bold summary, content list, purchases and links, privacy for children, age rules in different countries, changes, questions with the mailto button) and the footer carrying the new link between Support and the e-mail address. Top navigation unchanged.
  - Add the footer link `<a href="{{base}}royal-game-of-ur/age-suitability/">{{t:footer.age}}</a>` to `templates/privacy.html` and `templates/support.html` (same `&middot;` pattern), and to `templates/index.html`'s footer link row after Patreon.

- [x] 6. Translations (14 files: `fr`, `es`, `de`, `ar`, `zh`, `it`, `hi`, `tl`, `tr`, `ru`, `he`, `pt`, `ja`, `ko`)
  - Add every new key to each file, translated from the English text, in the same position as in `en.json`. Keep inline tags and tokens identical to English (`<a href="{{base}}royal-game-of-ur/privacy/">` and `.../support/`, `{app:title}`, `&rsquo;`); translate the link text. Write the "Last updated 3 November 2026" date in each language's format, following that language's `privacy.meta` string. No em or en dashes.
  - Use each language's existing app wording from `i18n/app-terms.json` through the tokens; do not retype app terms. Do not change any `_review` value.
  - Run `python3 scripts/check_i18n.py` and fix anything it reports (key sets, tags, tokens, dashes, template keys).

- [x] 7. Generate and run the full checks
  - Run `python3 scripts/build.py`; confirm it writes the 15 new pages (`royal-game-of-ur/age-suitability/index.html` and `<code>/royal-game-of-ur/age-suitability/index.html`) and regenerates the Privacy, Support and landing pages and `sitemap.xml`.
  - Run `python3 scripts/check_i18n.py`, `python3 scripts/build.py --check` and `python3 scripts/test_build.py`. All new and existing tests must pass, including any that were failing before (none are expected). Report counts and the commit the results were run on.

- [x] 8. Documentation
  - In `README.md`, add the new page to the repository layout comment and wherever Privacy and Support are listed as pages. In `i18n/README.md`, mention the `age.*` and `footer.age` keys where the page-specific keys are described. State that the Age Suitability URL is the English page address.

- [x] 9. Visual check
  - Serve the site locally with `python3 -m http.server 8080 --bind 127.0.0.1 --directory .` and open the English, German, Arabic, Hebrew and Japanese age pages at desktop and phone widths (the browser tool refuses localhost addresses, so use `playwright-cli open`, which asks for approval). Compare against the Support page: header, language menu, list, contact button, footer. Check RTL direction in Arabic and Hebrew, that the six-item list and the button wrap cleanly in German, and that the footer link on Privacy, Support and the landing page opens the page. Fix any layout problem in the template or strings and re-run task 7.
  - Stop the local server when done.

- [~] 10. Pull request
  - Rebase on current `main`, push `feature/age-suitability-page` (one plain push, branch named explicitly), and open a pull request titled "Add Age Suitability page for The Royal Game of Ur" whose description lists the URL to enter in App Store Connect (`https://lumoxia.art/royal-game-of-ur/age-suitability/`, App Information, Age Rating, Age Suitability URL (Optional)), the test counts with the commit they were run on, and a reminder that the translations are `unreviewed`. Write the description to a file and use `--body-file`.
  - Wait for the review, address comments after verifying each one, rebase if needed, and stop. Only the owner merges.

- [ ] 11. After the merge (owner step, not agent work)
  - Once GitHub Pages has deployed, open `https://lumoxia.art/royal-game-of-ur/age-suitability/` and confirm it loads over HTTPS without sign-in, then paste it into App Store Connect's Age Suitability URL field and confirm on the live form that the field accepts it.
