window.OrbitDiagram = (function() {
  'use strict';

  function OrbitDiagram(selector, options) {
    this.elt = document.querySelector(selector);
    this.selector = selector;
    this.orbit_svg = null;

    options = options || {};
    this.DIAGRAM_HEIGHT = options.diagram_height || this.elt.offsetHeight;
    this.DIAGRAM_WIDTH = options.diagram_width || this.elt.offsetWidth;
    this.SUN_X = options.sun_x || this.DIAGRAM_WIDTH / 2;
    this.SUN_Y = options.sun_y || this.DIAGRAM_HEIGHT / 2 - 10;
    this.PIXELS_PER_AU = options.pixels_per_au || 50;
  }

  OrbitDiagram.prototype.prepareRender = function() {
    this.elt.innerHTML = '';
    this.orbit_svg = d3.select(this.selector)
        .append('svg:svg')
        .attr('width', this.DIAGRAM_WIDTH)
        .attr('height', this.DIAGRAM_HEIGHT)

    this.plotSun();
  }

  OrbitDiagram.prototype.renderPlanets = function(useSmartLabels, labelThreshold) {
    var args = [
      [0.38709893, 0.20563069, 77.45779628, 'purple', 'Mercury'],
      [0.72333199, 0.00677323, 131.60246718, 'orange', 'Venus'],
      [1.00000011, 0.01671022, 102.93768193, 'cyan', 'Earth'],
      [1.52366231, 0.0935, 336.04084, 'red', 'Mars'],
      [5.20336301, 0.04839266, 14.72847983, 'orange', 'Jupiter'],
      [9.577177295536776E+00, 5.101889921719987E-02, 3.394422648650336E+02, 'green', 'Saturn'],
      [1.914496966635462E+01, 4.832662948112808E-02, 9.942704504702185E+01, 'blue', 'Uranus'],
      [3.009622263428050E+01, 7.362571187193770E-03, 2.586226409499831E+02, 'purple', 'Neptune'],
    ];

    var usedLabel = false;
    for (var i=0; i < args.length; i++) {
      if (useSmartLabels && !usedLabel && args[i][0] > labelThreshold) {
        // Show the first label with an orbit larger than the threshold.
        this.plotOrbit.apply(this, args[i]);
      } else {
        // Don't show a label.
        this.plotOrbit.apply(this, args[i].slice(0, args[i].length - 1));
      }
    }
  }

  OrbitDiagram.prototype.render = function(a, e, w) {
    this.prepareRender();
    this.renderPlanets();
    return this.renderAnother(a, e, w);
  }

  OrbitDiagram.prototype.renderAnother = function(a, e, w) {
    return this.plotOrbit(a, e, w, 'white');
  }

  OrbitDiagram.prototype.plotOrbit = function(a, e, w, color, labelText) {
    var sqrtme = 1 - e * e;
    var b = a * Math.sqrt(Math.max(0, sqrtme));
    var f = a * e;

    var rx = b * this.PIXELS_PER_AU;
    var ry = Math.abs(a * this.PIXELS_PER_AU);
    var foci = f * this.PIXELS_PER_AU;

    return this.plotCoords(rx, ry, foci, w, color, labelText);
  }

  OrbitDiagram.prototype.plotCoords = function(rx, ry, f, rotate_deg, color, labelText) {
    color = color || 'white';
    var cx = this.SUN_X;
    var cy = this.SUN_Y + f;

    var ellipse = this.orbit_svg.append('svg:ellipse')
        .style('stroke', color)
        .style('fill', 'none')
        .attr('rx', rx)
        .attr('ry', ry)
        .attr('cx', cx)
        .attr('cy', cy)
        .attr('transform', 'rotate(' + rotate_deg + ', ' + this.SUN_X + ', ' + this.SUN_Y + ')')

    if (labelText) {
      this.orbit_svg.append('text')
          .attr('x', cx + rx*0.65)
          .attr('y', cy + ry*0.65)
          .style('stroke', color)
          .style('fill', color)
          .style('background-color', '#000')
          .style('font-size', 10)
          .text(labelText);
    }

    return ellipse;
  }

  OrbitDiagram.prototype.plotSun = function() {
    this.orbit_svg.append('svg:ellipse')
        .style('stroke', 'yellow')
        .style('fill', 'yellow')
        .attr('rx', 2)
        .attr('ry', 2)
        .attr('cx', this.SUN_X)
        .attr('cy', this.SUN_Y);
  }

  return OrbitDiagram;
})();
