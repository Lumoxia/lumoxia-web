# lumoxia-web

The public marketing website for **Lumoxia**, a small indie studio that rebuilds
ancient games as apps. Makers of *The Royal Game of Ur*.

Live site: **[lumoxia.art](https://lumoxia.art)** (served via GitHub Pages).

## Stack

A dependency-free static site: HTML, CSS and a little inline SVG and JavaScript.
Nothing to build.

```
index.html      # single-page landing site
styles.css      # Mesopotamian-inspired theme (the colours of the Lumoxia board: brown, sand and gold)
assets/
  logo.svg      # full horizontal wordmark + emblem
  mark.svg      # square emblem (favicon / OG / avatar)
CNAME           # custom domain for GitHub Pages
.nojekyll       # serve files as-is, skip Jekyll processing
```

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
