import React, { Component }from 'react';
import ReactDOM from 'react-dom';
import Header from './components/header_bar/header';
import MainLayout from './components/main_layout/main_layout';

class App extends Component{
  constructor(props){
    super(props);

    this.state={
      row: '0',
      col: '0',
      width: '0'
    };
  }

  onChangeState(row, col, width){
    this.setState({
      row: row,
      col: col,
      width: width
    });
  }

  render() {
    const changeState = (row, col, width) => this.onChangeState(row, col, width);
    return (
      <div>
        <Header onChangeState= { changeState }/>
        <MainLayout
        row = { this.state.row }
        col = { this.state.col }
        />
      </div>
    );
  }
}


ReactDOM.render(<App /> , document.querySelector('.container'));
