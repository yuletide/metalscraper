#!/bin/bash
pipenv run python export.py > bands.geojson
ogr2ogr -progress "PG:host=localhost dbname=postgres" bands.geojson -nln bands.bands -overwrite
tippecanoe -z14 -o bands.mbtiles -r1 --cluster-distance=10 bands.geojson --read-parallel --force