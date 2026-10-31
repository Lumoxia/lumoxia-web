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

## Not shown yet

| Service | Album link | Why it is held back |
|---|---|---|
| Amazon Music | `https://music.amazon.co.uk/albums/B0HPHDCLP1` | The official logos are on a public Box folder ("AM Logos") whose download did not run from automation. Use "Dark background, horizontal". |
| Deezer | `https://www.deezer.com/en/album/1132172601` | The logo downloads on deezerbrand.com need a sign-in. |
| Tidal | `https://tidal.com/album/573680338` | Tidal's design page links no logo file. Its rules: white logo on black, clear space twice the logo's height, so it needs its own row. Its minimum height is only in a figure on the page. Tidal's "do not display TIDAL content next to similar services" sits in its API content rules, which this site does not use. |
