import React from 'react';
import {BrowserRouter as Router, Route, Routes} from 'react-router-dom';
import Home from '../Home/Home';
import * as routes from '../../Paths/paths.js';

//this may have problems because of webpack
const AppRouter = () => {
  return (
    <Router>
      <Routes>
        <Route path={routes.HOME} element={<Home />}> </Route>
        <Route path='*' element={<Home />} />
      </Routes>
    </Router>
  )
}

export default AppRouter;
