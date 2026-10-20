# MIT License
#
# Copyright (c) 2026 ZEISS Industrial Quality Solutions
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

"""Build the documentation news page and its RSS 2.0 feed.

The extension reads article dates and optional descriptions from MyST front
matter, renders the articles into the news index, and writes the RSS feed at
the end of a successful Sphinx build.
"""

from __future__ import annotations

import ast
import copy
from dataclasses import dataclass
from datetime import datetime, timezone
from email.utils import format_datetime
from pathlib import Path
from typing import Any
from urllib.parse import urljoin
from xml.etree import ElementTree

from docutils import nodes
from docutils.parsers.rst import Directive
from sphinx.application import Sphinx


NEWS_INDEX_DOCNAME = "news/news"


class NewsListNode(nodes.General, nodes.Element):
    """Placeholder node replaced with the rendered news article list."""

    pass


class NewsListDirective(Directive):
    """Insert a placeholder for the generated news article list."""

    has_content = False
    required_arguments = 0
    optional_arguments = 0

    def run(self) -> list[nodes.Node]:
        """Return the node that will be populated during doctree resolution."""

        return [NewsListNode()]


@dataclass(frozen=True)
class NewsEntry:
    """Normalized metadata and content summary for one news article."""

    docname: str
    title: str
    publication_date: datetime
    description: str


def _front_matter(app: Sphinx, docname: str) -> dict[str, Any]:
    """Return the MyST front matter associated with a document."""

    metadata = app.env.metadata.get(docname, {})
    if not isinstance(metadata, dict):
        return {}

    myst_metadata = metadata.get("myst")
    if isinstance(myst_metadata, dict):
        front_matter = myst_metadata.get("front_matter")
        if isinstance(front_matter, dict):
            return front_matter

    front_matter = metadata.get("front_matter")
    if isinstance(front_matter, dict):
        return front_matter

    return metadata


def _mapping(value: Any, field: str) -> dict[str, Any]:
    """Return a metadata value as a mapping, including serialized mappings."""

    if isinstance(value, dict):
        return value
    if isinstance(value, str):
        try:
            parsed = ast.literal_eval(value)
        except (SyntaxError, ValueError):
            parsed = None
        if isinstance(parsed, dict):
            return parsed
    raise ValueError(f"{field} metadata must be a mapping")


def _news_metadata(app: Sphinx, docname: str) -> dict[str, Any]:
    """Return the ``news`` metadata for an article document."""

    return _mapping(_front_matter(app, docname).get("news", {}), f"{docname}: news")


def _parse_date(value: Any, docname: str) -> datetime:
    """Parse an article date and normalize it to UTC."""

    if isinstance(value, datetime):
        parsed = value
    elif isinstance(value, str):
        try:
            parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError as error:
            raise ValueError(f"{docname}: invalid news.date {value!r}") from error
    else:
        raise ValueError(f"{docname}: news.date must be an ISO timestamp")

    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)


def _document_section(app: Sphinx, docname: str) -> nodes.section:
    """Return the first section in an article after resolving references."""

    doctree = app.env.get_doctree(docname)
    app.env.resolve_references(doctree, docname, app.builder)
    sections = doctree.findall(nodes.section)
    section = next(iter(sections), None)
    if section is None:
        raise ValueError(f"{docname}: news article must contain a section heading")
    return section


def _plain_text(section: nodes.section) -> str:
    """Return the first non-empty paragraph as normalized plain text."""

    for paragraph in section.findall(nodes.paragraph):
        text = " ".join(paragraph.astext().split())
        if text:
            return text
    return ""


def _article_docnames(app: Sphinx) -> list[str]:
    """Return document names for all news articles except the index page."""

    return sorted(
        docname
        for docname in app.env.found_docs
        if docname.startswith("news/") and docname != NEWS_INDEX_DOCNAME
    )


def _entries(app: Sphinx) -> list[NewsEntry]:
    """Collect and sort news entries by publication date, newest first."""

    entries = []
    for docname in _article_docnames(app):
        metadata = _news_metadata(app, docname)
        section = _document_section(app, docname)
        title = section.next_node(nodes.title)
        if title is None:
            raise ValueError(f"{docname}: news article must contain a title")

        description = metadata.get("description") or _plain_text(section)
        entries.append(
            NewsEntry(
                docname=docname,
                title=title.astext(),
                publication_date=_parse_date(metadata.get("date"), docname),
                description=" ".join(str(description).split()),
            )
        )

    return sorted(
        entries,
        key=lambda entry: (-entry.publication_date.timestamp(), entry.docname),
    )


def _feed_config(app: Sphinx) -> dict[str, Any]:
    """Return the RSS configuration from the news index front matter."""

    return _mapping(
        _front_matter(app, NEWS_INDEX_DOCNAME).get("newsfeed", {}),
        f"{NEWS_INDEX_DOCNAME}: newsfeed",
    )


def _render_entries(app: Sphinx, placeholder: NewsListNode) -> None:
    """Replace the news-list placeholder with rendered article sections."""

    builder = app.builder
    rendered = []
    for entry in _entries(app):
        if rendered:
            rendered.append(nodes.raw("", '<hr class="feed-ref" />', format="html"))
        section = copy.deepcopy(_document_section(app, entry.docname))
        for title_node in section.findall(nodes.title):
            for child in tuple(title_node.children):
                if isinstance(child, nodes.reference):
                    inline = nodes.inline()
                    inline += child
                    title_node.replace(child, inline)
        title = section.next_node(nodes.title)
        assert title is not None
        article_link = builder.get_relative_uri(NEWS_INDEX_DOCNAME, entry.docname)
        if section["ids"]:
            article_link += f"#{section['ids'][0]}"
        reference = nodes.reference(
            entry.title,
            nodes.Text(entry.title),
            refuri=article_link,
            internal=False,
        )
        inline = nodes.inline()
        inline += reference
        title.children = [inline]
        section.insert(
            1,
            nodes.paragraph(
                "",
                f"Published on {entry.publication_date.strftime('%Y-%m-%d %H:%M:%S')}",
            ),
        )
        rendered.append(section)
    placeholder.replace_self(rendered)


def _on_doctree_resolved(app: Sphinx, doctree: nodes.document, docname: str) -> None:
    """Render news placeholders when the news index doctree is resolved."""

    if docname != NEWS_INDEX_DOCNAME:
        return
    for placeholder in doctree.findall(NewsListNode):
        _render_entries(app, placeholder)


def _write_rss(app: Sphinx, exception: Exception | None) -> None:
    """Write the configured RSS feed after a successful Sphinx build."""

    if exception is not None:
        return

    config = _feed_config(app)
    base_link = str(config["link"]).rstrip("/") + "/"
    rss_path = Path(app.outdir) / str(config.get("rss", "index.rss"))
    rss_path.parent.mkdir(parents=True, exist_ok=True)

    rss = ElementTree.Element("rss", {"version": "2.0"})
    channel = ElementTree.SubElement(rss, "channel")
    ElementTree.SubElement(channel, "title").text = str(config["title"])
    ElementTree.SubElement(channel, "link").text = base_link
    ElementTree.SubElement(channel, "description").text = str(config["title"])

    for entry in _entries(app):
        item = ElementTree.SubElement(channel, "item")
        article_link = urljoin(base_link, app.builder.get_target_uri(entry.docname))
        ElementTree.SubElement(item, "title").text = entry.title
        ElementTree.SubElement(item, "link").text = article_link
        ElementTree.SubElement(item, "description").text = entry.description
        ElementTree.SubElement(item, "pubDate").text = format_datetime(
            entry.publication_date
        )
        guid = ElementTree.SubElement(item, "guid", {"isPermaLink": "true"})
        guid.text = article_link

    ElementTree.ElementTree(rss).write(
        rss_path,
        encoding="utf-8",
        xml_declaration=True,
    )


def setup(app: Sphinx) -> dict[str, Any]:
    """Register the news node, directive, and Sphinx event handlers."""

    app.add_node(NewsListNode)
    app.add_directive("news-list", NewsListDirective)
    app.connect("doctree-resolved", _on_doctree_resolved)
    app.connect("build-finished", _write_rss)
    return {
        "version": "1.0",
        "parallel_read_safe": True,
        "parallel_write_safe": False,
    }