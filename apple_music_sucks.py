import requests
from bs4 import BeautifulSoup
import json
import re

TEST_URL = "https://music.apple.com/us/playlist/music/pl.u-38oWZyEtPmrV1p6"
def get_songs(url):
    response = requests.get(url)

    mybytes = response.text

    with open('playlist_html', "w", encoding="utf-8") as f:
        f.write(mybytes)

    with open('playlist_html', 'r', encoding='utf-8') as f:
        contents = f.read()

    soup = BeautifulSoup(contents, 'html.parser')

    # Find the <script> tag with the id 'serialized-server-data'
    script_tag = soup.find('script', {'id': 'serialized-server-data'})

    # Extract the JSON string from this tag
    json_str = script_tag.string if script_tag else ''

    # Parse the JSON string into a Python object
    json_data = json.loads(json_str)

    songs = [{}] * len(json_data[0]['data']['seoData']['ogSongs'])
    for idx, song in enumerate(json_data[0]['data']['seoData']['ogSongs']):
        songs[idx] = {"song_name":song['attributes']['name'], "artist_name": song['attributes']['artistName']}

    return songs