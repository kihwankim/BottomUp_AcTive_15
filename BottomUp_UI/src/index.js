import React, {Component} from 'react';
import ReactDOM from 'react-dom';
import { Provider } from 'react-redux';
import { createStore, applyMiddleware } from 'redux';
import reducers from './reducers';
import App from './Components/app';

const createStoreWithMiddleware = applyMiddleware()(createStore);

ReactDOM.render(
  <Provider store= { createStoreWithMiddleware(reducers) }>
  <App/>
  </Provider>
  , document.querySelector('.container'));
