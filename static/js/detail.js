(function() {
var config = {
  container: 'celestial-map',
  //projection: 'stereographic',
  //projection: 'airy',
  projection: 'equirectangular',
  datapath: 'https://ofrohn.github.io/data/',
  location: true,
  dsos: {
    show: true,
  },
  stars: {
    show: true,
    limit: 5.5,
    names: false,
  },
  constellations: {
    show: true,
    desig: false,  // Show full names of constellations
  },
  planets: {
    show: true,
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
Celestial.display(config);

// Load the rest of the page.
window.pageReady = true;
})();
