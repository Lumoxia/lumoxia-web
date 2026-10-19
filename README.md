# lumoxia-web

The public marketing website for **Lumoxia**, a small indie studio that rebuilds
ancient games as apps. Makers of *The Royal Game of Ur*.

Live site: **[lumoxia.art](https://lumoxia.art)** (served via GitHub Pages).

## Stack

A dependency-free static site: HTML, CSS and a little inline SVG and JavaScript. It is available in nine languages
(the same ones as the app). Each language is a pre-generated page committed to the repository, so the deployed site
needs no build step. The pages are generated from templates and translation files by a small Python script.

```
index.html      # generated: landing page (English). Other languages: fr/ es/ de/ ar/ zh/ it/ hi/ tl/
royal-game-of-ur/  # generated: Privacy and Support pages (English)
templates/      # page templates the pages are generated from
i18n/           # languages.json, strings/<code>.json, app-terms.json (see i18n/README.md)
scripts/        # build.py (generator), check_i18n.py, tests
styles.css      # Mesopotamian-inspired theme (the colours of the Lumoxia board: brown, sand and gold)
assets/
  logo.svg      # full horizontal wordmark + emblem
  mark.svg      # square emblem (favicon / OG / avatar)
  lang.js       # language menu behaviour
  lang-detect.js # first-visit language choice, inlined into the English pages
CNAME           # custom domain for GitHub Pages
.nojekyll       # serve files as-is, skip Jekyll processing
```

## Editing the site

Do not edit the generated pages by hand. Change a template (`templates/`) or a string (`i18n/strings/*.json`), then:

```bash
python3 scripts/build.py          # regenerate the pages
python3 scripts/check_i18n.py     # translations: same keys, tags and tokens everywhere, no em or en dashes
python3 scripts/test_build.py     # generated pages, links, language menu
```

Commit the sources and the generated pages together. CI (`.github/workflows/check.yml`) fails a pull request if the
committed pages differ from what the generator produces. Python 3 is the only requirement.

## Local preview

```bash
python3 -m http.server 8080 --bind 127.0.0.1 --directory .
# then open http://127.0.0.1:8080
```

## Deployment

GitHub Pages is configured to build from the `main` branch (root).
The `CNAME` file binds the site to `lumoxia.art`.

### DNS (configure at the registrar for lumoxia.art)

Apex domain `lumoxia.art` → GitHub Pages A/AAAA records:

```
A     185.199.108.153
A     185.199.109.153
A     185.199.110.153
A     185.199.111.153
AAAA  2606:50c0:8000::153
AAAA  2606:50c0:8001::153
AAAA  2606:50c0:8002::153
AAAA  2606:50c0:8003::153
```

(Optionally add `CNAME www → lumoxia.github.io.` and let GitHub redirect `www`.)

## License

© Lumoxia. All rights reserved.

## Publishing

Every push to `main`, including a merged pull request, publishes the site through `.github/workflows/pages.yml`.
There is nothing to tag or release. The workflow can also be run by hand from the Actions tab. In the repository
settings, Pages must use "GitHub Actions" as its source; the custom domain `lumoxia.art` is kept by the `CNAME` file.
