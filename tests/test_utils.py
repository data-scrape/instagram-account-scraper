"""
Unit tests for Instagram Account Scraper utility functions.
"""

import pytest
import time
from unittest.mock import patch, MagicMock

from ig_scraper.utils import (
    rate_limit,
    retry,
    format_number,
    parse_hashtags,
    parse_mentions,
    sanitize_filename,
    ProgressBar,
)


class TestFormatNumber:
    """Tests for format_number utility."""

    def test_millions(self):
        assert format_number(1_000_000) == "1.0M"
        assert format_number(2_500_000) == "2.5M"

    def test_thousands(self):
        assert format_number(1_000) == "1.0K"
        assert format_number(15_000) == "15.0K"

    def test_small_numbers(self):
        assert format_number(0) == "0"
        assert format_number(42) == "42"
        assert format_number(999) == "999"


class TestParseHashtags:
    """Tests for parse_hashtags utility."""

    def test_single_hashtag(self):
        assert parse_hashtags("Hello #world") == ["world"]

    def test_multiple_hashtags(self):
        result = parse_hashtags("Check #this #out #now")
        assert result == ["this", "out", "now"]

    def test_no_hashtags(self):
        assert parse_hashtags("No hashtags here") == []

    def test_empty_caption(self):
        assert parse_hashtags("") == []
        assert parse_hashtags(None) == []

    def test_underscore_hashtags(self):
        assert parse_hashtags("Love #new_york_city") == ["new_york_city"]

    def test_numbers_in_hashtags(self):
        assert parse_hashtags("Year #2026 goals") == ["2026"]


class TestParseMentions:
    """Tests for parse_mentions utility."""

    def test_single_mention(self):
        assert parse_mentions("Hello @world") == ["world"]

    def test_multiple_mentions(self):
        result = parse_mentions("Check @this @out @now")
        assert result == ["this", "out", "now"]

    def test_no_mentions(self):
        assert parse_mentions("No mentions here") == []

    def test_empty_caption(self):
        assert parse_mentions("") == []
        assert parse_mentions(None) == []

    def test_underscore_mentions(self):
        assert parse_mentions("Follow @user_name_123") == ["user_name_123"]


class TestSanitizeFilename:
    """Tests for sanitize_filename utility."""

    def test_clean_filename(self):
        assert sanitize_filename("clean_name") == "clean_name"

    def test_special_chars(self):
        result = sanitize_filename('file<>:"/\\|?*name')
        assert "<" not in result
        assert ">" not in result
        assert ":" not in result

    def test_long_filename(self):
        long_name = "a" * 300
        result = sanitize_filename(long_name)
        assert len(result) <= 200

    def test_trailing_dot(self):
        result = sanitize_filename("filename.")
        assert not result.endswith(".")


class TestRateLimitDecorator:
    """Tests for rate_limit decorator."""

    def test_rate_limit_adds_delay(self):
        @rate_limit(min_delay=0.01, max_delay=0.02)
        def test_func():
            return "result"

        start = time.time()
        result = test_func()
        elapsed = time.time() - start

        assert result == "result"
        assert elapsed >= 0.01

    def test_rate_limit_preserves_function(self):
        @rate_limit(min_delay=0.01, max_delay=0.01)
        def add(a, b):
            return a + b

        assert add(2, 3) == 5


class TestRetryDecorator:
    """Tests for retry decorator."""

    def test_retry_succeeds_first_time(self):
        call_count = 0

        @retry(max_retries=3, backoff_factor=0.01)
        def test_func():
            nonlocal call_count
            call_count += 1
            return "success"

        result = test_func()
        assert result == "success"
        assert call_count == 1

    def test_retry_fails_then_succeeds(self):
        call_count = 0

        @retry(max_retries=3, backoff_factor=0.01)
        def test_func():
            nonlocal call_count
            call_count += 1
            if call_count < 2:
                raise ValueError("fail")
            return "success"

        result = test_func()
        assert result == "success"
        assert call_count == 2

    def test_retry_all_failures(self):
        @retry(max_retries=2, backoff_factor=0.01)
        def test_func():
            raise ValueError("always fails")

        with pytest.raises(ValueError):
            test_func()


class TestProgressBar:
    """Tests for ProgressBar."""

    def test_progress_bar_completion(self):
        with ProgressBar(5, "Test") as bar:
            for _ in range(5):
                bar.update()

    def test_progress_bar_partial(self):
        with ProgressBar(10, "Test") as bar:
            bar.update(3)

    def test_progress_bar_zero_total(self):
        with ProgressBar(0, "Test") as bar:
            pass  # should not crash

    def test_progress_bar_context_manager(self):
        bar = ProgressBar(3, "Test")
        with bar:
            bar.update()
            bar.update()
            bar.update()
