# IMPORT STATEMENTS
import pandas as pd
import numpy as np
import sklearn
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import OneHotEncoder
from sklearn import preprocessing
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from sklearn import metrics
from sklearn.feature_extraction.text import TfidfVectorizer
from scipy.spatial.distance import cdist

# USEFUL FUNCTIONS
 

def clean_fake_lists(df,col, quotation_mark):
    """
    Clean columns containing fake lists which are actually just strings.
    ---
    Input:
    df (pandas dataframe): dataframe of interest
    col (string): column containing fake list
    quotation_marks (string): delimiter in column
    ---
    Output:
    df (pandas dataframe): cleaned dataframe
    """
    df[col] = df[col].str.replace("[","")
    df[col] = df[col].str.replace("]","")
    df[col] = df[col].str.replace(quotation_mark,"")
    df[col] = df[col].str.lower()
    return df

def genre_preprocess(df, col):
    '''
    Preprocess the genre data
    ---
    Input: 
    df (pandas dataframe): dataframe of interest
    col (string): column containing list to split
    
    Output: 
    df (pandas dataframe): dataframe containing split column as a list
    '''
    col_name = col + '_list'
    df[col_name] = df[col].apply(lambda x: x.split(" "))
    return df

def scale_columns(df, columns):
    """
    Perform z-score scaling using StandardScaler and normalization using MinMaxScaler.
    ---
    Input:
    df (pandas dataframe): dataframe of interest
    columns (list): list containing columns to scale
    ---
    Output:
    df (pandas dataframe): cleaned dataframe
    """
    for col in columns:
        standard_scaler = StandardScaler()
        col_name = col + '_zscaled'
        df[col_name] = pd.DataFrame(standard_scaler.fit_transform(df[[col]]))
        min_max_scaler = MinMaxScaler()
        col_name = col + '_norm'
        df[col_name] = pd.DataFrame(min_max_scaler.fit_transform(df[[col]]))
    return df

###################################################
"""
LMAO there are 3 ways to get a similar result to OHE

"""

def onehotencode_data(df, col):
    '''
    Perform one-hot encoding on specified column (col) and return a new dataframe.
    ---
    Input: 
    df (pandas dataframe): dataframe of interest
    col (string): column to perform one-hot encode on
        
    Output: 
    df_encode (pandas dataframe): dataframe containing one-hot encoded values.
    '''
    to_encode = df[[col]]
    # proper one-hot encoding
    le = preprocessing.LabelEncoder()
    # changing to correct category
    to_encode[col] = to_encode[col].astype('category')
    X_2 = to_encode.apply(le.fit_transform)
    # fitting and encoding data
    encoder = OneHotEncoder(handle_unknown='ignore')
    encoder.fit(X_2)
    onehotlabels = encoder.transform(X_2).toarray()
    labeled = pd.DataFrame(onehotlabels)
    # rename dataframe
    sorted_col_names = list(df[col].unique())
    sorted_col_names.sort()
    key_dict = {}
    for i in range(len(sorted_col_names)):
        if i not in key_dict:
            key_dict[i] = sorted_col_names[i]
    df_encode = df_encode.rename(columns=key_dict)
    return df_encode

def ohe_prep(df, col):
    '''
    Create ohe of specified column.
    ---
    Input: 
    df (pandas dataframe): dataframe of interest
    col (string): column containing records to calculate tf-idf
    
    Output: 
    tf_idf (pandas dataframe): dataframe containing ohe value
    '''
    tf_df = pd.get_dummies(df[col])
    feature_names = tf_df.columns
    tf_df.columns = [col + "|" + str(i) for i in feature_names]
    tf_df.reset_index(drop = True, inplace = True)    
    return tf_df

def tf_idf_transform(df, col):
    '''
    Create ohe of specified column.
    ---
    Input: 
    df (pandas dataframe): dataframe of interest
    col (string): column containing records to calculate tf-idf
    
    Output: 
    tf_idf (pandas dataframe): dataframe containing ohe value
    '''
    # TF-IDF implementation
    combined_df = genre_preprocess(df, col)
    new_col = col + '_list'
    tfidf = TfidfVectorizer()
    tfidf_matrix =  tfidf.fit_transform(combined_df[new_col].apply(lambda x: " ".join(x)))
    tfidf_matrix_df = pd.DataFrame(tfidf_matrix.toarray())
    tfidf_matrix_df.columns = ['col1' + "|" + i for i in tfidf.get_feature_names_out()]
    # genre_df.drop(columns='col1|unknown') # Drop unknown genre
    tfidf_matrix_df.reset_index(drop = True, inplace=True)
    return tfidf_matrix_df
###################################################

def generate_playlist_feature(complete_feature_set, playlist_df):
    '''
    Summarize a user's playlist into a single vector and generate feature set of songs not in playlist_df.
    ---
    Input: 
    complete_feature_set (pandas dataframe): Dataframe containing the features of all the spotify songs
    playlist_df (pandas dataframe): Dataframe containing playlist to sample from
        
    Output: 
    vectorized_playlist (pandas series): single vector feature that summarizes playist_df using sum(axis = 0)
    nonplaylist_features (pandas dataframe): Dataframe containing feature of songs not in the playlist
    '''
    
    # Find song features in the playlist
    playlist_features = complete_feature_set[complete_feature_set['track_id'].isin(playlist_df['track_id'].values)]
    # Find all non-playlist song features
    nonplaylist_features = complete_feature_set[~complete_feature_set['track_id'].isin(playlist_df['track_id'].values)]
    vectorized_playlist = playlist_features.drop(columns = "track_id")
    return vectorized_playlist.sum(axis = 0), nonplaylist_features

def generate_playlist_recos(df, vectorized_playlist, nonplaylist_features, top_songs):
    '''
    Generated recommendation based on cosine similarity of songs in a specific playlist.
    ---
    Input: 
    df (pandas dataframe): Dataframe containing all details of all the spotify songs
    vectorized_playlist (pandas series): single vector feature that summarizes playist_df using sum(axis = 0)
    nonplaylist_features (pandas dataframe): Dataframe containing feature of songs not in the playlist
    top_songs (int): Integer representing top x songs to generate
        
    Output: 
    recommendations: Top {top_songs} recommendations for that playlist
    '''
    non_playlist_df = df[df['track_id'].isin(nonplaylist_features['track_id'].values)]
    # Find cosine similarity between the playlist and the complete song set
    non_playlist_df['similarity'] = cosine_similarity(nonplaylist_features.drop('track_id', axis = 1).values, vectorized_playlist.values.reshape(1, -1))[:,0]
    recommendations = non_playlist_df.sort_values('similarity',ascending = False).head(top_songs)
    
    return recommendations

main_df = pd.read_csv('Datasets/jessica_ver.csv')

# scaling columns
to_scale = ['Popularity', 'key', 'loudness', 'tempo', 'duration_ms', 'time_signature']

# normalize to_scale columns
prep_df = scale_columns(main_df, to_scale)

# tf-idf the genre
tfidf_df = tf_idf_transform(prep_df, 'genre')

feature_of_interest = ['track_id', 'danceability', 'energy', 'mode', 'speechiness',
       'acousticness', 'instrumentalness', 'liveness', 'valence',
       'Popularity_norm', 'key_norm',
       'loudness_norm',  'tempo_norm', 
       'duration_ms_norm', 'time_signature_norm']
feature_df = pd.concat([prep_df[feature_of_interest],tfidf_df], axis=1)

# top songs from Posty Bae
practice_playlist = main_df[(main_df['artist_name'] == 'Post Malone') &  (main_df['Popularity'] > 85)]

single_vector, nonplaylist_features = generate_playlist_feature(feature_df, practice_playlist)
reccomendation = generate_playlist_recos(main_df, single_vector, nonplaylist_features, 10)
print(reccomendation)

# printing reccommendation should work
# will update this code another day