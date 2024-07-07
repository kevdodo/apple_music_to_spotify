from flask import Flask, request, redirect
from requests_oauthlib import OAuth2Session
from requests.auth import HTTPBasicAuth
import requests
import json

app = Flask(__name__)
with open("client_id") as f:
    CLIENT_ID = f.readline().strip("\n")
# print(client_id)
with open("client_secret") as f:
    CLIENT_SECRET = f.readline().strip("\n")

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
REDIRECT_URI = 'http://localhost:7777/callback'

SCOPE = [
    "user-read-email",
    "playlist-read-collaborative"
]

@app.route("/login")
def login():
    spotify = OAuth2Session(CLIENT_ID, scope=SCOPE, redirect_uri=REDIRECT_URI)
    authorization_url, state = spotify.authorization_url(AUTH_URL)
    return redirect(authorization_url)

@app.route("/callback", methods=['GET'])
def callback():
    code = request.args.get('code')
    res = requests.post(TOKEN_URL,
        auth=HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET),
        data={
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': REDIRECT_URI
        })
    return json.dumps(res.json())

if __name__ == '__main__':
    app.run(port=7777,debug=True)