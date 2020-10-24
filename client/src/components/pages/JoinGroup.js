import React, { Component } from "react";
import NotFound from "./NotFound.js";
class JoinGroup extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    return (
          <>
            <NavBar/>
            <Router>
                <h1>Join a group!</h1>
                <h2> This is still a skeleton, but it'll be awesome soon!</h2>
              <Skeleton
                path="/"
              />
              <NotFound default />
            </Router>
          </>
        );
  }
}

export default JoinGroup;
