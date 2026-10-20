# Translations

The site is available in thirteen languages: the nine of the app *The Royal Game of Ur*, in the app's order, then four
the site added first:
English, Français, Español, Deutsch, العربية, 中文, Italiano, हिन्दी, Tagalog, Türkçe, Русский, עברית, Português.

The app's `LocaleInfo.all` in `ios/UrCore/Sources/UrCore/Localisation/Localisation.swift` in the app repository defines
the first nine. The site is ahead of the app for Turkish, Russian, Hebrew and Portuguese, so the app-repo comparison below
reports those four as missing from the app until the app ships them, and `sync_app_terms.py` cannot refresh their entries in
`app-terms.json` (they are drafted by hand). The app repository is private, so CI cannot read it. On your own machine:

```bash
python3 scripts/check_i18n.py --app-repo ../royalgameofurl_mobile_app
```

## Files

| File | What it is |
|---|---|
| `languages.json` | The thirteen languages: code, `lang` tag, native name, short label, direction, font set |
| `strings/<code>.json` | Every translatable string for one language. `en.json` is the source. Keys starting with `_` are notes |
| `app-terms.json` | The app's own wording (name, Single Player, 2 Players, Stats, ...) per language |
| `../templates/` | The page templates |

The generated pages (`/`, `/fr/`, `/ar/`, ...) are committed. Do not edit them by hand.

## Changing a string

1. Edit the key in `strings/en.json` and in the other twelve files (keys must match everywhere).
2. Run `python3 scripts/build.py`.
3. Run `python3 scripts/check_i18n.py` and `python3 scripts/test_build.py`.
4. Commit the strings and the generated pages together.

Strings may contain a few inline tags (`<a href>`, `<strong>`, `<small>`, `<bdi>`) and the tokens `{{base}}` (path to the
language's root) and `{app:key}` (the app's own wording from `app-terms.json`). Tags and tokens must match English.
Em dashes and en dashes are not allowed.

To refresh `app-terms.json` after the app's strings change:
`python3 scripts/sync_app_terms.py --app-repo ../royalgameofurl_mobile_app`.

## Review status

The translations were drafted with AI assistance and have **not** been reviewed by native speakers. Each file records this
in its `_review` key (`unreviewed`). When a native speaker has checked a language, change it to
`reviewed by <name>, <date>`.

Things a reviewer should look at first: the wording the app does not define (the gear icon and book icon descriptions,
"board button", "Apps" in the iOS Settings path, the "This website" paragraph on the Privacy page, the month name in the
"Last updated" date), and whether text fits the buttons and cards (German, French, Russian and Tagalog run long).

To submit a correction, edit the string file and run the steps above, or open an issue naming the language and key.

Portuguese is written to read naturally in both Brazil and Portugal, so a reviewer from either country should check it.
Where the two differ (the iOS Settings app is Ajustes in Brazil and Definições in Portugal), both are named or a shared
word is used; see its `_review` key. Hebrew uses plural or neutral phrasing where it can and masculine imperatives for
buttons. The "Nine languages" line on the home page describes the app, which does not yet include the four new languages.

## Store attribution

`footer.trademarks` (Apple and Google trademark lines) is kept in English in every language on purpose. The App Store and Google Play badges live in `assets/badges/` and are not shown yet; see `assets/badges/README.md` for how to add them once the listings exist.
