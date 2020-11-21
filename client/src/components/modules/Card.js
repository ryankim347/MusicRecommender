import React, { Component } from "react";
import "./Card.css";
class Card extends Component {
  constructor(props) {
    super(props);

    this.state = {
    };
  }

  componentDidMount() {    

  }

  render() {
    let arr = this.props.artists;
    arr.join(", ");

    let title = this.props.title;
    console.log(title);
    let paren = title.indexOf('(') == -1 ? title.length : title.indexOf('(')-1;
    console.log(paren);
    let feat = title.indexOf("(") == -1 ? "" : title.substring(title.indexOf("(") + 1, title.indexOf(")"));

    title = title.substring(0, paren);

    console.log(feat);

    return (
          <>
            <div className='Card-container'>
                <div className='Card-img' style={{backgroundImage: "url(" + this.props.img + ")"}}> </div> 
                <div className='Card-title'> {title} </div>
                <div className='Card-artist'> {this.props.artists.filter((e) => this.props.title.indexOf(e) == -1).join(", ")} </div>
                <div className='Card-feat'> {feat} </div>
                   
            </div>
          </>
        );
  }
}

export default Card;


// render() {
//   let arr = this.props.artists;
//   arr.join(", ");


//   return (
//         <>
//           <div className='Card-container'>
//               <div className='Card-img' style={{backgroundImage: "url(" + this.props.img + ")"}}> </div> 
//               <div className='Card-title'> {this.props.title.substring(0, paren)} </div>
//               <div className='Card-artist'> {this.props.artists.filter((e) => this.props.title.indexOf(e) == -1).join(", ")} </div>
//               <div className='Card-feat'> {feat} </div>
              
//           </div>
//         </>
//       );
// }

// let paren = this.props.title.indexOf('(') != -1 ? this.props.title.indexOf('(') - 1 : title.length; 
// let feat = this.props.title.indexOf('(') != -1 ? this.props.title.substring(this.props.title.indexOf('(') + 1, this.props.title.indexOf(')')) : '';
