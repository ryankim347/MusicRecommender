# shows a user's playlists (need to be authenticated via oauth)

import sys
import spotipy
import spotipy.util as util
import pandas as pd

username = '22bta3ohppqii7dyfd24rraoa' #allen
SPOTIPY_CLIENT_ID='7525df977f1744be9053410f87c3143f'
SPOTIPY_CLIENT_SECRET='c1da1b76d3214b57a6068909bf9b0f8d'
SPOTIPY_REDIRECT_URI='http://localhost:8888/callback/'

SPOTIPY_SCOPE = 'user-top-read, playlist-read-collaborative'

token = util.prompt_for_user_token(username = username, 
                                   scope = SPOTIPY_SCOPE, 
                                   client_id = SPOTIPY_CLIENT_ID, 
                                   client_secret = SPOTIPY_CLIENT_SECRET, 
                                   redirect_uri = SPOTIPY_REDIRECT_URI)

if token:
   sp = spotipy.Spotify(auth=token)

top_tracks = sp.current_user_top_tracks(limit = 20, time_range = 'short_term')
uris = []
names = []
for item in top_tracks['items']:
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
print([i['name'] for i in top_artists['items']])
top_artist_uris = [i['uri'] for i in top_artists['items']]
data = pd.DataFrame(data, index = names)
normalized = (data-data.mean())/data.std()
mean = data.mean()
recommended = sp.recommendations(seed_artists = top_artist_uris[4:5], seed_genres = None, seed_tracks = None, limit = 20, country = None,
            target_acousticness = mean['acousticness'],
            target_danceability = mean['danceability'], target_energy = mean['energy'],
            target_instrumentalness = mean['instrumentalness'], 
            target_liveness = mean['liveness'], target_loudness = mean['loudness'],
            target_valence = mean['valence'], min_popularity = 50)    
for track in recommended['tracks']:
    print(track['name'], [artist['name'] for artist in track['artists']])
