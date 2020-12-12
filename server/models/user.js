const mongoose = require("mongoose");

const UserSchema = new mongoose.Schema({
  name: String,
  user_id: String,
  access_token: String,
  refresh_token: String,
});

// compile model from schema
module.exports = mongoose.model("user", UserSchema);
