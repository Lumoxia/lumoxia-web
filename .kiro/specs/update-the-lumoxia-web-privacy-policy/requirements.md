# Requirements: Privacy policy must say that backup can copy saved progress off the device

## Goal

The English Privacy page (https://lumoxia.art/royal-game-of-ur/privacy/) says in "What the app stores on your device": "This information never leaves your device." On Android that is no longer true. The Android app now sets `allowBackup="true"` and Android Auto Backup (and device-to-device transfer) can copy the app's one saved-data file to the user's own Google Account. The page must say so, plainly, before the Android release that enables backup ships (the policy's own "Changes to this policy" section promises this, and the Android release checklist item 15a treats it as a release blocker).

What does not change: the app still sends nothing itself, declares no internet permission, and Lumoxia still receives and can read nothing. The policy must stay true on both counts. The Play Data safety answers stay "No" and are out of scope.

Use the existing pipeline: edit `i18n/strings/*.json` (and `templates/privacy.html` only if a section must be added), run `python3 scripts/build.py`, commit sources and generated pages together. Do not edit generated pages by hand.

## Facts the copy must be consistent with

Source: `STORE/data-safety-backup-change.md` in the Android repo (`royalgameofur_android_app`), written 2026-11-01.

- The backed-up file holds settings, statistics, the finished-games counter, unlocked boards and colours, and the festive-boards record.
- The cached "owned" hint of the paid unlock is NOT in the backup. The purchase itself is held by Google Play or the App Store, as the page already says.
- The copy is made and kept by Google (Android) under Google's privacy policy. Lumoxia cannot read it. The app itself transmits nothing.
- Erasing statistics in the app does not erase a backup already made; that copy is replaced by the next backup, and the user can delete backups in their Google account settings.

## Acceptance criteria

1. **The false sentence is gone.** No language version of the Privacy page says that the saved information "never leaves your device". The replacement says: it stays on the device and is never sent to Lumoxia; Lumoxia cannot see it; the app itself sends it nowhere; if the user uses their phone's backup, the device may copy it, and only it, to the user's own account (Google Account on Android) so it comes back after a reinstall or on a new phone; that copy is made and kept by Google under its own privacy policy and Lumoxia cannot read it.
2. **Progress is named.** The "what the app stores" bullet list gains a third item: progress (how many games the user has finished, which boards and stone colours are unlocked, which festive boards they have), so the page lists everything the backup contains.
3. **Deleting and erasing are accurate.** The paragraph says that "Reset all statistics" erases the statistics on the device, that an existing backup keeps the older copy until the next backup replaces it, and that backups can be deleted in the Google account settings. "Deleting the app removes everything" is narrowed to "removes it from the device".
4. **Retention section matches.** "Retention, deletion and sharing" no longer says what the app stores "stays on your device" without qualification. It says it stays on the device and in the user's own backup if they use one, and that a backup stays in the user's account until they delete it there. "Lumoxia holds no data about you" and "shares no data with anyone" stay, because they remain true.
5. **Purchase note unchanged.** The unlock record stays with Apple or Google; the policy does not claim the purchase is in the backup.
6. **Still-true claims stay.** "Does not collect any data about you", "the game itself sends nothing to the internet or to any server of ours" and the meta description stay as they are. No wording suggests Lumoxia collects, receives or shares backup data.
7. **Date.** `privacy.meta` "Last updated" changes from 25 October 2026 to 2 November 2026 in all 15 languages (the date written in each language's own format, month name included). The existing test that rejects the old date pattern is updated to reject "25" for the new wording.
8. **All 15 languages change together.** The same keys change in `i18n/strings/en.json` and the other 14 files (same keys, tags and tokens; no em or en dashes; `_review` left as `unreviewed`; translations drafted with AI assistance as before). The 13 generated-file count in the Android checklist is out of date; the site has 15 languages and the Android checklist note is updated by the owner, not here.
9. **Build and checks pass.** `python3 scripts/build.py` has been run and the generated pages (`/royal-game-of-ur/privacy/`, `/fr/...` to `/ko/...`) are committed with the sources. `python3 scripts/check_i18n.py`, `python3 scripts/test_build.py` and `python3 scripts/test_check.py` pass, and the CI check "committed pages equal generated pages" is green.
10. **Tests guard the claim.** `scripts/test_build.py` gains a check, for every language, that the privacy page mentions the backup paragraph key and that no page still contains the old "never leaves" sentence (checked through the old English string and through the new key being present in each language).
11. **Tone.** Plain, direct, solo-studio voice, no "we", no legal filler, no personal name.

## Decisions

1. **iOS and iCloud (recommended: name iCloud too).** The page serves both apps (`privacy.meta` says "for iOS and Android"). On iOS the same settings travel in the platform's default iCloud and device backups, so "never leaves your device" is equally imprecise there. Recommended: one sentence covering both, "your own Google Account (Android) or iCloud (iPhone and iPad)", as the Android repo's suggested wording does. Risk: the Android repo marks the iCloud claim as INFERRED (platform default, not tested on a device), so the owner confirms it against the iOS app before publishing. Alternative: say only "your own Google Account on Android" and leave iOS silent, which keeps the page narrowly true but leaves the iOS wording imprecise.
2. **Translations (recommended: update all 14 now, marked unreviewed).** Keys must match across the 15 files and CI enforces it, so partial updates are not possible. The new sentences are drafted with AI assistance like the rest of the site and flagged `unreviewed`. Alternative: none, since the build and key-match check forbid English-only changes.
3. **Wording of the "Retention" and "stores" paragraphs (decided by the Android spec, reused here).** Use the suggested replacements in `STORE/data-safety-backup-change.md`, edited to the exact wording of the acceptance criteria above.

## Out of scope

- Play Console Data safety answers (stay "No").
- Android store listing text and the Android checklist edits.
- Any change to what the app does, to `support` or the home page, or to `privacy.site.p` (this website's own language-remember note).
- Native-speaker review of translations.
