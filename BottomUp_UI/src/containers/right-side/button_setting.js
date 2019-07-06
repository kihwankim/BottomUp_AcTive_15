import React, {Component} from 'react';
import { connect } from 'react-redux';

class SettingButton extends Component{
  render(){
    return (
      <input
        type = "button"
        className="button"
        value="Setting"
        onClick = { () => this.onClickAndStoreAtDB() }
      />
    );
  }

  onClickAndStoreAtDB(){
    console.log(this.props.activeArray);
    if(!this.props.activeArray || this.props.activeArray.length == 0){
      alert("this is not correct data or Empty data");
    }else{

    }
    //여기에 디비 연결 코드 작성 하면되 activeArray 변수이고 이 변수는 this.props.activeArray
    //이렇게 쓰면되
  }
}

function mapStateToProps(state){
  return {
    activeArray: state.activeArray
  };
}

export default connect(mapStateToProps)(SettingButton);
