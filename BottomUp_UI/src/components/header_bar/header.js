//header -> 입력들어오는것담당
import React, { Component } from 'react';

class Header extends Component {
  constructor(props){
    super(props);

    this.state = {
      row: '0',
      col: '0',
      width: '0'
    };
  }

  onInputChagne(row, col, width){
    this.setState({
      row: row,
      col: col,
      width: width
    });
    this.props.onChangeState(row, col, width);
  }

  render(){
    return (
      <div className= "header-list">
        <div className="row">
          <span className = "row-input">row : </span>
          <input
            value = {this.state.row}
            onChange = { event => this.onInputChagne(event.target.value, this.state.col, this.state.width) }
          />
        </div>
        <div className="col">
          <span className= "col-input">col : </span>
          <input
            value = {this.state.col}
            onChange = { event => this.onInputChagne(this.state.row, event.target.value, this.state.width) }
          />
        </div>
        <div className="width">
          <span className = "width-input">width : </span>
          <input
            value = {this.state.width}
            onChange = { event => this.onInputChagne(this.state.row , this.state.col, event.target.value) }
          />
        </div>
      </div>
    );
  }
}

export default Header;
