import React, {Component} from 'react';

class MainLayout extends Component {
    constructor(props) {
        super(props);
    }

    writeContent(td) {
        let printCase = this.props.printCase;
        if(printCase == 0){
            td.innerText = "W";
        }else if(printCase == 1){
            td.innerText = "D";
        }else if(printCase == 2){
            td.innerText = "Pi";
        }else if(printCase == 3){
            td.innerText = "B";
        }else{
          td.innerText = "";
        }
    }

    createTable = () => {
        let table = [];
        // Outer loop to create parent

        for (let i = 0; i < parseInt(this.props.row); i++) {
            let children = [];
            //Inner loop to create children
            for (let j = 0; j < parseInt(this.props.col); j++) {
                children.push(<td onClick={event => this.writeContent(event.target)}></td>);
            }
            //Create the parent and add the children
            table.push(<tr>{children}</tr>);
        }
        return table;
    }

    render() {
        if (!this.props.row || this.props.row == 0
            || !this.props.col || this.props.col == 0) {
            console.log("row is not" + this.props.row)
            return <div> please wait...</div>
        }

        return (
            <div>
                <table className="main-layout">
                    {this.createTable()}
                </table>
            </div>
        );
    }
}

export default MainLayout;
