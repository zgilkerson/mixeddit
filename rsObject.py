class rsObject:
    def __init__(self, ogTitle):
        self.ogTitle = ogTitle
        self.parseRedditTitle(ogTitle)

    def parseRedditTitle(self, ogTitle):
        self.parsable = ogTitle
        self.artist = ogTitle
        self.track = ogTitle
