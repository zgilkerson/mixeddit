import praw

from mixeddit.mixeddit import Mixeddit


class Reddit():

    @staticmethod
    def parseSubreddit(subreddit):
        reddit = praw.Reddit('mixeddit')
        if reddit.read_only is not True:
            exit()
        mixeddit_list = []
        for submission in reddit.subreddit(subreddit
                                           ).top('week', limit=100):
            parsedTitle = Mixeddit(submission.title)
            if parsedTitle.valid:
                mixeddit_list.append(parsedTitle)
        return mixeddit_list
