"""
Unit tests for Instagram Account Scraper CLI.
"""

import pytest
import json
import sys
from unittest.mock import patch, MagicMock
from io import StringIO

from ig_scraper.cli import build_parser, main, output_result
from ig_scraper.models import Profile, Post
from ig_scraper import __version__


class TestParser:
    """Tests for CLI argument parser."""

    def test_parser_version(self):
        parser = build_parser()
        with pytest.raises(SystemExit):
            parser.parse_args(["--version"])

    def test_profile_command(self):
        parser = build_parser()
        args = parser.parse_args(["profile", "nasa"])
        assert args.command == "profile"
        assert args.username == "nasa"

    def test_posts_command(self):
        parser = build_parser()
        args = parser.parse_args(["posts", "nasa", "--limit", "10"])
        assert args.command == "posts"
        assert args.username == "nasa"
        assert args.limit == 10

    def test_posts_command_default_limit(self):
        parser = build_parser()
        args = parser.parse_args(["posts", "nasa"])
        assert args.limit == 12

    def test_reels_command(self):
        parser = build_parser()
        args = parser.parse_args(["reels", "nasa", "--limit", "5"])
        assert args.command == "reels"
        assert args.limit == 5

    def test_hashtag_command(self):
        parser = build_parser()
        args = parser.parse_args(["hashtag", "travel", "--limit", "20"])
        assert args.command == "hashtag"
        assert args.hashtag == "travel"
        assert args.limit == 20

    def test_batch_command(self):
        parser = build_parser()
        args = parser.parse_args(["batch", "accounts.txt", "--limit", "5"])
        assert args.command == "batch"
        assert args.file == "accounts.txt"

    def test_all_command(self):
        parser = build_parser()
        args = parser.parse_args(["all", "nasa", "--posts", "20"])
        assert args.command == "all"
        assert args.username == "nasa"
        assert args.posts == 20

    def test_global_options(self):
        parser = build_parser()
        args = parser.parse_args([
            "--output", "out.json",
            "--format", "csv",
            "--delay", "5.0",
            "--quiet",
            "profile", "nasa",
        ])
        assert args.output == "out.json"
        assert args.format == "csv"
        assert args.delay == 5.0
        assert args.quiet is True

    def test_login_option(self):
        parser = build_parser()
        args = parser.parse_args([
            "--login", "user", "pass",
            "profile", "nasa",
        ])
        assert args.login == ["user", "pass"]

    def test_proxy_option(self):
        parser = build_parser()
        args = parser.parse_args([
            "--proxy", "http://proxy:8080",
            "profile", "nasa",
        ])
        assert args.proxy == "http://proxy:8080"


class TestOutputResult:
    """Tests for output_result function."""

    def test_output_profile_to_stdout(self, capsys):
        profile = Profile(username="test", followers=100)
        args = MagicMock(output=None, format="json", quiet=False)
        output_result(profile, args)
        captured = capsys.readouterr()
        assert '"username": "test"' in captured.out

    def test_output_profile_to_file(self, tmp_path):
        profile = Profile(username="test", followers=100)
        output_file = tmp_path / "out.json"
        args = MagicMock(output=str(output_file), format="json", quiet=True)
        output_result(profile, args)
        data = json.loads(output_file.read_text(encoding="utf-8"))
        assert data["username"] == "test"

    def test_output_post_list(self, capsys):
        posts = [Post(shortcode="ABC1"), Post(shortcode="ABC2")]
        args = MagicMock(output=None, format="json", quiet=False)
        output_result(posts, args)
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert len(data) == 2

    def test_output_string_list(self, capsys):
        args = MagicMock(output=None, format="json", quiet=False)
        output_result(["email1@test.com", "email2@test.com"], args)
        captured = capsys.readouterr()
        assert "email1@test.com" in captured.out


class TestMainCLI:
    """Integration tests for the CLI main function."""

    def test_no_command_prints_help(self, capsys):
        with pytest.raises(SystemExit):
            main([])
        captured = capsys.readouterr()
        assert "ig-scraper" in captured.out or "usage" in captured.out.lower()

    @patch("ig_scraper.cli.InstagramScraper")
    def test_profile_command_execution(self, mock_scraper_class, capsys):
        mock_scraper = MagicMock()
        mock_scraper_class.return_value = mock_scraper
        mock_profile = Profile(username="nasa", followers=85000000)
        mock_scraper.get_profile.return_value = mock_profile

        main(["profile", "nasa", "--quiet"])

        captured = capsys.readouterr()
        assert "nasa" in captured.out
        assert "85000000" in captured.out
