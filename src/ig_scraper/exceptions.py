"""Custom exceptions for Instagram Scraper."""


class InstagramScraperError(Exception):
    """Base exception for all Instagram Scraper errors."""

    pass


class LoginRequiredError(InstagramScraperError):
    """Raised when an operation requires Instagram login but none is provided."""

    def __init__(self, message="This operation requires Instagram login credentials."):
        super().__init__(message)


class RateLimitError(InstagramScraperError):
    """Raised when Instagram rate-limits requests."""

    def __init__(self, message="Rate limit exceeded. Please wait before retrying."):
        super().__init__(message)


class ProfileNotFoundError(InstagramScraperError):
    """Raised when a profile is not found."""

    def __init__(self, username):
        super().__init__(f"Profile '{username}' not found or does not exist.")


class PrivateProfileError(InstagramScraperError):
    """Raised when trying to access a private profile without being a follower."""

    def __init__(self, username):
        super().__init__(
            f"Profile '{username}' is private. "
            "Login as a follower to access this profile."
        )


class ConnectionError(InstagramScraperError):
    """Raised when network connection to Instagram fails."""

    pass


class SessionExpiredError(InstagramScraperError):
    """Raised when the Instagram session has expired."""

    def __init__(self):
        super().__init__("Instagram session has expired. Please re-login.")
