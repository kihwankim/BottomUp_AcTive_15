import React, {Component} from 'react';

class ButtonList extends Component{
    constructor(props){
        super(props);
        this.state = {case : 0};
    }

    render() {
        return (
            <div className="button-list">
                <button className="button">Window</button>
                <br/><br/>
                <button className="button">Door</button>
                <br/><br/>
                <button className="button">Pi</button>
                <br/><br/>
                <button className="button">Bridge</button>

            </div>
        );
    }
}
export default ButtonList;
