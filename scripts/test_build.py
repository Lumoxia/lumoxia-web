"""Tests for scripts/build.py and the generated site. Run: python3 scripts/test_build.py"""
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

    def test_english_text_unchanged(self):
        pairs = [("index", "index.html"), ("privacy", "royal-game-of-ur/privacy/index.html"),
                 ("support", "royal-game-of-ur/support/index.html")]
        for name, rel in pairs:
            before = visible((BEFORE / PAGES[name]).read_text("utf-8"))
            after = visible(self.out[rel])
            if name == "privacy":
                # the one intended addition: the "This website" section
                i = after.index("This website")
                after = after[:i] + after[i + 2:]
            self.assertEqual(after, before, name)

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
            self.assertEqual(html.count('dir="rtl"') >= 1, l["code"] == "ar", l["code"])
            canon = "https://lumoxia.art/" + prefix + "royal-game-of-ur/support/"
            self.assertIn(f'<link rel="canonical" href="{canon}" />', html)
            self.assertEqual(len(re.findall(r'rel="alternate" hreflang="', html)), 10)
            self.assertIn('hreflang="x-default" href="https://lumoxia.art/royal-game-of-ur/support/"', html)

    def test_menu_has_nine_in_order_one_current(self):
        for l in self.langs:
            prefix = "" if l["code"] == "en" else l["code"] + "/"
            html = self.out[prefix + "index.html"]
            codes = re.findall(r'data-lang="([a-z]{2})"', html)
            self.assertEqual(codes, [x["code"] for x in self.langs])
            self.assertEqual(html.count('aria-current="true"'), 1)
            self.assertRegex(html, rf'aria-current="true"[^>]*data-lang="{l["code"]}"|data-lang="{l["code"]}"[^>]*aria-current="true"')

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
