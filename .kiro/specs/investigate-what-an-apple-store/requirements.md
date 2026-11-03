# Requirements: Age Suitability page for The Royal Game of Ur

## Background: what an Apple "Age Suitability URL" is

The Age Suitability URL is an **optional** field in App Store Connect, in the Age Ratings dialog (App Information, Age Rating), next to the calculated rating and the "override to a higher age rating" options. It was introduced alongside Apple's updated age rating system (new tiers 4+, 9+, 13+, 16+, 18+, announced at WWDC25; the field is described in Apple's December 2025 developer news "New Requirements for Social Media Apps in Australia").

What Apple says about it:

- The developer may link to "a developer-hosted website with details about the app and its age-related content".
- "When enabled, this URL appears on the App Store product page under the age ratings details section."
- Apple's suggested use is region-specific information and requirements, for example Australia's prohibition on under-16s holding a social media account.
- The field is only for apps that have a dedicated page with age suitability details. Leaving it empty has no effect on the rating.

What Apple does **not** specify: any required or typical content, a length or format limit, whether the URL must be localised, or whether it may differ per region. The sources read do not say. So "typical contents" below is a convention drawn from Apple's wording and from what the Royal Game of Ur app actually does, not an Apple template. Whether the live App Store Connect form accepts one URL only, and whether the page must be HTTPS and publicly reachable, is to be checked on the live form at submission time (the privacy page already satisfies both).

Sources: [Set an app age rating (Apple)](https://developer.apple.com/help/app-store-connect/manage-app-information/set-an-app-age-rating), [New Requirements for Social Media Apps in Australia (Apple)](https://developer.apple.com/news/?id=y1bckxf8), [Age ratings values and definitions (Apple)](https://developer.apple.com/help/app-store-connect/reference/app-information/age-ratings-values-and-definitions).

## Goal

Add one more page to the Lumoxia website, specific to The Royal Game of Ur, that can be entered as the Age Suitability URL in App Store Connect. It is built, translated and tested exactly like the existing Privacy and Support pages.

## User stories and acceptance criteria

### 1. A parent or player can learn whether the app suits a child

As a parent arriving from the App Store product page, I want a plain explanation of what is and is not in the game, so I can judge whether it suits my child.

Acceptance criteria:

1. The page is served at `/royal-game-of-ur/age-suitability/` (English) and `/<code>/royal-game-of-ur/age-suitability/` for each of the other 14 site languages.
2. It opens with a one-paragraph summary (bold, like the Privacy page's "In short"): the game is a two-player abstract dice and strategy board game with no violence, no chat, no accounts, no ads and no tracking.
3. A section "What is in the game" states the content facts that drive an age rating, each as a short statement a reader can verify:
   - no violence or realistic or cartoon fighting: stones race along a board and can send an opposing stone back to the start;
   - no gambling and no simulated gambling: dice decide moves but nothing is wagered and nothing can be won or lost of real or virtual value;
   - no profanity, sexual or mature content, drug, alcohol or tobacco references, and no horror or fear content;
   - the app contains no user-generated content, and no messaging, chat or other contact between players;
   - one-device two-player play and play against the computer only; no online multiplayer;
   - no location, contacts, photos, camera or microphone access.
4. A section "Purchases and links" states: one optional one-time in-app purchase that opens every board and stone colour, handled by Apple, with Apple's own parental controls (Ask to Buy, Screen Time) deciding whether a child can buy; the Rules panel opens a few web links in the browser (Lumoxia pages, a history video, sound-tool credits) and that sets of links lead to sites Lumoxia does not control.
5. A section "Privacy for children" states in one or two sentences that the app collects no personal information from anyone, and links to the Privacy page for the full policy.
6. A section "Region-specific rules" states that the app is not a social media app and has no accounts, so age-based social media restrictions (for example Australia's under-16 rule) do not apply to it. It uses a short, factual sentence; it does not give legal advice.
7. A section "Questions" gives the support address `rgur-support@lumoxia.art` (same mailto as the other pages, with a subject specific to age suitability) and a link to the Support page.
8. The page states a "Last updated" date in the same `doc-meta` style as the other pages.

### 2. The page matches the rest of the site

As the site owner, I want the new page to look and behave like the Privacy and Support pages so that nothing is special-cased.

Acceptance criteria:

1. It is generated from a new template in `templates/` and strings in `i18n/strings/<code>.json`, through `scripts/build.py`; the generated pages are committed; no page is edited by hand.
2. It uses the same header, language menu, footer, `doc` article styling, fonts per language, RTL handling (Arabic, Hebrew), `canonical` and `hreflang` alternates (including `x-default`) as the Support page.
3. All 15 languages exist, with identical keys, tags and tokens, no em or en dashes, and the `_review` note set to `unreviewed`, exactly as for the other pages (`scripts/check_i18n.py` passes). The app's own wording (name, Single Player, 2 Players and so on) comes from `i18n/app-terms.json` through `{app:key}` tokens, not typed text.
4. The new URLs are in `sitemap.xml` with their alternates in the same way as the Privacy and Support pages, and `robots.txt` does not block them.
5. `scripts/test_build.py` covers the new page (generated for every language, links resolve, language menu present, metadata and canonical correct, content facts from criterion 1.3 present in every language), and CI's "generated pages are up to date" check passes.
6. The README and `i18n/README.md` mention the new page where they list the pages.

### 3. The page is reachable from the site, and can be used in App Store Connect

Acceptance criteria:

1. Each language's Privacy and Support pages and the landing page footer link to the new page, using a footer link labelled "Age suitability" (translated). Whether it also joins the top navigation is a decision recorded below.
2. The English URL `https://lumoxia.art/royal-game-of-ur/age-suitability/` is the value to paste into the Age Suitability URL field. The final summary of the build gives this URL and says in which App Store Connect screen it goes.
3. The page is public and does not require JavaScript, cookies or sign-in to read.

### 4. The page never contradicts the app, the Privacy page or the store listing

Acceptance criteria:

1. Every factual claim on the page is checked against the Privacy page and the app's behaviour as documented in this repository; where they overlap (no data, one optional purchase, browser links, children) the wording is consistent.
2. The page does not promise anything the app cannot guarantee (for example it does not claim to be "safe for all children"; it describes content and leaves the judgement to the reader).
3. If the app later adds anything that changes these facts (online play, chat, ads), this page is updated before the change ships; the page says so in a "Changes" sentence like the Privacy page's.

## Out of scope

- Filling in the App Store Connect age rating questionnaire, or choosing the rating (tracked separately as the age-rating issue in the iOS repository).
- Google Play content rating (IARC) and any Google Play equivalent of this URL.
- Native-speaker review of the translations (they stay `unreviewed` like the existing pages).
- Changes to the app itself.

## Decisions to confirm

| # | Question | Recommended |
|---|---|---|
| D1 | Should the page state the rating tier (for example "4+")? | No. Describe the content only; the tier is calculated by Apple from the questionnaire, may be re-computed by Apple when the system changes, and a number on our page could drift from the store page. |
| D2 | Should "Age suitability" also join the top navigation next to Privacy and Support? | No. Footer links only; the top navigation stays as it is, since this is a store-compliance page rather than something players look for. |
| D3 | Include the "Region-specific rules" section (criterion 1.6)? | Yes, short and factual, because it is the use case Apple names for the field. |
