import spotipy 
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.oauth2 import SpotifyOAuth
import spotipy.util as util
import csv
import sklearn as sk
from sklearn.linear_model import LinearRegression

SPOTIPY_CLIENT_ID='02c185ba203a46569894df2b081befb0'
SPOTIPY_CLIENT_SECRET='80a722d051234ad7a2661e0330629876'
SPOTIPY_REDIRECT_URI='localhost:/callback'
SPOTIPY_SCOPE = "user-library-read"
#  user-top-read

'''
scope = "user-library-read"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

results = sp.current_user_saved_tracks()
for idx, item in enumerate(results['items']):
    track = item['track']
    print(idx, track['artists'][0]['name'], " – ", track['name'])
'''


''' 
birdy_uri = 'spotify:artist:2WX2uTcsvV5OnS0inACecP'
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials())

results = spotify.artist_albums(birdy_uri, album_type='album')
albums = results['items']
while results['next']:
    results = spotify.next(results)
    albums.extend(results['items'])

for album in albums:
    print(album['name'])
'''


token = util.prompt_for_user_token(username = "55ib4yory7fwkmkn033uewc5j", 
                                   scope = SPOTIPY_SCOPE, 
                                   client_id = SPOTIPY_CLIENT_ID, 
                                   client_secret = SPOTIPY_CLIENT_SECRET, 
                                   redirect_uri = SPOTIPY_REDIRECT_URI)
    
def get_fets(uris):
    if token:
        sp = spotipy.Spotify(auth=token)
        fets = sp.audio_features(uris)
        fets_list = []
        for fet in fets:
            fets_list.append(list(fet.values())[:11])
        return fets_list
    
def get_top_tracks(num):    
    if token:
        sp = spotipy.Spotify(auth=token)
        print(token)
        
        #sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=SPOTIPY_SCOPE))
        
        results = sp.current_user_top_tracks(num)
        uris = []
        for idx, item in enumerate(results['items']):
            #print(item)
            track = item['name']
            uris.append(item['uri'])
            #print(idx, item['artists'][0]['name'], " – ", track)
        return get_fets(uris)


        
X = get_top_tracks(50)
Y = [i+1 for i in range(len(X))]
#print(X,Y)
lin_reg = LinearRegression()
lin_reg.fit(X,Y)
print(lin_reg.coef_,lin_reg.intercept_)


from sklearn.metrics import r2_score
print(lin_reg.predict(X))
print(r2_score(Y,lin_reg.predict(X)))

test_uris = ['2MZSXhq4XDJWu6coGoXX1V','0KguOhywc5F45rbguTi97U','4JpazKcfOhbwqZrsYhzHee']
Xt = get_fets(test_uris)
print(Xt)
print(lin_reg.predict(Xt))
   
   
   
