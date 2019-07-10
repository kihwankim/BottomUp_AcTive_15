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
            // 기존 데이터 베이스 삭제
            firebase.database().ref('bottomup').remove();

            let directionInfo=[[-1,0],[0,1],[1,0], [0,-1]];

            for (let height = 1; height <= this.props.maxNumber; height++) {

                // document.getElementById("table-body")
                let myTableArray = [];
                let piCount = 1;


                // 테이블을 2차원 배열로 생성
                // 동시에 라즈베리파이 인덱싱
                let pis = [
                    {height: height}
                ];


                $(`table#${height} tr`).each(function () {
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

                // 라즈베리파이 주변 값 확인
                // 동시에 객체 생성하여 데이터 베이스에 업로드
                for(let i = 0; i < myTableArray.length; i++){
                    for(let j = 0; j < myTableArray[i].length; j++){
                        if($.isNumeric(myTableArray[i][j])){
                            let piNumber = myTableArray[i][j];
                            let startRow, startCol, data;
                            let directionalDatas = [];
                            for (let direction = 0; direction < 4; direction++) {
                                data = indexGuard(i+directionInfo[direction][0], j+directionInfo[direction][1], myTableArray.length, myTableArray[i].length) ?
                                    myTableArray[i+directionInfo[direction][0]][j+directionInfo[direction][1]] : "N";
                                if(data == "B"){
                                    startRow = i;
                                    startCol = j;
                                    while(indexGuard(startRow+directionInfo[direction][0], startCol+directionInfo[direction][1], myTableArray.length, myTableArray[i].length)){
                                        startRow = startRow+directionInfo[direction][0];
                                        startCol = startCol+directionInfo[direction][1];
                                        if(myTableArray[startRow][startCol] == "B"){
                                            continue;
                                        }else if($.isNumeric(myTableArray[startRow][startCol])){
                                            data = myTableArray[startRow][startCol];
                                        }else{
                                            break;
                                        }
                                    }
                                }
                                directionalDatas.push(data);
                            }

                            let pi ={
                                piNumber : piNumber,
                                top : directionalDatas[0],
                                right : directionalDatas[1],
                                bottom : directionalDatas[2],
                                left : directionalDatas[3]
                            };
                            pis.push(pi);
                        }
                    }
                }

                firebase.database().ref('bottomup').push(pis)
                // 이곳에 원하는 요소 추가하면 된다.
                    .then(() => {
                        console.log(pis);
                        console.log('INSERTED!');
                    }).catch((error) => {
                    console.log(error);
                })
            }
        }
    }
}

function mapStateToProps(state) {
    return {
        activeArray: state.activeArray,
        row: state.activeRow,
        col: state.activeCol,
        maxNumber: state.activeMaxHeight
    };
}

export default connect(mapStateToProps)(SettingButton);
