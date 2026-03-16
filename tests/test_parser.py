"""Tests for markdown parsing and TOC generation."""
import pytest
from readme_toc.parser import (
    Header,
    parse_headers,
    generate_anchor,
    assign_anchors,
    generate_toc
)


class TestParseHeaders:
    def test_parse_basic_headers(self):
        content = "# Title\n## Section\n### Subsection"
        headers = parse_headers(content)
        assert len(headers) == 3
        assert headers[0].level == 1
        assert headers[0].text == "Title"
        assert headers[1].level == 2
        assert headers[2].level == 3

    def test_parse_with_max_depth(self):
        content = "# H1\n## H2\n### H3\n#### H4"
        headers = parse_headers(content, max_depth=2)
        assert len(headers) == 2
        assert all(h.level <= 2 for h in headers)

    def test_parse_empty_content(self):
        headers = parse_headers("")
        assert headers == []

    def test_parse_no_headers(self):
        content = "Just some text\nNo headers here"
        headers = parse_headers(content)
        assert headers == []


class TestGenerateAnchor:
    def test_basic_anchor(self):
        assert generate_anchor("Hello World") == "hello-world"

    def test_special_characters_removed(self):
        assert generate_anchor("Hello! @World#") == "hello-world"

    def test_multiple_spaces(self):
        assert generate_anchor("Hello   World") == "hello-world"

    def test_leading_trailing_hyphens(self):
        assert generate_anchor("--Hello--") == "hello"


class TestAssignAnchors:
    def test_unique_anchors(self):
        headers = [
            Header(1, "Title", 0),
            Header(2, "Section", 1)
        ]
        assign_anchors(headers)
        assert headers[0].anchor == "title"
        assert headers[1].anchor == "section"

    def test_duplicate_anchors(self):
        headers = [
            Header(1, "Title", 0),
            Header(2, "Title", 1),
            Header(3, "Title", 2)
        ]
        assign_anchors(headers)
        assert headers[0].anchor == "title"
        assert headers[1].anchor == "title-1"
        assert headers[2].anchor == "title-2"


class TestGenerateToc:
    def test_generate_basic_toc(self):
        headers = [
            Header(1, "Title", 0),
            Header(2, "Section", 1)
        ]
        headers[0].anchor = "title"
        headers[1].anchor = "section"
        toc = generate_toc(headers)
        assert "- [Title](#title)" in toc
        assert "  - [Section](#section)" in toc

    def test_generate_empty_toc(self):
        toc = generate_toc([])
        assert toc == ""

    def test_proper_indentation(self):
        headers = [
            Header(2, "H2", 0),
            Header(3, "H3", 1),
            Header(4, "H4", 2)
        ]
        for h in headers:
            h.anchor = h.text.lower()
        toc = generate_toc(headers)
        lines = toc.split('\n')
        assert lines[0].startswith("- ")
        assert lines[1].startswith("  - ")
        assert lines[2].startswith("    - ")
