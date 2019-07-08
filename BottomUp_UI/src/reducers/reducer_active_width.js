export default function(state = '0', action){
  switch(action.type){
    case 'CHANGE_WIDTH':
        console.log("width : " + action.payload);
        return action.payload;
    }
  return state;
}
