import scraperwiki
import json
from geojson import Point, Feature, FeatureCollection
import geojson
import re
import ast
# import shapely


def get_geocoded_bands(limit=''):
    if limit: limit = " LIMIT " + str(limit)
    return scraperwiki.sqlite.select("* FROM swdata where geo_geom IS NOT NULL and geo_place_name <> '-1'" + limit)

bands = []

for band in get_geocoded_bands():
    # band_geom = geojson.loads(band['geo_geom'])
    band_center = ast.literal_eval(band['geo_center'])
    band_point = Point(band_center)
    # print (band_point)
    # print(band_geom)
    band_feature = Feature(geometry=band_point, properties=band)
    # print(band_feature)
    bands.append(band_feature)

print(FeatureCollection(bands))
