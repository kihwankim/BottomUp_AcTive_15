export default function(state = '0', action){
  switch(action.type){
    case 'CHANGE_WIDTH':
        return action.payload;
    }
  return state;
}
