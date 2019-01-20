import React from 'react';
import ReactDOM from 'react-dom';

import Search from './components/Search.jsx';
import SearchAndVisualize from './components/SearchAndVisualize.jsx';

Array.from(document.getElementsByClassName('react-search')).forEach(elt => {
  ReactDOM.render(<Search/>, elt);
});

Array.from(document.getElementsByClassName('react-search-and-visualize')).forEach(elt => {
  ReactDOM.render(<SearchAndVisualize/>, elt);
});
