import React, {Component} from 'react';
import { connect } from 'react-redux';

import { changeRow } from '../../actions/change_row';
import { changeCol } from '../../actions/change_col';
import { changeWidth } from '../../actions/change_width';
import { bindActionCreators } from 'redux';

class Header extends Component {
    render() {
        return (
          <div className="header-list">
              <div className="row">
                  <span className="row-input">row : </span>
                  <input
                      value = { this.props.activeRow }
                      onChange={ (event) => this.props.changeRow(event.target.value) }
                  />
              </div>
              <div className="col">
                  <span className="col-input">col : </span>
                  <input
                      value = { this.props.activeCol }
                      onChange={ event => this.props.changeCol(event.target.value) }
                  />
              </div>
              <div className="width">
                  <span className="width-input">width : </span>
                  <input
                      value = { this.props.activeWidth }
                      onChange={ event => this.props.changeWidth(event.target.value) }
                  />
              </div>
          </div>
        );
    }
}

function mapStateToProps(state){
  return {
    activeRow: state.activeRow,
    activeCol: state.activeCol,
    activeWidth: state.activeWidth
  };
}

function mapDispatchToProps(dispatch) {
  return bindActionCreators( {
    changeRow : changeRow,
    changeCol : changeCol,
    changeWidth : changeWidth
   }, dispatch);
}

export default connect(mapStateToProps, mapDispatchToProps)(Header);
