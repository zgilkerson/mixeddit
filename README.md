Concept:

    Take the top of the week from [Shreddit](reddit.com/r/metal) and pipe it into a spotify playlist.

### The Files
* [`app.py`](app.py)
    * Main file for now. When ran will grab the top 100 posts of the past week.
* [`rsObject.py`](rsObject.py)
    * Reddit-Spotify Object. Has attributes like the original reddit post name, if it is a valid song, and what the artist and track name are.
* [`spooter.py`](spooter.py)
    * Spotify API wrapper
* `test*.py`
    * test files for the respective py files