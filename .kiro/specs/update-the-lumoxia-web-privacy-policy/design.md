# Design: Privacy policy says backup can copy saved progress off the device

Implements `requirements.md` (approved). Decisions fixed there: name both Google Account (Android) and iCloud (iPhone and iPad); update all 15 languages in one change, AI-drafted, `_review` left `unreviewed`.

## Approach

Content-only change in the existing generator pipeline. No new files, no new tokens, no JavaScript, no style changes.

```
i18n/strings/<15 files>.json  ->  scripts/build.py  ->  royal-game-of-ur/privacy/index.html + <lang>/royal-game-of-ur/privacy/index.html
templates/privacy.html            (one new <li>, one new <p>)
scripts/fixtures/english-before/iap-changes.json, scripts/test_build.py   (tests)
```

Never edit generated pages by hand; CI runs `build.py --check`.

## String changes (`i18n/strings/en.json`, then the 14 others)

Keys keep the same tags and tokens in every language (`check_i18n.py` enforces it; no em or en dashes). `{app:statsReset}` stays the app's own wording per language.

| Key | Change |
|---|---|
| `privacy.meta` | Date becomes 2 November 2026, in each language's own format and month name. Machine-translation notices already in tr, ru, he, pt stay. |
| `privacy.stores.p1` | "on your device only" becomes "on your device": "The app keeps a few things on your device, so the game remembers them next time:". Without this the intro contradicts the backup paragraph. |
| `privacy.stores.l3` (new) | "your progress: how many games you have finished, which boards and stone colours you have unlocked, and which festive boards you have." |
| `privacy.stores.p2` (rewritten) | "This information stays on your device and is never sent to Lumoxia. Lumoxia cannot see it, and the app itself sends it nowhere. If you use your phone's backup, your device may copy this information, and only this information, to your own Google Account (Android) or iCloud (iPhone and iPad), so that it comes back when you reinstall the app or move to a new phone. Google or Apple makes and keeps that copy under their own privacy policies, and Lumoxia cannot read it." |
| `privacy.stores.p3` (new) | "You can erase the statistics at any time with &ldquo;{app:statsReset}&rdquo; in the Stats panel. A backup you already made keeps the older copy until your next backup replaces it, and you can delete backups in your Google or Apple account settings. Deleting the app removes the information from the device." |
| `privacy.keep.p` | "Lumoxia holds no data about you, so there is nothing to keep, delete or hand over, and no consent to withdraw. What the app stores stays on your device, and in your own Google or Apple backup if you use one. Deleting the app removes it from the device; a backup you made stays in your account until you delete it there. Lumoxia shares no data with anyone. The record of a purchase is kept by Apple or Google, so ask them about it." |

Unchanged on purpose: `privacy.short`, `meta.privacy.description`, `privacy.not.*`, `privacy.iap.*`, `privacy.changes.p`, `privacy.site.p`, and the support page. Each still holds: Lumoxia collects, receives and shares nothing, and the app itself makes no request. The backup is made by the operating system, not the app. The paid unlock is not in the backup, and the copy does not say it is.

## Template (`templates/privacy.html`)

In "What the app stores on your device": add `<li>{{t:privacy.stores.l3}}</li>` after `l2`, and `<p>{{t:privacy.stores.p3}}</p>` after `p2`. Nothing else in the template changes. Right-to-left languages (ar, he) need no markup change: the new text is plain prose inside the existing `<p>` and `<li>`.

## Translation process

1. Edit English first; run `python3 scripts/build.py` to see the English page.
2. Draft the same six keys plus `privacy.meta` for fr, es, de, ar, zh, it, hi, tl, tr, ru, he, pt, ja, ko, reusing each language's existing wording for "your device", "backup", "Google Account", "iCloud", "reset statistics" and its existing date format. Use the app's own labels via `{app:...}` tokens only where English already does.
3. Names Google, Google Account and iCloud are not translated, as Apple and Google already are not.
4. `_review` stays `unreviewed` in every file. Whether native speakers should look at the new paragraph first is already covered by the "Review status" note in `i18n/README.md`; no README change is needed.

## Tests

`scripts/test_build.py` currently compares the English privacy page against `scripts/fixtures/english-before/privacy.html` after undoing the intended edits listed in `scripts/fixtures/english-before/iap-changes.json`. The new edits must be registered there or `test_english_text_unchanged` fails.

- `iap-changes.json` `changed`: add `privacy.stores.p1` and `privacy.stores.p2` with their pre-change English text (the old strings, exactly as in the fixture). `privacy.meta` is already listed there.
- `iap-changes.json` `added`: add `privacy.stores.l3` and `privacy.stores.p3`. `privacy.keep.p` is already in `added`, so its new text is covered by the same swap.
- New test `test_privacy_says_backup_can_copy_data` in `scripts/test_build.py`, for every language: the page contains the strings of `privacy.stores.l3`, `privacy.stores.p2`, `privacy.stores.p3` and `privacy.keep.p`; `privacy.meta` does not contain "25"; and for English the page text contains neither "never leaves your device" nor "removes everything". The existing `assertNotIn("21", ...)` stays.
- For non-English pages the old sentence cannot be searched in each language without holding the old translations, so the guarantee there is that `privacy.stores.p2` is a different, present string. The key-match checks of `check_i18n.py` ensure no language is missing it.

`check_i18n.py` and `test_check.py` need no change.

## Verification

```bash
python3 scripts/build.py
python3 scripts/check_i18n.py
python3 scripts/test_check.py
python3 scripts/test_build.py
python3 scripts/build.py --check
```

Then open `royal-game-of-ur/privacy/index.html` and one right-to-left page (`ar/`) through `python3 -m http.server 8080 --bind 127.0.0.1 --directory .` and read the "What the app stores" and "Retention" sections.

## Release and rollout

The branch is `feature/privacy-backup`. It is opened in the main repo, committed with sources and generated pages together, pushed, and a pull request is opened. Merge to `main` publishes through GitHub Pages. Per the Android checklist (item 15a), merge it before or with the Android release that enables backup. The iCloud sentence rests on the platform default and is not tested on a device; the owner confirms it against the iOS app before merging. The owner also updates the Android checklist's "13 files" note; it is not changed here.

## Risks

- **iCloud claim unverified.** Mitigation: called out in the pull request description; one clause to remove if the iOS app turns out not to be backed up.
- **Machine-drafted legal text in 14 languages.** Mitigation: English is authoritative (tr, ru, he, pt already say so in their date line); all are marked `unreviewed`.
- **Fixture test drift.** Mitigation: the fixture edits above; `test_build.py` fails loudly if any listed key is missing from the page.
