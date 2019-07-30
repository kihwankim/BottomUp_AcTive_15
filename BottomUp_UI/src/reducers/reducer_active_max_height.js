export default function(state = '', action){
  switch(action.type){
    case 'CHANGE_MAX_HEIGHT':
        return action.payload;
  }
  return state;
}
