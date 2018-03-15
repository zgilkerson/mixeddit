import re

# https://regex101.com/r/T3eOko/10
REDDIT_TITLE_PATTERN = re.compile(
    r"^(?P<genre>\[.*\])?[ -]*(?P<artist>.+?(?=( -| - |- )))"
    r"-(?P<track>.+?(?=( -| - |- |\(|\[|\n|$)))(?P<misc>[-\(\[].*)?$")


class Mixeddit:
    """Object representing Reddit and Spotify information."""

    def __init__(self, reddit_title):
        self.reddit_title = reddit_title
        self.valid = False
        self.artist = None
        self.track = None
        self.check_title()

    def check_title(self):
        """Checks if the Reddit title is potentially valid."""

        if ("-" not in self.reddit_title or
                "Shreddit" in self.reddit_title or
                "「" in self.reddit_title or
                "[TOUR]" in self.reddit_title):
            return
        self.parse_reddit_title()

    def parse_reddit_title(self):
        """Attempts to pull an artist and track out of the Reddit title."""

        parsedTitle = REDDIT_TITLE_PATTERN.match(self.reddit_title)
        if parsedTitle is not None:
            self.artist = parsedTitle.group('artist').strip(' \"')
            self.track = parsedTitle.group('track').strip(' \"')
            if self.artist is not None and self.track is not None:
                self.valid = True
