#!/bin/bash
echo "Exporting scraper to geojson"
pipenv run python export.py > geojson/bands.geojson
echo "Importing geojson to postgres"
ogr2ogr -progress "PG:host=localhost dbname=postgres" geojson/bands.geojson -nln bands.bands -overwrite
# cd geojson && mtsds --sync
# tippecanoe -z14 -o ../mbtiles/bands_cluster.mbtiles -r1 --cluster-distance=20 bands.geojsonl --read-parallel --force