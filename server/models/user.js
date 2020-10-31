const mongoose = require("mongoose");

const UserSchema = new mongoose.Schema({
  name: String,
  topSongs: {
    type: [String],
    default: []
  },
  topArtists: {
    type: [String],
    default: []
  }
});

// compile model from schema
module.exports = mongoose.model("user", UserSchema);
