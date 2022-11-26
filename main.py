import json
import spotipy #conda install -c conda-forge spotipy
import pandas as pd
from spotipy.oauth2 import SpotifyClientCredentials
import spotipy.util as util

def call_playlist(creator, playlist_id):
    # https://open.spotify.com/user/11186902480?si=e3caa534abae4484
    # https://open.spotify.com/playlist/6fGLs25lr5oX3UeU3waD6k?si=63f09731409742fa
    
    #step1

    playlist_features_list = ["artist","album","track_name",  "track_id","danceability","energy","key","loudness","mode", "speechiness","instrumentalness","liveness","valence","tempo", "duration_ms","time_signature"]
    
    playlist_df = pd.DataFrame(columns = playlist_features_list)
    
    #step2
    
    playlist = sp.user_playlist_tracks(creator, playlist_id)["items"]
    print(playlist)
    for track in playlist:
        # Create empty dict
        playlist_features = {}
        # Get metadata
        playlist_features["artist"] = track["track"]["album"]["artists"][0]["name"]
        playlist_features["album"] = track["track"]["album"]["name"]
        playlist_features["track_name"] = track["track"]["name"]
        playlist_features["track_id"] = track["track"]["id"]
        
        # Get audio features
        audio_features = sp.audio_features(playlist_features["track_id"])[0]
        for feature in playlist_features_list[4:]:
            playlist_features[feature] = audio_features[feature]
        
        # Concat the dfs
        track_df = pd.DataFrame(playlist_features, index = [0])
        playlist_df = pd.concat([playlist_df, track_df], ignore_index = True)

    #Step 3
        
    return playlist_df



if __name__ == '__main__':
    
    # Importing login info
    path='/home/kotrebor/data_repo/spotify_pssw.csv'
    login_info = pd.read_csv(path)
    client_id = login_info.iloc[0]['client_id']
    client_secret = login_info.iloc[0]['client_secret']


    client_credentials_manager = SpotifyClientCredentials(client_id, client_secret)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # Only one that works for now

    playlists = sp.user_playlists('11186902480')
    #print(playlist)
    while playlists:
        for i, playlist in enumerate(playlists['items']):
            print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
        if playlists['next']:
            playlists = sp.next(playlists)
        else:
            playlists = None
    
    call_playlist("11186902480", "6fGLs25lr5oX3UeU3waD6k")