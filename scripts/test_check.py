"""Tests for scripts/check_i18n.py. Run: python3 scripts/test_check.py"""
import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import check_i18n as c

EN = {
    "a.text": "Hello <strong>world</strong>",
    "a.link": 'See <a href="{{base}}x/">this</a> and {app:title}',
    "_review": "source",
}


def good(**over):
    d = {"a.text": "Bonjour <strong>monde</strong>",
         "a.link": 'Voir <a href="{{base}}x/">ceci</a> et {app:title}', "_review": "unreviewed"}
    d.update(over)
    return d


class StringChecks(unittest.TestCase):
    def errs(self, other):
        return c.check_strings({"en": EN, "fr": other})

    def test_clean(self):
        self.assertEqual(self.errs(good()), [])

    def test_missing_key(self):
        d = good(); del d["a.text"]
        self.assertTrue(any("missing" in e and "a.text" in e for e in self.errs(d)))

    def test_extra_key(self):
        self.assertTrue(any("extra" in e and "zz" in e for e in self.errs(good(zz="x"))))

    def test_empty_value(self):
        self.assertTrue(any("empty" in e for e in self.errs(good(**{"a.text": "  "}))))

    def test_changed_tag(self):
        self.assertTrue(any("tags" in e for e in self.errs(good(**{"a.text": "Bonjour <em>monde</em>"}))))

    def test_changed_href(self):
        bad = 'Voir <a href="{{base}}y/">ceci</a> et {app:title}'
        self.assertTrue(any("tags" in e for e in self.errs(good(**{"a.link": bad}))))

    def test_changed_app_token(self):
        bad = 'Voir <a href="{{base}}x/">ceci</a> et {app:rules}'
        self.assertTrue(any("tokens" in e for e in self.errs(good(**{"a.link": bad}))))

    def test_changed_template_token(self):
        bad = 'Voir <a href="x/">ceci</a> et {app:title}'
        self.assertTrue(any("tags" in e or "tokens" in e for e in self.errs(good(**{"a.link": bad}))))

    def test_em_dash(self):
        self.assertTrue(any("dash" in e for e in self.errs(good(**{"a.text": "a — b <strong>c</strong>"}))))

    def test_en_dash(self):
        self.assertTrue(any("dash" in e for e in self.errs(good(**{"a.text": "a – b <strong>c</strong>"}))))

    def test_underscore_keys_ignored(self):
        self.assertEqual(self.errs(good(_extra="x")), [])


class LanguageChecks(unittest.TestCase):
    PINNED = ["en", "fr", "es", "de", "ar", "zh", "it", "hi", "tl"]

    def langs(self, codes):
        return [{"code": k} for k in codes]

    def test_clean(self):
        self.assertEqual(c.check_languages(self.langs(self.PINNED), self.PINNED, self.PINNED), [])

    def test_order_differs(self):
        e = c.check_languages(self.langs(reversed(self.PINNED)), self.PINNED, self.PINNED)
        self.assertTrue(e)

    def test_missing_string_file(self):
        e = c.check_languages(self.langs(self.PINNED), self.PINNED[:-1], self.PINNED)
        self.assertTrue(any("strings" in x for x in e))

    def test_extra_language(self):
        e = c.check_languages(self.langs(self.PINNED + ["pt"]), self.PINNED + ["pt"], self.PINNED)
        self.assertTrue(e)


class TemplateChecks(unittest.TestCase):
    def test_unknown_key(self):
        e = c.check_templates({"index": "{{t:nope}}"}, {"a.text"})
        self.assertTrue(any("nope" in x for x in e))

    def test_unknown_token(self):
        e = c.check_templates({"index": "{{bogus}}"}, {"a.text"})
        self.assertTrue(any("bogus" in x for x in e))

    def test_known(self):
        self.assertEqual(c.check_templates({"index": "{{t:a.text}} {{base}}"}, {"a.text"}), [])

    def test_dash_in_template(self):
        e = c.check_templates({"index": "a — b"}, set())
        self.assertTrue(any("dash" in x for x in e))


class AppRepoParse(unittest.TestCase):
    def test_parse(self):
        swift = 'LocaleInfo(code: "ar", label: "العربية", short: "ع", direction: .rtl),\nLocaleInfo(code: "tl", label: "Tagalog", short: "TL", direction: .ltr),'
        got = c.parse_app_locales(swift)
        self.assertEqual(got[0], {"code": "ar", "label": "العربية", "short": "ع", "dir": "rtl"})
        self.assertEqual(got[1]["code"], "tl")


if __name__ == "__main__":
    unittest.main()
