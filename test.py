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
import collections
from spotipy.oauth2 import SpotifyClientCredentials

client_credentials_manager = SpotifyClientCredentials()
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

playlists = sp.user_playlists('spotify')
while playlists:
    for i, playlist in enumerate(playlists['items']):
        print("%4d %s %s" % (i + 1 + playlists['offset'], playlist['uri'],  playlist['name']))
    if playlists['next']:
        playlists = sp.next(playlists)
    else:
        playlists = None
        
username = '22bta3ohppqii7dyfd24rraob' #allen
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

'''top_tracks = sp.current_user_top_tracks(limit = 20, time_range = 'short_term')
top_tracks2 = sp.current_user_top_tracks(limit = 20, time_range = 'long_term')
uris = []
names = []
for item in top_tracks['items']:
    names.append(item['name'])
    uris.append(item['uri'])
for item in top_tracks2['items']:
    if not item['name'] in names:
        names.append(item['name'])
        uris.append(item['uri'])'''

data = {'acousticness': [], 
        'danceability': [], 
        'energy': [], 
        'instrumentalness': [], 
        'liveness': [], 
        'loudness': [], 
        'valence': []}
print('0')
'''fets = data.keys()
for item in sp.audio_features(uris):
    for j in fets:
        data[j].append(item[j])

top_artists = sp.current_user_top_artists(limit=20, offset=0, time_range='short_term')
top_artist_uris = [i['uri'] for i in top_artists['items']]
data = pd.DataFrame(data, index = names)
normalized = (data-data.mean())/data.std()
std = data.std()
mean = data.mean()'''

"""errors = []
for i in range(1, 10):
  kmeans = KMeans(init = 'random', n_clusters = i, n_init = 10, max_iter = 300, random_state = 42)
  kmeans.fit(normalized)
  errors.append(kmeans.inertia_)
centers = kmeans.cluster_centers_
plt.plot(errors)
plt.show()
tracks = set()

for center in centers:
  for i in range(len(center)):
    center[i] *= std[i]
    center[i] += mean[i]
  num = centers.tolist().index(center.tolist())
  recommended = sp.recommendations(seed_artists = None, seed_genres = ['pop', 'hip-hop', 'r-n-b'], seed_tracks = None, limit = 10, country = None,
            target_acousticness = center[0],
            target_danceability = center[1], target_energy = center[2],
            target_instrumentalness = center[3], 
            target_liveness = center[4], target_loudness = center[5],
            target_valence = center[6], min_popularity = 50)
  for track in recommended['tracks']:
    tracks.add(track['name'] + ' -- '+ ', '.join([artist['name'] for artist in track['artists']]) + ' ' + str(num))
for track in tracks:
  print(track)"""
def get_fets(uris):
  names = []
  for i in list(uris):
    try:
      names.append(sp.track(i)['name'])
    except:
      uris.remove(i)
  data = {'acousticness': [], 
          'danceability': [], 
          'energy': [], 
          'instrumentalness': [], 
          'liveness': [], 
          'loudness': [], 
          'valence': []}
  fets = data.keys()
  features = []
  for i in range(len(uris)//100):
    features.extend(sp.audio_features(uris[100*i:100*(i+1)]))
  features.extend(sp.audio_features(uris[100*(len(uris)//100):]))
  for item in features:
    for j in fets:
        data[j].append(item[j])
  return pd.DataFrame(data, index = uris)

playlists = sp.current_user_playlists()
playlists = [sp.playlist(i['id']) for i in playlists['items']]
playlist_dict = {}
tracks = collections.defaultdict(lambda: 0)
centers = []
for playlist in playlists:
  playlist_dict[playlist['uri']] = playlist['tracks']['items']

print('1')
for playlist in playlist_dict:
  #uris = [i['track']['uri'] for i in playlist_dict[playlist]]
  #data = get_fets(uris)
  for i in playlist_dict[playlist]:
    uri = i['track']['uri']
    tracks[uri] += 1
  #kmeans = KMeans(init = 'random', n_clusters = 2, n_init = 10, max_iter = 10, random_state = 42)
  #kmeans.fit(data)
  #clusters = kmeans.cluster_centers_
  #centers.extend(list(clusters))
#-----------------------------
data = get_fets(list(tracks.keys()))
kmeans = KMeans(init = 'random', n_clusters = 10, n_init = 10, max_iter = 10, random_state = 42)
kmeans.fit(data)
centers = list(kmeans.cluster_centers_)
#-----------------------------
print('2')
def distance2(uris, centers):
  res = []
  for uri in uris:
    distance2 = float('inf')
    try:
      features = data.loc[uri]
    except:
      continue
    for center in centers:
      distance2 = min(dist(center, features)/tracks[uri], distance2)
    res.append((uri, distance2))
  return res

def dist(center, features):
  ans = 0
  fets = data.keys()
  for i in range(len(center)):
    ans += (center[i] - features[fets[i]])**2
  return ans

distances = distance2(tracks, centers)
distances = sorted(distances, key = lambda x: x[1])
for i in range(50):
  print(sp.track(distances[i][0])['name'], sp.track(distances[i][0])['preview_url'])

  
