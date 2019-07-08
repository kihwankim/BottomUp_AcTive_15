import React, {Component} from 'react';
import {connect} from 'react-redux';

import firebase from 'firebase';

import $ from 'jquery';

class SettingButton extends Component {

    // render 전에 실행
    componentWillMount() {
        const firebaseConfig = {
            apiKey: "AIzaSyAllT3vsvGW9wv63Azr4tA_rkeLNcYL3lA",
            authDomain: "bottomup-sync.firebaseapp.com",
            databaseURL: "https://bottomup-sync.firebaseio.com",
            projectId: "bottomup-sync",
            storageBucket: "bottomup-sync.appspot.com",
            messagingSenderId: "384565070097",
            appId: "1:384565070097:web:9682fe90dcfa7724"
        };

        firebase.initializeApp(firebaseConfig);

        console.log(firebase);
    }

    render() {
        return (
            <input
                type="button"
                className="button"
                value="Setting"
                onClick={() => this.onClickAndStoreAtDB()}
            />
        );
    }

    onClickAndStoreAtDB() {
        function indexGuard(row, col, maxRow, maxCol) {
            if(row < 0 || col < 0 || row >= maxRow || col >= maxCol){
                return false;
            }else{
                return true;
            }
        }
        if (!this.props.activeArray || this.props.activeArray.length == 0) {
            alert("this is not correct data or Empty data");
        } else {
            // document.getElementById("table-body")
            let myTableArray = [];
            let piCount = 1;
            let direction=[[-1,0],[0,1],[1,0], [0,-1]];

            // 테이블을 2차원 배열로 생성
            // 동시에 라즈베리파이 인덱싱
            $("table#setting-table tr").each(function () {
                let arrayOfThisRow = [];
                let tableData = $(this).find('td');
                if (tableData.length > 0) {
                    tableData.each(function () {
                        if($(this).text() == "Pi"){
                            arrayOfThisRow.push(piCount.toString());
                            ++piCount;
                        }else{
                            arrayOfThisRow.push($(this).text());
                        }
                    });
                    myTableArray.push(arrayOfThisRow);
                }
            });

            // 기존 데이터 베이스 삭제
            firebase.database().ref('bottomup').remove();

            // 라즈베리파이 주변 값 확인
            // 동시에 객체 생성하여 데이터 베이스에 업로드
            for(let i = 0; i < myTableArray.length; i++){
                for(let j = 0; j < myTableArray[i].length; j++){
                    if($.isNumeric(myTableArray[i][j])){
                        let piNumber = myTableArray[i][j];

                        let top = indexGuard(i+direction[0][0], j+direction[0][1], myTableArray.length, myTableArray[i].length) ?
                            myTableArray[i+direction[0][0]][j+direction[0][1]] : "N";

                        let right = indexGuard(i+direction[1][0], j+direction[1][1], myTableArray.length, myTableArray[i].length) ?
                            myTableArray[i+direction[1][0]][j+direction[1][1]] : "N";

                        let bottom = indexGuard(i+direction[2][0], j+direction[2][1], myTableArray.length, myTableArray[i].length) ?
                            myTableArray[i+direction[2][0]][j+direction[2][1]] : "N";

                        let left = indexGuard(i+direction[3][0], j+direction[3][1], myTableArray.length, myTableArray[i].length) ?
                            myTableArray[i+direction[3][0]][j+direction[3][1]] : "N";

                        let pi ={
                            piNumber : piNumber,
                            top : top,
                            right : right,
                            bottom : bottom,
                            left : left
                        }
                        firebase.database().ref('bottomup').push(pi)
                            // 이곳에 원하는 요소 추가하면 된다.
                         .then(() => {
                            console.log('INSERTED!');
                        }).catch((error) => {
                            console.log(error);
                        })
                    }
                }
            }

        }
    }
}

function mapStateToProps(state) {
    return {
        activeArray: state.activeArray,
        row: state.activeRow,
        col: state.activeCol
    };
}

export default connect(mapStateToProps)(SettingButton);
