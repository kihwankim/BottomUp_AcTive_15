import React, {Component} from 'react';

class MainLayout extends Component{
    constructor(props){
        super(props);
        this.state = {
            row: 5,
            col: 3
        };
    }

    createTable = () => {
        let table = []
        // Outer loop to create parent
        for (let i = 0; i < this.state.row; i++) {
            let children = []
            //Inner loop to create children
            for (let j = 0; j < this.state.col; j++) {
                children.push(<td>{`Column ${j + 1}`}</td>)
            }
            //Create the parent and add the children
            table.push(<tr>{children}</tr>)
        }
        return table
    }

    render() {
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
