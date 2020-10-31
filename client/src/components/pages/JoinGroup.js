import React, { Component } from "react";
import NotFound from "./NotFound.js";
import NavBar from "./../modules/NavBar.js";
import {
    BrowserRouter as Router,
    Switch,
    Route,
    Link
  } from "react-router-dom";

import './JoinGroup.css';
class JoinGroup extends Component {
  constructor(props) {
    super(props);

    this.state = {
      showGroups : false,
      showPlaylists : false
    };
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
                </div>

              </div>
          </>
        );
  }
}

export default JoinGroup;
