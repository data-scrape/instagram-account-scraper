"""
Unit tests for Instagram Account Scraper data models.
"""

import json
import pytest
from datetime import datetime

from ig_scraper.models import (
    Profile, Post, Reel, Story, Hashtag,
    DataExporter,
)
from ig_scraper.exceptions import (
    InstagramScraperError,
    LoginRequiredError,
    RateLimitError,
    ProfileNotFoundError,
    PrivateProfileError,
)


class TestProfile:
    """Tests for Profile data model."""

    @pytest.fixture
    def sample_profile(self):
        return Profile(
            username="testuser",
            user_id="123456789",
            full_name="Test User",
            biography="This is a test bio #testing",
            external_url="https://example.com",
            followers=10000,
            following=500,
            posts_count=150,
            is_private=False,
            is_verified=True,
            is_business=True,
            business_category="Personal Blog",
            profile_pic_url="https://example.com/pic.jpg",
        )

    def test_to_dict(self, sample_profile):
        d = sample_profile.to_dict()
        assert d["username"] == "testuser"
        assert d["followers"] == 10000
        assert d["is_verified"] is True

    def test_to_json(self, sample_profile):
        json_str = sample_profile.to_json()
        data = json.loads(json_str)
        assert data["username"] == "testuser"
        assert data["followers"] == 10000

    def test_to_csv_row(self, sample_profile):
        row = sample_profile.to_csv_row()
        assert row[0] == "testuser"
        assert row[5] == 10000  # followers
        assert row[9] is False  # is_private
        assert row[10] is True  # is_verified

    def test_default_values(self):
        p = Profile(username="newuser")
        assert p.followers == 0
        assert p.is_private is False
        assert p.is_verified is False
        assert p.cached_at  # should have a timestamp


class TestPost:
    """Tests for Post data model."""

    @pytest.fixture
    def sample_post(self):
        return Post(
            shortcode="ABC123",
            owner="testuser",
            caption="Check this out! #awesome #test @friend",
            post_url="https://instagram.com/p/ABC123/",
            post_type="GraphImage",
            like_count=500,
            comment_count=25,
            media_urls=["https://example.com/media.jpg"],
            hashtags=["awesome", "test"],
            mentions=["friend"],
        )

    def test_to_dict(self, sample_post):
        d = sample_post.to_dict()
        assert d["shortcode"] == "ABC123"
        assert d["like_count"] == 500

    def test_to_json(self, sample_post):
        data = json.loads(sample_post.to_json())
        assert data["shortcode"] == "ABC123"
        assert data["hashtags"] == ["awesome", "test"]

    def test_default_values(self):
        p = Post(shortcode="XYZ")
        assert p.like_count == 0
        assert p.media_urls == []
        assert p.hashtags == []


class TestReel:
    """Tests for Reel data model."""

    def test_reel_creation(self):
        reel = Reel(
            shortcode="REEL1",
            owner="testuser",
            caption="My first reel",
            view_count=10000,
            like_count=500,
            duration=15.5,
        )
        assert reel.shortcode == "REEL1"
        assert reel.view_count == 10000
        assert reel.duration == 15.5

    def test_to_json(self):
        reel = Reel(shortcode="REEL1", owner="user")
        data = json.loads(reel.to_json())
        assert data["shortcode"] == "REEL1"


class TestStory:
    """Tests for Story data model."""

    def test_story_creation(self):
        story = Story(
            owner="testuser",
            media_url="https://example.com/story.jpg",
            media_type="GraphImage",
        )
        assert story.owner == "testuser"
        assert story.media_type == "GraphImage"


class TestHashtag:
    """Tests for Hashtag data model."""

    def test_hashtag_creation(self):
        tag = Hashtag(hashtag="travel", post_count=50000000)
        assert tag.hashtag == "travel"
        assert tag.post_count == 50000000

    def test_to_json(self):
        tag = Hashtag(hashtag="travel", post_count=100)
        data = json.loads(tag.to_json())
        assert data["hashtag"] == "travel"


class TestDataExporter:
    """Tests for DataExporter."""

    @pytest.fixture
    def profiles(self):
        return [
            Profile(username="user1", followers=1000),
            Profile(username="user2", followers=2000),
        ]

    def test_to_json_single(self):
        profile = Profile(username="test", followers=100)
        result = DataExporter.to_json(profile)
        data = json.loads(result)
        assert data["username"] == "test"

    def test_to_json_list(self, profiles):
        result = DataExporter.to_json(profiles)
        data = json.loads(result)
        assert len(data) == 2
        assert data[0]["username"] == "user1"

    def test_to_csv(self, profiles):
        csv = DataExporter.to_csv(profiles)
        lines = csv.strip().split("\n")
        assert len(lines) == 3  # header + 2 rows
        assert "username" in lines[0]

    def test_to_csv_has_correct_headers(self, profiles):
        csv = DataExporter.to_csv(profiles)
        headers = csv.split("\n")[0].split(",")
        assert "username" in headers
        assert "followers" in headers
        assert "is_verified" in headers


class TestExceptions:
    """Tests for custom exceptions."""

    def test_login_required_error(self):
        with pytest.raises(LoginRequiredError):
            raise LoginRequiredError()

    def test_profile_not_found_error(self):
        with pytest.raises(ProfileNotFoundError):
            raise ProfileNotFoundError("nonexistent_user")

    def test_private_profile_error(self):
        with pytest.raises(PrivateProfileError):
            raise PrivateProfileError("private_user")

    def test_rate_limit_error(self):
        with pytest.raises(RateLimitError):
            raise RateLimitError()

    def test_base_exception(self):
        with pytest.raises(InstagramScraperError):
            raise InstagramScraperError("test")

    def test_exception_inheritance(self):
        assert issubclass(LoginRequiredError, InstagramScraperError)
        assert issubclass(ProfileNotFoundError, InstagramScraperError)
        assert issubclass(PrivateProfileError, InstagramScraperError)
        assert issubclass(RateLimitError, InstagramScraperError)
