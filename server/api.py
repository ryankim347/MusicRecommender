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
load_dotenv()
app = Flask(__name__)
CORS(app)
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
mongo = PyMongo(app)
SPOTIPY_CLIENT_ID= os.environ.get("SPOTIFY_ID")
SPOTIPY_CLIENT_SECRET= os.environ.get("SPOTIFY_SECRET")
SPOTIPY_REDIRECT_URI="http://localhost:5000/join"
#SPOTIPY_REDIRECT_URI="http://localhost:3000/store_data"
SPOTIPY_SCOPE = "user-library-read playlist-read-private user-top-read"
login_object = spotipy.oauth2.SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                    client_secret=SPOTIPY_CLIENT_SECRET,
                                    redirect_uri=SPOTIPY_REDIRECT_URI,
                                    scope=SPOTIPY_SCOPE)
sp = spotipy.Spotify(auth_manager=login_object)
@app.route('/login', methods=["GET"])
def login():
    return {"url": login_object.get_authorize_url()}
@app.route('/store_data')
def store_data():
    print(sp.current_user_saved_tracks()['items'][0])
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