from flask import Flask
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util
import os

app = Flask(__name__)
@app.route('/login')
def login():
    SPOTIPY_CLIENT_ID= os.environ.get("SPOTIFY_ID")
    SPOTIPY_CLIENT_SECRET= os.environ.get("SPOTIFY_SECRET")
    SPOTIPY_REDIRECT_URI="http://localhost:5000/join"
    SPOTIPY_SCOPE = "user-library-read playlist-read-private user-top-read"


    token = util.prompt_for_user_token(username = "55ib4yory7fwkmkn033uewc5j",
                                    client_id = SPOTIPY_CLIENT_ID,
                                    client_secret = SPOTIPY_CLIENT_SECRET,
                                    redirect_uri = SPOTIPY_REDIRECT_URI,
                                    scope = SPOTIPY_SCOPE)

    if token:
        sp = spotipy.Spotify(auth=token)
        print(token)


        results = sp.current_user_top_tracks(limit=1)

        #results = sp.current_user_recently_played(limit=50, after=None, before=None)
        print(results['items'])
if __name__ == '__main__':
    app.run()