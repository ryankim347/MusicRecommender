from flask import Flask
from flask import request, jsonify, make_response, after_this_request
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util
import os
from flask_cors import CORS
import pymongo
from pymongo import MongoClient
from flask_pymongo import PyMongo
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import bottle
import sys
load_dotenv()
app = Flask(__name__)
CORS(app)
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
# mongo = PyMongo(app)
SPOTIPY_CLIENT_ID= os.environ.get("SPOTIFY_ID")
SPOTIPY_CLIENT_SECRET= os.environ.get("SPOTIFY_SECRET")
SPOTIPY_REDIRECT_URI="http://localhost:5000/join"
#SPOTIPY_REDIRECT_URI="http://localhost:3000/store_data"
SPOTIPY_SCOPE = "user-library-read playlist-read-private user-top-read"
SPOTIPY_CACHE = '.spotipyoauthcache'
sp_oauth = SpotifyOAuth( SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET,SPOTIPY_REDIRECT_URI,scope=SPOTIPY_SCOPE,cache_path=SPOTIPY_CACHE )

@app.route('/login')
def login():
    access_token = ""
    token_info = sp_oauth.get_cached_token()
    print('test1',file=sys.stderr)
    if token_info:
        print("Found cached token!")
        access_token = token_info['access_token']
    else:
        print('test',file=sys.stderr)
        code = sp_oauth.parse_response_code(bottle.request.url)
        if code:
            print("Found Spotify auth code in Request URL! Trying to get valid access token...")
            token_info = sp_oauth.get_access_token(code)
            access_token = token_info['access_token']

    if access_token:
        print("Access token available! Trying to get user information...")
        sp = spotipy.Spotify(access_token)
        results = sp.current_user()
        return results

    else:
        print('rip')
# login_object = spotipy.oauth2.SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
#                                     client_secret=SPOTIPY_CLIENT_SECRET,
#                                     redirect_uri=SPOTIPY_REDIRECT_URI,
#                                     scope=SPOTIPY_SCOPE)
# @app.route('/login', methods=["GET"])
# def login():
#     return {"url": login_object.get_authorize_url()}
@app.route('/store_data')
def store_data():
    print(sp.current_user_saved_tracks()['items'][0])
@app.route('/control', methods=["GET"])
def control():
    SPOTIPY_CLIENT_ID='1548a7d62d9c4c05b39eebae0966dc77'
    SPOTIPY_CLIENT_SECRET='02fdc9c261f44911ae6c5f780fb39dbf'
    SPOTIPY_REDIRECT_URI='http://localhost:8888/callback/'
    SPOTIPY_SCOPE = "user-library-read playlist-read-private user-top-read"


    token = util.prompt_for_user_token(username = "22rww2kb2qbigzixvwjqoi5ea",
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
# def store-data():


    # if token:
    #     sp = spotipy.Spotify(auth=token)
    #     print(token)


    #     results = sp.current_user_top_tracks(limit=1)

    #     #results = sp.current_user_recently_played(limit=50, after=None, before=None)
    #     print(results['items'])
# @app.route('/store_data', methods=["GET"])
# def store_data():

if __name__ == '__main__':
    app.run(port=3000)