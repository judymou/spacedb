import React from 'react';
import PropTypes from 'react-proptypes';

import AsyncSelect from 'react-select/lib/Async';

const loadOptions = (inputValue, callback) => {
  return new Promise(resolve => {
    if (inputValue.length < 3) {
      resolve([]);
      return;
    }
    fetch(`/api/objects/search?q=${inputValue}`).then(resp => {
      return resp.json()
    }).then(respJson => {
      resolve(respJson.results.map(result => {
        return {
          label: result.fullname,
          value: result.slug,
        };
      }));
    });
  });
};

class Search extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      inputValue: '',
    };
  }

  handleChange(inputValue) {
    this.setState({ inputValue })
    window.location.href = `/asteroid/${inputValue.value}`;
  }

  render() {
    return (
      <AsyncSelect
        cacheOptions
        loadOptions={loadOptions}
        onChange={this.handleChange.bind(this)}
        placeholder="Search for an asteroid or comet..."
        className="topnav__react-search__control"
      />
    );
  }
}

Search.propTypes = {
  blah: PropTypes.string,
};

export default Search;
