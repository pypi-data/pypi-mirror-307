"""Custom exceptions for the Quarto Paper Fetcher."""


class QuartoFetchError(Exception):
    """Base exception for all Quarto Paper Fetcher errors."""

    pass


class GitError(QuartoFetchError):
    """Base exception for git operations."""

    pass


class GitTimeoutError(GitError):
    """Raised when git operations timeout."""

    pass


class GitAuthenticationError(GitError):
    """Raised when git authentication fails."""

    pass


class QuartoError(QuartoFetchError):
    """Base exception for Quarto operations."""

    pass


class ConfigurationError(QuartoFetchError):
    """Raised for configuration-related errors."""

    pass
