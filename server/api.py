from imports import *
import cluster 

load_dotenv()
app = Flask(__name__)
CORS(app)
# app.config["MONGO_URI"] = MONGO_URI
mongo = PyMongo(app)
app.config["MONGO_URI"]='mongodb+srv://sean:smr-sean@smr-cluster.n7vwr.mongodb.net/website?retryWrites=true&w=majority'
SPOTIPY_CLIENT_ID='1548a7d62d9c4c05b39eebae0966dc77'
SPOTIPY_CLIENT_SECRET='02fdc9c261f44911ae6c5f780fb39dbf'
SPOTIPY_REDIRECT_URI="http://localhost:5000/join"
SPOTIPY_SCOPE = "user-library-read playlist-read-private user-top-read"

login_object = spotipy.oauth2.SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                    client_secret=SPOTIPY_CLIENT_SECRET,
                                    redirect_uri=SPOTIPY_REDIRECT_URI,
                                    scope=SPOTIPY_SCOPE)

sp = spotipy.Spotify(auth_manager=login_object)

# you need to pip install dnspython library for pymongo to work

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
    user_collection = mongo.db.users
    if(user_collection.find_one({"user id": sp.me()['id']}) == None):
        user_collection.insert({'name': sp.me()['display_name'], 'user id': sp.me()['id'], 'refresh token': login_object.get_access_token()['refresh_token'], 'access token': login_object.get_access_token()['access_token']})

    return {"url": login_object.get_authorize_url()}

@app.route('/top', methods=["GET"])
def top():   
    top = sp.current_user_top_tracks(limit=20, offset=0, time_range='medium_term')["items"]
    
    def get_fets(uris,token):
    sp = spotipy.Spotify(auth=token)
    fets = sp.audio_features(uris)
    fets_list = []
    for fet in fets:
        fets_list.append(list(fet.values())[:11])
        #print(fet)
        fets_list[-1].pop(2) #remove the key
        fets_list[-1][2] /= 50 #normalize loudness, should actually do stats tho lol
        fets_list[-1][-1] /= 100    #normalize tempo
    return fets_list
    
    def get_top_tracks(num,token):    
        sp = spotipy.Spotify(auth=token)
        uris = []
        tracks = []
        results = sp.current_user_top_tracks(limit=num,time_range='medium_term')
        for idx, item in enumerate(results['items']):
            #print(item)
            track = item['name']
            tracks.append(track)
            uris.append(item['uri'])
            #print(idx, item['artists'][0]['name'], " – ", track)
        results = sp.current_user_top_tracks(limit=num,time_range='short_term')
        for idx, item in enumerate(results['items']):
            if item['uri'] not in uris:
                track = item['name']
                tracks.append(track)
                uris.append(item['uri'])
        return (get_fets(uris,sp),tracks,uris)
            
    def satisfy(tracks,users,max_songs):
        from sklearn.cluster import KMeans
        from sklearn.cluster import MeanShift
        num_clusters = 3
        uris = list(tracks.keys())
        X = [tracks[uri]['features'] for uri in uris]
        clustering = KMeans(n_clusters=num_clusters,random_state=0).fit(X)
        playlist_songs = set()
        clusters = [[] for j in range(num_clusters)]
        cluster_counts = [{} for j in range(num_clusters)]
        for i in range(len(uris)): #fill with the tracks in each cluster
            clusters[clustering.labels_[i]].append(uris[i])
            for user in tracks[uris[i]]['users']:
                cluster_counts[clustering.labels_[i]][user] = cluster_counts[clustering.labels_[i]].get(user,0) + 1
        max_min = 0
        winner = None
        cluster_scores = []
        for i in range(len(cluster_counts)): #find the cluster that optimizes for group taste 
            counts = cluster_counts[i]
            max_count = 0
            min_count = 10**9
            for user in users:
                max_count = max(counts.get(user,0),max_count)
                min_count = min(counts.get(user,0),min_count)
            cluster_scores.append((i,min_count/max_count))
            #if max_min < min_count/max_count:
            #    max_min = min_count/max_count
            #    winner = i
        cluster_scores.sort(key=lambda x: x[1],reverse=True)
        winner = 0
        unequal = False #check if some users counts are low
        cluster_pointer = [0 for j in range(num_clusters)] #latest song to be added from each cluster
        while len(playlist_songs) < max_songs:
            if winner == None:
                print('Error when computing counts')
                cluster = np.random.randint(0,num_clusters)
            else:
                cluster = cluster_scores[winner][0]
            roll_familiarity = np.random.uniform()
            playlist_songs.add(clusters[cluster][cluster_pointer[cluster]])
            cluster_pointer[cluster] += 1
            if cluster_pointer[cluster] == len(clusters[cluster]):
                winner += 1
                if winner == num_clusters:
                    break
            #if roll_familiarity < familiarity:
            #    playlist_songs.add(clusters[cluster][cluster_pointer[cluster]])
            #else:
            #    recommended = sp.recommendations(seed_tracks = st,limit=10,target_danceability=clustering.cluster_centers_[i][0],target_energy=clustering.cluster_centers_[i][1])['tracks']
            #    for track in recommended:
            #        playlist_songs.add(track)
            #        break
            #TODO: choose random song based on familiarity ratio
            #TODO: update fairness counts
            #TODO: check if unequal
        return playlist_songs
    tracks = {}
    users = []
    user_collection = mongo.db.users
    cursor = user_collection.find({})
    for user in cursor:
        token = user['access token']
        user_id = user['user id']
        if user_id not in users:
            users.append(user_id)
            fets,track_names,uris = get_top_tracks(50,token)
            for i in range(len(fets)):
                if uris[i] not in tracks.keys():
                    tracks[uris[i]] = {'features': fets[i], 'users': [user_id]}
                else:
                    tracks[uris[i]]['users'].append(user_id)
    playlist_songs = satisfy(tracks,users,max_songs=20)
    for user in users:
        token = user['access token']
        sp = spotipy.Spotify(auth=token)
        user_id = user['user id']
        sp.user_playlist_create(user_id,'smrDemo',public=True,description='Made with love by AIM Labs')
        playlists = sp.current_user_playlists(limit=50)
        for playlist in playlists['items']:
            if playlist['name'] == 'smrDemo':
                break
        sp.playlist_add_items(playlist['id'],list(playlist_songs))

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
    SPOTIPY_CLIENT_ID='1548a7d62d9c4c05b39eebae0966dc77'
    SPOTIPY_CLIENT_SECRET='02fdc9c261f44911ae6c5f780fb39dbf'
    SPOTIPY_REDIRECT_URI='http://localhost:8888/callback/'
    SPOTIPY_SCOPE = "user-library-read playlist-read-private user-top-read"


    token = util.prompt_for_user_token(username = "55ib4yory7fwkmkn033uewc5j",
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