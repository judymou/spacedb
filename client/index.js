import React from 'react';
import ReactDOM from 'react-dom';

import Search from './components/Search.jsx';

Array.from(document.getElementsByClassName('react-search')).forEach(elt => {
  ReactDOM.render(<Search/>, elt);
});
