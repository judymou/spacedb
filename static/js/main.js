(function() {
  // Create the visualization and put it in our div.
  const viz = new Spacekit.Container(document.getElementById('vis-container'), {
    assetPath: 'http://localhost:8001/src/assets',
    jed: 2458461.459,
  });

  // Create a skybox using NASA TYCHO artwork.
  viz.createSkybox(Spacekit.SkyboxPresets.NASA_TYCHO);

  // Create our first object - the sun - using a preset space object.
  viz.createObject('sun', Spacekit.SpaceObjectPresets.SUN);

  // Then add some planets
  viz.createObject('mercury', Spacekit.SpaceObjectPresets.MERCURY);
  viz.createObject('venus', Spacekit.SpaceObjectPresets.VENUS);
  viz.createObject('earth', Spacekit.SpaceObjectPresets.EARTH);
  viz.createObject('mars', Spacekit.SpaceObjectPresets.MARS);
  viz.createObject('jupiter', Spacekit.SpaceObjectPresets.JUPITER);
  viz.createObject('saturn', Spacekit.SpaceObjectPresets.SATURN);
  viz.createObject('uranus', Spacekit.SpaceObjectPresets.URANUS);
  viz.createObject('neptune', Spacekit.SpaceObjectPresets.NEPTUNE);

  // Add spacex's tesla roadster
  // Data from https://ssd.jpl.nasa.gov/horizons_batch.cgi?batch=1&COMMAND=-143205&CENTER=%27500@10%27&MAKE_EPHEM=YES&TABLE_TYPE=ELEMENTS&START_TIME=2018-05-01&STOP_TIME=%272018-05-01+00:00:01%27&OUT_UNITS=AU-D&REF_PLANE=ECLIPTIC&REF_SYSTEM=J2000&TP_TYPE=ABSOLUTE&ELEM_LABELS=YES&CSV_FORMAT=NO&OBJ_DATA=YES

  const spaceobject = viz.createObject('spaceobject', {
    ephem: new Spacekit.Ephem(window.EPHEMERIS, 'deg'),
    ecliptic: {
      displayLines: true,
    },
  });
})();
