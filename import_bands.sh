pipenv run python export.py > bands.geojson
ogr2ogr -progress "PG:host=localhost dbname=postgres" bands.geojson -nln bands -overwrite