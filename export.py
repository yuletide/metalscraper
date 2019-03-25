import scraperwiki
import json
import geojson
# import shapely


def get_geocoded_bands():
    return scraperwiki.sqlite.select("* FROM swdata where geo_place_name IS NOT NULL and geo_place_name <> '-1'")

bands
for band in get_geocoded_bands():

