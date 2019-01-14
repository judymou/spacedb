function init3dVis() {
  return;

  // Create the visualization and put it in our div.
  const viz = new Spacekit.Container(document.querySelector('.vis-container'), Object.assign({
    //assetPath: 'http://localhost:8001/src/assets',
    assetPath: '/static/spacekit',
    startDate: Date.now(),
  }, window.VIZ_SIMULATION_OPTS));

  // Create a skybox using NASA TYCHO artwork.
  viz.createSkybox(Spacekit.SkyboxPresets.NASA_TYCHO);

  // Create our first object - the sun - using a preset space object.
  viz.createObject('sun', Spacekit.SpaceObjectPresets.SUN);

  // Then add some planets
  viz.createObject('mercury', Spacekit.SpaceObjectPresets.MERCURY);
  viz.createObject('venus', Spacekit.SpaceObjectPresets.VENUS);
  viz.createObject('earth', Object.assign(Spacekit.SpaceObjectPresets.EARTH, { labelText: 'Earth' }));
  viz.createObject('mars', Spacekit.SpaceObjectPresets.MARS);
  viz.createObject('jupiter', Spacekit.SpaceObjectPresets.JUPITER);
  viz.createObject('saturn', Spacekit.SpaceObjectPresets.SATURN);
  viz.createObject('uranus', Spacekit.SpaceObjectPresets.URANUS);
  viz.createObject('neptune', Spacekit.SpaceObjectPresets.NEPTUNE);

  window.EPHEMERIS.forEach(function(ephem) {
    const spaceobject = viz.createObject('spaceobject', Object.assign(window.VIZ_OBJECT_OPTS, {
      ephem: new Spacekit.Ephem(ephem, 'deg'),
    }));
  });

  // Controls
  document.querySelectorAll('.vis-controls__slower').forEach(function(elt) {
    elt.onclick = function() {
      viz.setJedPerSecond(viz.getJedPerSecond() * 0.1);
    };
  });
  document.querySelectorAll('.vis-controls__faster').forEach(function(elt) {
    elt.onclick = function() {
      viz.setJedPerSecond(viz.getJedPerSecond() * 10.0);
    };
  });
  document.querySelectorAll('.vis-controls__set-date').forEach(function(elt) {
    elt.onclick = function() {
      viz.setDate(new Date(prompt('Enter a date in the format YYYY-mm-dd.', '2000-01-01')));
    };
  });

  // Status line
  viz.onTick = function() {
    document.querySelectorAll('.vis-status').forEach(function(elt) {
      elt.innerHTML = viz.getDate().toLocaleString() + '';
    });
  };
}
