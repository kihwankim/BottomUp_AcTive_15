export default function(state = [], action){
  switch(action.type){
    case 'ARRAY':
        return action.payload;
  }
  return state;
}
