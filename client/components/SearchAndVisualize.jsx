import React from 'react';
import PropTypes from 'react-proptypes';

import AsyncSelect from 'react-select/lib/Async';

const INPUT_LENGTH_MIN = 3;

const loadOptions = (inputValue, callback) => {
  return new Promise(resolve => {
    if (inputValue.length < INPUT_LENGTH_MIN) {
      resolve([]);
      return;
    }
    fetch(`/api/asteroids?q=${inputValue}`).then(resp => {
      return resp.json()
    }).then(respJson => {
      resolve(respJson.results.map(result => {
        return {
          label: result.fullname,
          value: result.slug,
          ephem: result.ephem,
        };
      }));
    });
  });
};

class SearchAndVisualize extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      inputValue: '',
      selectedObjects: [],
    };
  }

  handleChange(inputValue) {
    if (window.vizcontainer) {
      const spaceobject = window.vizcontainer.createObject('spaceobject', Object.assign(window.VIZ_OBJECT_OPTS, {
        ephem: new Spacekit.Ephem(inputValue.ephem, 'deg'),
      }));
    }
    this.state.selectedObjects.push(
      <div className="tile">
        <a target="_blank" href={`/asteroid/${inputValue.value}`}>
          <h5>{inputValue.label}</h5>
        </a>
      </div>
    );
    this.setState({selectedObjects: this.state.selectedObjects});
  }

  render() {
    return (
      <div>
        <AsyncSelect
          cacheOptions
          loadOptions={loadOptions}
          onChange={this.handleChange.bind(this)}
          value={null}
          placeholder="Search for an asteroid or comet..."
          className="topnav__react-search__control"
          noOptionsMessage={() => {
            if (this.state.inputValue.length < INPUT_LENGTH_MIN) {
              return null;
            }
            return "No matching objects"
          }}
          styles={{
            input: base => ({
              ...base,
              color: "#fff"
            }),
            noOptionsMessage: base => ({
              ...base,
              color: "#ccc"
            }),
            loadingMessage: base => ({
              ...base,
              color: "#ccc"
            }),
          }}
          theme={(theme) => ({
            ...theme,
            borderRadius: 0,
            colors: {
            ...theme.colors,
              primary25: 'hotpink',
              primary: 'black',
              neutral0: '#000',
              neutral5: '#000a',
              neutral10: '#000b',
              neutral20: '#000c',
              neutral30: '#000d',
              neutral40: '#000e',
            },
          })}
        />
        {this.state.selectedObjects.length > 0 ? (
          <div className="item-container tile-list">
            {this.state.selectedObjects}
          </div>
        ): null}
      </div>
    );
  }
}

SearchAndVisualize.propTypes = {
  blah: PropTypes.string,
};

export default SearchAndVisualize;
