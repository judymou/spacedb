(function() {
  // Create the visualization and put it in our div.
  const viz = new Spacekit.Simulation(document.getElementById('shape-container'), {
    basePath: '/static/spacekit',
  });

  // Create a skybox using NASA TYCHO artwork.
  viz.createSkybox(Spacekit.SkyboxPresets.NASA_TYCHO);

  // Add some light.
  viz.createLight();
  viz.createAmbientLight();

  // Create an object for 1998 XO94
  const obj = viz.createShape('myobj', {
    shape: {
      shapeUrl: window.SHAPE_PATH,
    },
    rotation: {
      enable: true,
    },
  });
  viz.zoomToFit(obj, 2 /* offset */);
})();
