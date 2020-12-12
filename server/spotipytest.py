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

import base64, json, requests


CLIENT_ID= os.environ.get("SPOTIFY_ID")
CLIENT_SECRET= os.environ.get("SPOTIFY_SECRET")
CALLBACK_URL = "http://localhost"
PORT = "5000/join"

def getAuth(client_id, redirect_uri, scope):
    data = "{}client_id={}&response_type=code&redirect_uri={}&scope={}".format(SPOTIFY_URL_AUTH, client_id, redirect_uri, scope) 
    return data

def getToken(code, client_id, client_secret, redirect_uri):
    body = {
        "grant_type": 'authorization_code',
        "code" : code,
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "client_secret": client_secret
    }
        
     
    encoded = base64.b64encode("{}:{}".format(client_id, client_secret))
    headers = {"Content-Type" : HEADER, "Authorization" : "Basic {}".format(encoded)} 

    post = requests.post(SPOTIFY_URL_TOKEN, params=body, headers=headers)
    return handleToken(json.loads(post.text))
    
def handleToken(response):
    auth_head = {"Authorization": "Bearer {}".format(response["access_token"])}
    REFRESH_TOKEN = response["refresh_token"]
    return [response["access_token"], auth_head, response["scope"], response["expires_in"]]

def refreshAuth():
    body = {
        "grant_type" : "refresh_token",
        "refresh_token" : REFRESH_TOKEN
    }

    post_refresh = requests.post(SPOTIFY_URL_TOKEN, data=body, headers=HEADER)
    p_back = json.dumps(post_refresh.text)
    
    return handleToken(p_back)

def getUser():
    return getAuth(CLIENT_ID, "{}:{}/callback/".format(CALLBACK_URL, PORT), SCOPE)

def getUserToken(code):
    global TOKEN_DATA
    TOKEN_DATA = getToken(code, CLIENT_ID, CLIENT_SECRET, "{}:{}/callback/".format(CALLBACK_URL, PORT))
 
def refreshToken(time):
    time.sleep(time)
    TOKEN_DATA = refreshAuth()

def getAccessToken():
    return TOKEN_DATA
    
if token:
    sp = spotipy.Spotify(auth=token)
    print(token)


    results = sp.current_user_top_tracks(limit=12)

    #results = sp.current_user_recently_played(limit=50, after=None, before=None)
    print(results['items'])
    print('lol')
