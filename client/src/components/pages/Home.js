import React, { Component } from "react";
import Card from "../modules/Card.js";
import "./smr.css";

import './Home.css';
class Home extends Component {
  constructor(props) {
    super(props);

    this.state = {
        topTracks: [],
        card: [],
    };
  }

  componentDidMount() {    
    fetch('http://localhost:3000/create')
    .then(response => response.json())
    .then(data => {
      this.setState({card:<Card title={data.tracks[0]['title']} artists={data.tracks[0]['artist']} img={data.tracks[0]['img']}/> });

      let rows = [];
      for(let i = 1; i < data.tracks.length + 1; i++) {
          rows.push(<Card title={data.tracks[i-1]['title']} artists={data.tracks[i-1]['artist']} img={data.tracks[i-1]['img']}/>)          
      }
      this.setState({topTracks: rows})
  
    });

  }

  render() {
    return (
          <>
            <div className='Home-title'> <span> - </span> JUST FOR YOU <span> - </span> </div>
            <div className='Home-recContainer'> 
                {this.state.topTracks}
            </div>
          </>
        );
  }
}

export default Home;
