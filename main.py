import streamlit as st
import spotipy
import os
import webbrowser

from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyOAuth
from open_ai import generate_mood_suggestion
from retrieve_reference_playlist import *
from generate_playlist import *

load_dotenv()

spotify_client_id = os.getenv("SPOTIFY_CLIENT_ID")
spotify_client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=spotify_client_id, client_secret=spotify_client_secret, redirect_uri='http://localhost:8501/', scope='playlist-modify-public playlist-modify-private'))

st.set_page_config(page_title="Sentiment Tunes", page_icon='https://cdn3.emoji.gg/emojis/SpotifyLogo.png')

st.write("""
# Welcome to Sentiment Tunes!
""")
st.write("")
st.write("Our mission is simple: to curate a personalised playlist just for you, based on your current emotional state.")
st.write("Whether you're ecstatic, introspective, or somewhere in between, we've got a song for every emotion. We leverage data mining and sentiment analysis techniques to discover songs that match your feelings.")

st.write("Let's get started!")

query_params = st.experimental_get_query_params()
if 'code' in query_params:
    code = query_params['code'][0]
    token_info = sp.auth_manager.get_access_token(code)
    sp = spotipy.Spotify(auth=token_info['access_token'])
    user_info = sp.me()
    is_mood = False

    if (len(user_info['images']) > 0):
        user_img = user_info['images'][0]
        st.sidebar.image(user_img["url"])
    st.sidebar.write(user_info['display_name'])

    if st.sidebar.button("Logout"):
        os.remove(".cache")
        webbrowser.open("https://www.spotify.com/logout/")
        st.experimental_set_query_params()
        st.experimental_rerun()

    with st.form('user_form'):
        sentence_input = st.text_input("In a sentence, tell us how you're feeling, so we can find the perfect tunes to match your mood.")
        reference_playlist_url = st.text_input("If you have a favourite Spotify playlist that is public, share it with us!")
        submit_button = st.form_submit_button(label="Generate Playlist")
    if submit_button:
        if sentence_input:
            suggested_mood = generate_mood_suggestion(sentence_input)
            st.write(f"Suggested Mood: {suggested_mood}")
            is_mood = True
        if reference_playlist_url:
            idx = reference_playlist_url.find("?")
            spotify_playlist_id = reference_playlist_url[34:idx]
            playlist_data = get_track_ids(spotify_playlist_id, access_token)
            if is_mood:
                track_id_list = generate_playlist(playlist_data)
            else:
                track_id_list = generate_playlist(playlist_data, emotion='no')
            playlist_title = f'Sentiment Tunes\' recommended playlist'
            playlist = sp.user_playlist_create(user_info['id'], playlist_title, public=True)
            playlist_id = playlist['id']
            for track_id in track_id_list:
                sp.playlist_add_items(playlist_id, [track_id])
            cover_img = sp.playlist(playlist_id)["images"][0]["url"]
            st.markdown(f"""
                            <a href="https://open.spotify.com/playlist/{playlist_id}" target="_blank">
                                <figure>
                                    <img src="{cover_img}" width="200">
                                    <figcaption>{playlist_title}</figcaption>
                                </figure>
                            </a>
                        """, unsafe_allow_html=True)
    
else:
    if st.button("Login with Spotify"):
        st.write("Redirecting to Spotify login page...")
        auth_url = sp.auth_manager.get_authorize_url()
        webbrowser.open(auth_url)