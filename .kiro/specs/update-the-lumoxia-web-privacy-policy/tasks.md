# Tasks: Privacy policy says backup can copy saved progress off the device

Implements `requirements.md` and `design.md`. All paths are relative to `/Users/giorsi/Development/kiro/lumoxia-web`. Never edit generated pages by hand.

- [ ] 1. Branch
  - In the main repo, from an up-to-date `main`, create `feature/privacy-backup` (`git switch -c feature/privacy-backup`). Leave the untracked `.kiro/` folder as it is, except that the spec files are committed with the change.
  - Run `python3 scripts/test_build.py` once and note that it passes before any edit (baseline: 40 tests OK).

- [ ] 2. Register the intended edits in the fixture first (tests before code)
  - In `scripts/fixtures/english-before/iap-changes.json`, add to `changed`: `privacy.stores.p1` = "The app keeps a few things on your device only, so the game remembers them next time:" and `privacy.stores.p2` = the old sentence from `scripts/fixtures/english-before/privacy.html` ("This information never leaves your device. Lumoxia cannot see it. You can erase the statistics at any time with &ldquo;Reset all statistics&rdquo; in the Stats panel, and deleting the app removes everything."), copied exactly with the `{app:statsReset}` token in place of "Reset all statistics" as in the current English string.
  - Add to `added`: `privacy.stores.l3`, `privacy.stores.p3`.
  - Add `test_privacy_says_backup_can_copy_data` to `scripts/test_build.py`, as specified in the design: for every language the page contains `privacy.stores.l3`, `privacy.stores.p2`, `privacy.stores.p3` and `privacy.keep.p`, and `privacy.meta` does not contain "25"; for English the page text contains neither "never leaves your device" nor "removes everything". Keep the existing `assertNotIn("21", ...)`.
  - Run `python3 scripts/test_build.py`: the new test fails (keys absent), which proves it can fail.

- [ ] 3. English copy and template
  - In `i18n/strings/en.json`: set `privacy.meta` date to "2 November 2026"; change `privacy.stores.p1`; add `privacy.stores.l3` and `privacy.stores.p3`; rewrite `privacy.stores.p2` and `privacy.keep.p`, using the exact text in the design's string table.
  - In `templates/privacy.html`: add `<li>{{t:privacy.stores.l3}}</li>` after the `l2` item and `<p>{{t:privacy.stores.p3}}</p>` after the `p2` paragraph.
  - Do not touch `privacy.short`, `meta.privacy.description`, `privacy.not.*`, `privacy.iap.*`, `privacy.changes.p`, `privacy.site.p` or the support page.

- [ ] 4. Translate the 14 other languages
  - For fr, es, de, ar, zh, it, hi, tl, tr, ru, he, pt, ja, ko edit `i18n/strings/<code>.json`: the same six keys plus `privacy.meta`, with the date in each language's own format and month name (keep the machine-translation notice already present in tr, ru, he and pt).
  - Reuse each file's own wording for "your device", "backup", "reset statistics" and its date format. Keep `{app:statsReset}` and the inline tags exactly as in English. "Google", "Google Account", "iCloud" are not translated. No em or en dashes. Leave `_review` as `unreviewed`.
  - Three of these tasks are independent per language: if subagents are available, translate in parallel batches of about five languages, each writing only its own JSON files, then merge and run task 5.

- [ ] 5. Build and check
  - Run `python3 scripts/build.py` to regenerate the 15 privacy pages.
  - Run `python3 scripts/check_i18n.py` (same keys, tags and tokens, no dashes), `python3 scripts/test_check.py`, `python3 scripts/test_build.py` (includes the new test and the fixture comparison) and `python3 scripts/build.py --check`. All must pass; fix the sources, never the generated pages.
  - Confirm with `git diff --stat` that only `i18n/strings/*.json`, `templates/privacy.html`, `scripts/test_build.py`, the fixture JSON, the 15 generated privacy pages and the spec files changed, and with `grep -rn "never leaves" royal-game-of-ur */royal-game-of-ur` that no English page still has the old sentence.

- [ ] 6. Look at it
  - Serve with `python3 -m http.server 8080 --bind 127.0.0.1 --directory .` and read the "What the app stores" and "Retention" sections of the English page and of `/ar/` (right to left) and `/ja/` (date format) in the browser. Report what was seen; if the page was not opened, say so.

- [ ] 7. Commit and pull request
  - Commit message in a file and `git commit -F` (sources, generated pages, tests, fixture and spec files in one commit). Rebase on `main` if it has moved.
  - Push with `git push origin feature/privacy-backup` (one literal command), open the pull request with `gh pr create --body-file`, titled "Privacy policy: say that backup can copy saved progress to Google or iCloud". The description lists the three owner follow-ups below and links the Android note `STORE/data-safety-backup-change.md`.
  - Do not merge. Wait for review, address comments, and leave the merge to the owner.

- [ ] 8. Owner follow-ups (stated in the pull request, not done here)
  - Confirm the iCloud sentence against the iOS app before merging (the Android note marks it inferred; if wrong, remove "or iCloud (iPhone and iPad)" and the "or Apple" clauses).
  - Merge before or with the Android release that enables backup (checklist item 15a).
  - Update the Android checklist's "13 files" note to 15 languages.
