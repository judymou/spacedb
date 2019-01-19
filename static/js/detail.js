(function() {
var config = {
  datapath: 'https://ofrohn.github.io/data/',
  location: true,
  dsos: {
    show: false,
  },
  stars: {
    show: true,
    limit: 5,
    names: false,
  },
  constellations: {
    show: true,
    desig: false,  // Show full names of constellations
    namestyle: { fill:'#cccc99', align: 'center', baseline: 'middle',
                 font: ['12px Helvetica, Arial, sans-serif',  // Style for constellations
                        '9px Helvetica, Arial, sans-serif',  // Different fonts for diff.
                        '8px Helvetica, Arial, sans-serif']},// ranked constellations
    linestyle: { stroke: "#cccccc", width: 1, opacity: 0.3 },
  },
  planets: {
    show: true,
    //which: ['sol', 'mer', 'ven', 'lun', 'mar', 'jup', 'sat', 'ura', 'nep'],
    style: { fill: '#00ccff', font: 'bold 12px \'Lucida Sans Unicode\', Consolas, sans-serif',
             align: 'center', baseline: 'middle' },
    symbols: {
      'sol': {symbol: '\u25cf Sun', fill: '#ffff00'},
      'mer': {symbol: '\u25cf Mercury', fill: '#cccccc'},
      'ven': {symbol: '\u25cf Venus', fill: '#eeeecc'},
      'ter': {symbol: '\u2295', fill: '#00ffff'},
      'lun': {symbol: '\u25cf Moon', fill: '#ffffff'}, // overridden by generated cresent
      'mar': {symbol: '\u25cf Mars', fill: '#ff9999'},
      'cer': {symbol: '\u25cf Ceres', fill: '#cccccc'},
      'ves': {symbol: '\u25cf Vesta', fill: '#cccccc'},
      'jup': {symbol: '\u25cf Jupiter', fill: '#ff9966'},
      'sat': {symbol: '\u25cf Saturn', fill: '#ffcc66'},
      'ura': {symbol: '\u25cf Uranus', fill: '#66ccff'},
      'nep': {symbol: '\u25cf Neptune', fill: '#6666ff'},
      'plu': {symbol: '\u25cf Pluto', fill: '#aaaaaa'},
      'eri': {symbol: '\u25cf Eris', fill: '#eeeeee'},

      'added-planet': {symbol: '\u25cf Special Planet', fill: 'pink'},
    },
  },
  mw: {
    style: { fill: '#ffffff', opacity: 0.05 }  // Style for MW layers
  },
  lines: {
    ecliptic: {show: true},
  },
  horizon: {  //Show horizon marker, if location is set and map projection is all-sky
    show: true,
    stroke: '#0000ff', // Line
    width: 1.0,
    fill: '#000000',   // Area below horizon
    opacity: 0.5
  }
};

// Asterisms canvas style properties for lines and text
const pointStyle = {
  stroke: 'rgba(255, 0, 204, 1)',
  fill: 'rgba(255, 0, 204, 0.15)'
};
const textStyle = {
  fill:'rgba(255, 0, 204, 1)',
  font: '25px Helvetica, Arial, sans-serif',
  align: 'left',
  baseline: 'bottom'
};
// JSON structure of the object to be displayed, in this case
// the Summer Triangle between Vega, Deneb and Altair
const jsonSnr = {
  'type':'FeatureCollection',
  // this is an array, add as many objects as you want
  'features':[
    {'type':'Feature',
      'id':'SomeDesignator',
      'properties': {
        // Name
        'name':'Some Name',
        // Size in arcminutes
        'dim': 10,
        'mag': -50,
        'type': 'spaceobject',
      }, 'geometry':{
        // the line object as an array of point coordinates
        'type':'Point',
        'coordinates': [80.7653, 38.7837]
      }
  }
]};

Celestial.add({type: 'planet', callback: function(error, json) {
  const eph = new Spacekit.Ephem(window.OBJECT_DEFINITIONS[0].ephem);
  const elements = {
    // https://github.com/ofrohn/d3-celestial/blob/master/src/kepler.js
    a: eph.get('a'),
    e: eph.get('e'),
    i: eph.get('i'),
    M: eph.get('ma'),
    ep: new Date((eph.get('epoch')-2440587.5)*86400000).toISOString().split("T")[0],
    w: eph.get('w'),
    N: eph.get('om'),
    n: eph.get('n', 'deg'),
  };
  var kep = Celestial.Kepler().id('added-planet').elements(elements);

  Celestial.container.selectAll(".planets")
         .data([kep])
         .enter().append("path")
         .attr("class", "planet");
  Celestial.redraw();
}, redraw: function() {
  // Select the added objects by class name as given previously
  /*
  Celestial.container.selectAll('.added-object').each(function(d) {
    if (!Celestial.origin) {
      return;
    }
    console.log(d.id())
    var dt = Celestial.date();
    var origin = Celestial.origin(dt).spherical();
    var eqcoords = d(dt).equatorial(origin);
    var pt = Celestial.mapProjection([eqcoords.ra, eqcoords.dec]);
    var r = 25;

    // draw on canvas
    // Set object styles
    Celestial.setStyle(pointStyle);
    // Start the drawing path
    Celestial.context.beginPath();
    // Thats a circle in html5 canvas
    Celestial.context.arc(pt[0], pt[1], r, 0, 2 * Math.PI);
    // Finish the drawing path
    Celestial.context.closePath();
    // Draw a line along the path with the prevoiusly set stroke color and line width
    Celestial.context.stroke();
    // Fill the object path with the prevoiusly set fill color
    Celestial.context.fill();
    // Set text styles
    Celestial.setTextStyle(textStyle);
    // and draw text on canvas
    Celestial.context.fillText('assss', pt[0]+r, pt[1]+r);
  });
 */
}});

/*
Celestial.add({type:'star', callback: function(error, json) {
  if (error) return console.warn(error);
  // Load the geoJSON file and transform to correct coordinate system, if necessary
  var objects = Celestial.getData(jsonSnr, config.transform);
  // Add to celestiasl objects container in d3
  Celestial.container.selectAll('.star')
  .data(objects.features)
  .enter().append('path')
  .attr('class', 'spaceobject');
  // Trigger redraw to display changes
  Celestial.redraw();
}, redraw: function() {
  // Select the added objects by class name as given previously
  Celestial.container.selectAll('.spaceobject').each(function(d) {
    // If point is visible (this doesn't work automatically for points)
    if (Celestial.clip(d.geometry.coordinates)) {
      // get point coordinates
      var pt = Celestial.mapProjection(d.geometry.coordinates);
      // object radius in pixel, could be varable depending on e.g. magnitude
      //var r = Math.pow(parseInt(d.properties.dim) * 0.25, 0.5);
      var r = 50;

      // draw on canvas
      // Set object styles
      Celestial.setStyle(pointStyle);
      // Start the drawing path
      Celestial.context.beginPath();
      // Thats a circle in html5 canvas
      Celestial.context.arc(pt[0], pt[1], r, 0, 2 * Math.PI);
      // Finish the drawing path
      Celestial.context.closePath();
      // Draw a line along the path with the prevoiusly set stroke color and line width
      Celestial.context.stroke();
      // Fill the object path with the prevoiusly set fill color
      Celestial.context.fill();
      // Set text styles
      Celestial.setTextStyle(textStyle);
      // and draw text on canvas
      Celestial.context.fillText(d.properties.name, pt[0]+r, pt[1]+r);
    }
  });
}});
*/
Celestial.display(config);

// Load the rest of the page.
window.pageReady = true;
})();
