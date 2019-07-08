import { combineReducers } from 'redux';
import ActiveRow from './reducer_active_row';
import ActiveCol from './reducer_active_col';
import ActiveWidth from './reducer_active_width';
import ActiveArray from './reducer_active_array';
import ActiveMaxHeight from './reducer_active_max_height';

const rootReducer = combineReducers({
  activeRow: ActiveRow,
  activeCol: ActiveCol,
  activeWidth: ActiveWidth,
  activeArray: ActiveArray,
  activeMaxHeight: ActiveMaxHeight
});

export default rootReducer;
