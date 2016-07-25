# sp-news

Create a playlist on Spotify with all the new songs from the artists you follow

## Dependencies

- [Spotipy](https://github.com/plamere/spotipy) - this requires that to be installed
- [Requests](https://github.com/kennethreitz/requests) - also this

## Quick Start
To get started, simply install spotipy and requests

Edit the lines:
```
playlistID = "your playlist ID"
username = "your username"
max_tracks_on_playlist = 400 # or whatever number of songs you want
```

And set your ENV variables:
```
export SPOTIPY_CLIENT_ID='your-spotify-client-id'
export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
export SPOTIPY_REDIRECT_URI='your-app-redirect-url'
export IFTTT_URL='an-ifttt-maker-trigger-url'
```

And run it...
