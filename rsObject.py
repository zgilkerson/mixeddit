import re

# https://regex101.com/r/T3eOko/10
pattern = re.compile(
    r"^(?P<genre>\[.*\])?[ -]*(?P<artist>.+?(?=( -| - |- )))-(?P<track>.+?(?=( -| - |- |\(|\[|\n|$)))(?P<misc>[-\(\[].*)?$")

class rsObject:
    """Short for Reddit-Spotify Object"""

    def __init__(self, ogTitle):
        self.ogTitle = ogTitle
        self.valid = False
        self.artist = None
        self.track = None
        self.parseRedditTitle()

    def parseRedditTitle(self):
        if "-" not in self.ogTitle or "Shreddit" in self.ogTitle or "「" in self.ogTitle or "[TOUR]" in self.ogTitle:
            return
        else:   
            self.valid = True
            parsedTitle = pattern.match(self.ogTitle)
            if parsedTitle is not None:
                self.artist = parsedTitle.group('artist').strip(' \"')
                self.track = parsedTitle.group('track').strip(' \"')
            if self.artist is None or self.track is None:
                self.valid = False
                self.artist = None
                self.track = None
