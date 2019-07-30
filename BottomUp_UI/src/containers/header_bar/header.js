import React, {Component} from 'react';
import {connect} from 'react-redux';
import {changeRow} from '../../actions/change_row';
import {changeCol} from '../../actions/change_col';
import {changeWidth} from '../../actions/change_width';
import {changeMaxHeight} from '../../actions/change_max_height';
import {bindActionCreators} from 'redux';
class Header extends Component {
    render() {
        return (
            <div className="header-list" id="container-for-input">
                <div className="row input-group" >
                    <span className="max-hegith-input input-group-text" id="inputGroup-sizing-sm">Row</span>
                    <input
                        value={this.props.activeRow}
                        onChange={(event) => this.props.changeRow(event.target.value)}
                        type="text" className="form-control h-auto" placeholder="Row"
                    />
                </div>
                <div className="col input-group">
                    <span className="max-hegith-input input-group-text" id="inputGroup-sizing-sm">Col</span>
                    <input
                        value={this.props.activeCol}
                        onChange={event => this.props.changeCol(event.target.value)}
                        type="text" className="form-control h-auto" placeholder="Col"
                    />
                </div>
                <div className="max-height input-group">
                    <span className="max-hegith-input input-group-text" id="inputGroup-sizing-sm">max</span>
                    <input
                        value={this.props.activeMaxHeight}
                        onChange={event => this.props.changeMaxHeight(event.target.value)}
                        type="text" className="form-control h-auto" placeholder="max Height"
                    />
                </div>
            </div>
        );
    }
}

function mapStateToProps(state) {
    return {
        activeRow: state.activeRow,
        activeCol: state.activeCol,
        activeWidth: state.activeWidth,
        activeMaxHeight: state.activeMaxHeight
    };
}

function mapDispatchToProps(dispatch) {
    return bindActionCreators({
        changeRow: changeRow,
        changeCol: changeCol,
        changeWidth: changeWidth,
        changeMaxHeight: changeMaxHeight
    }, dispatch);
}

export default connect(mapStateToProps, mapDispatchToProps)(Header);
