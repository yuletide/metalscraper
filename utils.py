import sys
import ast
import json
from tqdm import tqdm
from time import sleep
import scraperwiki


# finds all functions saved as python object str and encodes as json to avoid unsafe `literal_eval`
def jsonify_literals(field, count=False):
    print(f'converting {field} from python to json')
    records = scraperwiki.sqlite.select(
        # get all records encoded as python literals
        f'* from swdata WHERE {field} LIKE \"%\'%\" {"limit " + count if count else ""}'
    )
    for i, band in enumerate(tqdm(records)):
        # print(band['geo_context'])
        obj = ast.literal_eval(band[field])
        # print(obj)
        band[field] = json.dumps(obj)
        # print(band[field])
        scraperwiki.sqlite.save(unique_keys=['id'], data=band)
        if i % 100:
            # sqlite crash
            sleep(0.01)


def clean_old_placenames():
    records = scraperwiki.sqlite.select(
        "* from swdata WHERE location IS NOT NULL and location_utf is NULL")
    for band in records:
        band['location_utf'] = band['location'].encode(
            'ISO-8859-1').decode('utf-8')
        scraperwiki.sqlite.save(unique_keys=['id'], data=band)


jsonify_literals('geo_properties')
jsonify_literals('geo_geom')
