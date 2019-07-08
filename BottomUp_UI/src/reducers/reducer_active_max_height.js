export default function(state = 0, action){
  switch(action.type){
    case 'CHANGE_MAX_HEIGHT':
        return action.payload;
  }
  return state;
}
