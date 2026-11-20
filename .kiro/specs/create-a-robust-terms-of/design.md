# Design: Terms of Service page

## Approach in one paragraph

Add one more generated page, `terms`, to the existing static-site pipeline. It follows the Privacy and Age Suitability pages exactly: a template in `templates/`, an entry in `PAGES` in `scripts/build.py`, strings in `i18n/strings/<code>.json`, generated output committed. The sitemap, language menu, canonical and hreflang tags come for free from `PAGES`. No new dependency, no JavaScript, no CSS beyond what `styles.css` already has for `.doc`. The only genuinely new mechanism is two build-time constants for the publisher's legal identity.

Recorded decisions (from review): England and Wales law and courts with a consumer home-court exception; no arbitration and no class waiver; all fifteen languages, unreviewed, English prevails; lawyer review before the URL goes into a store.

## Files changed

| File | Change |
|---|---|
| `templates/terms.html` | New. Same shell as `privacy.html` (header, nav, `<article class="container doc">`, footer). |
| `scripts/build.py` | `PAGES["terms"] = ("terms.html", "royal-game-of-ur/terms/")`; constants `PUBLISHER_NAME`, `NOTICE_EMAIL`; two simple tokens `{{publisher}}` and `{{noticeemail}}`. |
| `scripts/check_i18n.py` | Add `publisher` and `noticeemail` to `SIMPLE_TOKENS` so strings may use them. |
| `i18n/strings/*.json` (15) | New `terms.*`, `meta.terms.title`, `meta.terms.description`, `nav.terms`, `footer.terms`, `privacy.terms.p`, `age.terms.p`. |
| `templates/privacy.html`, `support.html`, `age.html`, `index.html` | Footer link to Terms; nav link on privacy, support, age (and terms itself). |
| `templates/privacy.html`, `age.html` | One cross-reference paragraph each. |
| `scripts/test_build.py`, `scripts/test_check.py` | New tests (below); updated expected-additions lists. |
| `README.md`, `i18n/README.md` | Document the page, the identity constants and the first-review list. |
| Generated pages and `sitemap.xml` | Regenerated and committed with the sources. |

`templates/partials/head.html` needs no change: it already emits canonical, alternates and Open Graph from `{{t:meta.<page>.title}}`-style keys the template supplies.

## Publisher identity (the only new mechanism)

The terms must name the contracting party and say where notices go. The owner supplied (2026-11-20) the name **Lumoxia.Art** and the notices address `info@lumoxia.art`, and chose to publish no postal address (see requirements criterion 16 for the store and regulator risk). These are facts, not translations, so they live in `build.py` next to `PATREON_URL` and enter strings through tokens, never typed into a template or a language file:

```python
PUBLISHER_NAME = "Lumoxia.Art"
NOTICE_EMAIL = "info@lumoxia.art"
```

`render_page` adds `"publisher": html.escape(PUBLISHER_NAME)` and `"noticeemail": html.escape(NOTICE_EMAIL)` to `simple`. The `terms.publisher.p` string uses them: "These terms are offered by {{publisher}} (&ldquo;Lumoxia&rdquo;). Send notices and legal questions by email to {{noticeemail}}." The email is rendered as a `mailto:` link inside a `<bdi dir="ltr">`, as the footer does, so right-to-left pages display it correctly. Because tokens must match English in every language (`check_i18n.py` already enforces it), a translator cannot drop or alter them. Wherever the text says "Lumoxia" it is the short form defined there; "Lumoxia.Art" is written exactly so and is not translated.

Fail closed: `render_page` raises `BuildError` if either constant is empty. Switching to a postal address later is one added constant and one added token, with no change to the strings' structure; the design does not add that now.

## Page structure

Sections in order, each `h2` with one or more `p` and, where a list reads better, a `ul`. Keys are `terms.<section>.h`, `.p`, `.p1`, `.l1`... as on the Privacy page. Every `terms.*` key must appear on the page (the existing check that every `<page>.*` key is rendered is extended to `terms`).

| # | Section key | Covers (requirement criteria) |
|---|---|---|
| 0 | `terms.h1`, `terms.meta`, `terms.short` | Title, "Last updated", bold summary, English-prevails line (1, 3, 25) |
| 1 | `terms.agree` | Agreement, acceptance, relation to store terms (4) |
| 2 | `terms.licence` | Licence grant, "licensed not sold" (5) |
| 3 | `terms.use` | Prohibited acts, the ancient game stays free (6) |
| 4 | `terms.ip` | Ownership, third-party material, trademarks (7) |
| 5 | `terms.purchase` | The optional one-time unlock, store-handled payment and refunds, restore, free unlocks (8) |
| 6 | `terms.rights` | Rights that cannot be waived: UK CRA 2015, EU Directive 2019/770 and withdrawal, US state law (9) |
| 7 | `terms.warranty` | "As is", subject to statutory rights, conspicuous (10) |
| 8 | `terms.liability` | Cap and carve-outs (11) |
| 9 | `terms.links` | Third-party links and services (12) |
| 10 | `terms.privacy` | Pointer to the Privacy Policy (13) |
| 11 | `terms.updates` | App updates, no unilateral worsening for payers (14) |
| 12 | `terms.changes` | Changes to the terms, 30-day notice, not retroactive (15) |
| 13 | `terms.publisher` | Who the publisher is, notices address (16) |
| 14 | `terms.law` | England and Wales, consumer home-law and home-court exception (17) |
| 15 | `terms.disputes` | Email first, no arbitration, no ODR link (18) |
| 16 | `terms.general` | Severability, no waiver, entire agreement, assignment, third parties (19) |
| 17 | `terms.apple` | Apple's required terms as a list, one clause per `li` (20) |
| 18 | `terms.google` | Google Play paragraph (20) |
| 19 | `terms.export` | Sanctions and export, one sentence (21) |
| 20 | `terms.end` | Termination and survival (22) |
| 21 | `terms.age` | Family game, adult or parent-approved purchases (23) |
| 22 | `terms.contact` | `rgur-support@lumoxia.art`, same markup as Privacy's Contact |

Apple clauses are the list `terms.apple.l1` to `l8`, in the order of Apple's minimum terms: (1) agreement is with Lumoxia, not Apple; (2) scope of licence and the Media Services Terms; (3) maintenance and support; (4) warranty and the refund-from-Apple sentence; (5) product claims; (6) intellectual-property claims; (7) legal compliance and the embargo and restricted-party statement; (8) third-party terms and Apple as third-party beneficiary. Each clause is its own key so a test can assert each one is present in every language.

### Clause wording decisions (stated so they can be overruled)

- **Liability cap.** The amount the player paid Lumoxia through the store for the app in the previous twelve months; if nothing was paid, 10 pounds sterling or the equivalent in the player's currency.
- **Notice period for a material change.** 30 days.
- **Reply time to an email complaint.** 14 days, stated as a target ("aims to reply within 14 days"), not a guarantee, so it is not itself a breach risk.
- **Survival.** Sections on ownership, warranty, liability, governing law and general terms survive termination.
- **Unlock continuity (criterion 8, 14).** Phrased as a commitment to keep the unlock working for existing buyers on the platform stores as long as the app is distributed, and to tell players in advance of the app being withdrawn; no promise beyond that.
- **No arbitration words.** The page does not mention arbitration or class actions at all, even negatively, so there is nothing to misread. The English source test enforces this.
- **EU ODR.** The platform was retired in 2025, so there is no link and no mention.

### What each language shows

English is the source and prevails; the same `terms.short` and `terms.prevails` strings in every language state it, translated, and say the English text at `https://lumoxia.art/royal-game-of-ur/terms/` is the authoritative one. The legal-force clauses are translated closely, not paraphrased. `i18n/README.md` lists `terms.licence`, `terms.warranty`, `terms.liability`, `terms.law` and `terms.apple` as the first keys a native-speaking reviewer checks. Dates: `terms.meta` carries the date in each language's own format, the same way `privacy.meta` does.

## Links and navigation

- **Footer.** `templates/privacy.html`, `support.html` and `age.html` have one identical footer line (`Privacy · Support · Age suitability · email`); add `· Terms of Service` after Age suitability, with `footer.terms`. The home page footer (`templates/index.html`) has a separate link block (Patreon, Age suitability); add the Terms link beside Age suitability. `terms.html` carries the same footer.
- **Nav.** On privacy, support, age and terms, add `<a href="{{base}}royal-game-of-ur/terms/">{{t:nav.terms}}</a>` after Support, with `nav.terms` = "Terms". The home page nav uses on-page anchors and is not changed. The nav is a flex row already built for three links; the design checks four at the narrowest width in German, French, Russian and Tagalog (the long ones the i18n README names) and uses the short `nav.terms` label ("Terms", "Conditions", "Términos", "AGB", ...) to avoid wrapping.
- **Cross-references.** `privacy.terms.p` and `age.terms.p` are one-sentence paragraphs inserted before each page's Contact section: "The terms for using the app are on the Terms of Service page." with a link. They state no privacy or age fact, so their "Last updated" dates stay as they are.
- **Sitemap.** Driven by `PAGES`; the new page and its fifteen alternates appear automatically.
- **Language menu.** Driven by `PAGES`; works on the new page unchanged.
- **Privacy's Rules-panel sentence** (`privacy.links.p`) is not touched: the app's Rules panel does not link to the Terms.

## Enforceability design (how the page achieves "enforceable globally")

This section records why each clause is shaped the way it is, so the copy is not softened by a later edit.

1. **Consumer carve-outs are structural, not buried.** The disclaimer and the cap both begin "Subject to your statutory rights", and `terms.rights` is placed before them so a reader (and a court) sees the floor first. This is what keeps the clauses clear of the UK Consumer Rights Act 2015 Part 2 fairness test and the EU Unfair Contract Terms Directive 93/13/EEC.
2. **Mandatory carve-outs in the cap.** Death and personal injury by negligence, fraud, gross negligence and wilful misconduct, and anything non-excludable are carved out in words, because a cap that tries to cover them can be struck whole in England and is void for the covered parts in most EU states.
3. **Conspicuous.** The warranty disclaimer and the cap use `<strong>` for the operative sentence, which satisfies the "conspicuous" expectation of US courts without capital-letter blocks that are hard to read and to translate (right-to-left and CJK languages have no capitals).
4. **No forum overreach.** England and Wales law governs, but a consumer keeps their home country's mandatory protections and may sue at home (Brussels I Recast Article 18; UK Consumer Rights Act). That is the form that survives; a clause stripping it would be unenforceable against EU consumers.
5. **No arbitration or class waiver.** Void against UK and EU consumers and a frequent unconscionability target in US states; omitted entirely (Decision 2).
6. **Severability sentence in the general terms**, and a cap written as separate numbered limits so that striking one leaves the others (the "blue pencil" form English courts will apply).
7. **Plain, transparent text.** Fairness law requires transparency; short paragraphs and an upfront summary do real legal work as well as UX work.
8. **Store terms align.** The Apple clauses follow Apple's published minimum terms for a custom licence, so Apple does not substitute its standard EULA. The Google paragraph states only what Google's terms already provide.
9. **Withdrawal right.** Stated as the store's mechanism, with the loss-on-delivery wording the Digital Content Directive allows only where the consumer has consented, which the store collects at purchase. The page does not attempt to collect that consent itself.

None of this is legal advice; the final English text is for a lawyer before the store URL is set (Decision 4).

## Tests

Added to `scripts/test_build.py`, following the existing per-language patterns (`PRIVACY_DATES`, key-presence loops):

1. **Generated everywhere.** `royal-game-of-ur/terms/index.html` exists for all fifteen languages and is added to `test_expected_files`, `test_sitemap_lists_everything`, and the link-checking test that resolves every `href`.
2. **Footer and nav.** Every generated page's footer contains a link to its own language's Terms page; privacy, support, age and terms navs contain it.
3. **Every key rendered.** `terms.*` keys all appear in the generated page; the existing `<page>.*` check is extended with `terms`.
4. **Store clauses by key.** For every language, `terms.apple.l1` to `l8`, `terms.google` and `terms.export` appear on the page. In English the Apple list text contains "third-party beneficiar", "embargo" and "not Apple" so a copy edit cannot silently drop them.
5. **Identity.** The page contains `PUBLISHER_NAME` and `NOTICE_EMAIL` verbatim in every language; `build.render_page` raises `BuildError` when either is empty (tested with a patched empty value).
6. **Enforceability guards.** In English: no match for `arbitrat`, `class action`, `class-action`; `terms.rights` appears before `terms.warranty` and `terms.liability` in the page; the liability text contains the death and personal injury and fraud carve-outs.
7. **Dates.** `TERMS_DATES` per language (same format table as `PRIVACY_DATES`); `terms.meta` contains it. The test for old dates is not needed: this is a new page.
8. **Existing-page regression.** `test_english_text_unchanged` allows exactly the intended additions (the footer Terms link, nav Terms link, and the two cross-reference sentences) and nothing else on privacy, support and home; the age page is covered by its own checks. Privacy and Age "Last updated" dates stay as they are.
9. **`test_check.py`.** One test that `check_strings` accepts `{{publisher}}` and `{{noticeemail}}` in a string and rejects an unknown token.

CI already runs `test_check.py`, `check_i18n.py`, `build.py --check` and `test_build.py` on any change under `i18n/`, `templates/`, `scripts/`, `styles.css`, `assets/`, `*/index.html` and `royal-game-of-ur/**`; no workflow change is needed.

## Documentation

- `README.md`: add the Terms page to the layout list, and note that `PUBLISHER_NAME`/`NOTICE_EMAIL` live in `scripts/build.py` and that the Terms URL is the one entered in App Store Connect (License Agreement, Custom) and the Play listing, as the Age Suitability URL is.
- `i18n/README.md`: list the `terms.*` keys with `privacy.*`/`age.*`, name the two identity tokens (not translated), and add the first-review list above.

## Rollout order

1. Owner supplies the publisher name and notices email (done: Lumoxia.Art, info@lumoxia.art).
2. Author English strings and template; build; tests green on English.
3. Translate the other fourteen; `check_i18n.py` green.
4. Footer, nav and cross-reference changes; regenerate; full checks.
5. PR from a feature branch in the main repo; AI or human review; merge; Pages publishes on merge to `main`.
6. After lawyer review of the final English text, the owner enters the URL in App Store Connect and Play Console. Not part of this change.

## Risks and how the design handles them

| Risk | Handling |
|---|---|
| A store or regulator requires a postal address that the page omits | Recorded in requirements criterion 16; adding one later is one constant and one token. |
| A translator weakens a legal clause | Close-translation rule, English-prevails clause, first-review list, `unreviewed` flag, key-presence tests for store clauses. |
| Nav wraps at four links in long languages | Short `nav.terms` labels, checked in German, French, Russian and Tagalog at 320 px. |
| A later edit adds an arbitration or class-waiver clause | English-source test fails the build. |
| The app starts to collect data or adds chat, ads or accounts | Out of scope here, but `terms.updates` and the Age page already promise page updates before such a change ships; the README notes the Terms are revised with them. |
| Apple's minimum terms change | The eight Apple clauses are separate keys, so one clause can be updated in all languages with the usual same-keys rule. |
