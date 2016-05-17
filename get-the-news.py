import spotipy
import spotipy.util as util

# https://open.spotify.com/user/floresrobles/playlist/3Kz9W3n6zGkHVBtoGU9mwI
playlistID = "3Kz9W3n6zGkHVBtoGU9mwI"
username = "floresrobles"
max_tracks_on_playlist = 400

scope = 'playlist-modify-public'
max_albums_per_call = 20
max_tracks_per_call = 100

def fetch_followed_artists(sp):
    artists = []
    response = sp.current_user_followed_artists()
    while response:
        artists.extend(response['artists']['items'])
        response = sp.next(response['artists'])
    return artists

def fetch_albums(sp, artists, type):
    albums = []
    for artist in artists:
        response = sp.artist_albums(artist['id'], album_type=type, country="US")
        while response:
            albums.extend(response["items"])
            response = sp.next(response)
    return albums

def fetch_full_albums(sp, albums):
    full_albums = [dict() for x in range(len(albums))]
    for start in range(0, len(albums), max_albums_per_call):
        response = sp.albums([album["id"] for album in albums[start: start + max_albums_per_call]])
        full_albums.extend(response['albums'])
    return full_albums

def order_albums(albums):
    albums = [album for album in albums if "release_date" in album]
    ordered = sorted(albums, key=lambda album: album["release_date"], reverse=True)
    return ordered

def filter_tracks(sp, full_albums):
    tracks = []
    for album in full_albums:
        tracks.extend(album["tracks"]["items"])
    return tracks

def set_tracks(sp, tracks, playlist_id):
    sp.user_playlist_replace_tracks(username, playlist_id, [track["uri"] for track in tracks[0:max_tracks_per_call]])
    for start in range(max_tracks_per_call, max_tracks_on_playlist, max_tracks_per_call):
        sp.user_playlist_add_tracks(username, playlist_id, [track["uri"] for track in tracks[start:start + max_tracks_per_call]])

token = util.prompt_for_user_token(username, scope = scope)

if token:
    sp = spotipy.Spotify(auth=token)
    artists = fetch_followed_artists(sp)
    albums = fetch_albums(sp, artists, 'album,single')
    full_albums = fetch_full_albums(sp, albums)
    ordered_albums = order_albums(full_albums)
    tracks = filter_tracks(sp, ordered_albums)
    set_tracks(sp, tracks, playlistID)
else:
    print("Can't get token for", username)
