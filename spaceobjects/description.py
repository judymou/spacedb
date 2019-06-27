'''
Helpers for building an asteroid description.
'''

COMET_CLASSES = set(['COM', 'CTc', 'ETc', 'HTC', 'HYP', 'JFc', 'JFC', 'PAR'])

def get_diameter_comparison(roid):
    diameter = roid.get_diameter_estimate()
    if not diameter:
        return None

    diameter_sq = diameter * diameter

    # http://www.decisionsciencenews.com/2015/02/20/put-size-countries-perspective-comparing-us-states/
    # https://en.wikipedia.org/wiki/List_of_United_States_cities_by_area
    if diameter_sq < 0.04:
        return 'a school bus or smaller'
    if diameter_sq < 0.110:
        return 'a football field'
    if diameter_sq < 0.0728434:
        return 'the U.S. White House'
    if diameter_sq < 0.234718:
        return 'the U.S. Capitol building'
    if diameter_sq < 1.280:
        return 'the Golden Gate Bridge'
    if diameter_sq < 2.35932:
        return 'the U.S. Pentagon'
    if diameter_sq < 8.848:
        return 'Mount Everest'
    if diameter_sq < 21:
        return 'the island of Manhattan'
    if diameter_sq < 97:
        return 'the San Francisco Bay'
    if diameter_sq < 124:
        return 'the city of Boston'
    if diameter_sq < 214:
        return 'the city of Cleveland, Ohio'
    if diameter_sq < 239:
        return 'the city of Baltimore'
    if diameter_sq < 370:
        return 'the city of Philadelphia'
    if diameter_sq < 400:
        return 'the city of Denver'
    if diameter_sq < 953:
        return 'the city of Indianapolis'
    if diameter_sq < 999:
        return 'the city of Dallas'
    if diameter_sq < 1213:
        return 'the city of New York'
    if diameter_sq < 1302:
        return 'the city of Los Angeles'
    if diameter_sq < 1625:
        return 'the city of Houston'
    if diameter_sq < 5000:
        return 'the U.S. state of Rhode Island'
    if diameter_sq < 14000:
        return 'the U.S. state of Delaware'
    if diameter_sq < 22000:
        return 'the U.S. state of Connecticut'
    if diameter_sq < 24000:
        return 'the U.S. state of New Jersey'
    if diameter_sq < 27000:
        return 'the U.S. state of Vermont'
    if diameter_sq < 32000:
        return 'the U.S. state of Massachusetts'
    if diameter_sq < 62000:
        return 'the U.S. state of Maryland'
    if diameter_sq < 82000:
        return 'the U.S. state of West Virginia'
    if diameter_sq < 91000:
        return 'the U.S. state of South Carolina'
    if diameter_sq < 94000:
        return 'Portugal'
    if diameter_sq < 104000:
        return 'South Korea'
    if diameter_sq < 109000:
        return 'Iceland'
    if diameter_sq < 119000:
        return 'the U.S. state of Virginia'
    if diameter_sq < 125000:
        return 'the U.S. state of Pennsylvania'
    if diameter_sq < 134000:
        return 'the U.S. state of Mississippi'
    if diameter_sq < 170000:
        return 'the U.S. state of Iowa'
    if diameter_sq < 200000:
        return 'the U.S. state of South Dakota'
    if diameter_sq < 300000:
        return 'Great Britain'
    if diameter_sq < 400000:
        return 'Japan'
    if diameter_sq < 500000:
        return 'France'
    if diameter_sq < 700000:
        return 'the U.S. state of Texas'
    return 'the U.S. state of Alaska'

# Approximate mapping from Tholen spectral type to SMASS, from Asterank
# https://github.com/typpo/asterank/blob/master/data/pipeline/run/10_sbdb/horizon.py
THOLEN_MAPPINGS = {
  'M': 'M',
  'E': 'M',
  'P': 'P',
  'B': 'B',
  'C': 'C',
  'F': 'C',
  'G': 'Cgh',
  'Q': 'Q',
  'R': 'R',
  'V': 'V',
  'T': 'T',
  'D': 'D',
  'A': 'A',
}

# Keys are asteroid spectra type. Values are maps from a material
# to the percent mass of each material.
SPECTRA_INDEX = {
    '?': {},
    'A': {},
    'B': {
        'hydrogen': 0.235,
        'nitrogen': 0.001,
        'ammonia': 0.001,
        'iron': 10,
    },
    'C': {# from Keck report at http: //www.kiss.caltech.edu/study/asteroid/asteroid_final_report.pdf
        'water': .2,
        'iron': .166,
        'nickel': .014,
        'cobalt': .002,

        #volatiles 'hydrogen': 0.235,
        'nitrogen': 0.001,
        'ammonia': 0.001,
    },
    'Ch': {# from Keck report at http: //www.kiss.caltech.edu/study/asteroid/asteroid_final_report.pdf
        'water': .2,
        'iron': .166,
        'nickel': .014,
        'cobalt': .002,

        #volatiles 'hydrogen': 0.235,
        'nitrogen': 0.001,
        'ammonia': 0.001,
    },
    'Cg': {# from Keck report at http: //www.kiss.caltech.edu/study/asteroid/asteroid_final_report.pdf
        'water': .2,
        'iron': .166,
        'nickel': .014,
        'cobalt': .002,

        #volatiles 'hydrogen': 0.235,
        'nitrogen': 0.001,
        'ammonia': 0.001,
    },
    'Cgh': {# from Keck report at http: //www.kiss.caltech.edu/study/asteroid/asteroid_final_report.pdf
        'water': .2,
        'iron': .166,
        'nickel': .014,
        'cobalt': .002,

        #volatiles 'hydrogen': 0.235,
        'nitrogen': 0.001,
        'ammonia': 0.001,
    },
    'C type': {# from Keck report at http: //www.kiss.caltech.edu/study/asteroid/asteroid_final_report.pdf
        'water': .2,
        'iron': .166,
        'nickel': .014,
        'cobalt': .002,

        #volatiles 'hydrogen': 0.235,
        'nitrogen': 0.001,
        'ammonia': 0.001,
    },
    'Cb': {# transition object between C and B# from Keck report at http: //www.kiss.caltech.edu/study/asteroid/asteroid_final_report.pdf
        'water': .1,
        'iron': .083,
        'nickel': .007,
        'cobalt': .001,

        #volatiles 'hydrogen': 0.235,
        'nitrogen': 0.001,
        'ammonia': 0.001,
    },
    'D': {
        'water': 0.000023,
    },
    'E': {

    },
    'K': {# cross between S and C# from Keck report at http: //www.kiss.caltech.edu/study/asteroid/asteroid_final_report.pdf
        'water': .1,
        'iron': .083,
        'nickel': .007,
        'cobalt': .001,

        #volatiles 'hydrogen': 0.235,
        'nitrogen': 0.001,
        'ammonia': 0.001,
    },
    'L': {
        'magnesium silicate': 1e-30,
        'iron silicate': 0,
        'aluminum': 7
    },
    'Ld': {# copied from S
        'magnesium silicate': 1e-30,
        'iron silicate': 0,
    },
    'M': {
        'iron': 88,
        'nickel': 10,
        'cobalt': 0.5,
    },
    'O': {
        'nickel-iron': 2.965,
        'platinum': 1.25,
    },
    'P': {# correspond to CI, CM carbonaceous chondrites
        'water': 12.5,
    },
    'R': {
        'magnesium silicate': 1e-30,
        'iron silicate': 0,
    },
    'S': {
        'magnesium silicate': 1e-30,
        'iron silicate': 0,
    },
    #Sa, Sq, Sr, Sk, and Sl all transition objects(assume half / half)
    'Sa': {
        'magnesium silicate': 5e-31,
        'iron silicate': 0,
    },
    'Sq': {
        'magnesium silicate': 1e-30,
        'iron silicate': 0,
    },
    'Sr': {
        'magnesium silicate': 1e-30,
        'iron silicate': 0,
    },
    'Sk': {
        'magnesium silicate': 1e-30,
        'iron silicate': 0,
    },
    'Sl': {
        'magnesium silicate': 1e-30,
        'iron silicate': 0,
    },
    'S(IV)': {
        'magnesium silicate': 1e-30,
        'iron silicate': 0,
    },
    'Q': {
        'nickel-iron': 13.315,
    },
    'R': {
        'magnesium silicate': 1e-30,
        'iron silicate': 0,
    },
    'T': {
        'iron': 6,
    },
    'U': {

    },
    'V': {
        'magnesium silicate': 1e-30,
        'iron silicate': 0,
    },

    #TODO use density to decide what kind of X the object is ?

    'X' : {# TODO these vals only apply to M - type within X
        'iron': 88,
        'nickel': 10,
        'cobalt': 0.5,
    },
    'Xe': {# TODO these vals only apply to M - type within X
        'iron': 88,
        'nickel': 10,
        'cobalt': 0.5,
    },
    'Xc': {# TODO these vals only apply to M - type within X
        'iron': 88,
        'nickel': 10,
        'cobalt': 0.5,
        'platinum': 0.005,
    },
    'Xk': {# TODO these vals only apply to M - type within X
        'iron': 88,
        'nickel': 10,
        'cobalt': 0.5,
    },
    'comet': {# no estimates for now, because assumed mass, etc.would be off
    },
}

def composition(roid):
    ret = []
    spec = roid.sbdb_entry.get('spec_B')
    if not spec:
        # Try to convert Tholen to SMASS spectral classification
        spec = roid.sbdb_entry.get('spec_T')
        if not spec:
            return []
        spec = THOLEN_MAPPINGS.get(spec)
        if not spec:
            return []
    return SPECTRA_INDEX.get(spec, {}).keys()
