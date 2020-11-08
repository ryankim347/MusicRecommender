const User = require("./models/user")

var SpotifyWebApi = require("spotify-web-api-node");

var Promise = require("promise");

require('dotenv').config();

var spotifyApi = new SpotifyWebApi({
  clientId: process.env.SPOTIFY_ID,
  clientSecret: process.env.SPOTIFY_SECRET,
  redirectUri: "http://localhost:5000/join",
});

userAuthenticate = (req, res) => {
  var scopes = ['user-read-private', 'user-read-email', 'playlist-read-private'];
  var authorizeURL = spotifyApi.createAuthorizeURL(scopes);
  res.send({url: authorizeURL});
}

addUser = (req,res) => {
  var code = req.query.code;
  var state = req.query.state;
  var name = state.split("-----")[0]
  spotifyApi.authorizationCodeGrant(code).then(
    function (data) {
      console.log("The access token expires in " + data.body["expires_in"]);
      console.log("The access token is " + data.body["access_token"]);
      // Save the access token so that it's used in future calls
      spotifyApi.setAccessToken(data.body["access_token"]);
      spotifyApi.setRefreshToken(data.body['refresh_token']);
      
      const user = new User({
        name: "Name",
        topSongs: ["Song 1", "Song 2"],
        topArtists: ["Artist 1", "Artist 2"],
      })
      user.save(function (err) {
        if (err) return handleError(err);
      })
    },
    function (err) {
      console.log("Something went wrong when retrieving an access token", err);
    }
  )
}

module.exports = {
  userAuthenticate
};