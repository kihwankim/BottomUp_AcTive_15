import React, {Component} from 'react';

import SettingButton from './button_setting';
import { connect } from 'react-redux';
import { bindActionCreators } from  'redux';
import { makeArray } from '../../actions/make_array';

class ButtonList extends Component{
    constructor(props){
        super(props);
        this.state = {case : 4};
    }

    printCaseSelect(printCase){
      this.setState({
        case : printCase
      });
    }

    setDataAndMakeArray(row, col){
      let table = [];
      // Outer loop to create parent

      for (let i = 0; i < parseInt(row); i++) {
        let children = [];
        //Inner loop to create children
        for (let j = 0; j < parseInt(col); j++) {
          children.push(<td onClick={event => this.writeContent(event.target)}></td>);
        }
        //Create the parent and add the children
        table.push(<tr>{children}</tr>);
      }

      this.props.makeArray(table);
    }

    writeContent(td) {
        let printCase = this.state.case;
        if(printCase == 0){
            td.innerText = "W";
        }else if(printCase == 1){
            td.innerText = "D";
        }else if(printCase == 2){
            td.innerText = "Pi";
        }else if(printCase == 3){
            td.innerText = "B";
        }else{
          td.innerText = "";
        }
    }

    render() {
        return (
            <div className="button-list">
                <button className="button" onClick={ () => this.setDataAndMakeArray(this.props.activeRow, this.props.activeCol) }>data setting</button>
                <br/><br/>
                <button className="button" onClick={event => this.printCaseSelect(0)}>Window</button>
                <br/><br/>
                <button className="button" onClick={event => this.printCaseSelect(1)}>Door</button>
                <br/><br/>
                <button className="button" onClick={event => this.printCaseSelect(2)}>Pi</button>
                <br/><br/>
                <button className="button" onClick={event => this.printCaseSelect(3)}>Bridge</button>
                <br/><br/>
                <button className="button" onClick={event => this.printCaseSelect(4)}>Empty</button>
                <br/><br/>
                <SettingButton />
            </div>
        );
    }
}

function mapStateToProps(state){
  return {
    activeRow: state.activeRow,
    activeCol: state.activeCol
  };
}

function mapDispatchToProps(dispatch) {
  return bindActionCreators( {
     makeArray : makeArray
   }, dispatch);
}

export default connect(mapStateToProps, mapDispatchToProps)(ButtonList);