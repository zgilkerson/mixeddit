class SpotifyError(Exception):
    """Raised when Spotify API calls return an error code."""

    def __init__(self, message):
        self.message = message