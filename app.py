import praw
import json
from mixeddit import Mixeddit
from spotify import Spotify


def main():
    rs = reddit_get_titles()
    spotify_update_playlist(rs)


def reddit_get_titles(subreddit='metal', time_period='week', limit=100):
    reddit = praw.Reddit('mixeddit')
    print('Running in read only mode?')
    if reddit.read_only is not True:
        exit()
    mixeddit_list = []
    for submission in reddit.subreddit(subreddit).top(time_period, limit=100):
        parsedTitle = Mixeddit(submission.title)
        if parsedTitle.valid:
            mixeddit_list.append(parsedTitle)
    # with open('testFiles/Reddit/parseRedditTitle.json', 'r') as json_file:
    #     test_json = json.load(json_file)
    #     for submission in range(0, len(test_json)):
    #         parsed_title = Mixeddit(test_json[submission]['ogTitle'])
    #         if parsed_title.valid:
    #             mixeddit_list.append(parsed_title)
    return mixeddit_list


def spotify_update_playlist(mixeddit_list, playlist_name='TopOfShreddit'):
    spotify = Spotify()
    user_id = spotify.user_get_current_user_id()
    playlist_id = spotify.playlist_get_id(user_id, playlist_name)
    track_uri_list = []
    for reddit_track in mixeddit_list:
        search_results = spotify.search(reddit_track.track, 'track')
        try:
            for spotify_track in search_results['tracks']['items']:
                if (spotify_track['artists'][0]['name'].lower() ==
                        reddit_track.artist.lower()):
                    track_uri_list.append(spotify_track['uri'])
                    break
        except KeyError:
            print('=============================')
            print(json.dumps(search_results))
            print('attempted to find track {}'.format(reddit_track.track))
            print('=============================')
    spotify.playlist_replace(user_id, playlist_id, track_uri_list)


if __name__ == '__main__':
    main()
