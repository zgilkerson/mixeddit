# import praw
import json
from rsObject import rsObject
from spooter import spooter

def main():
    rsObjects = redditGetTitles()
    spotifyUpdatePlaylist(rsObjects)

def redditGetTitles(subreddit='metal', timePeriod='week', limit=100):
    # reddit = praw.Reddit('shreddit2spotify')
    # print('Running in read only mode?')
    # if reddit.read_only is not True:
        # exit()
    rsObjects = []
    # for submission in reddit.subreddit(subreddit).top(timePeriod, limit=100):
    #     parsedTitle = rsObject(submission.title)
    #     if parsedTitle.valid:
    #         rsObjects.append(parsedTitle)
    with open('testCases.json', 'r') as testJson:
        loadedJson = json.load(testJson)
        for i in range(0, len(loadedJson)):
            parsedTitle = rsObject(loadedJson[i]['ogTitle'])
            if parsedTitle.valid:
                rsObjects.append(parsedTitle)
    return rsObjects

def spotifyUpdatePlaylist(rsObjects, playlistName='TopOfShreddit'):
    spotify = spooter()
    playlistID = spotify.playlistGetId(playlistName)
    userID = spotify.currentUserGetId()
    spotifyTrackURIList = []
    for redditTrack in rsObjects:
        searchResults = spotify.search(redditTrack.track, 'track')
        try:
            for spotifyTrack in searchResults['tracks']['items']:
                if(spotifyTrack['artists'][0]['name'].lower() == redditTrack.artist.lower()):
                    spotifyTrackURIList.append(spotifyTrack['uri'])
                    break
        except KeyError:
            print('=============================')
            print(json.dumps(searchResults))
            print('attempted to find track {}'.format(redditTrack.track))
            print('=============================')
    spotify.playlistReplace(userID, playlistID, spotifyTrackURIList) 

if __name__ == '__main__':
    main()
