import React, {Component} from 'react';

import MainLayout from './main_layout/main_layout'
import ButtonList from './right-side/button_list'
import Header from './header_bar/header';

class App extends Component {
    constructor(props) {
        super(props);

        this.state = {
            row: '0',
            col: '0',
            width: '0',
            printCase: 4
        };
    }

    onChangeState(row, col, width) {
        this.setState({
            row: row,
            col: col,
            width: width
        });
    }

    render() {
        const changeState = (row, col, width) => this.onChangeState(row, col, width);

        return (
            <div className="wrapper">
                <div className="head">
                    <Header onChangeState={changeState}/>
                </div>
                <div className="left">
                    <MainLayout
                        row={this.state.row}
                        col={this.state.col}
                        printCase={this.state.printCase}
                    />
                </div>
                <div className="right">
                    <ButtonList
                        onPrintCaseSelect = {printCase => this.setState({printCase})}
                    />
                </div>
            </div>

        );
    }
}
export default App;
