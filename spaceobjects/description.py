'''
Helpers for building an asteroid description.
'''

# https://pdssbn.astro.umd.edu/data_other/objclass.shtml
ORBIT_CLASS_MAPPING = {
    'COM': {
        'desc_short': 'Comet',
        'desc_long': 'Comets whose orbits do not match any defined orbit class',
        'desc_orbit': 'whose orbit does not match any defined comet orbit class',
    },
    'CTc': {
        'desc_short': 'Comet',
        'desc_long': 'Chiron-type comet, as defined by Levison and Duncan (TJupiter > 3; a > aJupiter)',
        # See https://scholar.google.com/scholar?hl=en&as_sdt=0%2C5&q=chiron+comet+levinson+duncan&btnG=
        'desc_orbit': 'whose orbit is approximately between Jupiter and Neptune',
    },
    'ETc': {
        'desc_short': 'Encke-type Comet',
        'desc_long': 'Encke-type comet, as defined by Levison and Duncan (TJupiter > 3; a < aJupiter)',
        'desc_orbit': 'whose orbit brings it closer to the sun than Jupiter',
    },
    'HTC': {
        'desc_short': 'Halley-type Comet',
        'desc_long': 'Halley-type comet, classical definition (20 y < P < 200 y)',
        'desc_orbit': 'with an orbit that has medium-length periods and is highly inclined with respect to the ecliptic plane of the solar system',
    },
    'HYP': {
        'desc_short': 'Hyperbolic Comet',
        'desc_long': 'Comets on hyperbolic orbits (e > 1.0)',
        'desc_orbit': 'with a trajectory through the solar system likely originating from the Oort Cloud',
    },
    'JFc': {
        'desc_short': 'Jupiter-family Comet',
        'desc_long': 'Jupiter-family comets, as defined by Levison and Duncan (2 < TJupiter < 3)',
        'desc_orbit': 'whose orbit features a relatively short period, low inclination, and is controlled by Jupiter\'s gravitational effects',
    },
    'JFC': {
        'desc_short': 'Jupiter-family Comet',
        'desc_long': 'Jupiter-family comets, classical definition (P < 20 y)',
        'desc_orbit': 'whose orbit features a relatively short period, low inclination, and is controlled by Jupiter\'s gravitational effects',
    },
    'PAR': {
        'desc_short': 'Parabolic Comet',
        'desc_long': 'Comets on parabolic orbits (e = 1.0)',
        'desc_orbit': 'with an extremely long orbital period, likely originating from the Oort Cloud',
    },

    'AMO': {
        'desc_short': 'Amor-class Asteroid',
        'desc_long': 'Near-Earth asteroid whose orbits are similar to that of 1221 Amor (a > 1.0 AU; 1.017 AU < q < 1.3 AU)',
        'desc_orbit': 'whose orbit approaches the orbit of Earth but does not cross it',
    },
    'APO': {
        'desc_short': 'Apollo-class Asteroid',
        'desc_long': 'Near-Earth asteroids whose orbits cross the Earth\'s orbit similar to that of 1862 Apollo (a > 1.0 AU; q < 1.017 AU).',
        'desc_orbit': 'whose orbit crosses the orbit of Earth',
    },
    'AST': {
        'desc_short': 'Asteroid',
        'desc_long': 'Asteroid orbit not matching any defined orbit class',
        'desc_orbit': 'whose orbit does not match any defined asteroid orbital class',
    },
    'ATE': {
        'desc_short': 'Aten-class Asteroid',
        'desc_long': 'Near-Earth asteroid orbits similar to that of 2062 Aten (a < 1.0 AU; Q > 0.983 AU)',
        'desc_orbit': 'whose orbit could bring it in close proximity to Earth',
    },
    'CEN': {
        'desc_short': 'Centaur-class Asteroid',
        'desc_long': 'Objects with orbits between Jupiter and Neptune (5.5 AU < a < 30.1 AU)',
        'desc_orbit': 'with an orbit between Jupiter and Neptune',
    },
    'HYA': {
        'desc_short': 'Hyperbolic Asteroid',
        'desc_long': 'Asteroids on hyperbolic orbits (e > 1.0)',
        'desc_orbit': 'with an orbit not bound to the sun',
    },
    'IEO': {
        'desc_short': 'Interior-Earth Asteroid',
        'desc_long': 'Asteroids with orbits contained entirely within the orbit of the Earth (Q < 0.983 AU)',
        'desc_orbit': 'with an orbit that is entirely confined within Earth\'s orbit',
    },
    'IMB': {
        'desc_short': 'Inner Main-belt Asteroid',
        'desc_long': 'Asteroids with orbital elements constrained by (a < 2.0 AU; q > 1.666 AU)',
        'desc_orbit': 'orbiting between Mars and Jupiter within the inner portion of the asteroid belt',
    },
    'MBA': {
        'desc_short': 'Main-belt Asteroid',
        'desc_long': 'Asteroids with orbital elements constrained by (2.0 AU < a < 3.2 AU; q > 1.666 AU)',
        'desc_orbit': 'orbiting between Mars and Jupiter in the main portion of the asteroid belt',
    },
    'MCA': {
        'desc_short': 'Mars-crossing Asteroid',
        'desc_long': 'Asteroids that cross the orbit of Mars constrained by (1.3 AU < q < 1.666 AU; a < 3.2 AU)',
        'desc_orbit': 'with an orbit that crosses the orbit of Mars',
    },
    'OMB': {
        'desc_short': 'Outer Main-belt Asteroid',
        'desc_long': 'Asteroids with orbital elements constrained by (3.2 AU < a < 4.6 AU)',
        'desc_orbit': 'that orbits between Mars and Jupiter in the outer reaches of the main asteroid belt',
    },
    'PAA': {
        'desc_short': 'Parabolic Asteroid',
        'desc_long': 'Asteroids on parabolic orbits (e = 1.0)',
        'desc_orbit': 'with an unusual orbit that brings it far beyond the normal boundaries of asteroids in the solar system',
    },
    'TJN': {
        'desc_short': 'Jupiter Trojan',
        'desc_long': 'Asteroids traped in Jupiter\'s L4/L5 Lagrange points (4.6 AU < a < 5.5 AU; e < 0.3)',
        'desc_orbit': 'that shares Jupiter\'s orbit around the sun',
    },
    'TNO': {
        'desc_short': 'Trans-Neptunian Object',
        'desc_long': 'Objects with orbits outside Neptune (a > 30.1 AU)',
        'desc_orbit': 'that orbits at a distance greater than the average distance of Neptune from the sun',
    },
}

def get_orbit_class(roid):
  return ORBIT_CLASS_MAPPING.get(roid.sbdb_entry['class'])['desc_short']

def get_orbit_desc(roid):
  return ORBIT_CLASS_MAPPING.get(roid.sbdb_entry['class'])['desc_orbit']

def get_diameter_comparison(roid):
  diameter_str = roid.sbdb_entry.get('diameter')
  if not diameter_str:
      return None

  diameter = float(diameter_str) ** 2

  # http://www.decisionsciencenews.com/2015/02/20/put-size-countries-perspective-comparing-us-states/
  # https://en.wikipedia.org/wiki/List_of_United_States_cities_by_area
  if diameter < 370:
      return 'the city of Philadelphia'
  if diameter < 400:
      return 'the city of Denver'
  if diameter < 953:
      return 'the city of Indianapolis'
  if diameter < 999:
      return 'the city of Dallas'
  if diameter < 1213:
      return 'the city of New York'
  if diameter < 1302:
      return 'the city of Los Angeles'
  if diameter < 1625:
      return 'the city of Houston'
  if diameter < 5000:
      return 'the U.S. state of Rhode Island'
  if diameter < 14000:
      return 'the U.S. state of Delaware'
  if diameter < 22000:
      return 'the U.S. state of Connecticut'
  if diameter < 24000:
      return 'the U.S. state of New Jersey'
  if diameter < 27000:
      return 'the U.S. state of Vermont'
  if diameter < 32000:
      return 'the U.S. state of Massachusetts'
  if diameter < 62000:
      return 'the U.S. state of Maryland'
  if diameter < 82000:
      return 'the U.S. state of West Virginia'
  if diameter < 91000:
      return 'the U.S. state of South Carolina'
  if diameter < 94000:
      return 'Portugal'
  if diameter < 104000:
      return 'South Korea'
  if diameter < 109000:
      return 'Iceland'
  if diameter < 119000:
      return 'the U.S. state of Virginia'
  if diameter < 125000:
      return 'the U.S. state of Pennsylvania'
  if diameter < 134000:
      return 'the U.S. state of Mississippi'
  if diameter < 170000:
      return 'the U.S. state of Iowa'
  if diameter < 200000:
      return 'the U.S. state of South Dakota'
  if diameter < 300000:
      return 'the U.K.'
  if diameter < 400000:
      return 'Japan'
  if diameter < 500000:
      return 'France'
  if diameter < 700000:
      return 'the U.S. state of Texas'
  return 'the U.S. state of Alaska'
