import streamlit as st
import spotipy
import os
import webbrowser

from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
from open_ai import generate_mood_suggestion

load_dotenv()

spotify_client_id = os.getenv("SPOTIFY_CLIENT_ID")
spotify_client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=spotify_client_id, client_secret=spotify_client_secret, redirect_uri='http://localhost:8501/', scope='playlist-modify-public playlist-modify-private'))

st.write("""
# generate your personalised album!
""")

query_params = st.experimental_get_query_params()
if 'code' in query_params:
    code = query_params['code'][0]
    token_info = sp.auth_manager.get_access_token(code)
    sp = spotipy.Spotify(auth=token_info['access_token'])

    st.write("Logged in as:")
    user_info = sp.me()
    st.write(f"Display Name: {user_info['display_name']}")
    st.write(f"Spotify ID: {user_info['id']}")

    sentence_input = st.text_input("how was your day?")
    suggested_mood = generate_mood_suggestion(sentence_input)

    spotify_link_input = st.text_input("paste your favourite spotify album's link here!")
    print(spotify_link_input)

    # TO-DO: recommender system output
    track_id_list = ["2SAqBLGA283SUiwJ3xOUVI", "5rb9QrpfcKFHM1EUbSIurX", "3a1lNhkSLSkpJE4MSHpDu9", "4iZ4pt7kvcaH6Yo8UoZ4s2"]
    playlist = []
    playlist = sp.user_playlist_create(user_info['id'], 'Your New Playlist', public=True)
    playlist_id = playlist['id']
    for track_id in track_id_list:
        sp.playlist_add_items(playlist_id, [track_id])
    st.markdown(f'<a href="https://open.spotify.com/playlist/{playlist_id}" target="_blank">Listen to the Playlist on Spotify</a>', unsafe_allow_html=True)

else:
    if st.button("Login with Spotify"):
        st.write("Redirecting to Spotify login page...")
        auth_url = sp.auth_manager.get_authorize_url()
        webbrowser.open(auth_url, new=2)