import React, {Component} from 'react';
import { connect } from 'react-redux';

class MainLayout extends Component {
    constructor(props){
      super(props);
    }

    renderTables(){
      let number = 0;
      return this.props.activeArray.map((table) => {
        number +=1;
        let data = number.toString() + "-1";
        return (
          <div key={data}>
            {number}
            <table key={number} className="main-layout table table-bordered table-striped" id={number}>
              <thead></thead>
              <tbody>
                  {table}
              </tbody>
            </table>
          </div>
        );
      });
    }

    render() {
        if (this.props.isSetting == 0) {
            return (<div> please wait...</div>);
        }

        return (
            <div>
              { this.renderTables() }
            </div>
        );
    }
}

function mapStateToProps(state){
  return {
    activeArray: state.activeArray
  };
}//객체 상태로 넘겨줘야함

export default connect(mapStateToProps)(MainLayout);
