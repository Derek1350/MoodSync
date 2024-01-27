import spotipy
from spotipy.oauth2 import SpotifyOAuth
import json

CLIENT_ID = "c1d08315a1d6428ca10982e127609784"
CLIENT_SECRET = "a95d73741d93442cbab0cf8a6068e0ca"
REDIRECT_URI="https://example.com/"
USERNAME="2n3vohg923lg7ustb6fang577"
scope="playlist-modify-private"
access_token= "BQAqjqcdN5v9jxE5qMQLpFz6oAZ6R-RgAUGUEyvw2VQKlaEajvxXcEYIRU6dxurdUNuL0Cvp88bs4dHiZ1FaSpoamAsCJ2lKPVgcs4ElR03VLU9fo8ffVJ6XlznzNdjAPOKOgprOg2v5iT1T9eVRXPt7WXoYe9ygFdMnesjyxC1tpSDzrcy9d0TQ3J2l1lr_P76KgIYqpwqc--xLvjNZ98VKIubQVjRksk1RWw"
spotify=spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=CLIENT_ID,client_secret=CLIENT_SECRET,scope=scope,redirect_uri=REDIRECT_URI,username=USERNAME))
USER_ID=spotify.current_user()["id"]

def addToSpotify():
    song_uri=[]
    with open("currentEmotionSongs.json","r") as file:
        data=json.load(file)

    for key, value in data.items():
        if key=='Emotion':
            continue
        search_results = spotify.search(q=f"track:{value}") 
        try:
            uri = search_results["tracks"]["items"][0]['uri']
            song_uri.append(uri)
        except IndexError:
            print(f"{value} doesn't exist in Spotify. Skipped.")

    playlist=spotify.user_playlist_create(user=USERNAME,name=f"SUGGESTED {(data['Emotion']).upper()} SONGS",public=False)
    id=playlist["id"]

    spotify.playlist_add_items(playlist_id=id,items=song_uri)