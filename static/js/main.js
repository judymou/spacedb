function init3dVis() {
  // Create the visualization and put it in our div.
  const viz = new Spacekit.Simulation(document.querySelector('.vis-container'), Object.assign({
    //basePath: 'http://localhost:8001/src',
    basePath: '/static/spacekit',
    startDate: Date.now(),
  }, window.VIZ_SIMULATION_OPTS));

  viz.renderOnlyInViewport();

  // Create a skybox using NASA TYCHO artwork.
  //viz.createSkybox(Spacekit.SkyboxPresets.NASA_TYCHO);
  viz.createStars();

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
  window.vizcontainer = viz;

  window.spaceobjects = {};
  window.OBJECT_DEFINITIONS.forEach(function(objDef, idx) {
    const spaceobject = viz.createObject(`spaceobject${idx}`, Object.assign(window.VIZ_OBJECT_OPTS, {
      ephem: new Spacekit.Ephem(objDef.ephem, 'deg'),
      labelText: objDef.name,
    }));

    if (idx === 0) {
      viz.zoomToFit(spaceobject, 0.5);
    }

    window.spaceobjects[objDef.slug] = spaceobject;
  });

  /*
  window.BACKGROUND_OBJECT_DEFINITIONS.forEach(function(objDef, idx) {
    viz.createObject(`spaceobject-background${idx}`, {
      hideOrbit: true,
      particleSize: 5,
      ephem: new Spacekit.Ephem(objDef.ephem, 'deg'),
    });
  });
 */
  if (typeof window.BACKGROUND_QUERY_URL !== 'undefined') {
    fetch(`${window.BACKGROUND_QUERY_URL}?limit=2000`).then(function(resp) {
      return resp.json();
    }).then(function(result) {
      result.data.forEach(function(objDef, idx) {
        viz.createObject(`spaceobject-background${idx}`, {
          hideOrbit: true,
          particleSize: 8,
          ephem: new Spacekit.Ephem(objDef, 'deg'),
        });
      });
    });

  }

  // Controls
  document.querySelectorAll('.vis-controls__slower').forEach(function(elt) {
    elt.onclick = function() {
      viz.setJdPerSecond(viz.getJdPerSecond() * 0.1);
    };
  });
  document.querySelectorAll('.vis-controls__faster').forEach(function(elt) {
    elt.onclick = function() {
      viz.start();
      viz.setJdPerSecond(viz.getJdPerSecond() * 10.0);
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

function initReferenceTables() {
  document.querySelectorAll('.reference-table-gradient').forEach(function(elt) {
    elt.onclick = function() {
      // Hide gradient
      elt.style.display = 'none';

      // Show full table
      elt.parentElement.children[0].style.overflow = 'visible';
      elt.parentElement.children[0].style.maxHeight = 'none';
    };
  });
}
