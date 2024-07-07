import requests
import webbrowser

def get_client_id():
    with open("client_id") as f:
        client_id = f.readline().strip("\n")
    return client_id

def get_client_secret():
    with open("client_secret") as f:
        client_secret = f.readline().strip("\n")

scope = ["user-read-email", "user-read-private", "playlist-modify-private"]

redirect_uri = "http://localhost:7777/callback"


def get_access_token():
    # auth_string = client_id + ':' + client_secret
    # auth_bytes = auth_string.encode()
    # auth_64 = str(base64.b64encode(auth_bytes), 'utf-8')

    url = "https://accounts.spotify.com/authorize?"
    params = {'client_id': client_id,
              'response_type': 'code',
              'redirect_uri': redirect_uri,
              'scope' :scope}

    response = requests.get(url, params, allow_redirects=True)
    webbrowser.open(response.url)

def get_auth_header(token):
    return {"Authorization": "Bearer " + token}

token = get_access_token()
