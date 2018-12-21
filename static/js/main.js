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

  window.EPHEMERIS.forEach(function(ephem) {
    const spaceobject = viz.createObject('spaceobject', Object.assign(window.VIZ_OPTS, {
      ephem: new Spacekit.Ephem(ephem, 'deg'),
    }));
  });
})();
