class LauncherError(Exception):
    """Base exception for launcher errors"""
    pass

class UpdateError(LauncherError):
    """Raised when there's an error during update process"""
    pass

class DownloadError(LauncherError):
    """Raised when there's an error during file download"""
    pass

class ExtractionError(LauncherError):
    """Raised when there's an error during file extraction"""
    pass
