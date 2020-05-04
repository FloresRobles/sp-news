#!/usr/bin/env python3

import os
import spotipy
import spotipy.util as util
import telegram

playlist_id = "3Kz9W3n6zGkHVBtoGU9mwI"
username = "floresrobles"
max_tracks_on_playlist = 400
country = "FR" 

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
        response = sp.artist_albums(artist['id'], album_type=type, country=country)
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

def get_playlist(sp, playlist_id):
    results = sp.user_playlist(username, playlist_id, fields="tracks,next")
    tracks = results['tracks']
    items = tracks["items"]
    while tracks['next']:
        tracks = sp.next(tracks)
        items.extend(tracks["items"])
    return items

def set_tracks(sp, tracks, playlist_id):
    sp.user_playlist_replace_tracks(username, playlist_id, [track["uri"] for track in tracks[0:max_tracks_per_call]])
    for start in range(max_tracks_per_call, max_tracks_on_playlist, max_tracks_per_call):
        sp.user_playlist_add_tracks(username, playlist_id, [track["uri"] for track in tracks[start:start + max_tracks_per_call]])

def get_news():
  token = util.prompt_for_user_token(username, scope = scope)

  if token:
    sp = spotipy.Spotify(auth=token)
    artists = fetch_followed_artists(sp)
    albums = fetch_albums(sp, artists, 'album,single')
    full_albums = fetch_full_albums(sp, albums)
    ordered_albums = order_albums(full_albums)
    tracks = filter_tracks(sp, ordered_albums)[:max_tracks_on_playlist]
    old_tracks = get_playlist(sp, playlist_id)
    old_tracks_ids = [track["track"]["id"] for track in old_tracks]
    tracks_ids = [track["id"] for track in tracks]
    new_tracks_ids = [val for val in tracks_ids if val not in old_tracks_ids]
    new_tracks = [track["artists"][0]["name"] + ", "  + track["name"] for track in tracks if track["id"] in new_tracks_ids]
    if len(new_tracks_ids) > 0:
      set_tracks(sp, tracks, playlist_id)
      bot = telegram.Bot(token=os.getenv('TELEGRAM_TOKEN'))
      bot.send_message(chat_id=os.getenv('TELEGRAM_CHAT_ID'), text="\n".join(new_tracks)[0:4095])

  else:
    print("Update token in env")

get_news()
