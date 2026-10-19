"""Refresh i18n/app-terms.json from the app's Localizable.xcstrings (run on the owner's machine only).

    python3 scripts/sync_app_terms.py --app-repo ../royalgameofurl_mobile_app
"""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KEYS = ["title", "modeShortHvc", "modeShortHvh", "statsLabel", "statsReset", "rules", "settingsLabel",
        "soundLabel", "shakeLabel", "langLabel"]
APP_CODE = {"tl": "fil"}  # Xcode stores Tagalog as fil


def extract(catalogue, codes):
    strings = catalogue["strings"]
    out = {}
    for code in codes:
        app = APP_CODE.get(code, code)
        table = {}
        for key in KEYS:
            try:
                table[key] = strings[key]["localizations"][app]["stringUnit"]["value"]
            except KeyError:
                raise SystemExit(f"app catalogue has no {key} for {app}")
        out[code] = table
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--app-repo", required=True)
    args = ap.parse_args()
    cat = json.loads((Path(args.app_repo) / "ios/UrGame/Localisation/Localizable.xcstrings").read_text("utf-8"))
    codes = [l["code"] for l in json.loads((ROOT / "i18n/languages.json").read_text("utf-8"))]
    data = extract(cat, codes)
    (ROOT / "i18n/app-terms.json").write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", "utf-8")
    print("wrote i18n/app-terms.json for", ", ".join(codes))


if __name__ == "__main__":
    sys.exit(main())
