export default function(state = '0', action){
  switch(action.type){
    case 'CHANGE_ROW':
      console.log("row : " + action.payload);
      return action.payload;
  }
  return state;
}
