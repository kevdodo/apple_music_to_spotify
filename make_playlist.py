import base64
import json
with open("client_id") as f:
    client_id = f.readline().strip("\n")
# print(client_id)
with open("client_secret") as f:
    client_secret = f.readline().strip("\n")
    
CODE ='AQAeZiu9CLDexCdyAi7eIjJSCo_R5qbyPGKHCUcH9E4ombQjZrMrfYQUPQiOP5mBdbAKZb-XuhS27-JMyaAcIQZa8MI7KGSSs7NwM2Xw6jj9yuAxZ4We2e6obn4qdPTJ-BTfzySEBMEVYreEkKt_D8RPwpYsgwyutgegmgxNasvSYPR_qQTo5e-4nOodg25WlYXJsvbsSQKB_xI'

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
# with open("access_token", 'w') as f:
#     f.write(token)

with open("access_token", 'r') as f:
    token = f.read()

r = requests.get("https://api.spotify.com/v1/me", headers=get_auth_header(token))
userid = r.json()['id']
assert r.status_code == 200


new_playlist = {"name": "new palylist",
                "desc": "playlist",
                "public": False}

response = requests.post(
    f'https://api.spotify.com/v1/users/{userid}/playlists',
    headers={**get_auth_header(token), "Content-Type": "application/json"},
    data=json.dumps(new_playlist)
)
print(response)

# assert response.status_code == 200
