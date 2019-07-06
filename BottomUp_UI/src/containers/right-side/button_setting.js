import React, {Component} from 'react';
import {connect} from 'react-redux';

import firebase from 'firebase';

class SettingButton extends Component {

    // render 전에 실행
    componentWillMount() {
        var firebaseConfig = {
            apiKey: "AIzaSyAllT3vsvGW9wv63Azr4tA_rkeLNcYL3lA",
            authDomain: "bottomup-sync.firebaseapp.com",
            databaseURL: "https://bottomup-sync.firebaseio.com",
            projectId: "bottomup-sync",
            storageBucket: "bottomup-sync.appspot.com",
            messagingSenderId: "384565070097",
            appId: "1:384565070097:web:9682fe90dcfa7724"
        };

// Initialize Firebase
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
        if (!this.props.activeArray || this.props.activeArray.length == 0) {
            alert("this is not correct data or Empty data");
        } else {
            
        }
        //여기에 디비 연결 코드 작성 하면되 activeArray 변수이고 이 변수는 this.props.activeArray
        //이렇게 쓰면되

    }
}

function mapStateToProps(state) {
    return {
        activeArray: state.activeArray
    };
}

export default connect(mapStateToProps)(SettingButton);
