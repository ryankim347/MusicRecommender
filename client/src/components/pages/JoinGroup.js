import React, { Component } from "react";
import NotFound from "./NotFound.js";
import NavBar from "./../modules/NavBar.js";
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Link
  } from "react-router-dom";
<<<<<<< HEAD
import "./smr.css";
=======
>>>>>>> 2ba1469454bbd90b3ccb1d5aa0240148dbc747b8

import './JoinGroup.css';
class JoinGroup extends Component {
  constructor(props) {
    super(props);

    this.state = {
      showGroups : false,
<<<<<<< HEAD
      showPlaylists : false,
      topTracks : []
    };
  }

  componentDidMount() {
    fetch('http://localhost:3000/create')
      .then(response => response.json())
      .then(data => {
        this.setState({topTracks: data.tracks});
        console.log(data.tracks);
      });
    console.log("this is supposed to return something");
    
=======
      showPlaylists : false
    };
>>>>>>> 2ba1469454bbd90b3ccb1d5aa0240148dbc747b8
  }

  render() {
    let groups = [];
    let playlists = []
    let alph = "ABCDEFGHIJKLMNOPQRSTUVWXYZ";

    for(let i = 0; i < 5; i++ ) {
      groups.push(<div className='JoinGroup-entry'> {"Group " + alph[i]} </div>);
    }
    groups.push(<hr/>);

    for(let i = 11; i < 16; i++ ) {
      playlists.push(<div className='JoinGroup-entry'> {"Playlist " + alph[i]} </div>);
    }
    playlists.push(<hr/>);

<<<<<<< HEAD


    let tracks = [];
    for(let i = 0; i < this.state.topTracks.length; i++) {
      tracks.push(
        <div>
          <h1> {this.state.topTracks[i].title} </h1>
          <div> {this.state.topTracks[i].artist.join(' ')} </div>          
        </div>

      );
    }

=======
>>>>>>> 2ba1469454bbd90b3ccb1d5aa0240148dbc747b8
    return (
          <>
              <div className='JoinGroup-container'>
                <div className='JoinGroup-sideBar'> 
                  <div className='JoinGroup-name'> helu </div>
                  <hr/>
                  <div className='JoinGroup-header' onClick = {() => this.setState({showGroups: !this.state.showGroups})}> My Groups </div>
                  <hr/>
                  {this.state.showGroups && groups}
                  <div className='JoinGroup-header' onClick = {() => this.setState({showPlaylists: !this.state.showPlaylists})}> Saved Playlists </div>
                  <hr/>
                  {this.state.showPlaylists && playlists}

                </div>
                <div className='JoinGroup-content'> 
                  <div className='JoinGroup-name'> GROUP A </div>
                  <div  className='JoinGroup-header'> Members </div>
                  <div  className='JoinGroup-header'> Now playing </div>
                  <div  className='JoinGroup-header'> Coming  Up </div>
<<<<<<< HEAD
                  {tracks}
=======
>>>>>>> 2ba1469454bbd90b3ccb1d5aa0240148dbc747b8
                </div>

              </div>
          </>
        );
  }
}

export default JoinGroup;
