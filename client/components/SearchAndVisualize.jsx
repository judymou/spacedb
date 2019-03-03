import React from 'react';
import PropTypes from 'react-proptypes';

import AsyncSelect from 'react-select/lib/Async';

import { parseQuery } from '../util';

const INPUT_LENGTH_MIN = 3;

const loadOptions = (inputValue, callback) => {
  return new Promise(resolve => {
    if (inputValue.length < INPUT_LENGTH_MIN) {
      resolve([]);
      return;
    }
    fetch(`/api/objects/search?q=${inputValue}`).then(resp => {
      return resp.json()
    }).then(respJson => {
      resolve(respJson.results.map(result => {
        return {
          label: result.fullname,
          vizLabel: result.name,
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
    this._objCount = 0;
    this.state = {
      inputValue: '',
      selectedObjects: [],
    };
  }

  componentDidMount() {
    const query = parseQuery(location.hash);
    if (query.ob) {
      fetch(`/api/objects?slugs=${query.ob}`).then(resp => {
        return resp.json()
      }).then(respJson => {
        this.addMany(respJson.results.map(result => {
          return {
            label: result.fullname,
            vizLabel: result.name,
            value: result.slug,
            ephem: result.ephem,
          };
        }), {
          showLabel: true,
          showOrbit: true,
          updateHash: true,
        });
      });
    }
    if (query.cat) {
      fetch(`/api/category/${query.cat}?limit=3000`).then(resp => {
        return resp.json()
      }).then(respJson => {
        this.addMany(respJson.data.map(result => {
          return {
            label: result.fullname,
            vizLabel: result.name,
            value: result.slug,
            ephem: result.ephem,
          };
        }), {
          showLabel: false,
          showOrbit: false,
          updateHash: false,
          particleSize: 8,
        });
      });

    }
  }

  addMany(objs, opts) {
    opts = opts || {};
    objs.forEach(obj => {
      const key = `spaceobject${this._objCount++}`;
      window.vizcontainer.createObject(key, Object.assign(window.VIZ_OBJECT_OPTS, {
        ephem: new Spacekit.Ephem(obj.ephem, 'deg'),
        // Show short name
        labelText: opts.showLabel ? obj.vizLabel : undefined,
        hideOrbit: !opts.showOrbit,
        particleSize: opts.particleSize,
      }));
    });

    if (opts.updateHash) {
      this.setState(prevState => ({ selectedObjects: prevState.selectedObjects.concat(objs) }), () => {
        window.location.hash = '#ob=' + this.state.selectedObjects.map(object => object.value).join(',');
      });
    }
  }

  handleChange(inputValue) {
    this.addMany([inputValue], {
      showLabel: true,
      showOrbit: true,
      updateHash: true,
    });
  }

  getObjectList() {
    return this.state.selectedObjects.map(object => {
      return (
        <div className="tile" key={`selectedObject-${object.value}`}>
          <a target="_blank" href={`/asteroid/${object.value}`}>
            <h5>{object.label}</h5>
          </a>
        </div>
      );
    });
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
              primary25: '#404040',
              primary: 'black',
              neutral0: '#1d1d1d',
              neutral5: '#000a',
              neutral10: '#000b',
              neutral20: '#666',
              neutral30: '#000d',
              neutral40: '#000e',
            },
          })}
        />
        {this.state.selectedObjects.length > 0 ? (
          <div className="item-container tile-list">
            {this.getObjectList()}
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
