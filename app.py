# import praw
import json
from rsObject import rsObject
from spooter import spooter

# reddit = praw.Reddit('shreddit2spotify')

def main():
    # print('Running in read only mode?')
    # if reddit.read_only is not True:
        # exit()
    rsObjects = []
    # for submission in reddit.subreddit('metal').top('week', limit=100):
    #     parsedTitle = rsObject(submission.title)
    #     if parsedTitle.valid:
    #         rsObjects.append(parsedTitle)
    with open('testCases.json', 'r') as testJson:
        loadedJson = json.load(testJson)
        for i in range(0, len(loadedJson)):
            parsedTitle = rsObject(loadedJson[i]['ogTitle'])
            if parsedTitle.valid:
                rsObjects.append(parsedTitle)

    spotify = spooter()
    playlistID = spotify.get_playlist_id("TopOfShreddit")
    print(playlistID)
    userID = spotify.get_current_user_id()
    print(userID)
    spotifyTrackURIList = []
    # print(searchResults)
    for redditTrack in rsObjects:
        searchResults = spotify.search(redditTrack.track, 'track')
        try:
            for spotifyTrack in searchResults['tracks']['items']:
                if(spotifyTrack['artists'][0]['name'].lower() == redditTrack.artist.lower()):
                    spotifyTrackURIList.append(spotifyTrack['uri'])
                    break
        except KeyError:
            print("=============================")
            print(json.dumps(searchResults))
            print("attempted to find track {}".format(redditTrack.track))
            print("=============================")
    print("found {} tracks on spotify".format(len(spotifyTrackURIList)))
    spotify.replace_playlist(userID, playlistID, spotifyTrackURIList)
        

if __name__ == '__main__':
    main()
