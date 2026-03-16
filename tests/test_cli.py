"""Tests for CLI interface."""
import pytest
import sys
from pathlib import Path
from io import StringIO
from readme_toc.cli import create_parser, main


class TestCreateParser:
    def test_parser_defaults(self):
        parser = create_parser()
        args = parser.parse_args(['test.md'])
        assert args.file == 'test.md'
        assert args.depth == 6
        assert args.start_marker == '<!-- toc -->'
        assert args.end_marker == '<!-- tocstop -->'
        assert args.dry_run is False

    def test_parser_custom_depth(self):
        parser = create_parser()
        args = parser.parse_args(['test.md', '--depth', '3'])
        assert args.depth == 3


class TestMain:
    def test_file_not_found(self, monkeypatch, capsys):
        monkeypatch.setattr(sys, 'argv', ['readme-toc', 'nonexistent.md'])
        exit_code = main()
        assert exit_code == 1
        captured = capsys.readouterr()
        assert "not found" in captured.err

    def test_empty_input(self, monkeypatch, capsys):
        monkeypatch.setattr(sys, 'argv', ['readme-toc'])
        monkeypatch.setattr(sys.stdin, 'read', lambda: '')
        exit_code = main()
        assert exit_code == 1
        captured = capsys.readouterr()
        assert "Empty input" in captured.err

    def test_no_headers_warning(self, tmp_path, monkeypatch, capsys):
        test_file = tmp_path / "test.md"
        test_file.write_text("Just text, no headers")
        monkeypatch.setattr(sys, 'argv', ['readme-toc', str(test_file)])
        exit_code = main()
        assert exit_code == 0
        captured = capsys.readouterr()
        assert "No headers found" in captured.err

    def test_successful_update(self, tmp_path, monkeypatch, capsys):
        test_file = tmp_path / "test.md"
        test_file.write_text("# Title\n## Section")
        monkeypatch.setattr(sys, 'argv', ['readme-toc', str(test_file)])
        exit_code = main()
        assert exit_code == 0
        result = test_file.read_text()
        assert "<!-- toc -->" in result
        assert "[Title](#title)" in result

    def test_dry_run(self, tmp_path, monkeypatch, capsys):
        test_file = tmp_path / "test.md"
        original = "# Title\n## Section"
        test_file.write_text(original)
        monkeypatch.setattr(sys, 'argv', ['readme-toc', str(test_file), '--dry-run'])
        exit_code = main()
        assert exit_code == 0
        assert test_file.read_text() == original
        captured = capsys.readouterr()
        assert "<!-- toc -->" in captured.out
