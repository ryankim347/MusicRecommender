import React, { Component } from "react";
import NotFound from "./NotFound.js";
import NavBar from "./../modules/NavBar.js";
import Skeleton from "./Skeleton.js";
import Button from 'react-bootstrap/Button';
import 'bootstrap/dist/css/bootstrap.min.css';
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Link
  } from "react-router-dom";
import { post } from "../../utilities.js";

class LoginPage extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    console.log("got to login page");
    return (
          <>
            <NavBar/>
            <div>
                <h1>Welcome to our social music recommender!</h1>
                <hr></hr>
                <h2>Login with Spotify below:</h2>
                <Button variant="outline-success"
                    onClick={()=>{
                        post("api/addCategoryAuthenticate",{
                            playlistId: this.props.playlistId, name: this.props.category.name
                        }).then((data1)=>{
                            window.location.href = data1.url
                        })
                    }}
                >Login with Spotify</Button>{' '}
            </div>
          </>
        );
  }
}

export default LoginPage;
