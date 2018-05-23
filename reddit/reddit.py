import praw

from mixeddit.mixeddit import Mixeddit


class Reddit():

    @staticmethod
    def parseSubreddit(subreddit, sort_by, time_filter, limit):
        reddit = praw.Reddit('mixeddit')
        if reddit.read_only is not True:
            exit()
        mixeddit_list = []
        subreddits = []
        if not time_filter:
            time_filter = 'week'
        if sort_by == 'hot':
            subreddits = reddit.subreddit(subreddit).hot(limit=limit)
        elif sort_by == 'new':
            subreddits = reddit.subreddit(subreddit).new(limit=limit)
        elif sort_by == 'rising':
            subreddits = reddit.subreddit(subreddit).rising(limit=limit)
        elif sort_by == 'controversial':
            subreddits = (reddit.subreddit(subreddit).
                          controversial(time_filter=time_filter, limit=limit))
        elif sort_by == 'top':
            subreddits = (reddit.subreddit(subreddit).
                          top(time_filter=time_filter, limit=limit))
        for submission in subreddits:
            parsedTitle = Mixeddit(submission.title)
            if parsedTitle.valid:
                mixeddit_list.append(parsedTitle)
        return mixeddit_list
