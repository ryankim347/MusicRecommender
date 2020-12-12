from imports import *
import cluster 

load_dotenv()
app = Flask(__name__)
CORS(app)
# app.config["MONGO_URI"] = MONGO_URI
mongo = PyMongo(app)

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