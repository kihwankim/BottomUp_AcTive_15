import React, {Component} from 'react';
import SettingButton from './button_setting';

class ButtonList extends Component{
    constructor(props){
        super(props);
        this.state = {case : 4};
    }

    printCaseSelect(printCase){
        this.props.onPrintCaseSelect(printCase);
    }

    render() {
        return (
            <div className="button-list">
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
export default ButtonList;
