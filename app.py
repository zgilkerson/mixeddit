import praw
from rsObject import rsObject

reddit = praw.Reddit('shreddit2spotify')

# Possible regex
# https://regex101.com/r/T3eOko/10
def parseTitle(title):
    return rsObject(title)

def main():
    print('Running in read only mode?')
    if reddit.read_only is not True:
        exit()
    for submission in reddit.subreddit('metal').top('week', limit=100):
        print(parseTitle(submission.title))

if __name__ == '__main__':
    main()
