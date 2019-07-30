export default function(state = '', action){
  switch(action.type){
    case 'CHANGE_COL':
        return action.payload;
  }
  return state;
}
