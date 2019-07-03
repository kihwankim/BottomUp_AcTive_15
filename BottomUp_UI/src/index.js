import React, { Component }from 'react';
import ReactDOM from 'react-dom';

class App extends Component{
  constructor(props){
    super(props);

    this.state={
      
    };
  }
  render() {
    return (
      <div>
        Hi
      </div>
    );
  }
}

ReactDOM.render(<App /> , document.querySelector('.container'));
