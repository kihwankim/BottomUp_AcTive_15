import React, {Component} from 'react';
import ReactDOM from 'react-dom';
import MainLayout from './components/main_layout/main_layout'
import ButtonList from './components/right-side/button_list'
import Header from './components/header_bar/header';

class App extends Component {
    constructor(props) {
        super(props);

        this.state = {
            row: '0',
            col: '0',
            width: '0'
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
                    />
                </div>
                <div className="right">
                    <ButtonList/>
                </div>
            </div>

        );
    }
}

ReactDOM.render(<App/>, document.querySelector('.container'));
