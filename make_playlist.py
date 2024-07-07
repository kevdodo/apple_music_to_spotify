import base64
import json
import requests

from time import sleep
from gen_playlists import get_client_id, get_client_secret
from apple_music_sucks import get_songs
import pprint

from urllib.parse import quote

client_id = get_client_id()
client_secret = get_client_secret()

TEST_URL = "https://music.apple.com/us/playlist/music/pl.u-38oWZyEtPmrV1p6"

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

with open("code.txt") as f:
    CODE = f.readline().strip("\n")

encoded_credentials = base64.b64encode(client_id.encode() + b':' + client_secret.encode()).decode("utf-8")

token_headers = {
    "Authorization": "Basic " + encoded_credentials,
    "Content-Type": "application/x-www-form-urlencoded"
}

token_data = {
    "grant_type": "authorization_code",
    "code": CODE,
    "redirect_uri": "http://localhost:7777/callback"
}

# r = requests.post("https://accounts.spotify.com/api/token", data=token_data, headers=token_headers)
# print(r)
# token = r.json()['access_token']
# with open("access_token.txt", 'w') as f:
#     f.write(token)

with open("access_token.txt", 'r') as f:
    token = f.read()


def get_user_id(token):
    r = requests.get("https://api.spotify.com/v1/me", headers=get_auth_header(token))
    userid = r.json()['id']
    assert r.status_code == 200
    return userid

def make_playlist(token):
    userid = get_user_id(token)
    new_playlist = {"name": "new palylist",
                    "desc": "playlist",
                    "public": True}

    response = requests.post(
        f'https://api.spotify.com/v1/users/{userid}/playlists',
        headers={**get_auth_header(token), "Content-Type": "application/json"},
        data=json.dumps(new_playlist)
    )
    print(response.json())
    return response.json()


def search_track(token, track_name, artist_name):
    headers = get_auth_header(token)

    url = r'https://api.spotify.com/v1/search?'

    track_name = quote(track_name)
    artist_name = quote(artist_name)

    query = rf'q=name%3A{track_name}%2520artist%3A{artist_name}&type=track&limit=1'

    query = query.replace(" ", "+")

    response = requests.get(url + query, headers=headers)
    print(response)
    return response.json()['tracks']


def add_to_playlist(token, track_uris, playlist_id):

    # userid = get_user_id(token)

    playlist_url_api =  f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks"

    print(type(track_uri))

    add_track = {'uris' : track_uris, 'position': 0}
    print(json.dumps(add_track))

    response = requests.post(
            playlist_url_api,
            headers={**get_auth_header(token), "Content-Type": "application/json"},
            data=json.dumps(add_track)
        )
    
    print(response)


    
if __name__ == '__main__':
    playlist_info = make_playlist(token)
    playlist_id = playlist_info['id']
    print(playlist_id)

    # print(track_uri)

    songs = get_songs(TEST_URL)
    # pprint.pprint(songs)


    # song_name = 'Call This # Now'
    # artist_name = 'The Garden'

    # track_info = search_track(token, song_name, artist_name)
    # track_uri = track_info['items'][0]['uri']
    # print(track_uri)

    track_uris = []
    cnt = 0


    for song in songs:
        song_name, artist_name = song['song_name'], song['artist_name']

        track_info = search_track(token, song_name, artist_name)
        track_uri = track_info['items'][0]['uri']

        print("Adding:", song_name, "   By:", artist_name)
        sleep(3)
        track_uris.append(track_uri)
        cnt += 1
        if cnt == 10:
            cnt = 0
            add_to_playlist(token, track_uris, playlist_id)
            track_uris = []