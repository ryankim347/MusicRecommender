import React, { Component } from "react";
import NotFound from "./NotFound.js";
import NavBar from "./../modules/NavBar.js";
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Link
  } from "react-router-dom";

class Room extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
          <>
                <h1>Welcome to our social music recommender!</h1>
                <h2> This is still a skeleton, but it'll be awesome soon!</h2>
          </>
        );
  }
}

export default Room;
