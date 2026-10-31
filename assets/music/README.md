# Streaming logos

Official logos and badges for the streaming services that carry the album *Bronze and Hide*. They are shown in the
Music section of the home page (see `MUSIC_SERVICES` in `scripts/build.py`). A service is listed on the site only when
its official file is in this folder.

Rules to keep for every file: do not redraw, recolour, crop, stretch, rotate or add effects. Keep each vendor's clear
space on every side. Fetch updates from the vendor, never edit a file.

| File | Service | Source (fetched 2026-10-31) | Variant and rules that apply |
|---|---|---|---|
| `apple-music/<code>.svg` | Apple Music | Apple Marketing Toolbox, album page, "Badges and Lockups", `https://toolbox.marketingtools.apple.com/api/v2/badges/listen-on-apple-music/badge/<locale>/download`, file `standard-white.svg` | "Listen on Apple Music" standard badge with white text, for dark backgrounds. Localised: en-us, fr-fr, es-es, de-de, zh-cn, it-it, tl-ph, tr-tr, ru-ru, he-il, pt-br, ja-jp, ko-kr. Apple has no badge for Arabic or Hindi, so those pages use the English one. At least 30 px high; clear space one tenth of the badge height; one Apple badge only, placed first when other music badges appear; never translate "Apple Music"; credit line in the footer. |
| `spotify.svg` | Spotify | `https://developer.spotify.com/images/guidelines/design/2024-spotify-full-logo.zip`, file `Full_Logo_White_RGB.svg` | Full logo (icon and wordmark) in white, the monochrome version for dark backgrounds. At least 70 px wide; clear space half the icon height. Spotify's design page says not to use its brand together with other brands. That sentence sits in its developer branding rules, which are written for apps on the Spotify Platform. This site uses no Spotify API, metadata or artwork, so it is read as not applying to a plain link. If Spotify objects, remove the entry from `MUSIC_SERVICES` and delete the file. |
| `youtube.png` | YouTube | `https://brand.youtube/youtube-logo`, zip `youtube-logo.zip`, file `Digital/01 Full Color/yt_logo_fullcolor_white_digital.png` | Full-colour logo with white text, for dark backgrounds. YouTube supplies PNG only. Height at least 100 px on screen, so it has its own row at 100 px; clear space is defined by the triangle in the icon, and 32 px is kept. The triangle must stay white; never outline, recolour, add shadows, rotate, skew or stretch. |
| `amazon-music.png` | Amazon Music | Supplied by Giorgio Orsi on 2026-10-31 from Amazon's official "AM Logos" folder (linked from `https://artists.amazonmusic.com/brand-guidelines`); file `Amazon_Music_Logo_Horizontal_RGB_White_Music_Cyan_MASTER.png` | "Dark background" horizontal lockup (white "amazon", cyan "music"), the primary logo. Clear space is the x-height of "music"; the 16 px padding is larger. The minimum size is only in a figure on Amazon's page that could not be read, so 32 px high is not confirmed against it. Amazon's page asks for no credit line. |
| `deezer.png` | Deezer | Supplied by Giorgio Orsi on 2026-10-31 from Deezer's brand site (`https://deezerbrand.com/document/88`, which needs a sign-in); file `Logo_Vertical.png` | Vertical lockup (heart and white wordmark), Deezer's default lockup, in colour with a white wordmark for dark backgrounds. Shown 56 px high so the wordmark stays legible. Deezer's clear space and minimum size are in figures on its page that could not be read, so neither is confirmed; 16 px of padding is kept. Deezer's page asks for no credit line. |
| `tidal.png` | Tidal | Supplied by Giorgio Orsi on 2026-10-31 from Tidal's brand material; file `tidal_logo.png`; rules from `https://developer.tidal.com/documentation/guidelines/guidelines-design-guidelines` (v3.0, May 2024) | Full horizontal logo (diamond and wordmark), white on black as Tidal requires; the black is part of the file. The file has its own margin, so it is shown 92 px high, which makes the logo itself about 32 px high. Clear space is twice the logo height (64 px) and it has its own row. Tidal's minimum height is only in a figure on its page that could not be read, so it is not confirmed. Tidal's "do not display TIDAL content next to content from similar services" sits in its API content rules (metadata, artwork, playback), which this site does not use, so it is read as not applying to a plain link. |

## Provenance of the three supplied files

Amazon Music, Deezer and Tidal files were handed over by Giorgio Orsi on 2026-10-31, not fetched by the build agent, and
have **not yet been compared** with the vendors' current files. Whoever merges this should compare each and record the
result here.

| File | Vendor page the file and rules come from | Compared with the vendor's current file |
|---|---|---|
| `amazon-music.png` | `https://artists.amazonmusic.com/brand-guidelines` ("AM Logos" Box folder) | not yet |
| `deezer.png` | `https://deezerbrand.com/document/88#/-/logo-1` (sign-in needed) | not yet |
| `tidal.png` | rules: `https://developer.tidal.com/documentation/guidelines/guidelines-design-guidelines`; the page the file itself was downloaded from was not stated | not yet |

## If a vendor objects

Spotify's and Tidal's developer or API rules about using their brand beside other brands or services are read as not
applying to a plain link, because this site uses no Spotify or Tidal API, metadata or artwork. If either vendor (or any
other) objects, delete its entry from `MUSIC_SERVICES` in `scripts/build.py`, delete its file here, and rebuild.

## Narrow screens

At 420 px wide or less, the YouTube row drops its side padding so the 100 px-high logo (about 297 px wide) fits the page.
Its minimum height is kept; the page edge is the only thing near it. Tidal instead scales its logo down with the screen
and keeps its clear space at twice the logo height.
