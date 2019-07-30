export default function(state = '', action){
  switch(action.type){
    case 'CHANGE_ROW':
      return action.payload;
  }
  return state;
}
