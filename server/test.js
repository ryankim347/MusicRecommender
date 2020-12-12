let SpotifyWebApi = require('spotify-web-api-node');

let SPOTIFY_SCOPES = ['user-library-read', 'playlist-read-private', 'user-top-read'];
let SPOTIFY_CLIENT_ID='1548a7d62d9c4c05b39eebae0966dc77'
let SPOTIFY_CLIENT_SECRET='02fdc9c261f44911ae6c5f780fb39dbf'
let SPOTIFY_REDIRECT_URI="http://localhost:5000/join"


// Setting credentials can be done in the wrapper's constructor, or using the API object's setters.
var spotifyApi = new SpotifyWebApi({
  redirectUri: SPOTIFY_REDIRECT_URI,
  clientSecret: SPOTIFY_CLIENT_SECRET,
  clientId: SPOTIFY_CLIENT_ID
});

// Create the authorization URL
var authorizeURL = spotifyApi.createAuthorizeURL(SPOTIFY_SCOPES);

// https://accounts.spotify.com:443/authorize?client_id=5fe01282e44241328a84e7c5cc169165&response_type=code&redirect_uri=https://example.com/callback&scope=user-read-private%20user-read-email&state=some-state-of-my-choice
console.log(authorizeURL);

let code = 'AQCYathPXMDb9GiZmttUoRgly8t1xFXmkKYapypmLlIlMdWbRla137HNMmPHb5S0hEE3WKO9fQdQG0XWNBWP-JiX5av4OQk_B5hm7SwvnryYHbcqDFgmawzbzo94U5CdEbAQXMgAiHNu2KJnJyNtPXECY72rioNgjuw0J57dupO8zB_vJHobhHsm4-bfE-qeIOL8BCqStvibO67gykDXJR7I7M9GFCcHUeN1G4-OaSl79mTbwfID'

spotifyApi.authorizationCodeGrant(code).then(
  function(data) {
    console.log('The token expires in ' + data.body['expires_in']);
    console.log('The access token is ' + data.body['access_token']);
    console.log('The refresh token is ' + data.body['refresh_token']);

    // Set the access token on the API object to use it in later calls
    spotifyApi.setAccessToken(data.body['access_token']);
    spotifyApi.setRefreshToken(data.body['refresh_token']);
  },
  function(err) {
    console.log('Something went wrong!', err);
  }
);

spotifyApi.getAccessToken().then(
  (data) => {
    console.log('access: ' + data);
  }
)


// let options = {
//   limit: 20,
//   time_range: 'long_term'
// }

// console.log(spotifyApi.getMyTopTracks(options))