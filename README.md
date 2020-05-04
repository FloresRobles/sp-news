# sp-news

Create a playlist on Spotify with all the new songs from the artists you follow.

## Quick Start
To get started, simply install the dependencies.

Edit the lines:

```
playlistID = "your playlist ID"
username = "your username"
max_tracks_on_playlist = 400 
country = "FR" 
```

Set your ENV variables:
```
export SPOTIPY_CLIENT_ID='your-spotify-client-id'
export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
export SPOTIPY_REDIRECT_URI='your-app-redirect-url'
```

Run locally, and login into spotify.

```
sh run.sh
```

Use the generated file to schedule it in a web service like heroku. 

Chill and wake up to your new music.