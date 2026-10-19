"""Checks for the website translations. Standard library only.

    python3 scripts/check_i18n.py                       # CI checks
    python3 scripts/check_i18n.py --app-repo <path>     # also compare languages.json with the app's LocaleInfo.all
"""
import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PINNED_CODES = ["en", "fr", "es", "de", "ar", "zh", "it", "hi", "tl", "tr", "ru", "he", "pt"]
DASHES = ("—", "–")
SIMPLE_TOKENS = {"base", "root", "lang", "dir", "htmllang", "canonical", "alternates", "langmenu", "fonts",
                 "detect", "fsclass", "oglocale", "path"}
TAG_RE = re.compile(r"<\s*(/?)\s*([a-zA-Z][a-zA-Z0-9]*)([^>]*)>")
HREF_RE = re.compile(r'href\s*=\s*"([^"]*)"')
TOKEN_RE = re.compile(r"\{\{[^}]+\}\}|\{app:[A-Za-z0-9]+\}")
TEMPLATE_TOKEN_RE = re.compile(r"\{\{([a-z]+)(?::([^}]*))?\}\}")


def tags_of(value):
    out = []
    for m in TAG_RE.finditer(value):
        href = HREF_RE.search(m.group(3))
        out.append((m.group(1), m.group(2).lower(), href.group(1) if href else None))
    return out


def tokens_of(value):
    return sorted(TOKEN_RE.findall(value))


def check_strings(strings):
    """strings: {code: {key: value}} with 'en' as the source. Returns a list of error messages."""
    errors = []
    en = {k: v for k, v in strings["en"].items() if not k.startswith("_")}
    for code, table in strings.items():
        keys = {k: v for k, v in table.items() if not k.startswith("_")}
        for k in en:
            if k not in keys:
                errors.append(f"{code}: missing key {k}")
        for k in keys:
            if k not in en:
                errors.append(f"{code}: extra key {k}")
        for k, v in keys.items():
            if not isinstance(v, str) or not v.strip():
                errors.append(f"{code}: empty value for {k}")
                continue
            if any(d in v for d in DASHES):
                errors.append(f"{code}: {k} contains an em or en dash")
            if code != "en" and k in en:
                if tags_of(v) != tags_of(en[k]):
                    errors.append(f"{code}: {k} has different inline tags or links from English")
                if tokens_of(v) != tokens_of(en[k]):
                    errors.append(f"{code}: {k} has different tokens from English")
    return errors


def check_languages(languages, string_codes, pinned=PINNED_CODES):
    errors = []
    codes = [l["code"] for l in languages]
    if codes != list(pinned):
        errors.append(f"languages.json codes {codes} differ from the pinned languages {list(pinned)}")
    if sorted(string_codes) != sorted(codes):
        errors.append(f"i18n/strings files {sorted(string_codes)} do not match languages.json {sorted(codes)}")
    return errors


def check_templates(templates, keys):
    errors = []
    for name, text in templates.items():
        if any(d in text for d in DASHES):
            errors.append(f"template {name} contains an em or en dash")
        for m in TEMPLATE_TOKEN_RE.finditer(text):
            kind, arg = m.group(1), m.group(2)
            if kind in ("t", "attr", "url"):
                if arg not in keys:
                    errors.append(f"template {name} uses unknown key {arg}")
            elif kind == "include":
                continue
            elif kind not in SIMPLE_TOKENS or arg is not None:
                errors.append(f"template {name} uses unknown token {m.group(0)}")
    return errors


def parse_app_locales(swift):
    pat = re.compile(r'LocaleInfo\(code:\s*"([^"]+)",\s*label:\s*"([^"]+)",\s*short:\s*"([^"]+)",\s*direction:\s*\.(ltr|rtl)\)')
    return [{"code": a, "label": b, "short": c, "dir": d} for a, b, c, d in pat.findall(swift)]


def check_against_app(languages, swift):
    errors = []
    app = parse_app_locales(swift)
    if not app:
        return ["could not find any LocaleInfo entries in the app source"]
    mine = [{k: l[k] for k in ("code", "label", "short", "dir")} for l in languages]
    if app != mine:
        errors.append(f"languages.json differs from the app's LocaleInfo.all:\n  app:  {app}\n  site: {mine}")
    return errors


def load_all(root=ROOT):
    languages = json.loads((root / "i18n/languages.json").read_text("utf-8"))
    strings = {}
    for p in sorted((root / "i18n/strings").glob("*.json")):
        strings[p.stem] = json.loads(p.read_text("utf-8"))
    templates = {}
    for p in sorted((root / "templates").rglob("*.html")):
        templates[str(p.relative_to(root / "templates"))] = p.read_text("utf-8")
    return languages, strings, templates


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--app-repo")
    args = ap.parse_args(argv)
    languages, strings, templates = load_all()
    errors = check_languages(languages, list(strings))
    if "en" in strings:
        errors += check_strings(strings)
        errors += check_templates(templates, {k for k in strings["en"] if not k.startswith("_")})
    else:
        errors.append("i18n/strings/en.json is missing")
    if args.app_repo:
        swift = Path(args.app_repo) / "ios/UrCore/Sources/UrCore/Localisation/Localisation.swift"
        errors += check_against_app(languages, swift.read_text("utf-8"))
    for e in errors:
        print("ERROR:", e)
    print("i18n checks:", "FAILED" if errors else "ok")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
