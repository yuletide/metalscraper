#!/bin/bash
pipenv run python export.py > geojson/bands.geojson
ogr2ogr -progress "PG:host=localhost dbname=postgres" geojson/bands.geojson -nln bands.bands -overwrite
tippecanoe -z14 -o mbtiles/bands_cluster.mbtiles -r1 --cluster-distance=10 geojson/bands.geojson --read-parallel --force
cd geojson && mtsds --sync