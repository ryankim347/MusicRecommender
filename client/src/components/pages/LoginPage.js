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
import "./smr.css";
import "./Login.css";


class LoginPage extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    console.log("got to login page");
    return (
          <>
            <div className='Login-title'> H A R M O N Y </div>
            <div className='Login-body'> AI powered music recommendations for groups</div>
            <div className='Login-body'> connecting people together through music</div>

            <div className='Login-button' onClick={()=>{
                    console.log("just clicked")
                    post("/api/userAuthenticate").then((data)=>{
                        window.location.href = data.url
                    })
                }} >
                  <div className='Login-buttonText'> Login with Spotify</div>
            
            </div>

          </>
        );
  }
}

export default LoginPage;
