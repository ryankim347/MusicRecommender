var SpotifyWebApi = require("spotify-web-api-node");

var Promise = require("promise");

var spotifyApi = new SpotifyWebApi({
  clientId: "35f22fffdcc243789c2ba7fba37304d6",
  clientSecret: "bd2679206da8455f92859696bbd44018",
  redirectUri: "http://localhost:5000/join",
});

userAuthenticate = (req, res) => {
  var scopes = ['user-read-private', 'user-read-email', 'playlist-read-private']
  var authorizeURL = spotifyApi.createAuthorizeURL(scopes);
  res.send({url: authorizeURL});
}

module.exports = {
  userAuthenticate
};