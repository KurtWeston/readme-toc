"""Tests for TOC insertion and update functionality."""
import pytest
from readme_toc.updater import (
    find_toc_markers,
    insert_toc,
    remove_toc_section
)


class TestFindTocMarkers:
    def test_find_existing_markers(self):
        content = "# Title\n<!-- toc -->\nOld TOC\n<!-- tocstop -->\n## Section"
        markers = find_toc_markers(content, "<!-- toc -->", "<!-- tocstop -->")
        assert markers == (1, 3)

    def test_no_markers_found(self):
        content = "# Title\n## Section"
        markers = find_toc_markers(content, "<!-- toc -->", "<!-- tocstop -->")
        assert markers is None

    def test_only_start_marker(self):
        content = "# Title\n<!-- toc -->\n## Section"
        markers = find_toc_markers(content, "<!-- toc -->", "<!-- tocstop -->")
        assert markers is None


class TestInsertToc:
    def test_update_existing_toc(self):
        content = "# Title\n<!-- toc -->\nOld\n<!-- tocstop -->\n## Section"
        new_toc = "- [Title](#title)\n  - [Section](#section)"
        result = insert_toc(content, new_toc, "<!-- toc -->", "<!-- tocstop -->")
        assert "Old" not in result
        assert new_toc in result
        assert "<!-- toc -->" in result
        assert "<!-- tocstop -->" in result

    def test_insert_new_toc(self):
        content = "# Title\n## Section"
        new_toc = "- [Title](#title)"
        result = insert_toc(content, new_toc, "<!-- toc -->", "<!-- tocstop -->")
        assert "<!-- toc -->" in result
        assert "<!-- tocstop -->" in result
        assert new_toc in result
        assert result.index("<!-- toc -->") < result.index("# Title")


class TestRemoveTocSection:
    def test_remove_existing_toc(self):
        content = "# Title\n<!-- toc -->\nTOC content\n<!-- tocstop -->\n## Section"
        result = remove_toc_section(content)
        assert "TOC content" not in result
        assert "# Title" in result
        assert "## Section" in result

    def test_no_toc_to_remove(self):
        content = "# Title\n## Section"
        result = remove_toc_section(content)
        assert result == content
