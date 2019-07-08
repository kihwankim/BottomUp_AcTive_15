import React, {Component} from 'react';
import { connect } from 'react-redux';

class MainLayout extends Component {

    render() {
        if (!this.props.activeRow || this.props.activeRow == 0
            || !this.props.activeCol || this.props.activeCol == 0) {
            return <div> please wait...</div>
        }

        return (
            <div>
                <table className="main-layout">
                    <thead></thead>
                    <tbody id="table-body">
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
