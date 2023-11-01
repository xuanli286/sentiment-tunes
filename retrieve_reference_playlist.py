import os
import json
import requests
import pandas as pd
from dotenv import load_dotenv
import csv

# Load environment variables
load_dotenv()

# Spotify API credentials
grant_type = 'client_credentials'
client_id = os.getenv("SPOTIFY_CLIENT_ID")
client_secret = os.getenv("SPOTIFY_CLIENT_SECRET")


# getting access token
def get_access_token(client_id: str, client_secret: str, grant_type: str = 'client_credentials'):
    url = f'https://accounts.spotify.com/api/token?grant_type={grant_type}&client_id={client_id}&client_secret={client_secret}'
    
    try:
        response = requests.post(url, headers={'Content-Type': 'application/x-www-form-urlencoded'})
        response.raise_for_status()  # Raise an exception for HTTP errors
        access_token = 'Bearer ' + json.loads(response.text)['access_token']
        status_code = response.status_code
        return status_code, access_token
    except requests.exceptions.RequestException as e:
        # Handle any exception that occurred during the request
        print(f"Error: {e}")
        return None, None  # Return None for both status code and access token in case of an error

# Get the status code and access token
status_code, access_token = get_access_token(client_id, client_secret, grant_type)

if status_code:
    print(f"*** Status Code: {status_code}")
    print(f"*** Access Token: {access_token}")
else:
    print("Failed to obtain an access token.")



# Function to make API requests and get data
def get_data(url: str, access_token: str, verbose: bool = False):
    response = requests.get(url, headers={'Authorization': access_token})
    result = json.loads(response.text)
    if verbose:
        print('Response body:\n', result)
    return result


# FUNCTION: to get a list of track ids from a playlist
# this would be the reference playlist
def get_track_ids(playlist_id, access_token):
    # Spotify API endpoint
    url = "https://api.spotify.com/v1/playlists/{}/tracks".format(playlist_id)
    retrieve_data = get_data(url, access_token)

    track_id_arr = []

    if 'items' in retrieve_data.keys(): 
        for n in retrieve_data['items']:
            track_id_arr.append(n['track']['id'])

    return track_id_arr


# Retreive track ids of default playlist based on user's input mood
def get_track_ids_mood(mood, access_token):
    mood_data = pd.read_csv(f"default_playlist_dataset/{mood}.csv")
    default_playlist_df = pd.DataFrame(mood_data)
    track_ids_mood = default_playlist_df['id'].tolist()
    return track_ids_mood


# FUNCTION to get track features
def get_track_features(track_id_list: list, access_token: str):
    for i in range(0, len(track_id_list), 100):

        request_text = ",".join(track_id_list)
        url = 'https://api.spotify.com/v1/audio-features?ids=' + request_text
        result = get_data(url, access_token)

        track_features_list = result.get("audio_features", [])

    # Create a DataFrame from the list of features
    track_features_df = pd.DataFrame(track_features_list)

    # Drop unnecessary columns
    track_features_df.drop(columns=['type', 'uri', 'track_href', 'analysis_url'], inplace=True)
    track_features_df.rename(columns={'id':'track_id'}, inplace=True)

    print(track_features_df)
    return track_features_df


if __name__ == "__main__":
    # get user input
    reference_playlist_url = 'https://open.spotify.com/playlist/4VhOeTuLzUqmcOSp5SsyiQ?si=865f716de78d47c5' #to change this value
    idx = reference_playlist_url.find("?")
    playlist_id_input = (reference_playlist_url[34:idx])

    # calling get_track_id to obtain reference playlist
    playlist_data = get_track_ids(playlist_id_input, access_token)
    if playlist_data:
        # Process the retrieved playlist data as needed
        print(playlist_data)

    get_track_features(playlist_data, access_token)
    get_track_ids_mood('amazement', access_token)
