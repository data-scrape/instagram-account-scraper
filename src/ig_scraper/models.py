"""
Data models for Instagram scraped data.

Defines typed dataclasses for Profile, Post, Story, Reel, and Hashtag
to provide structured, serializable output.
"""

from __future__ import annotations

import json
import csv
import io
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Optional


@dataclass
class Profile:
    """Instagram user profile data."""

    username: str
    user_id: str = ""
    full_name: str = ""
    biography: str = ""
    external_url: str = ""
    followers: int = 0
    following: int = 0
    posts_count: int = 0
    is_private: bool = False
    is_verified: bool = False
    is_business: bool = False
    business_category: str = ""
    profile_pic_url: str = ""
    profile_pic_hd_url: str = ""
    cached_at: str = field(default_factory=lambda: datetime.utcnow().isoformat())

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    def to_csv_row(self) -> list:
        d = self.to_dict()
        return [
            d["username"], d["user_id"], d["full_name"], d["biography"],
            d["external_url"], d["followers"], d["following"], d["posts_count"],
            d["is_private"], d["is_verified"], d["is_business"],
            d["business_category"], d["profile_pic_url"], d["cached_at"],
        ]


@dataclass
class Post:
    """Instagram post data (photo, carousel, or video)."""

    shortcode: str
    owner: str = ""
    caption: str = ""
    post_url: str = ""
    post_type: str = ""  # GraphImage, GraphVideo, GraphSidecar
    like_count: int = 0
    comment_count: int = 0
    view_count: int = 0  # for videos
    timestamp: str = ""
    location: str = ""
    media_urls: list = field(default_factory=list)
    tagged_users: list = field(default_factory=list)
    hashtags: list = field(default_factory=list)
    mentions: list = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)


@dataclass
class Reel:
    """Instagram Reel data."""

    shortcode: str
    owner: str = ""
    caption: str = ""
    video_url: str = ""
    thumbnail_url: str = ""
    view_count: int = 0
    like_count: int = 0
    comment_count: int = 0
    play_count: int = 0
    duration: float = 0.0
    timestamp: str = ""
    music_title: str = ""
    music_artist: str = ""

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)


@dataclass
class Story:
    """Instagram Story data."""

    owner: str
    media_url: str = ""
    media_type: str = ""  # GraphImage, GraphVideo
    timestamp: str = ""
    duration: float = 0.0
    view_count: int = 0
    caption: str = ""
    story_url: str = ""

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)


@dataclass
class Hashtag:
    """Instagram hashtag data."""

    hashtag: str
    post_count: int = 0
    top_posts: list = field(default_factory=list)
    recent_posts: list = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)

    def to_json(self, indent: int = 2) -> str:
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)


class DataExporter:
    """Export scraped data to multiple formats."""

    CSV_PROFILE_HEADERS = [
        "username", "user_id", "full_name", "biography",
        "external_url", "followers", "following", "posts_count",
        "is_private", "is_verified", "is_business",
        "business_category", "profile_pic_url", "cached_at",
    ]

    CSV_POST_HEADERS = [
        "shortcode", "owner", "caption", "post_url", "post_type",
        "like_count", "comment_count", "view_count", "timestamp",
        "location", "media_urls", "tagged_users", "hashtags", "mentions",
    ]

    @staticmethod
    def to_json(data, indent: int = 2) -> str:
        """Export single object or list to JSON string."""
        if isinstance(data, list):
            return json.dumps(
                [d.to_dict() if hasattr(d, "to_dict") else d for d in data],
                indent=indent, ensure_ascii=False,
            )
        if hasattr(data, "to_dict"):
            return data.to_json(indent=indent)
        return json.dumps(data, indent=indent, ensure_ascii=False)

    @staticmethod
    def to_csv(profiles: list, output: str | None = None) -> str:
        """Export profiles list to CSV. Returns CSV string or writes to file."""
        buf = io.StringIO()
        writer = csv.writer(buf)
        writer.writerow(DataExporter.CSV_PROFILE_HEADERS)
        for p in profiles:
            if hasattr(p, "to_csv_row"):
                writer.writerow(p.to_csv_row())
            else:
                writer.writerow([p.get(h, "") for h in DataExporter.CSV_PROFILE_HEADERS])
        result = buf.getvalue()
        buf.close()
        if output:
            with open(output, "w", newline="", encoding="utf-8") as f:
                f.write(result)
        return result

    @staticmethod
    def to_excel(data, output: str) -> None:
        """Export data to Excel file (requires openpyxl)."""
        try:
            from openpyxl import Workbook
        except ImportError:
            raise ImportError(
                "openpyxl is required for Excel export. "
                "Install with: pip install openpyxl"
            )
        wb = Workbook()

        if isinstance(data, Profile):
            ws = wb.active
            ws.title = "Profile"
            d = data.to_dict()
            for key, value in d.items():
                ws.append([key, value])
        elif isinstance(data, list) and data and isinstance(data[0], Profile):
            ws = wb.active
            ws.title = "Profiles"
            ws.append(DataExporter.CSV_PROFILE_HEADERS)
            for p in data:
                ws.append(p.to_csv_row())
        elif isinstance(data, list) and data and isinstance(data[0], Post):
            ws = wb.active
            ws.title = "Posts"
            ws.append(DataExporter.CSV_POST_HEADERS)
            for p in data:
                d = p.to_dict()
                ws.append([
                    d["shortcode"], d["owner"], d["caption"], d["post_url"],
                    d["post_type"], d["like_count"], d["comment_count"],
                    d["view_count"], d["timestamp"], d["location"],
                    "|".join(d["media_urls"]), "|".join(d["tagged_users"]),
                    "|".join(d["hashtags"]), "|".join(d["mentions"]),
                ])

        wb.save(output)
