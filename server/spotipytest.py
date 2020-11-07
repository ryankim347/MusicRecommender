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
SPOTIPY_CLIENT_ID= os.environ.get("SPOTIFY_ID")
SPOTIPY_CLIENT_SECRET= os.environ.get("SPOTIFY_SECRET")
SPOTIPY_REDIRECT_URI="http://localhost:5000/join"
SPOTIPY_REDIRECT_URI="http://localhost:3000/store-user"
# SPOTIPY_REDIRECT_URI="http://localhost:3000/store_data"
SPOTIPY_SCOPE = "user-library-read playlist-read-private user-top-read"
#spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials())
login = spotipy.oauth2.SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID,
                                client_secret=SPOTIPY_CLIENT_SECRET,
                                redirect_uri=SPOTIPY_REDIRECT_URI,
                                scope=SPOTIPY_SCOPE)
print(login.get_authorize_url())
token = util.prompt_for_user_token(scope = SPOTIPY_SCOPE, 
                                client_id = SPOTIPY_CLIENT_ID, 
                                client_secret = SPOTIPY_CLIENT_SECRET, 
                                redirect_uri = SPOTIPY_REDIRECT_URI)
if token:
    sp = spotipy.Spotify(auth=token)
    print(token)


    results = sp.current_user_top_tracks(limit=12)

    #results = sp.current_user_recently_played(limit=50, after=None, before=None)
    print(results['items'])
    print('lol')
