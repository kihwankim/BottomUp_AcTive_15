import React, {Component} from 'react';

import MainLayout from '../containers/main/main_layout'
import ButtonList from '../containers/right-side/button_list'
import Header from '../containers/header_bar/header';

class App extends Component {
  constructor(props) {
    super(props);

    this.state = {
      isSetting: 0
    };
  }

  render() {
    return (
      <div className="wrapper">
          <div className="head">
              <Header />
          </div>
          <div className="left">
              <MainLayout isSetting={ this.state.isSetting }/>
          </div>
          <div className="right">
              <ButtonList onSetData={ isSetting => this.setState({isSetting}) } />
          </div>
      </div>
    );
  }
}



export default App;
