export default function(state = '0', action){
  switch(action.type){
    case 'CHANGE_ROW':
      return action.payload;
  }
  return state;
}
