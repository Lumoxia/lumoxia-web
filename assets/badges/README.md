# Store badges

Stored for later. They are not shown on any page yet, because neither app has a store listing to link to. Both
vendors only allow their badge to link to a live listing of the app.

| File | Source |
|---|---|
| `app-store.svg` | Apple "Download on the App Store" badge, black, US-UK, from Apple's [Marketing Resources](https://tools.applemediaservices.com/) |
| `google-play.png` | Google "Get it on Google Play" badge, English, from [Google Play badges](https://play.google.com/intl/en_us/badges/) (Google distributes this badge as PNG) |

Rules to keep: do not redraw, recolour, crop or add effects. Keep Apple's clear space (one quarter of the badge height)
and Google's clear space (the badge's own transparent margin) on every side. Apple's minimum height is 40 px for the
SVG at its native size; show the Google badge at no less than 40 px of visible height. Use the localised badge for the
language of the page when each vendor offers one.

To show them: add each badge as an `<a href="<listing URL>"><img ...></a>` next to the "Coming soon" pill, or in its
place once that store has the app. The trademark lines are already in the footer (`footer.trademarks`).
