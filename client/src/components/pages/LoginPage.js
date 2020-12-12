import React, { Component } from "react";
import { get, post } from "../../utilities.js";
import "./smr.css";
import "./Login.css";


class LoginPage extends Component {
  constructor(props) {
    super(props);

    this.login = this.login.bind(this);
  }

  login(e) {
    get("/api/login").then((res) => location.href = res.url);
  }

  render() {
    return (
          <>
            <div className='Login-title'> H A R M O N Y </div>
            <div className='Login-body'> AI powered music recommendations for groups</div>
            <div className='Login-body'> connecting people together through music</div>

            <div className='Login-button' onClick={this.login} >
                  <div className='Login-buttonText'> Login with Spotify</div>
            </div>

          </>
        );
  }
}


                    // fetch('http://localhost:3000/login')
                    //   .then(response => response.json())
                    //   .then(data => location.href = data.url);
                    // console.log("just clicked")
                    // fetch('http://localhost:3000/login', {mode: 'cors'}).then(data=>{
                    //   console.log("this is data.url");
                    //   console.log(data.json());
                    //   window.location.href = data.url;
                    // });
                    //post("/api/userAuthenticate").then((data)=>{
                    //    window.location.href = data.url
                    //})

export default LoginPage;
