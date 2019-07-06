import React, {Component} from 'react';

import MainLayout from '../containers/main/main_layout'
import ButtonList from '../containers/right-side/button_list'
import Header from '../containers/header_bar/header';

class App extends Component {
  constructor(props) {
    super(props);
  }

  render() {

    return (
      <div className="wrapper">
          <div className="head">
              <Header />
          </div>
          <div className="left">
              <MainLayout />
          </div>
          <div className="right">
              <ButtonList />
          </div>
      </div>
    );
  }
}



export default App;
