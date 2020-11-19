# shows a user's playlists (need to be authenticated via oauth)

import sys
import spotipy
import spotipy.util as util
import pandas as pd
import matplotlib.pyplot as plt 
import sklearn
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import StandardScaler

def allen_cluster(sp):
    top_tracks = sp.current_user_top_tracks(limit = 20, time_range = 'short_term')
    top_tracks2 = sp.current_user_top_tracks(limit = 20, time_range = 'long_term')
    uris = []
    names = []
    for item in top_tracks['items']:
        names.append(item['name'])
        uris.append(item['uri'])
    for item in top_tracks2['items']:
        if not item['name'] in names:
            names.append(item['name'])
            uris.append(item['uri'])

    data = pd.DataFrame()
    data = {'acousticness': [], 
            'danceability': [], 
            'energy': [], 
            'instrumentalness': [], 
            'liveness': [], 
            'loudness': [], 
            'valence': []}
    fets = data.keys()
    for item in sp.audio_features(uris):
        for j in fets:
            data[j].append(item[j])

    top_artists = sp.current_user_top_artists(limit=20, offset=0, time_range='short_term')
    top_artist_uris = [i['uri'] for i in top_artists['items']]
    data = pd.DataFrame(data, index = names)
    normalized = (data-data.mean())/data.std()
    mean = data.mean()

    kmeans = KMeans(init = 'random', n_clusters = 3, n_init = 10, max_iter = 300, random_state = 42)
    kmeans.fit(normalized)
    centers = kmeans.cluster_centers_

    for center in centers:
        num = centers.tolist().index(center.tolist())
        recommended = sp.recommendations(seed_artists = None, seed_genres = ['pop', 'hip-hop', 'r-n-b'], seed_tracks = None, limit = 10, country = None,
                    target_acousticness = center[0],
                    target_danceability = center[1], target_energy = center[2],
                    target_instrumentalness = center[3], 
                    target_liveness = center[4], target_loudness = center[5],
                    target_valence = center[6], min_popularity = 50)
    
    tracks = []

    for track in recommended['tracks']:
        tr = {}
        tr['title'] = track['name']
        tr['artist'] = [artist['name'] for artist in track['artists']]
        tracks.append(tr)

    return tracks