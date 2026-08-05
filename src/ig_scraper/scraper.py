"""
Instagram Account Scraper - Core scraper engine.

Uses instaloader as the backend for accessing Instagram's data.
Provides a clean, typed API for scraping profiles, posts, reels,
stories, hashtags, and follower data.

Usage:
    from ig_scraper import InstagramScraper

    scraper = InstagramScraper()
    profile = scraper.get_profile("nasa")
    print(profile.followers)  # 85000000

    # With login for private data
    scraper.login("username", "password")
    posts = scraper.get_posts("username", limit=10)
"""

from __future__ import annotations

import os
import json
import time
import logging
from typing import Optional
from datetime import datetime

try:
    import instaloader
except ImportError:
    instaloader = None

from ig_scraper.models import Profile, Post, Reel, Story, Hashtag, DataExporter
from ig_scraper.exceptions import (
    InstagramScraperError,
    LoginRequiredError,
    RateLimitError,
    ProfileNotFoundError,
    PrivateProfileError,
    ConnectionError,
)
from ig_scraper.utils import (
    rate_limit, retry, parse_hashtags, parse_mentions,
    sanitize_filename, ProgressBar,
)

logger = logging.getLogger("ig_scraper")


class InstagramScraper:
    """Scraper for Instagram account data.

    Scrapes public (and private with login) Instagram profile data including
    profile info, posts, reels, stories, hashtags, and follower lists.

    Args:
        username: Instagram username for login (optional).
        password: Instagram password for login (optional).
        session_file: Path to session file for login persistence.
        proxy: Proxy URL (e.g., "http://user:pass@host:port").
        rate_limit_delay: Delay between requests in seconds.
        user_agent: Custom user agent string.
        max_retries: Maximum retry attempts for failed requests.

    Example:
        >>> scraper = InstagramScraper()
        >>> profile = scraper.get_profile("natgeo")
        >>> print(f"{profile.full_name}: {profile.followers} followers")

        >>> # Login for private data
        >>> scraper = InstagramScraper(username="myuser", password="mypass")
        >>> posts = scraper.get_posts("private_account", limit=20)
    """

    def __init__(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        session_file: Optional[str] = None,
        proxy: Optional[str] = None,
        rate_limit_delay: float = 2.0,
        user_agent: Optional[str] = None,
        max_retries: int = 3,
    ):
        if instaloader is None:
            raise ImportError(
                "instaloader is required. Install with: pip install instaloader"
            )

        self.username = username
        self.password = password
        self.session_file = session_file or os.path.join(
            os.path.expanduser("~"), ".ig_scraper_session"
        )
        self.proxy = proxy
        self.rate_limit_delay = rate_limit_delay
        self.max_retries = max_retries
        self._logged_in = False

        # Initialize instaloader
        loader_kwargs = {
            "download_videos": False,
            "download_video_thumbnails": False,
            "download_comments": True,
            "save_metadata": False,
            "post_metadata_txt_pattern": "",
            "storyitem_metadata_txt_pattern": "",
            "max_connection_attempts": max_retries,
        }

        if user_agent:
            loader_kwargs["user_agent"] = user_agent

        if proxy:
            loader_kwargs["proxy"] = proxy

        self.loader = instaloader.Instaloader(**loader_kwargs)

        # Auto-login if credentials provided
        if username and password:
            self.login(username, password)
        elif session_file and os.path.exists(self.session_file):
            self._load_session()

    # === Login Management ===

    def login(self, username: str, password: str) -> bool:
        """Login to Instagram for accessing private data and higher rate limits.

        Args:
            username: Instagram username.
            password: Instagram password.

        Returns:
            True if login successful.

        Raises:
            LoginRequiredError: If login fails.
        """
        try:
            self.loader.login(username, password)
            self.loader.save_session_to_file(self.session_file)
            self.username = username
            self._logged_in = True
            logger.info(f"Logged in as @{username}")
            return True
        except Exception as e:
            raise LoginRequiredError(
                f"Login failed for @{username}: {e}. "
                "Instagram may require 2FA or session verification."
            )

    def _load_session(self) -> bool:
        """Load saved session from file."""
        try:
            self.loader.load_session_from_file(self.username or "", self.session_file)
            self._logged_in = True
            logger.info("Session loaded from file")
            return True
        except Exception as e:
            logger.warning(f"Failed to load session: {e}")
            return False

    def logout(self):
        """Logout and remove session file."""
        self.loader.close()
        self._logged_in = False
        if os.path.exists(self.session_file):
            os.remove(self.session_file)
            logger.info("Session removed")

    @property
    def is_logged_in(self) -> bool:
        """Check if currently logged in."""
        return self._logged_in

    # === Profile Scraping ===

    @rate_limit(min_delay=1.0, max_delay=2.5)
    @retry(max_retries=3, backoff_factor=2.0)
    def get_profile(self, username: str) -> Profile:
        """Scrape an Instagram user's profile information.

        Args:
            username: Instagram username to scrape.

        Returns:
            Profile object with all public profile data.

        Raises:
            ProfileNotFoundError: If profile doesn't exist.
            PrivateProfileError: If profile is private and not logged in as follower.
            LoginRequiredError: If login is needed but not provided.

        Example:
            >>> scraper = InstagramScraper()
            >>> profile = scraper.get_profile("nasa")
            >>> print(profile.followers)  # 85000000
            >>> print(profile.biography)
        """
        logger.info(f"Scraping profile: @{username}")

        try:
            profile = instaloader.Profile.from_username(
                self.loader.context, username
            )
        except instaloader.exceptions.ProfileNotExistsException:
            raise ProfileNotFoundError(username)
        except instaloader.exceptions.PrivateProfileNotFollowedException:
            raise PrivateProfileError(username)
        except Exception as e:
            if "login" in str(e).lower():
                raise LoginRequiredError(str(e))
            raise InstagramScraperError(f"Failed to scrape profile @{username}: {e}")

        return Profile(
            username=profile.username,
            user_id=str(profile.userid),
            full_name=profile.full_name,
            biography=profile.biography,
            external_url=profile.external_url or "",
            followers=profile.followers,
            following=profile.followees,
            posts_count=profile.mediacount,
            is_private=profile.is_private,
            is_verified=profile.is_verified,
            is_business=profile.is_business_account,
            business_category=profile.business_category_name or "",
            profile_pic_url=profile.profile_pic_url,
            profile_pic_hd_url=getattr(profile, "profile_pic_url_hd", profile.profile_pic_url),
        )

    # === Posts Scraping ===

    @rate_limit(min_delay=1.5, max_delay=3.0)
    @retry(max_retries=3, backoff_factor=2.0)
    def get_posts(
        self,
        username: str,
        limit: int = 12,
        only_posts: bool = True,
        only_reels: bool = False,
    ) -> list[Post]:
        """Scrape recent posts from an Instagram profile.

        Args:
            username: Instagram username.
            limit: Maximum number of posts to scrape (default 12).
            only_posts: Filter to only show photo/carousel posts.
            only_reels: Filter to only show reels/video posts.

        Returns:
            List of Post objects.

        Example:
            >>> posts = scraper.get_posts("nasa", limit=10)
            >>> for post in posts:
            ...     print(f"{post.shortcode}: {post.like_count} likes")
        """
        logger.info(f"Scraping {limit} posts from @{username}")

        try:
            profile = instaloader.Profile.from_username(
                self.loader.context, username
            )
        except instaloader.exceptions.ProfileNotExistsException:
            raise ProfileNotFoundError(username)
        except instaloader.exceptions.PrivateProfileNotFollowedException:
            raise PrivateProfileError(username)

        posts = []
        count = 0

        with ProgressBar(min(limit, profile.mediacount), f"Scraping @{username}") as bar:
            for post in profile.get_posts():
                if count >= limit:
                    break

                post_type = self._get_post_type(post)
                is_reel = post_type == "GraphVideo" and post.typename == "GraphVideo"

                if only_posts and is_reel:
                    bar.update()
                    continue
                if only_reels and not is_reel:
                    bar.update()
                    continue

                media_urls = []
                if post.typename == "GraphSidecar":
                    for node in post.get_sidecar_nodes():
                        media_urls.append(node.video_url if node.is_video else node.url)
                else:
                    media_urls.append(post.video_url if post.is_video else post.url)

                caption = post.caption or ""
                tagged = []
                try:
                    tagged = [tag.username for tag in post.get_tags()]
                except Exception:
                    pass

                posts.append(Post(
                    shortcode=post.shortcode,
                    owner=username,
                    caption=caption,
                    post_url=f"https://www.instagram.com/p/{post.shortcode}/",
                    post_type=post.typename,
                    like_count=post.likes,
                    comment_count=post.comments,
                    view_count=getattr(post, "video_view_count", 0) or 0,
                    timestamp=post.date.utc_isoformat() if post.date else "",
                    location=str(post.location) if post.location else "",
                    media_urls=media_urls,
                    tagged_users=tagged,
                    hashtags=parse_hashtags(caption),
                    mentions=parse_mentions(caption),
                ))

                count += 1
                bar.update()

        logger.info(f"Scraped {len(posts)} posts from @{username}")
        return posts

    # === Reels Scraping ===

    def get_reels(self, username: str, limit: int = 12) -> list[Reel]:
        """Scrape recent reels from an Instagram profile.

        Args:
            username: Instagram username.
            limit: Maximum number of reels to scrape.

        Returns:
            List of Reel objects.

        Note:
            Instagram's Reels API is limited. This method filters
            video posts from the user's feed.
        """
        logger.info(f"Scraping reels from @{username}")

        posts = self.get_posts(username, limit=limit * 3)
        reels = []

        for post in posts:
            if post.post_type == "GraphVideo":
                reels.append(Reel(
                    shortcode=post.shortcode,
                    owner=username,
                    caption=post.caption,
                    video_url=post.media_urls[0] if post.media_urls else "",
                    thumbnail_url="",
                    view_count=post.view_count,
                    like_count=post.like_count,
                    comment_count=post.comment_count,
                    play_count=post.view_count,
                    timestamp=post.timestamp,
                ))
                if len(reels) >= limit:
                    break

        logger.info(f"Scraped {len(reels)} reels from @{username}")
        return reels

    # === Stories Scraping ===

    def get_stories(self, usernames: list[str]) -> dict:
        """Scrape active stories from Instagram profiles.

        Args:
            usernames: List of Instagram usernames.

        Returns:
            Dict mapping username -> list of Story objects.

        Raises:
            LoginRequiredError: Stories require authentication.

        Example:
            >>> scraper.login("user", "pass")
            >>> stories = scraper.get_stories(["nasa", "natgeo"])
            >>> for user, user_stories in stories.items():
            ...     print(f"@{user}: {len(user_stories)} active stories")
        """
        if not self._logged_in:
            raise LoginRequiredError("Scraping stories requires Instagram login.")

        logger.info(f"Scraping stories for {len(usernames)} users")

        results = {}

        for username in usernames:
            try:
                profile = instaloader.Profile.from_username(
                    self.loader.context, username
                )
                stories = []

                for story in self.loader.get_stories(userids=[profile.userid]):
                    for item in story.get_items():
                        stories.append(Story(
                            owner=username,
                            media_url=item.video_url if item.is_video else item.url,
                            media_type=item.typename,
                            timestamp=item.date.utc_isoformat() if item.date else "",
                            duration=getattr(item, "video_duration", 0.0) or 0.0,
                        ))

                results[username] = stories
                logger.info(f"  @{username}: {len(stories)} stories")

            except Exception as e:
                logger.error(f"Failed to scrape stories for @{username}: {e}")
                results[username] = []

        return results

    # === Hashtag Scraping ===

    @rate_limit(min_delay=2.0, max_delay=4.0)
    @retry(max_retries=2, backoff_factor=3.0)
    def get_hashtag_posts(self, hashtag: str, limit: int = 20) -> Hashtag:
        """Scrape posts for a given hashtag.

        Args:
            hashtag: Hashtag without the # symbol.
            limit: Maximum number of posts to scrape.

        Returns:
            Hashtag object with top and recent posts.

        Example:
            >>> result = scraper.get_hashtag_posts("travel", limit=10)
            >>> print(f"#{result.hashtag}: {result.post_count} posts")
        """
        hashtag = hashtag.lstrip("#")
        logger.info(f"Scraping hashtag: #{hashtag}")

        try:
            hashtag_obj = instaloader.Hashtag.from_name(
                self.loader.context, hashtag
            )
        except Exception as e:
            raise InstagramScraperError(f"Failed to scrape hashtag #{hashtag}: {e}")

        posts = []
        count = 0

        for post in hashtag_obj.get_posts():
            if count >= limit:
                break
            caption = post.caption or ""
            posts.append(Post(
                shortcode=post.shortcode,
                owner=post.owner_username,
                caption=caption,
                post_url=f"https://www.instagram.com/p/{post.shortcode}/",
                post_type=post.typename,
                like_count=post.likes,
                comment_count=post.comments,
                timestamp=post.date.utc_isoformat() if post.date else "",
                media_urls=[post.video_url if post.is_video else post.url],
                hashtags=parse_hashtags(caption),
                mentions=parse_mentions(caption),
            ))
            count += 1

        return Hashtag(
            hashtag=hashtag,
            post_count=hashtag_obj.mediacount,
            top_posts=posts,
        )

    # === Follower/Following Scraping ===

    def get_followers(self, username: str, limit: int = 100) -> list[str]:
        """Get a list of an account's followers.

        Args:
            username: Instagram username.
            limit: Maximum followers to retrieve.

        Returns:
            List of follower usernames.

        Raises:
            LoginRequiredError: Follower scraping requires authentication.
        """
        if not self._logged_in:
            raise LoginRequiredError("Scraping followers requires Instagram login.")

        logger.info(f"Scraping {limit} followers from @{username}")

        try:
            profile = instaloader.Profile.from_username(
                self.loader.context, username
            )
        except instaloader.exceptions.ProfileNotExistsException:
            raise ProfileNotFoundError(username)

        followers = []
        count = 0

        with ProgressBar(limit, f"Followers @{username}") as bar:
            for follower in profile.get_followers():
                if count >= limit:
                    break
                followers.append(follower.username)
                count += 1
                bar.update()

        return followers

    def get_following(self, username: str, limit: int = 100) -> list[str]:
        """Get a list of accounts that a user is following.

        Args:
            username: Instagram username.
            limit: Maximum following to retrieve.

        Returns:
            List of following usernames.

        Raises:
            LoginRequiredError: Following scraping requires authentication.
        """
        if not self._logged_in:
            raise LoginRequiredError("Scraping following requires Instagram login.")

        logger.info(f"Scraping {limit} following from @{username}")

        try:
            profile = instaloader.Profile.from_username(
                self.loader.context, username
            )
        except instaloader.exceptions.ProfileNotExistsException:
            raise ProfileNotFoundError(username)

        following = []
        count = 0

        with ProgressBar(limit, f"Following @{username}") as bar:
            for followee in profile.get_followees():
                if count >= limit:
                    break
                following.append(followee.username)
                count += 1
                bar.update()

        return following

    # === Email Extraction ===

    def extract_emails(self, username: str, posts_limit: int = 50) -> list[str]:
        """Extract email addresses from a profile's bio and recent posts.

        Args:
            username: Instagram username.
            posts_limit: Number of posts to scan for emails.

        Returns:
            List of unique email addresses found.

        Example:
            >>> emails = scraper.extract_emails("somebusiness")
            >>> print(emails)  # ['contact@somebusiness.com']
        """
        import re

        email_pattern = re.compile(
            r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
        )
        emails = set()

        # Get emails from bio
        try:
            profile = self.get_profile(username)
            if profile.biography:
                found = email_pattern.findall(profile.biography)
                emails.update(found)
            if profile.external_url:
                found = email_pattern.findall(profile.external_url)
                emails.update(found)
        except Exception as e:
            logger.warning(f"Failed to get profile for email extraction: {e}")

        # Get emails from post captions
        try:
            posts = self.get_posts(username, limit=posts_limit)
            for post in posts:
                if post.caption:
                    found = email_pattern.findall(post.caption)
                    emails.update(found)
        except Exception as e:
            logger.warning(f"Failed to get posts for email extraction: {e}")

        return sorted(emails)

    # === Batch Operations ===

    def scrape_all(self, username: str, posts_limit: int = 12) -> dict:
        """Scrape all available data for an Instagram account.

        Args:
            username: Instagram username.
            posts_limit: Maximum posts to scrape.

        Returns:
            Dict with profile, posts, and optionally reels data.

        Example:
            >>> data = scraper.scrape_all("nasa")
            >>> print(data["profile"].followers)
            >>> print(len(data["posts"]))
        """
        result = {"username": username}

        # Profile
        try:
            result["profile"] = self.get_profile(username)
        except Exception as e:
            logger.error(f"Failed to scrape profile: {e}")
            result["profile"] = None

        # Posts
        try:
            result["posts"] = self.get_posts(username, limit=posts_limit)
        except Exception as e:
            logger.error(f"Failed to scrape posts: {e}")
            result["posts"] = []

        # Reels
        try:
            result["reels"] = self.get_reels(username, limit=12)
        except Exception as e:
            logger.error(f"Failed to scrape reels: {e}")
            result["reels"] = []

        # Emails
        try:
            result["emails"] = self.extract_emails(username, posts_limit)
        except Exception as e:
            logger.error(f"Failed to extract emails: {e}")
            result["emails"] = []

        return result

    def batch_scrape(self, usernames: list[str], posts_limit: int = 5) -> list[dict]:
        """Scrape multiple Instagram accounts in batch.

        Args:
            usernames: List of Instagram usernames.
            posts_limit: Posts to scrape per account.

        Returns:
            List of scrape result dicts.

        Example:
            >>> results = scraper.batch_scrape(["nasa", "natgeo", "natgeotravel"])
            >>> for r in results:
            ...     print(f"@{r['username']}: {r['profile'].followers} followers")
        """
        results = []
        total = len(usernames)

        with ProgressBar(total, "Batch scraping") as bar:
            for i, username in enumerate(usernames):
                logger.info(f"[{i+1}/{total}] Scraping @{username}")
                try:
                    data = self.scrape_all(username, posts_limit=posts_limit)
                    results.append(data)
                except Exception as e:
                    logger.error(f"Failed to scrape @{username}: {e}")
                    results.append({"username": username, "error": str(e)})
                bar.update()

        return results

    # === Export ===

    def export_profile(self, profile: Profile, format: str = "json", output: str = None):
        """Export profile data in multiple formats.

        Args:
            profile: Profile object to export.
            format: Output format (json, csv, excel).
            output: Output file path. If None, returns string.
        """
        if format == "json":
            data = profile.to_json()
            if output:
                with open(output, "w", encoding="utf-8") as f:
                    f.write(data)
            return data
        elif format == "csv":
            return DataExporter.to_csv([profile], output)
        elif format == "excel":
            if not output:
                raise ValueError("output file path required for Excel format")
            DataExporter.to_excel(profile, output)
        else:
            raise ValueError(f"Unsupported format: {format}")

    # === Internal Helpers ===

    @staticmethod
    def _get_post_type(post) -> str:
        """Determine post type from instaloader post object."""
        return getattr(post, "typename", "GraphImage")
