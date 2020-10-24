const mongoose = require("mongoose");
//skeleton from partyy.life
const RoomSchema = new mongoose.Schema({
  name: String, // randomly generated, part of URL
  category: Object,
  host: {
    userId: String, // userId
    name: String
  },
  users: {
    type: [String],
    default: []
  },
  gameId: {
    type: String,
    default: "Waiting",
  },
  status: {
    type: String, // "Waiting" or "InProgress" or "Finished"
    default: "Waiting"
  },
  created: { type: Date, default: Date.now },
  closed: {
    type: Boolean, 
    default: false
  },
  private: {
    type: Boolean,
    default: false
  },
  userIdHistory: {
    type: [String],
    default: []
  }
});

// compile model from schema
module.exports = mongoose.model("room", RoomSchema)
