import scraperwiki
import json
from geojson import Point, Feature, FeatureCollection
import geojson
import ast

def get_geocoded_bands(limit=''):
    if limit: limit = " LIMIT " + str(limit)
    return scraperwiki.sqlite.select("* FROM swdata where geo_geom IS NOT NULL and geo_place_name <> '-1'" + limit)

bands = []

print('{"features": [')
for band in get_geocoded_bands():
    # band_center = ast.literal_eval(band['geo_center']) # parse the array
    band_geom = ast.literal_eval(band['geo_geom'])
    band_feature = Feature(geometry=band_geom, properties=band)
    bands.append(band_feature)
    print(json.dumps(band_feature)+',') # for tippecanoe --read-parallel

print('], "type": "FeatureCollection"}')
# print(geojson.dumps(FeatureCollection(bands)))
