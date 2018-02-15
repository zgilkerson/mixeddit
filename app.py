import praw
import re

reddit = praw.Reddit('shreddit2spotify')

# Possible regex
# (?P<genre>\[.*\])?[ -]*(?P<artist>[^-\n]*) - (?P<song>[^-\(\[\n]*)(?P<misc>[-\(\[].*)?
def parseTitle(title):
    return title

def main():
    print('Running in read only mode?')
    if reddit.read_only is not True:
        exit()
    for submission in reddit.subreddit('metal').top('week', limit=100):
        print(parseTitle(submission.title))

if __name__ == '__main__':
    main()
