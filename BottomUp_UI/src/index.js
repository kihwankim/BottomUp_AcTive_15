import React, {Component} from 'react';
import ReactDOM from 'react-dom';
import MainLayout from './components/main_layout/main_layout'


class App extends Component {
    constructor(props) {
        super(props);

        this.state = {};
    }

    render() {
        return (
            <div className="total">
                <div className="wrapper">
                    <div className="head">head</div>
                    <div className="left">
                        <MainLayout/>
                    </div>
                    <div className="right">right</div>
                </div>
            </div>
        );
    }
}

ReactDOM.render(<App/>, document.querySelector('.container'));
