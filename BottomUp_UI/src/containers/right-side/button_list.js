import React, {Component} from 'react';

import SettingButton from './button_setting';
import { connect } from 'react-redux';
import { bindActionCreators } from  'redux';
import { makeArray } from '../../actions/make_array';

class ButtonList extends Component{
    constructor(props){
        super(props);
        this.state = {
          case : 4,
        };
    }

    printCaseSelect(printCase){
      this.setState({
        case : printCase
      });
    }

    setDataAndMakeArray(row, col, height){
      this.props.onSetData(1);
      let tables = [];
      // Outer loop to create parent
      for(let indexOfHeights = 0; indexOfHeights < parseInt(height); indexOfHeights++){
        let table = [];
        let keyData = indexOfHeights.toString();
        for (let i = 0; i < parseInt(row); i++) {
          let children = [];
          //Inner loop to create children
          let keyDataAndI = i.toString() + keyData;
          for (let j = 0; j < parseInt(col); j++) {
            let keyDataAndIAndJ = keyDataAndI + j.toString();
            children.push(<td key={keyDataAndIAndJ} onClick={event => this.writeContent(event.target)}></td>);
          }
          //Create the parent and add the children
          table.push(<tr key={keyDataAndI}>{children}</tr>);
        }
        tables.push(table);
      }
      if(tables.length == 0){
        alert("please insert correct data");
      }
      this.props.makeArray(tables);
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
        }else if(printCase == 5){
            td.innerText = "S";
        }else{
          td.innerText = "";
        }
    }

    render() {
        return (
            <div className="button-list">
                <button className="button" onClick={ () => this.setDataAndMakeArray(this.props.activeRow, this.props.activeCol, this.props.activeMaxHeight) }>data setting</button>
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
                <button className="button" onClick={event => this.printCaseSelect(5)}>Stairs</button>
                <br/><br/>
                <SettingButton />
            </div>
        );
    }
}

function mapStateToProps(state){
  return {
    activeRow: state.activeRow,
    activeCol: state.activeCol,
    activeMaxHeight: state.activeMaxHeight
  };
}

function mapDispatchToProps(dispatch) {
  return bindActionCreators( {
     makeArray : makeArray
   }, dispatch);
}

export default connect(mapStateToProps, mapDispatchToProps)(ButtonList);
