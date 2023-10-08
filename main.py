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

st.set_page_config(page_title="Sentiment Tunes", page_icon='https://cdn3.emoji.gg/emojis/SpotifyLogo.png')

st.write("""
# generate your personalised album!
""")

query_params = st.experimental_get_query_params()
if 'code' in query_params:
    code = query_params['code'][0]
    token_info = sp.auth_manager.get_access_token(code)
    sp = spotipy.Spotify(auth=token_info['access_token'])
    user_info = sp.me()

    user_img = user_info['images'][0]
    st.sidebar.image(user_img["url"])
    st.sidebar.write(user_info['display_name'])

    if st.sidebar.button("Logout"):
        os.remove(".cache")
        webbrowser.open("https://www.spotify.com/logout/")
        st.experimental_set_query_params()
        st.experimental_rerun()

    with st.form('user_form'):
        sentence_input = st.text_input("how was your day?")
        submit_button = st.form_submit_button(label="Generate Playlist")
    if submit_button:
        suggested_mood = generate_mood_suggestion(sentence_input)
        st.write(f"Suggested Mood: {suggested_mood}")
        # TO-DO: recommender system output
        if suggested_mood:
            track_id_list = ["2SAqBLGA283SUiwJ3xOUVI", "5rb9QrpfcKFHM1EUbSIurX", "3a1lNhkSLSkpJE4MSHpDu9", "4iZ4pt7kvcaH6Yo8UoZ4s2"]
            playlist = []
            playlist_title = f'Your {", ".join(suggested_mood).title()} Playlist'
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

    # spotify_link_input = st.text_input("paste your favourite Spotify album's link here!")
    
else:
    if st.button("Login with Spotify"):
        st.write("Redirecting to Spotify login page...")
        auth_url = sp.auth_manager.get_authorize_url()
        webbrowser.open(auth_url)