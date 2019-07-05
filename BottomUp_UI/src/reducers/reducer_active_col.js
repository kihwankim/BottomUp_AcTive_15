export default function(state = '0', action){
  switch(action.type){
    case 'CHANGE_COL':
        console.log("col : " + action.payload);
        return action.payload;
  }
  return state;
}
