from imports import *
import cluster 
import flask_spotify_auth
import startup
from flask import Flask, redirect, request

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

load_dotenv()
app = Flask(__name__)
CORS(app)
app.config["MONGO_URI"] = MONGO_URI
mongo = PyMongo(app)

username = '22bta3ohppqii7dyfd24rraob' #allen
SPOTIPY_CLIENT_ID='7525df977f1744be9053410f87c3143f'
SPOTIPY_CLIENT_SECRET='c1da1b76d3214b57a6068909bf9b0f8d'
SPOTIPY_REDIRECT_URI='http://localhost:8888/callback/'
SPOTIPY_SCOPE = "user-library-read playlist-read-private user-top-read"



#print(login_object.get_access_token())
#sp = spotipy.Spotify(auth_manager=login_object)

# you need to pip install dnspython library for pymongo to work


@app.route('/callback/')
def callback():
    lz_uri = 'spotify:artist:36QJpDe2go2KgaRleHCDTp'

    startup.getUserToken(request.args['code'])
    global sp
    sp = spotipy.Spotify(auth = startup.getAccessToken()[0])
    return(sp.artist_top_tracks(lz_uri))

@app.route('/store', methods=["GET"])
def store():
    # token = util.prompt_for_user_token(username = "55ib4yory7fwkmkn033uewc5j",
    #                                client_id = SPOTIPY_CLIENT_ID,
    #                                client_secret = SPOTIPY_CLIENT_SECRET,
    #                                redirect_uri = SPOTIPY_REDIRECT_URI,
    #                                scope = SPOTIPY_SCOPE)

    # if token:
    #     sp = spotipy.Spotify(auth=token)
    #     print(token)

    user_collection = mongo.db.users

    user_collection.insert({'name': sp.me()['display_name'], 'user id': sp.me()['id'], 'refresh token': login_object.get_access_token()['refresh_token'], 'access token': login_object.get_access_token()['access_token']})
    return {'NAME': sp.me()['display_name'], 'USER_ID': sp.me(), 'REFRESH_TOKEN': login_object.get_access_token()['refresh_token'], 'ACCESS_TOKEN': login_object.get_access_token()['access_token']}

@app.route('/login', methods=["GET"])
def login():   
    if startup.getAccessToken():
        return redirect('/recommended')
    response = startup.getUser()
    
    return redirect(response)

@app.route('/recommended', methods = ["GET"])
def recommended():
    data = {'acousticness': [], 
        'danceability': [], 
        'energy': [], 
        'instrumentalness': [], 
        'liveness': [], 
        'loudness': [], 
        'valence': []}
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
    res = []
    for i in range(50):
        res.append(sp.track(distances[i][0])['name'])
    return '\n'.join(res)

@app.route('/top', methods=["GET"])
def top():   
    top = sp.current_user_top_tracks(limit=20, offset=0, time_range='medium_term')["items"]

    response = []
    for track in top:
        artists = ''
        for artist in track['artists']:
            artists += artist['name'] + ', '
        track_dict = {
            'name': track['name'],
            'artists': artists[:-2], 
            'uri': track['uri']
        }
        response.append(track_dict)

    return {"tracks": response}

@app.route('/create', methods=["GET"])
def create():   
    response = cluster.allen_cluster(sp)
    return {"tracks": list(response)}

@app.route('/control', methods=["GET"])
def control():
    username = '22bta3ohppqii7dyfd24rraob' #allen
    SPOTIPY_CLIENT_ID='7525df977f1744be9053410f87c3143f'
    SPOTIPY_CLIENT_SECRET='c1da1b76d3214b57a6068909bf9b0f8d'
    SPOTIPY_REDIRECT_URI='http://localhost:8888/callback/'
    SPOTIPY_SCOPE = "user-library-read playlist-read-private user-top-read"


    token = util.prompt_for_user_token(username = username,
                                   client_id = SPOTIPY_CLIENT_ID,
                                   client_secret = SPOTIPY_CLIENT_SECRET,
                                   redirect_uri = SPOTIPY_REDIRECT_URI,
                                   scope = SPOTIPY_SCOPE)

    if token:
        sp = spotipy.Spotify(auth=token)
        print(token)


        # results = sp.current_user_top_tracks(limit=1)

        # #results = sp.current_user_recently_played(limit=50, after=None, before=None)
        # print(results['items'])
        return token





if __name__ == '__main__':
    app.run(port=3000)