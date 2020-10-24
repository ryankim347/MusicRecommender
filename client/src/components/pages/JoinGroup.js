import React, { Component } from "react";
import NotFound from "./NotFound.js";
import NavBar from "./../modules/NavBar.js";
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Link
  } from "react-router-dom";
class JoinGroup extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
          <>
            <NavBar/>
            <Router>
              <div>
                <h1>Join a group!</h1>
                <h2> This is still a skeleton, but it'll be awesome soon :)</h2>
              </div>
            </Router>
          </>
        );
  }
}

export default JoinGroup;
