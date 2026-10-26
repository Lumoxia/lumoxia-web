"""Tests for scripts/build.py and the generated site. Run: python3 scripts/test_build.py"""
import html
import json
import re
import subprocess
import sys
import unittest
from html.parser import HTMLParser
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import build

ROOT = Path(__file__).resolve().parent.parent
BEFORE = ROOT / "scripts/fixtures/english-before"
PAGES = {"index": "index.html", "privacy": "privacy.html", "support": "support.html"}


class Visible(HTMLParser):
    """Collects visible text plus alt, aria-label and meta content, skipping the language menu and scripts."""
    VOID = {"br", "img", "meta", "link", "input", "hr"}

    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.items, self.skip, self.stack = [], 0, []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        skipping = tag in ("script", "style") or "data-lang-menu" in a
        if not self.skip and not skipping:
            for k in ("alt", "aria-label"):
                if a.get(k):
                    self.items.append(a[k])
            if tag == "meta" and a.get("content") and (a.get("name") == "description" or a.get("property") in ("og:title", "og:description")):
                self.items.append(a["content"])
        if tag not in self.VOID:
            self.stack.append((tag, skipping))
            self.skip += skipping

    def handle_endtag(self, tag):
        while self.stack:
            t, skipping = self.stack.pop()
            self.skip -= skipping
            if t == tag:
                break

    def handle_data(self, data):
        if not self.skip and data.strip():
            self.items.append(re.sub(r"\s+", " ", data.strip()))


def visible(html):
    p = Visible()
    p.feed(html)
    return p.items


class Engine(unittest.TestCase):
    def ctx(self, **kw):
        base = dict(strings={"a": "Hello {app:title}", "b": 'x "q" & y'}, app={"title": "Ur"},
                    simple={"base": "../../", "root": "../../"})
        base.update(kw)
        return build.Context(**base)

    def test_expand_t_and_app(self):
        self.assertEqual(build.expand("[{{t:a}}]", self.ctx()), "[Hello Ur]")

    def test_attr_escapes(self):
        self.assertEqual(build.expand("{{attr:b}}", self.ctx()), "x &quot;q&quot; &amp; y")

    def test_url_encodes(self):
        self.assertEqual(build.expand("{{url:a}}", self.ctx()), "Hello%20Ur")

    def test_patreon_token(self):
        self.assertEqual(build.expand("{{patreon}}", self.ctx(simple={"patreon": build.PATREON_URL})),
                         "https://www.patreon.com/lumoxia_art")

    def test_unknown_token_fails(self):
        with self.assertRaises(build.BuildError):
            build.expand("{{nope}}", self.ctx())

    def test_missing_key_fails(self):
        with self.assertRaises(build.BuildError):
            build.expand("{{t:zzz}}", self.ctx())

    def test_nested_base_in_value(self):
        ctx = self.ctx(strings={"a": '<a href="{{base}}x/">x</a>'})
        self.assertEqual(build.expand("{{t:a}}", ctx), '<a href="../../x/">x</a>')

    def test_base_depths(self):
        self.assertEqual(build.rel_prefix("index.html"), "")
        self.assertEqual(build.rel_prefix("royal-game-of-ur/support/index.html"), "../../")
        self.assertEqual(build.rel_prefix("fr/royal-game-of-ur/support/index.html", lang_dir="fr"), "../../")
        self.assertEqual(build.rel_prefix("fr/index.html", lang_dir="fr"), "")
        self.assertEqual(build.root_prefix("fr/royal-game-of-ur/support/index.html"), "../../../")
        self.assertEqual(build.root_prefix("index.html"), "")


class Generated(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.site = build.Site(ROOT)
        cls.out = cls.site.render_all()
        cls.langs = cls.site.languages

    def test_files_are_lf_and_end_with_newline(self):
        for path, text in self.out.items():
            self.assertNotIn("\r", text, path)
            self.assertTrue(text.endswith("\n"), path)

    def test_expected_files(self):
        for l in self.langs:
            prefix = "" if l["code"] == "en" else l["code"] + "/"
            for rel in ("index.html", "royal-game-of-ur/privacy/index.html", "royal-game-of-ur/support/index.html"):
                self.assertIn(prefix + rel, self.out)
        self.assertIn("sitemap.xml", self.out)

    def undo_iap_changes(self, items, page):
        """Put the pre-purchase English wording back in place of the intended in-app purchase edits."""
        spec = json.loads((BEFORE / "iap-changes.json").read_text("utf-8"))
        strings = self.site.strings["en"]

        def chunks(key, source):
            ctx = build.Context(strings=dict(source), app=self.site.app["en"], simple={"base": "", "root": ""})
            return visible("<p>" + build.expand("{{t:%s}}" % key, ctx) + "</p>")

        def swap(items, new, old):
            for i in range(len(items) - len(new) + 1):
                if items[i:i + len(new)] == new:
                    return items[:i] + old + items[i + len(new):], True
            return items, False

        for key, old_text in spec["changed"].items():
            new = chunks(key, strings)
            old = chunks(key, {key: old_text})
            items, _ = swap(items, new, old)  # a key may live on another page
        for key in spec["added"]:
            items, found = swap(items, chunks(key, strings), [])
            if key.startswith(page + "."):  # privacy.* lives on the privacy page, support.* on support
                self.assertTrue(found, "%s not found on %s" % (key, page))
        return items

    def test_english_text_unchanged(self):
        pairs = [("index", "index.html"), ("privacy", "royal-game-of-ur/privacy/index.html"),
                 ("support", "royal-game-of-ur/support/index.html")]
        for name, rel in pairs:
            before = visible((BEFORE / PAGES[name]).read_text("utf-8"))
            after = visible(self.out[rel])
            if name == "index":
                # the intended additions: Music section, Patreon button and footer link
                en = self.site.strings["en"]
                added = [html.unescape(en[k]) for k in ("nav.music", "music.h", "music.p1", "music.p2", "music.btn",
                                                        "contact.patreon", "contact.patreon.btn", "footer.patreon")]
                cleaned = []
                for t in after:
                    if t == en["footer.patreon"] and cleaned and cleaned[-1] == "\u00b7":
                        cleaned.pop()  # the separator in front of the Patreon footer link
                    for v in sorted(added, key=len, reverse=True):
                        t = t.replace(v, "").strip()
                    if t:
                        cleaned.append(t)
                after = cleaned
            after = self.undo_iap_changes(after, name)
            if name == "privacy":
                # the one intended addition: the "This website" section
                i = after.index("This website")
                after = after[:i] + after[i + 2:]
            self.assertEqual(after, before, name)

    def test_privacy_describes_the_optional_purchase(self):
        text = " ".join(visible(self.out["royal-game-of-ur/privacy/index.html"]))
        self.assertNotIn("no in-app purchases", text.lower())
        self.assertNotIn("does not connect to the internet", text.lower())
        self.assertIn("one optional", text)
        self.assertIn("Apple or Google", text)
        support = " ".join(visible(self.out["royal-game-of-ur/support/index.html"]))
        self.assertIn("Restore purchases", support)
        for lang, strings in self.site.strings.items():
            prefix = "" if lang == "en" else lang + "/"
            page = self.out[prefix + "royal-game-of-ur/privacy/index.html"]
            for key in ("privacy.iap.h", "privacy.keep.h"):
                self.assertIn(strings[key], page, "%s %s" % (lang, key))
            self.assertNotIn("21", strings["privacy.meta"], lang)  # the date of the old wording

    def test_android_and_store_attribution(self):
        home = " ".join(visible(self.out["index.html"]))
        self.assertIn("to iOS and Android", home)
        self.assertIn("It is not in the App Store or on Google Play yet.", home)
        for rel in ("royal-game-of-ur/privacy/index.html", "royal-game-of-ur/support/index.html"):
            self.assertIn("for iOS and Android", " ".join(visible(self.out[rel])), rel)
        for rel, text in self.out.items():
            if rel.endswith("index.html"):
                self.assertIn("trademarks of Google LLC", " ".join(visible(text)), rel)

    def test_music_section_and_patreon_links(self):
        for l in self.langs:
            prefix = "" if l["code"] == "en" else l["code"] + "/"
            text = self.out[prefix + "index.html"]
            self.assertLess(text.index('id="game"'), text.index('id="music"'), l["code"])
            self.assertLess(text.index('id="music"'), text.index('id="founder"'), l["code"])
            self.assertIn('href="#music"', text, l["code"])
            links = re.findall(r'<a [^>]*href="https://www\.patreon\.com/[^"]*"[^>]*>', text)
            self.assertEqual(len(links), 3, l["code"])  # music button, contact button, footer link
            for a in links:
                self.assertIn('href="https://www.patreon.com/lumoxia_art"', a)
                self.assertIn('target="_blank"', a)
                self.assertIn('rel="noopener"', a)
            for rel in ("royal-game-of-ur/privacy/index.html", "royal-game-of-ur/support/index.html"):
                self.assertNotIn("patreon", self.out[prefix + rel].lower(), rel)

    def test_contact_buttons_are_spaced(self):
        css = (ROOT / "styles.css").read_text()
        rule = re.search(r"(?m)^(\.cta)\s*\{([^}]*)\}", css)
        self.assertIsNotNone(rule, "no bare .cta rule in styles.css")
        for decl in ("display: flex", "gap: 14px", "flex-wrap: wrap"):
            self.assertIn(decl, rule.group(2))
        for l in self.langs:
            prefix = "" if l["code"] == "en" else l["code"] + "/"
            text = self.out[prefix + "index.html"]
            contact = text[text.index('id="contact"'):]
            row = re.search(r'<div class="cta"[^>]*>', contact)
            self.assertIsNotNone(row, l["code"])
            self.assertNotIn("style=", row.group(0), l["code"])

    def test_cta_rows_are_centred(self):
        css = (ROOT / "styles.css").read_text()
        rule = re.search(r"(?m)^(\.cta)\s*\{([^}]*)\}", css)
        self.assertIsNotNone(rule, "no bare .cta rule in styles.css")
        self.assertIn("justify-content: center", rule.group(2))
        self.assertNotRegex(css, r"\.(hero|cta-band) \.cta\b")

    def test_music_cta_has_no_inline_style(self):
        for l in self.langs:
            prefix = "" if l["code"] == "en" else l["code"] + "/"
            text = self.out[prefix + "index.html"]
            music = text[text.index('id="music"'):text.index('id="founder"')]
            row = re.search(r'<div class="cta"[^>]*>', music)
            self.assertIsNotNone(row, l["code"])
            self.assertNotIn("style=", row.group(0), l["code"])

    def test_no_embeds(self):
        for rel, text in self.out.items():
            if rel.endswith(".html"):
                self.assertNotIn("<audio", text, rel)
                self.assertNotIn("<iframe", text, rel)
                self.assertEqual(re.findall(r'<script[^>]+src="https?://[^"]*"', text), [], rel)

    def test_badges_stored_but_not_shown(self):
        for name in ("app-store.svg", "google-play.png"):
            self.assertTrue((ROOT / "assets/badges" / name).is_file(), name)
        for rel, text in self.out.items():
            self.assertNotIn("assets/badges", text, rel)

    def test_english_growth_under_15kb(self):
        for name, rel in [("index", "index.html"), ("privacy", "royal-game-of-ur/privacy/index.html"),
                          ("support", "royal-game-of-ur/support/index.html")]:
            before = len((BEFORE / PAGES[name]).read_bytes())
            self.assertLess(len(self.out[rel].encode()) - before, 15 * 1024, name)

    def test_lang_dir_canonical_alternates(self):
        for l in self.langs:
            prefix = "" if l["code"] == "en" else l["code"] + "/"
            html = self.out[prefix + "royal-game-of-ur/support/index.html"]
            self.assertIn(f'<html lang="{l["htmlLang"]}" dir="{l["dir"]}"', html)
            self.assertEqual(html.count('dir="rtl"') >= 1, l["code"] in ("ar", "he"), l["code"])
            canon = "https://lumoxia.art/" + prefix + "royal-game-of-ur/support/"
            self.assertIn(f'<link rel="canonical" href="{canon}" />', html)
            self.assertEqual(len(re.findall(r'rel="alternate" hreflang="', html)), len(self.langs) + 1)
            self.assertIn('hreflang="x-default" href="https://lumoxia.art/royal-game-of-ur/support/"', html)

    def test_menu_has_all_languages_in_order_one_current(self):
        for l in self.langs:
            prefix = "" if l["code"] == "en" else l["code"] + "/"
            html = self.out[prefix + "index.html"]
            codes = re.findall(r'data-lang="([a-z]{2})"', html)
            self.assertEqual(codes, [x["code"] for x in self.langs])
            self.assertEqual(html.count('aria-current="true"'), 1)
            self.assertRegex(html, rf'aria-current="true"[^>]*data-lang="{l["code"]}"|data-lang="{l["code"]}"[^>]*aria-current="true"')

    def test_fifteen_languages_in_order(self):
        self.assertEqual([l["code"] for l in self.langs],
                         ["en", "fr", "es", "de", "ar", "zh", "it", "hi", "tl", "tr", "ru", "he", "pt", "ja", "ko"])

    def test_hebrew_is_rtl_with_hebrew_font(self):
        html = self.out["he/index.html"]
        self.assertIn('dir="rtl"', html)
        self.assertIn('class="fs-hebrew"', html)
        self.assertIn("Noto+Sans+Hebrew", html)

    def test_russian_loads_cyrillic_fonts(self):
        html = self.out["ru/index.html"]
        self.assertIn('lang="ru"', html)
        self.assertIn("cyrillic", html)

    def test_turkish_and_portuguese_tags(self):
        self.assertIn('<html lang="tr" dir="ltr"', self.out["tr/index.html"])
        self.assertIn('<html lang="pt" dir="ltr"', self.out["pt/index.html"])

    def test_detect_script_only_on_english(self):
        for path, html in self.out.items():
            if not path.endswith(".html"):
                continue
            self.assertEqual("lumoxiaDetect" in html, not re.match(r"[a-z]{2}/", path), path)

    def test_links_resolve(self):
        for path, html in self.out.items():
            if not path.endswith(".html"):
                continue
            here = (ROOT / path).parent
            for m in re.finditer(r'(?:href|src)="([^"]+)"', html):
                u = m.group(1)
                if re.match(r"(https?:|mailto:|#|data:)", u):
                    continue
                u = u.split("#")[0].split("?")[0]
                if not u:
                    continue
                target = (ROOT / u.lstrip("/")) if u.startswith("/") else (here / u)
                key = str(target.resolve().relative_to(ROOT.resolve()))
                ok = target.is_file() or key in self.out or (key + "/index.html") in self.out or \
                     (target.is_dir() and (key.rstrip("/") + "/index.html") in self.out) or \
                     str(Path(key) / "index.html") in self.out or (key == "." and "index.html" in self.out)
                self.assertTrue(ok, f"{path}: broken link {m.group(1)}")

    def test_sitemap_lists_everything(self):
        sm = self.out["sitemap.xml"]
        for l in self.langs:
            prefix = "" if l["code"] == "en" else l["code"] + "/"
            for rel in ("", "royal-game-of-ur/privacy/", "royal-game-of-ur/support/"):
                self.assertIn(f"<loc>https://lumoxia.art/{prefix}{rel}</loc>", sm)

    def test_committed_output_is_current(self):
        for path, text in self.out.items():
            f = ROOT / path
            self.assertTrue(f.exists(), f"{path} not committed; run python3 scripts/build.py")
            self.assertEqual(f.read_text("utf-8"), text, f"{path} is stale; run python3 scripts/build.py")


class Detect(unittest.TestCase):
    def test_node_table(self):
        try:
            r = subprocess.run(["node", str(ROOT / "scripts/test_detect.js")], capture_output=True, text=True)
        except FileNotFoundError:
            self.skipTest("node not installed")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)


if __name__ == "__main__":
    unittest.main()
