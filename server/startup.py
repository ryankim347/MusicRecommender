from flask_spotify_auth import getAuth, refreshAuth, getToken

#Add your client ID
CLIENT_ID = "7525df977f1744be9053410f87c3143f"

#aDD YOUR CLIENT SECRET FROM SPOTIFY
CLIENT_SECRET = "c1da1b76d3214b57a6068909bf9b0f8d"

#Port and callback url can be changed or ledt to localhost:5000
PORT = "3000"
CALLBACK_URL = "http://localhost"

#Add needed scope from spotify user
SCOPE = 'user-top-read, playlist-read-collaborative'
#token_data will hold authentication header with access code, the allowed scopes, and the refresh countdown 
TOKEN_DATA = []


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