import scraperwiki
from geojson import Point, Feature, FeatureCollection
import geojson
import json
import ast


def get_geocoded_bands(limit=''):
    if limit:
        limit = " LIMIT " + str(limit)
    return scraperwiki.sqlite.select("* FROM swdata where geo_geom IS NOT NULL and geo_place_name <> '-1'" + limit)


# bands = []
PRECISION = 6

print('{"features": [')
bands_list = get_geocoded_bands()

for i, band in enumerate(bands_list):
    # band_center = ast.literal_eval(band['geo_center']) # should be the same as geom, but just in case
    band_geom = ast.literal_eval(band['geo_geom'])

    # Rounding to save space if needed:
    # coords=list(map(lambda c: round(c, PRECISION), band_geom['coordinates']))
    # band_geom['coordinates'] = coords

    band_feature = Feature(geometry=band_geom, properties=band)
    # bands.append(band_feature)
    if i < len(bands_list)-1:
        print(geojson.dumps(band_feature) + ',')
    else:
        print(geojson.dumps(band_feature))


print('], "type": "FeatureCollection"}')
# print(geojson.dumps(FeatureCollection(bands)))
