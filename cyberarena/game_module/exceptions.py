class CyberArenaGameModuleError(Exception):
    """Base exception for cyberarena game module."""


class LibraryError(CyberArenaGameModuleError):
    """Base exception for library."""


class LibraryFileNotFoundError(LibraryError, FileNotFoundError):
    """Exception for library for file not found."""
