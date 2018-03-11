class SpotifyError(Exception):
    """Base Class for Spotify.py errors"""
    pass


class SpotifySetUpError(SpotifyError):
    """Raised when Spotify has a problem during __init__."""


class SpotifyRunTimeError(SpotifyError):
    """Raised when Spotify API returns an error code."""
    def __init__(self, error_code, error_message):
        error_str = 'Spotify returned with error code: {}, '\
                    '{}, '.format(error_code, error_message)
        super().__init__(error_str)
        self.error_code = error_code
        self.error_message = error_message
