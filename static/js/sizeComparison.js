window.SizeComparison = (function() {
  'use strict';

  function SizeComparison(selector, options) {
    this.elt = document.querySelector(selector);
    this.selector = selector;
  
    options = options || {};
  }

  SizeComparison.prototype.initMap = function() {
    this.map = new google.maps.Map(this.elt, {
      zoom: 3,
      center: {lat: 37.090, lng: -95.712},
      mapTypeId: 'terrain',
      streetViewControl: false,
    });
  }

  SizeComparison.prototype.addCircle = function(diameter_km) {
    var objectCircle = new google.maps.Circle({
      strokeColor: '#FF0000',
      strokeOpacity: 0.8,
      strokeWeight: 2,
      fillColor: '#FF0000',
      fillOpacity: 0.35,
      map: this.map,
      center: {lat: 40.714, lng: -74.005},
      radius: diameter_km / 2 * 1000, 
    });
    this.map.fitBounds(objectCircle.getBounds());
  }

  SizeComparison.prototype.render = function(diameter_km) {
    this.initMap(diameter_km);
    this.addCircle(diameter_km);
  }
  return SizeComparison;
})();
