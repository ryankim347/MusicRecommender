/*
|--------------------------------------------------------------------------
| api.js -- server routes
|--------------------------------------------------------------------------
|
| This file defines the routes for your server.
|
*/
// import spotify api library
const SpotifyWebApi = require('spotify-web-api-node');
const SPOTIFY_SCOPES = ['user-library-read', 'playlist-read-private', 'user-top-read'];
const SPOTIFY_CLIENT_ID='1548a7d62d9c4c05b39eebae0966dc77'
const SPOTIFY_CLIENT_SECRET='02fdc9c261f44911ae6c5f780fb39dbf'
const SPOTIFY_REDIRECT_URI="http://localhost:5000/home"

const spotifyApi = new SpotifyWebApi({
  redirectUri: SPOTIFY_REDIRECT_URI,
  clientSecret: SPOTIFY_CLIENT_SECRET,
  clientId: SPOTIFY_CLIENT_ID
});

const express = require("express");
// import authentication library
const auth = require("./auth");

// api endpoints: all these paths will be prefixed with "/api/"
const router = express.Router();

//initialize socket›
const socket = require("./server-socket");

router.get('/hello', (req, res) => res.send('hello world'));

router.get("/login", (req, res) => {
  res.send({url: spotifyApi.createAuthorizeURL(SPOTIFY_SCOPES)});
});

router.post("/token", (req, res) => {
  spotifyApi.authorizationCodeGrant(req.body.code)
    .then(
      function(data) {
        // console.log(req.body.code);

        // console.log('The token expires in ' + data.body['expires_in']);
        // console.log('The access token is ' + data.body['access_token']);
        // console.log('The refresh token is ' + data.body['refresh_token']);

        // Set the access token on the API object to use it in later calls
        spotifyApi.setAccessToken(data.body['access_token']);
        spotifyApi.setRefreshToken(data.body['refresh_token']);
        res.send({token: data.body['access_token']});
        console.log('here is the access token again' + spotifyApi.getAccessToken());

      },
      function(err) {
        console.log('Something went wrong!', err);
      }
    );
});

router.get("/top", (req, res) => {
  let options = {
    limit: 20,
    time_range: 'long_term'
  }
  // spotifyApi.setAccessToken('BQAk5rpJ-dlDBVX2UTGo3eoLXMN0bGQRqO3eA0zm5zdXDxCjSG_rw5RhhEEvVDztzTxmgyK_g--vtS5koOmVZK6TzXwRVG9srqHfE8vngnpIeJR3zseD7ZDJze6uN4gp6ZsTpNY1ohJfrTkJpLJ96uh9DGaFPEAGmmVDdwjJPl6ZYqIg396oH-scsGHZ');
  console.log('access token in top ' + spotifyApi.getAccessToken());
  res.send('hello world');
  // spotifyApi.getMyTopTracks(options).then((data) => console.log(data.body.items));

  // res.send({url: spotifyApi.createAuthorizeURL(SPOTIFY_SCOPES)});
});


router.post("/initsocket", (req, res) => {
  // do nothing if user not logged in
  if (req.user) socket.addUser(req.user, socket.getSocketFromSocketID(req.body.socketid));
  res.send({});
});

// |------------------------------|
// | write your API methods below!|
// |------------------------------|

// anything else falls to this "not found" case
router.all("*", (req, res) => {
  console.log(`API route not found: ${req.method} ${req.url}`);
  res.status(404).send({ msg: "API route not found" });
});

module.exports = router;
