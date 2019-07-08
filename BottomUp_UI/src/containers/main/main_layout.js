import React, {Component} from 'react';
import { connect } from 'react-redux';

class MainLayout extends Component {
    constructor(props){
      super(props);
    }

    render() {
        if (this.props.isSetting == 0) {
            return (<div> please wait...</div>);
        }

        return (
            <div>
                <table className="main-layout" id="setting-table">
                    <thead></thead>
                    <tbody>
                        { this.props.activeArray }
                    </tbody>
                </table>
            </div>
        );
    }
}

function mapStateToProps(state){
  return {
    activeRow: state.activeRow,
    activeCol: state.activeCol,
    activeArray: state.activeArray
  };
}//객체 상태로 넘겨줘야함

export default connect(mapStateToProps)(MainLayout);
