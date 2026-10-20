import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace
from xml.etree import ElementTree

from docutils import nodes

import newsfeed


class FakeEnvironment:
    def __init__(self, metadata, doctrees):
        self.metadata = metadata
        self.found_docs = set(doctrees)
        self._doctrees = doctrees

    def get_doctree(self, docname):
        return self._doctrees[docname]

    def resolve_references(self, doctree, docname, builder):
        return None


class FakeBuilder:
    def get_relative_uri(self, fromdocname, docname):
        return f"{docname}.html"

    def get_target_uri(self, docname):
        return f"{docname}.html"


class NewsfeedTests(unittest.TestCase):
    def _app(self, metadata, doctrees):
        return SimpleNamespace(
            env=FakeEnvironment(metadata, doctrees),
            builder=FakeBuilder(),
        )

    def _article(self, title, description):
        section = nodes.section(ids=[title.lower().replace(" ", "-")])
        section += nodes.title("", title)
        section += nodes.paragraph("", description)
        document = nodes.document("", "")
        document += section
        return document

    def test_parse_date_assumes_utc(self):
        parsed = newsfeed._parse_date("2025-11-27 16:00", "news/article")

        self.assertEqual(parsed, datetime(2025, 11, 27, 16, tzinfo=timezone.utc))

    def test_entries_use_front_matter_and_sort_ties_by_docname(self):
        doctrees = {
            "news/z-last": self._article("Last", "Last summary"),
            "news/a-first": self._article("First", "First summary"),
        }
        metadata = {
            "news/z-last": {
                "myst": {
                    "front_matter": {"news": {"date": "2025-01-01 10:00"}}
                }
            },
            "news/a-first": {
                "myst": {
                    "front_matter": {"news": {"date": "2025-01-01 10:00"}}
                }
            },
        }

        entries = newsfeed._entries(self._app(metadata, doctrees))

        self.assertEqual([entry.docname for entry in entries], ["news/a-first", "news/z-last"])
        self.assertEqual(entries[0].description, "First summary")

    def test_write_rss_escapes_text_and_writes_absolute_links(self):
        doctrees = {"news/article": self._article("A & B", "A <summary>")}
        metadata = {
            "news/article": {
                "news": {"date": "2025-01-01 10:00", "description": "A <summary>"}
            },
            "news/news": {
                "newsfeed": {
                    "title": "Test News",
                    "link": "https://example.test/docs/2026/",
                    "rss": "index.rss",
                }
            },
        }
        with tempfile.TemporaryDirectory() as output_dir:
            app = self._app(metadata, doctrees)
            app.outdir = output_dir

            newsfeed._write_rss(app, None)

            root = ElementTree.parse(Path(output_dir) / "index.rss").getroot()
            item = root.find("./channel/item")
            self.assertIsNotNone(item)
            self.assertEqual(
                item.findtext("link"),
                "https://example.test/docs/2026/news/article.html",
            )
            self.assertEqual(item.findtext("description"), "A <summary>")
            self.assertIn("+0000", item.findtext("pubDate"))

    def test_render_entries_inserts_separators_between_articles(self):
        doctrees = {
            "news/first": self._article("First", "First summary"),
            "news/second": self._article("Second", "Second summary"),
        }
        metadata = {
            "news/first": {"news": {"date": "2025-01-01 10:00"}},
            "news/second": {"news": {"date": "2025-01-02 10:00"}},
        }
        app = self._app(metadata, doctrees)
        document = nodes.document("", "")
        placeholder = newsfeed.NewsListNode()
        document += placeholder

        newsfeed._render_entries(app, placeholder)

        self.assertEqual(len(document.children), 3)
        self.assertIsInstance(document.children[0], nodes.section)
        self.assertIsInstance(document.children[1], nodes.raw)
        self.assertEqual(document.children[1]["format"], "html")
        self.assertEqual(document.children[1].astext(), '<hr class="feed-ref" />')
        self.assertIsInstance(document.children[2], nodes.section)

    def test_missing_date_is_rejected(self):
        doctrees = {"news/article": self._article("Article", "Summary")}
        metadata = {"news/article": {"news": {}}}

        with self.assertRaisesRegex(ValueError, "news.date"):
            newsfeed._entries(self._app(metadata, doctrees))


if __name__ == "__main__":
    unittest.main()