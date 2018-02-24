class rsObject:
    def __init__(self, ogTitle):
        self.ogTitle = ogTitle
        self.parseRedditTitle(ogTitle)

    def parseRedditTitle(self, ogTitle):
        if(ogTitle.find('-') == -1):
            self.parsable = False
            self.artist = None
            self.track = None
        else:   
            self.parsable = ogTitle
            self.artist = ogTitle
            self.track = ogTitle
